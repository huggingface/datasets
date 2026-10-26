import bz2
import gzip
import io
import itertools
import os
import warnings
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..utils.file_utils import is_local_path, xopen


if TYPE_CHECKING:
    import biotite.structure

    from .features import FeatureType


# Per-atom annotations every biotite AtomArray has, with their storage dtype.
CORE_ANNOTATIONS = {
    "chain_id": "string",
    "res_id": "int32",
    "ins_code": "string",
    "res_name": "string",
    "hetero": "bool",
    "atom_name": "string",
    "element": "string",
}
# Optional per-atom annotations stored by default; they are filled from structure files when present.
DEFAULT_ANNOTATIONS = {"b_factor": "float32", "occupancy": "float32", "charge": "int8"}
# Value of a missing annotation, by storage dtype kind.
_FILL = {"string": "", "bool": False, "float": np.nan, "int": 0}

_FORMAT_BY_EXTENSION = {
    ".cif": "pdbx",
    ".mmcif": "pdbx",
    ".bcif": "pdbx",
    ".pdb": "pdb",
    ".ent": "pdb",
    ".mol": "mol",
    ".sdf": "mol",
    ".gro": "gro",
}
_COMPRESSION_EXTENSIONS = (".gz", ".gzip", ".bz2", ".zst")

_DECODERS: dict[str, Callable[[dict], Any]] = {}
_ENTRY_POINT_GROUP = "datasets.atomic_structure_decoders"


@dataclass
class AtomicStructure:
    """AtomicStructure [`Feature`] for atomic structures: proteins, nucleic acids, small molecules, complexes,
    crystals and simulation frames.

    A structure is stored as columns, following the data model of a
    [biotite](https://www.biotite-python.org) `AtomArray`:

    - `coord`: atom coordinates, one `(n_atoms, 3)` array per model (NMR models, trajectory frames, samples).
    - `annotations`: one value per atom for `chain_id`, `res_id`, `ins_code`, `res_name`, `hetero`, `atom_name`
      and `element`, plus the annotations declared in `annotations` (by default `b_factor`, `occupancy` and
      `charge`).
    - `bonds`: `(atom1, atom2, type)` with the biotite `BondType` codes (0 any, 1 single, 2 double, 3 triple,
      4 quadruple, 5-7 aromatic single/double/triple, 8 coordination, 9 aromatic).
    - `box`: the periodic cell of each model as a flattened 3x3 matrix, or null for non-periodic structures.
    - `global_annotations` and `pair_annotations`: optional per-structure values and sparse values for atom pairs,
      present when declared.

    Files are read once, when the dataset is created, so reading a structure back never parses a file and
    single columns (for example only coordinates) can be loaded on their own.

    Input: The AtomicStructure feature accepts as input:

    - A `str` or `pathlib.Path`: local path or URL of a PDBx/mmCIF (`.cif`, `.mmcif`), BinaryCIF (`.bcif`),
      PDB (`.pdb`, `.ent`), MOL/SDF (`.mol`, `.sdf`, first record) or GRO (`.gro`) file, optionally gzip,
      bz2 or zstd compressed.
    - `bytes`: the content of such a file. The format is detected from the content; MOL/SDF and GRO need a path.
    - A `dict` with `path` and/or `bytes` keys, as above.
    - A `biotite.structure.AtomArray` or `AtomArrayStack`. Pairwise and system-wide annotations of subclasses
      exposing `get_annotation(name, n_body=...)` are stored too.
    - An `rdkit.Chem.Mol` or an `ase.Atoms`.
    - A `dict` in the stored layout, e.g. a structure decoded with `decoder="numpy"`.

    Reading files and converting objects requires `biotite`.

    Output: depends on `decoder`. The default `"biotite"` returns a `biotite.structure.AtomArray`, or an
    `AtomArrayStack` when there are several models. `"numpy"` returns the stored layout as numpy arrays and needs
    no dependency. Other libraries can add decoders with
    [`~features.atomic_structure.register_atomic_structure_decoder`] or a `datasets.atomic_structure_decoders`
    entry point.

    Args:
        annotations (`dict[str, str]`, *optional*):
            Per-atom annotations to store in addition to the core ones, as `{name: dtype}` with dtypes as in
            [`Value`]. Defaults to `{"b_factor": "float32", "occupancy": "float32", "charge": "int8"}`. Names that
            are mmCIF `atom_site` items (e.g. `label_asym_id`) are read from mmCIF/BinaryCIF files.
        global_annotations (`dict[str, str]`, *optional*):
            Values describing the whole structure, as `{name: dtype}`.
        pair_annotations (`dict[str, str]`, *optional*):
            Values for pairs of atoms, as `{name: dtype}`, stored sparsely as `(atom1, atom2, value)`.
        decoder (`str`, defaults to `"biotite"`):
            Name of the decoder that builds the returned object.
        decode (`bool`, defaults to `True`):
            Whether to decode the structure. If `False`, returns the stored layout as nested Python lists.

    Example:

    ```py
    >>> from datasets import AtomicStructure, Dataset
    >>> ds = Dataset.from_dict({"structure": ["path/to/1abc.cif.gz"]}).cast_column("structure", AtomicStructure())
    >>> ds[0]["structure"]
    <biotite.structure.AtomArray ...>
    >>> ds = ds.cast_column("structure", AtomicStructure(decoder="numpy"))
    >>> ds[0]["structure"]["coord"].shape
    (1, 1234, 3)
    ```
    """

    annotations: Optional[dict[str, str]] = None
    global_annotations: Optional[dict[str, str]] = None
    pair_annotations: Optional[dict[str, str]] = None
    decoder: str = "biotite"
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "biotite.structure.AtomArray"
    pa_type: ClassVar[Any] = None  # set per instance in __post_init__, as it depends on the declared annotations
    _type: str = field(default="AtomicStructure", init=False, repr=False)

    def __post_init__(self):
        from .features import string_to_arrow

        for name in CORE_ANNOTATIONS:
            if self.annotations and name in self.annotations:
                raise ValueError(f"'{name}' is a core annotation and is always stored; remove it from `annotations`.")
        annotation_types = {**CORE_ANNOTATIONS, **self._extra_annotations()}
        fields = [
            ("coord", pa.list_(pa.list_(pa.list_(pa.float32(), 3)))),
            ("annotations", pa.struct([(k, pa.list_(string_to_arrow(v))) for k, v in annotation_types.items()])),
            (
                "bonds",
                pa.struct(
                    [("atom1", pa.list_(pa.int32())), ("atom2", pa.list_(pa.int32())), ("type", pa.list_(pa.int8()))]
                ),
            ),
            ("box", pa.list_(pa.list_(pa.float32(), 9))),
        ]
        if self.global_annotations:
            fields.append(
                (
                    "global_annotations",
                    pa.struct([(k, string_to_arrow(v)) for k, v in self.global_annotations.items()]),
                )
            )
        if self.pair_annotations:
            pair_type = lambda dtype: pa.struct(  # noqa: E731
                [
                    ("atom1", pa.list_(pa.int32())),
                    ("atom2", pa.list_(pa.int32())),
                    ("value", pa.list_(string_to_arrow(dtype))),
                ]
            )
            fields.append(
                ("pair_annotations", pa.struct([(k, pair_type(v)) for k, v in self.pair_annotations.items()]))
            )
        self.pa_type = pa.struct(fields)

    def __call__(self):
        return self.pa_type

    def _extra_annotations(self) -> dict[str, str]:
        return DEFAULT_ANNOTATIONS if self.annotations is None else self.annotations

    def encode_example(self, value: Union[str, os.PathLike, bytes, bytearray, dict, Any]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `os.PathLike`, `bytes`, `dict`, `biotite.structure.AtomArray`, `rdkit.Chem.Mol` or `ase.Atoms`):
                Data passed as input to AtomicStructure feature.

        Returns:
            `dict` in the stored layout.
        """
        if isinstance(value, dict) and "coord" in value:
            return self._normalize(value)
        if isinstance(value, (str, Path)):
            atoms = self._read(_read_file(str(value)), str(value))
        elif isinstance(value, (bytes, bytearray)):
            atoms = self._read(bytes(value), None)
        elif isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            data = value["bytes"] if value.get("bytes") is not None else _read_file(value["path"])
            atoms = self._read(bytes(data), value.get("path"))
        elif hasattr(value, "coord") and hasattr(value, "get_annotation_categories"):
            atoms = value
        elif type(value).__module__.startswith("rdkit."):
            _require_biotite("convert RDKit molecules")
            from biotite.interface.rdkit import from_mol

            atoms = from_mol(value, add_hydrogen=False)
        elif type(value).__module__.startswith("ase.") and hasattr(value, "get_positions"):
            atoms = _from_ase(value)
        else:
            raise ValueError(
                "An atomic structure should be a file path, file bytes, a dict with 'path' or 'bytes', a biotite "
                f"AtomArray, an RDKit Mol, an ASE Atoms or a dict in the stored layout, but got {type(value)}."
            )
        return self._from_atom_array(atoms)

    def decode_example(self, value: dict, token_per_repo_id=None) -> Any:
        """Decode example structure into the object returned by `decoder`.

        Args:
            value (`dict`):
                A structure in the stored layout.
            token_per_repo_id (`dict`, *optional*):
                Unused; structures are stored inline.

        Returns:
            The decoded structure, e.g. a `biotite.structure.AtomArray`.
        """
        if not self.decode:
            raise RuntimeError(
                "Decoding is disabled for this feature. Please use AtomicStructure(decode=True) instead."
            )
        return get_atomic_structure_decoder(self.decoder)(self._to_numpy(value))

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Features

        return self if self.decode else Features.from_arrow_schema(pa.schema(list(self.pa_type)))

    def cast_storage(self, storage: Union[pa.StringArray, pa.BinaryArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the AtomicStructure arrow storage type.

        The Arrow types that can be converted to the AtomicStructure pyarrow storage type are:

        - `pa.string()` or `pa.large_string()` - paths of structure files, which are read
        - `pa.binary()` or `pa.large_binary()` - contents of structure files, which are read
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})` - file references, which are read
        - a struct in the stored layout; missing annotations, bonds, boxes and declared global or pair
          annotations are filled with defaults, nulls or empty lists

        Args:
            storage (`Union[pa.StringArray, pa.BinaryArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the AtomicStructure arrow storage type.
        """
        is_struct = pa.types.is_struct(storage.type)
        if is_struct and storage.type.get_field_index("coord") >= 0:
            return pa.array(
                [None if value is None else self._normalize(value) for value in storage.to_pylist()], type=self.pa_type
            )
        is_file_reference = is_struct and {"bytes", "path"} & {f.name for f in storage.type}
        if is_file_reference or any(
            check(storage.type)
            for check in (pa.types.is_string, pa.types.is_large_string, pa.types.is_binary, pa.types.is_large_binary)
        ):
            encoded = [None if value is None else self.encode_example(value) for value in storage.to_pylist()]
            return pa.array(encoded, type=self.pa_type)
        raise TypeError(f"Can't cast {storage.type} to the AtomicStructure storage type.")

    # ------------------------------------------------------------------------------------------- reading

    def _read(self, data: bytes, path: Optional[str]) -> "biotite.structure.AtomArray":
        _require_biotite("read structure files")
        data = _decompress(data)
        file_format = _detect_format(data, path)
        extra = list(self._extra_annotations())
        if file_format == "pdbx":
            import biotite.structure.io.pdbx as pdbx

            binary = data[:1] and (0x80 <= data[0] <= 0x8F or data[0] in (0xDE, 0xDF))
            file = (
                pdbx.BinaryCIFFile.read(io.BytesIO(data)) if binary else pdbx.CIFFile.read(io.StringIO(data.decode()))
            )
            atom_site = file.block["atom_site"]
            readable = [
                name for name in extra if name in {"b_factor", "occupancy", "charge", "atom_id"} or name in atom_site
            ]
            return _models_or_first(
                lambda model: pdbx.get_structure(file, model=model, extra_fields=readable, include_bonds=True)
            )
        if file_format == "pdb":
            import biotite.structure.io.pdb as pdb

            file = pdb.PDBFile.read(io.StringIO(data.decode()))
            readable = [name for name in extra if name in {"b_factor", "occupancy", "charge", "atom_id"}]
            return _models_or_first(
                lambda model: file.get_structure(model=model, extra_fields=readable, include_bonds=True)
            )
        if file_format == "mol":
            import biotite.structure.io.mol as mol

            text = data.decode()
            file = mol.SDFile.read(io.StringIO(text)) if "$$$$" in text else mol.MOLFile.read(io.StringIO(text))
            return mol.get_structure(file)
        import biotite.structure.io.gro as gro

        return gro.GROFile.read(io.StringIO(data.decode())).get_structure()

    # -------------------------------------------------------------------------------------- conversions

    def _from_atom_array(self, atoms) -> dict:
        """biotite AtomArray / AtomArrayStack (or a subclass with 0- and 2-body annotations) -> stored layout."""
        coord = np.asarray(atoms.coord, dtype=np.float32)
        coord = coord[None] if coord.ndim == 2 else coord
        n_models, n_atoms = coord.shape[:2]
        present = set(atoms.get_annotation_categories())
        annotation_types = {**CORE_ANNOTATIONS, **self._extra_annotations()}
        dropped = present - set(annotation_types)
        if dropped:
            warnings.warn(
                f"Annotations {sorted(dropped)} are not declared in AtomicStructure(annotations=...) and are not stored."
            )
        annotations = {
            name: _column(atoms.get_annotation(name) if name in present else None, dtype, n_atoms)
            for name, dtype in annotation_types.items()
        }
        bonds = atoms.bonds.as_array() if atoms.bonds is not None else np.zeros((0, 3), dtype=np.int64)
        box = getattr(atoms, "box", None)
        if box is not None:
            box = np.asarray(box, dtype=np.float32).reshape(-1, 9)
            box = [list(b) for b in (np.repeat(box, n_models, axis=0) if len(box) == 1 else box)]
        out = {
            "coord": [list(model) for model in coord],
            "annotations": annotations,
            "bonds": {
                "atom1": bonds[:, 0].astype(np.int32),
                "atom2": bonds[:, 1].astype(np.int32),
                "type": bonds[:, 2].astype(np.int8),
            },
            "box": box,
        }
        if self.global_annotations:
            out["global_annotations"] = {
                name: _scalar(_n_body_annotation(atoms, name, 0), dtype)
                for name, dtype in self.global_annotations.items()
            }
        if self.pair_annotations:
            out["pair_annotations"] = {}
            for name, dtype in self.pair_annotations.items():
                pairs = _n_body_annotation(atoms, name, 2)
                indices = np.zeros((0, 2), dtype=np.int32) if pairs is None else np.asarray(pairs.pairs).reshape(-1, 2)
                values = [] if pairs is None else pairs.values
                out["pair_annotations"][name] = {
                    "atom1": indices[:, 0].astype(np.int32),
                    "atom2": indices[:, 1].astype(np.int32),
                    "value": _column(values, dtype, len(indices)),
                }
        return out

    def _normalize(self, value: dict) -> dict:
        """Stored-layout dict (lists or numpy, possibly incomplete) -> complete stored layout."""
        coord = np.asarray(_stack(value["coord"]), dtype=np.float32)
        coord = coord.reshape(-1, 3)[None] if coord.ndim < 3 else coord
        n_models, n_atoms = coord.shape[:2]
        annotations_in = value.get("annotations") or {}
        bonds_in = value.get("bonds") or {}
        n_bonds = 0 if bonds_in.get("atom1") is None else len(bonds_in["atom1"])
        box = value.get("box")
        out = {
            "coord": [list(model) for model in coord],
            "annotations": {
                name: _column(annotations_in.get(name), dtype, n_atoms)
                for name, dtype in {**CORE_ANNOTATIONS, **self._extra_annotations()}.items()
            },
            "bonds": {
                "atom1": _column(bonds_in.get("atom1"), "int32", n_bonds),
                "atom2": _column(bonds_in.get("atom2"), "int32", n_bonds),
                "type": _column(bonds_in.get("type"), "int8", n_bonds),
            },
            "box": None
            if box is None
            else [list(np.asarray(b, dtype=np.float32).reshape(9)) for b in _stack(box).reshape(-1, 9)],
        }
        if self.global_annotations:
            values = value.get("global_annotations") or {}
            out["global_annotations"] = {
                name: _scalar(values.get(name), dtype) for name, dtype in self.global_annotations.items()
            }
        if self.pair_annotations:
            values = value.get("pair_annotations") or {}
            out["pair_annotations"] = {}
            for name, dtype in self.pair_annotations.items():
                pairs = values.get(name) or {}
                n = 0 if pairs.get("atom1") is None else len(pairs["atom1"])
                out["pair_annotations"][name] = {
                    "atom1": _column(pairs.get("atom1"), "int32", n),
                    "atom2": _column(pairs.get("atom2"), "int32", n),
                    "value": _column(pairs.get("value"), dtype, n),
                }
        return out

    def _to_numpy(self, value: dict) -> dict:
        """Stored layout (Python lists, or numpy arrays from the numpy formatter) -> numpy arrays."""
        coord = np.asarray(_stack(value["coord"]), dtype=np.float32)
        coord = coord.reshape(-1, 3)[None] if coord.ndim < 3 else coord
        n_atoms = coord.shape[1]
        annotations_in = value.get("annotations") or {}
        bonds_in = value.get("bonds") or {}
        n_bonds = 0 if bonds_in.get("atom1") is None else len(bonds_in["atom1"])
        box = value.get("box")
        out = {
            "coord": coord,
            "annotations": {
                name: _to_numpy_column(annotations_in.get(name), dtype, n_atoms)
                for name, dtype in {**CORE_ANNOTATIONS, **self._extra_annotations()}.items()
            },
            "bonds": {
                name: _to_numpy_column(bonds_in.get(name), dtype, n_bonds)
                for name, dtype in (("atom1", "int32"), ("atom2", "int32"), ("type", "int8"))
            },
            "box": None if box is None else np.asarray(_stack(box), dtype=np.float32).reshape(-1, 3, 3),
        }
        if self.global_annotations:
            values = value.get("global_annotations") or {}
            out["global_annotations"] = {
                name: _scalar(values.get(name), dtype) for name, dtype in self.global_annotations.items()
            }
        if self.pair_annotations:
            values = value.get("pair_annotations") or {}
            out["pair_annotations"] = {}
            for name, dtype in self.pair_annotations.items():
                pairs = values.get(name) or {}
                n = 0 if pairs.get("atom1") is None else len(pairs["atom1"])
                out["pair_annotations"][name] = {
                    "atom1": _to_numpy_column(pairs.get("atom1"), "int32", n),
                    "atom2": _to_numpy_column(pairs.get("atom2"), "int32", n),
                    "value": _to_numpy_column(pairs.get("value"), dtype, n),
                }
        return out


def register_atomic_structure_decoder(name: str, decoder: Callable[[dict], Any]) -> None:
    """Register a decoder usable as `AtomicStructure(decoder=name)`.

    Args:
        name (`str`):
            Name of the decoder.
        decoder (`Callable[[dict], Any]`):
            Function taking a structure in the stored layout with numpy arrays (the `"numpy"` decoder output)
            and returning the decoded object.
    """
    _DECODERS[name] = decoder


def get_atomic_structure_decoder(name: str) -> Callable[[dict], Any]:
    """Return the decoder registered as `name`, loading `datasets.atomic_structure_decoders` entry points if needed."""
    if name not in _DECODERS:
        for entry_point in entry_points(group=_ENTRY_POINT_GROUP):
            if entry_point.name == name:
                register_atomic_structure_decoder(name, entry_point.load())
                break
        else:
            raise ValueError(f"Unknown atomic structure decoder '{name}'. Available decoders: {sorted(_DECODERS)}.")
    return _DECODERS[name]


# ----------------------------------------------------------------------------------------------- helpers


def _require_biotite(action: str) -> None:
    if not config.BIOTITE_AVAILABLE:
        raise ImportError(f"To {action}, please install 'biotite'.")


def _read_file(path: str) -> bytes:
    if is_local_path(path):
        with open(path, "rb") as f:
            return f.read()
    with xopen(path, "rb", download_config=DownloadConfig()) as f:
        return f.read()


def _decompress(data: bytes) -> bytes:
    if data[:2] == b"\x1f\x8b":
        return gzip.decompress(data)
    if data[:3] == b"BZh":
        return bz2.decompress(data)
    if data[:4] == b"\x28\xb5\x2f\xfd":
        if not config.ZSTANDARD_AVAILABLE:
            raise ImportError("To read zstd-compressed structure files, please install 'zstandard'.")
        import zstandard

        return zstandard.ZstdDecompressor().stream_reader(data).read()
    return data


def _detect_format(data: bytes, path: Optional[str]) -> str:
    if path:
        name = path.split("::")[0].lower()
        for ext in _COMPRESSION_EXTENSIONS:
            name = name.removesuffix(ext)
        for ext, file_format in _FORMAT_BY_EXTENSION.items():
            if name.endswith(ext):
                return file_format
    if data[:1] and (0x80 <= data[0] <= 0x8F or data[0] in (0xDE, 0xDF)):
        return "pdbx"  # BinaryCIF is a MessagePack map
    for line in data[:4096].splitlines():
        if line.startswith(b"data_"):
            return "pdbx"
        if line.strip() and not line.startswith(b"#"):
            break
    return "pdb"


def _models_or_first(get_structure: Callable[[Optional[int]], Any]):
    """All models as a stack, or the first model when models have different atoms."""
    try:
        return get_structure(None)
    except Exception as e:  # biotite raises when models can't be stacked
        warnings.warn(f"Keeping only the first model, as models can't be stacked: {e}")
        return get_structure(1)


def _from_ase(atoms) -> "biotite.structure.AtomArray":
    _require_biotite("convert ASE structures")
    import biotite.structure as struc

    symbols = atoms.get_chemical_symbols()
    atom_array = struc.AtomArray(len(symbols))
    atom_array.coord = atoms.get_positions()
    atom_array.element = np.array([s.upper() for s in symbols])
    atom_array.atom_name = np.array(symbols)
    atom_array.hetero[:] = True
    atom_array.set_annotation("charge", np.asarray(atoms.get_initial_charges()).round().astype(int))
    if any(atoms.pbc):
        atom_array.box = np.asarray(atoms.cell[:], dtype=np.float32)
    return atom_array


def _n_body_annotation(atoms, name: str, n_body: int):
    try:
        if name in atoms.get_annotation_categories(n_body=n_body):
            return atoms.get_annotation(name, n_body=n_body)
    except TypeError:  # a plain biotite array has no 0- or 2-body annotations
        pass
    return None


def _stack(values) -> np.ndarray:
    if isinstance(values, np.ndarray) and values.dtype == object:
        return np.stack([_stack(v) for v in values]) if len(values) else np.zeros((0, 3), dtype=np.float32)
    if (
        isinstance(values, list)
        and values
        and isinstance(values[0], list)
        and values[0]
        and isinstance(values[0][0], list)
    ):
        return np.asarray(
            [
                np.fromiter(itertools.chain.from_iterable(model), np.float32, 3 * len(model)).reshape(-1, 3)
                for model in values
            ]
        )
    return np.asarray(values)


def _kind(dtype: str) -> str:
    if dtype in ("string", "large_string"):
        return "string"
    if dtype == "bool":
        return "bool"
    return "float" if dtype.startswith("float") else "int"


def _column(values, dtype: str, length: int) -> Union[list, np.ndarray]:
    """One annotation column for Arrow: Python strings, or a numpy array of the storage dtype."""
    fill = _FILL[_kind(dtype)]
    if values is None:
        return [fill] * length if _kind(dtype) == "string" else np.full(length, fill, dtype=_numpy_dtype(dtype))
    if len(values) != length:
        raise ValueError(f"An annotation has {len(values)} values, expected {length}.")
    if _kind(dtype) == "string":
        return [fill if v is None else str(v) for v in (values.tolist() if isinstance(values, np.ndarray) else values)]
    values = list(values) if not isinstance(values, np.ndarray) else values
    if isinstance(values, list) and None in values:
        values = [fill if v is None else v for v in values]
    return np.asarray(values).astype(_numpy_dtype(dtype))


def _to_numpy_column(values, dtype: str, length: int) -> np.ndarray:
    """One stored column -> numpy, with missing values filled (strings as a numpy unicode array)."""
    kind = _kind(dtype)
    fill = _FILL[kind]
    np_dtype = str if kind == "string" else _numpy_dtype(dtype)
    if values is None:
        return np.full(length, fill, dtype=np_dtype)
    if isinstance(values, np.ndarray) and values.dtype != object:
        if values.dtype.kind == "f" and kind in ("int", "bool"):  # nulls arrive as NaN from the numpy formatter
            values = np.where(np.isnan(values), fill, values)
        return values.astype(np_dtype, copy=False)
    values = list(values)
    if None in values:
        values = [fill if v is None else v for v in values]
    return np.asarray(values, dtype=np_dtype)


def _scalar(value, dtype: str):
    if value is None:
        return None
    value = np.asarray(value).item()
    return str(value) if _kind(dtype) == "string" else value


def _numpy_dtype(dtype: str) -> np.dtype:
    return np.dtype({"string": object, "large_string": object, "float16": "float16"}.get(dtype, dtype))


# ------------------------------------------------------------------------------------- built-in decoders


def _decode_numpy(structure: dict) -> dict:
    return structure


def _decode_biotite(structure: dict):
    _require_biotite("decode atomic structures with decoder='biotite'")
    import biotite.structure as struc

    coord = structure["coord"]
    n_models, n_atoms = coord.shape[:2]
    atoms = struc.AtomArray(n_atoms) if n_models == 1 else struc.AtomArrayStack(n_models, n_atoms)
    atoms.coord = coord[0] if n_models == 1 else coord
    for name, values in structure["annotations"].items():
        atoms.set_annotation(name, values)
    bonds = structure["bonds"]
    atoms.bonds = struc.BondList(
        n_atoms, np.stack([bonds["atom1"], bonds["atom2"], bonds["type"]], axis=1).astype(np.int64)
    )
    if structure["box"] is not None:
        atoms.box = structure["box"][0] if n_models == 1 else structure["box"]
    if structure.get("global_annotations") or structure.get("pair_annotations"):
        warnings.warn(
            "A biotite AtomArray has no global or pair annotations; they are not returned. Use decoder='numpy' or a "
            "decoder that supports them."
        )
    return atoms


register_atomic_structure_decoder("biotite", _decode_biotite)
register_atomic_structure_decoder("numpy", _decode_numpy)
