import itertools
import os
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib.metadata import entry_points
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ._structure_io import ATOM_COLUMNS, BOND_COLUMNS, COORD_COLUMN, read_structure


if TYPE_CHECKING:
    from .features import FeatureType


_ARROW_TYPES = {"str": pa.string(), "int32": pa.int32(), "int8": pa.int8(), "float32": pa.float32()}
_ATOMS_TYPE = pa.struct(
    [(name, pa.list_(_ARROW_TYPES[dtype])) for name, dtype, _ in ATOM_COLUMNS]
    + [(COORD_COLUMN, pa.list_(pa.list_(pa.float32(), 3)))]
)
_BONDS_TYPE = pa.struct([(name, pa.list_(_ARROW_TYPES[dtype])) for name, dtype in BOND_COLUMNS])
# Decoded value for a missing item, per numpy dtype.
_NUMPY_FILL = {"int32": -1, "int8": 0, "float32": np.nan}

_DECODERS: dict[str, Callable[[dict], Any]] = {}
_ENTRY_POINT_GROUP = "datasets.structure_decoders"


@dataclass
class Structure:
    """Structure [`Feature`] for macromolecular structures (proteins, nucleic acids, ligands and complexes).

    A structure is stored as columns: one value per atom for each item of the PDBx/mmCIF `atom_site`
    category, plus the bonds the file records explicitly. Reading a structure does not parse a file, and
    the columns can be queried, filtered and projected like any other Arrow data.

    Stored layout:

    - `id`: the structure identifier (mmCIF data block name or PDB `HEADER` ID code).
    - `atoms`: per-atom lists named after mmCIF `atom_site` items: `group_PDB`, `pdbx_PDB_model_num`,
      `label_entity_id`, `label_asym_id`, `auth_asym_id`, `label_comp_id`, `label_seq_id`, `auth_seq_id`,
      `pdbx_PDB_ins_code`, `label_atom_id`, `label_alt_id`, `type_symbol`, `occupancy`, `B_iso_or_equiv`,
      `pdbx_formal_charge`, and `Cartn_xyz` (the `Cartn_x/y/z` coordinates as one `(n_atoms, 3)` column).
      All models and alternate locations are kept, one entry per `atom_site` row.
    - `bonds`: bonds recorded in the file (`struct_conn` in mmCIF/BinaryCIF, `CONECT` in PDB) as
      `atom_index_1`, `atom_index_2` (indices into the atoms of the first model), `conn_type_id` and
      `pdbx_value_order`. Bonds within standard residues are not stored in these files and are not added.

    Input: The Structure feature accepts as input:

    - A `str` or `pathlib.Path`: local path or URL of a PDB (`.pdb`, `.ent`), PDBx/mmCIF (`.cif`, `.mmcif`)
      or BinaryCIF (`.bcif`) file, optionally gzip, bz2 or zstd compressed. BinaryCIF needs `msgpack`.
    - `bytes`: the content of such a file (the format is detected from the content).
    - A `dict` with `path` and/or `bytes` keys, as above.
    - A `dict` in the stored layout (`atoms`, and optionally `id` and `bonds`), e.g. a decoded example.
    - A `biotite.structure.AtomArray` or `AtomArrayStack`.

    Output: depends on `decoder`. The default `"numpy"` decoder returns the stored layout with numpy
    arrays (missing `label_seq_id` as -1, missing `pdbx_formal_charge` as 0, missing floats as NaN).
    `"biotite"` returns a `biotite.structure.AtomArray` (or `AtomArrayStack` for several models). Other
    libraries can add decoders with [`~features.structure.register_structure_decoder`] or a
    `datasets.structure_decoders` entry point.

    Args:
        decoder (`str`, defaults to `"numpy"`):
            Name of the decoder that builds the returned object.
        decode (`bool`, defaults to `True`):
            Whether to decode the structure. If `False`, returns the stored layout as nested Python lists.

    Example:

    ```py
    >>> from datasets import Dataset, Structure
    >>> ds = Dataset.from_dict({"structure": ["path/to/1abc.cif.gz"]}).cast_column("structure", Structure())
    >>> ds[0]["structure"]["atoms"]["Cartn_xyz"].shape
    (1234, 3)
    >>> ds = ds.cast_column("structure", Structure(decoder="biotite"))
    >>> ds[0]["structure"]
    <biotite.structure.AtomArray ...>
    ```
    """

    decoder: str = "numpy"
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct([("id", pa.string()), ("atoms", _ATOMS_TYPE), ("bonds", _BONDS_TYPE)])
    _type: str = field(default="Structure", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, os.PathLike, bytes, bytearray, dict, Any]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `os.PathLike`, `bytes`, `dict` or `biotite.structure.AtomArray`):
                Data passed as input to Structure feature.

        Returns:
            `dict` in the stored layout.
        """
        if isinstance(value, (str, Path)):
            structure = read_structure(_read_file(str(value)), path=str(value))
        elif isinstance(value, (bytes, bytearray)):
            structure = read_structure(bytes(value))
        elif isinstance(value, dict) and "atoms" in value:
            structure = value
        elif isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            data = value["bytes"] if value.get("bytes") is not None else _read_file(value["path"])
            structure = read_structure(bytes(data), path=value.get("path"))
        elif hasattr(value, "coord") and hasattr(value, "get_annotation_categories"):
            structure = _from_biotite(value)
        else:
            raise ValueError(
                "A structure should be a file path, file bytes, a dict with 'path' or 'bytes', a dict with "
                f"'atoms', or a biotite AtomArray, but got {type(value)}."
            )
        return _to_storage(structure)

    def decode_example(self, value: dict, token_per_repo_id=None) -> Any:
        """Decode example structure into the object returned by `decoder`.

        Args:
            value (`dict`):
                A structure in the stored layout.
            token_per_repo_id (`dict`, *optional*):
                Unused; structures are stored inline.

        Returns:
            The decoded structure.
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Structure(decode=True) instead.")
        return get_structure_decoder(self.decoder)(_to_numpy(value))

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Features

        return self if self.decode else Features.from_arrow_schema(pa.schema(list(self.pa_type)))

    def cast_storage(self, storage: Union[pa.StringArray, pa.BinaryArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Structure arrow storage type.

        The Arrow types that can be converted to the Structure pyarrow storage type are:

        - `pa.string()` or `pa.large_string()` - paths of structure files, which are parsed
        - `pa.binary()` or `pa.large_binary()` - contents of structure files, which are parsed
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})` - file references, which are parsed
        - a struct with an `atoms` field in the stored layout; `id`, `bonds` and individual atom items may be
          omitted and are filled with nulls (atom items) or empty lists (bonds)

        Args:
            storage (`Union[pa.StringArray, pa.BinaryArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Structure arrow storage type.
        """
        is_file_reference = pa.types.is_struct(storage.type) and storage.type.get_field_index("atoms") < 0
        if (
            pa.types.is_string(storage.type)
            or pa.types.is_large_string(storage.type)
            or pa.types.is_binary(storage.type)
            or pa.types.is_large_binary(storage.type)
            or is_file_reference
        ):
            if is_file_reference and not {"bytes", "path"} & {f.name for f in storage.type}:
                raise TypeError(f"Can't cast {storage.type} to the Structure storage type.")
            encoded = [None if value is None else self.encode_example(value) for value in storage.to_pylist()]
            return pa.array(encoded, type=self.pa_type)
        if not pa.types.is_struct(storage.type):
            raise TypeError(f"Can't cast {storage.type} to the Structure storage type.")
        children = []
        for struct_field in self.pa_type:
            index = storage.type.get_field_index(struct_field.name)
            if index >= 0:
                child = storage.field(index)
                if pa.types.is_struct(struct_field.type):
                    child = _fill_struct(child, struct_field.type)
                children.append(array_cast(child, struct_field.type))
            elif struct_field.name == "bonds":
                empty = pa.array([[]] * len(storage), pa.list_(pa.int32()))
                children.append(
                    pa.StructArray.from_arrays(
                        [empty.cast(f.type) for f in struct_field.type], fields=list(struct_field.type)
                    )
                )
            else:
                children.append(pa.nulls(len(storage), struct_field.type))
        return pa.StructArray.from_arrays(children, fields=list(self.pa_type), mask=storage.is_null())


def register_structure_decoder(name: str, decoder: Callable[[dict], Any]) -> None:
    """Register a decoder usable as `Structure(decoder=name)`.

    Args:
        name (`str`):
            Name of the decoder.
        decoder (`Callable[[dict], Any]`):
            Function taking a structure in the stored layout with numpy arrays (the `"numpy"` decoder output)
            and returning the decoded object.
    """
    _DECODERS[name] = decoder


def get_structure_decoder(name: str) -> Callable[[dict], Any]:
    """Return the decoder registered as `name`, loading `datasets.structure_decoders` entry points if needed."""
    if name not in _DECODERS:
        for entry_point in entry_points(group=_ENTRY_POINT_GROUP):
            if entry_point.name == name:
                register_structure_decoder(name, entry_point.load())
                break
        else:
            raise ValueError(f"Unknown structure decoder '{name}'. Available decoders: {sorted(_DECODERS)}.")
    return _DECODERS[name]


def _read_file(path: str) -> bytes:
    if is_local_path(path):
        with open(path, "rb") as f:
            return f.read()
    with xopen(path, "rb", download_config=DownloadConfig()) as f:
        return f.read()


def _fill_struct(array: pa.StructArray, struct_type: pa.StructType) -> pa.StructArray:
    """Cast the fields of `array` to `struct_type`, adding missing fields as nulls and dropping extra ones."""
    if isinstance(array, pa.ChunkedArray):
        array = array.combine_chunks()
    children = [
        array_cast(array.field(f.name), f.type)
        if array.type.get_field_index(f.name) >= 0
        else pa.nulls(len(array), f.type)
        for f in struct_type
    ]
    return pa.StructArray.from_arrays(children, fields=list(struct_type), mask=array.is_null())


def _to_storage(structure: dict) -> dict:
    """Normalize a structure dict to the stored layout with flat numpy arrays (and Python lists for strings)."""
    atoms_in = structure["atoms"]
    n_atoms = len(atoms_in[COORD_COLUMN])
    atoms = {}
    for name, dtype, _ in ATOM_COLUMNS:
        values = atoms_in.get(name)
        atoms[name] = None if values is None else _column(values, dtype, n_atoms, name)
    coords = np.asarray(atoms_in[COORD_COLUMN], dtype=np.float32).reshape(n_atoms, 3)
    atoms[COORD_COLUMN] = list(coords)
    bonds_in = structure.get("bonds") or {}
    n_bonds = 0 if bonds_in.get("atom_index_1") is None else len(bonds_in["atom_index_1"])
    bonds = {}
    for name, dtype in BOND_COLUMNS:
        values = bonds_in.get(name)
        if values is None:
            if dtype != "str" and n_bonds:
                raise ValueError(f"Structure bonds are missing '{name}'.")
            values = [""] * n_bonds if dtype == "str" else []
        bonds[name] = _column(values, dtype, n_bonds, name)
    return {"id": structure.get("id") or "", "atoms": atoms, "bonds": bonds}


def _column(values, dtype: str, length: int, name: str) -> Union[list, np.ndarray]:
    if len(values) != length:
        raise ValueError(f"Structure item '{name}' has {len(values)} values, expected {length}.")
    if dtype == "str":
        return [str(v) for v in values]
    values = np.asarray(values)
    if values.dtype == object:  # contains missing values
        return [None if v is None else v for v in values.tolist()]
    return values.astype(dtype)


def _to_numpy(value: dict) -> dict:
    """Stored layout (Python lists, or numpy arrays from the numpy formatter) -> numpy arrays."""
    atoms_in, bonds_in = value["atoms"], value.get("bonds") or {}
    coords = atoms_in[COORD_COLUMN]
    if isinstance(coords, list):
        coords = np.fromiter(itertools.chain.from_iterable(coords), np.float32, 3 * len(coords))
    elif isinstance(coords, np.ndarray) and coords.dtype == object:
        coords = np.stack(coords) if len(coords) else np.zeros((0, 3))
    coords = np.asarray(coords, dtype=np.float32).reshape(-1, 3)
    atoms = {name: _as_numpy(atoms_in.get(name), dtype, len(coords)) for name, dtype, _ in ATOM_COLUMNS}
    atoms[COORD_COLUMN] = coords
    n_bonds = 0 if bonds_in.get("atom_index_1") is None else len(bonds_in["atom_index_1"])
    bonds = {name: _as_numpy(bonds_in.get(name), dtype, n_bonds) for name, dtype in BOND_COLUMNS}
    return {"id": value.get("id") or "", "atoms": atoms, "bonds": bonds}


def _as_numpy(values, dtype: str, length: int) -> np.ndarray:
    """Convert one stored column to numpy, filling missing values (see `_NUMPY_FILL`)."""
    fill = "" if dtype == "str" else _NUMPY_FILL[dtype]
    np_dtype = str if dtype == "str" else dtype
    if values is None:
        return np.full(length, fill, dtype=np_dtype)
    if isinstance(values, np.ndarray) and values.dtype != object:
        if values.dtype.kind == "f" and dtype not in ("str", "float32"):  # integers with nulls arrive as NaN
            values = np.where(np.isnan(values), fill, values)
        return values.astype(np_dtype, copy=False)
    values = list(values)
    if None in values:
        values = [fill if v is None else v for v in values]
    return np.asarray(values, dtype=np_dtype)


# ----------------------------------------------------------------------------------- built-in decoders

_BIOTITE_BOND_ORDER = {"sing": 1, "doub": 2, "trip": 3, "quad": 4}


def _decode_biotite(structure: dict):
    if not config.BIOTITE_AVAILABLE:
        raise ImportError("To decode structures with decoder='biotite', please install 'biotite'.")
    import biotite.structure as struc

    atoms = structure["atoms"]
    models = atoms["pdbx_PDB_model_num"]
    model_ids = np.unique(models)
    first = models == models[0]
    atom_array = struc.AtomArray(int(first.sum()))
    atom_array.coord = atoms[COORD_COLUMN][first]
    atom_array.chain_id = atoms["auth_asym_id"][first]
    atom_array.res_id = atoms["auth_seq_id"][first]
    atom_array.ins_code = atoms["pdbx_PDB_ins_code"][first]
    atom_array.res_name = atoms["label_comp_id"][first]
    atom_array.hetero = atoms["group_PDB"][first] == "HETATM"
    atom_array.atom_name = atoms["label_atom_id"][first]
    atom_array.element = atoms["type_symbol"][first]
    for annotation, item in [
        ("label_asym_id", "label_asym_id"),
        ("label_entity_id", "label_entity_id"),
        ("label_seq_id", "label_seq_id"),
        ("altloc_id", "label_alt_id"),
        ("b_factor", "B_iso_or_equiv"),
        ("occupancy", "occupancy"),
        ("charge", "pdbx_formal_charge"),
    ]:
        atom_array.set_annotation(annotation, atoms[item][first])
    bonds = structure["bonds"]
    order = [_BIOTITE_BOND_ORDER.get(o, 0) for o in bonds["pdbx_value_order"].tolist()]
    atom_array.bonds = struc.BondList(
        atom_array.array_length(),
        np.stack([bonds["atom_index_1"], bonds["atom_index_2"], np.asarray(order, dtype=np.int32)], axis=1),
    )
    if len(model_ids) == 1:
        return atom_array
    counts = {int((models == m).sum()) for m in model_ids}
    if len(counts) != 1:
        raise ValueError("Models have different atoms; use decoder='numpy' to read every model.")
    stack = struc.stack([atom_array] * len(model_ids))
    stack.coord = np.stack([atoms[COORD_COLUMN][models == m] for m in model_ids])
    return stack


def _from_biotite(atom_array) -> dict:
    """biotite AtomArray / AtomArrayStack -> stored layout."""
    coords = np.asarray(atom_array.coord, dtype=np.float32)
    n_models = coords.shape[0] if coords.ndim == 3 else 1
    coords = coords.reshape(-1, 3)
    n_atoms = coords.shape[0] // n_models
    categories = set(atom_array.get_annotation_categories())

    def annotation(name: str, default):
        values = atom_array.get_annotation(name) if name in categories else np.full(n_atoms, default)
        return np.tile(values, n_models)

    atoms = {
        "group_PDB": np.where(annotation("hetero", False), "HETATM", "ATOM"),
        "pdbx_PDB_model_num": np.repeat(np.arange(1, n_models + 1, dtype=np.int32), n_atoms),
        "label_entity_id": annotation("label_entity_id", ""),
        "label_asym_id": annotation("label_asym_id" if "label_asym_id" in categories else "chain_id", ""),
        "auth_asym_id": annotation("chain_id", ""),
        "label_comp_id": annotation("res_name", ""),
        "label_seq_id": annotation("label_seq_id", None),
        "auth_seq_id": annotation("res_id", 0),
        "pdbx_PDB_ins_code": annotation("ins_code", ""),
        "label_atom_id": annotation("atom_name", ""),
        "label_alt_id": annotation("altloc_id", ""),
        "type_symbol": annotation("element", ""),
        "occupancy": annotation("occupancy", np.nan),
        "B_iso_or_equiv": annotation("b_factor", np.nan),
        "pdbx_formal_charge": annotation("charge", 0),
        COORD_COLUMN: coords,
    }
    bonds = {}
    if atom_array.bonds is not None:
        order_names = {v: k for k, v in _BIOTITE_BOND_ORDER.items()}
        bond_array = atom_array.bonds.as_array()
        bonds = {
            "atom_index_1": bond_array[:, 0],
            "atom_index_2": bond_array[:, 1],
            "conn_type_id": [""] * len(bond_array),
            "pdbx_value_order": [order_names.get(int(o), "") for o in bond_array[:, 2]],
        }
    return {"id": "", "atoms": atoms, "bonds": bonds}


register_structure_decoder("numpy", lambda structure: structure)
register_structure_decoder("biotite", _decode_biotite)
