import bz2
import gzip
import io
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict


if TYPE_CHECKING:
    import biotite.structure
    from atomworks.io.utils.atom_array_plus import AtomArrayPlus, AtomArrayPlusStack

    from .features import FeatureType


_COMPRESSION_EXTENSIONS = (".gz", ".gzip", ".bz2", ".zst")


class _AtomicStructureModels(list):
    """Different-atom models retaining their source encoding for pass-through maps."""

    def __init__(self, models, encoded):
        super().__init__(models)
        self._hf_encoded = encoded


@dataclass
class AtomicStructure:
    """Atomic structures decoded with AtomWorks, with source files preserved in Arrow.

    Paths and bytes are stored without reading, parsing, decompressing or changing the file.
    Decoding uses the AtomWorks ``minimal`` preset: no optional chemical cleanup,
    atom completion, water removal or assembly construction. AtomWorks minimal parsing
    selects the first alternate conformer, normalizes identifiers and infers bonds;
    the original file bytes are retained unchanged. Live atom arrays, RDKit molecules and ASE structures
    are serialized as BinaryCIF using AtomWorks.

    Args:
        parse_config (`dict`, *optional*):
            Opt into AtomWorks preparation at decode time. Accepts a `preset` and
            `ParseConfig` fields. Unspecified preparation options use the `minimal`
            preset. For example, `{"remove_waters": True}` removes waters, while
            `{"preset": "default"}` also opts into atom completion and other cleanup.
            Loading options such as `altloc` and `model` apply during decoding too.
        assembly (`str`, *optional*):
            Biological assembly to build at decode time, e.g. `"1"`. Defaults to the
            asymmetric unit. Requires assembly definitions in the source file.
        decode (`bool`, defaults to `True`):
            If `False`, return `{"path": path, "bytes": bytes}` without AtomWorks.

    Inputs may be paths, file bytes, dictionaries with `path` and/or `bytes`, biotite
    atom arrays or stacks, RDKit `Mol`, or ASE `Atoms`. Supported files are PDB, mmCIF,
    BinaryCIF, MOL/SDF (first record), and Mol2, optionally gzip, bz2 or zstd compressed.
    MOL/SDF and Mol2 bytes need a filename in `path` to identify the format.

    Outputs are `AtomArrayPlus`, `AtomArrayPlusStack`, or a list of arrays for models
    with different atoms. Decoded arrays retain their original encoding in the `_hf_encoded` system annotation,
    like Audio, so re-encoding them preserves the source. Use ``materialize(atoms)``
    to explicitly save edits or a prepared result without changing the original array.
    """

    parse_config: Optional[dict] = None
    assembly: Optional[str] = None
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "atomworks.io.utils.atom_array_plus.AtomArrayPlus"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="AtomicStructure", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, os.PathLike, bytes, bytearray, dict, Any]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `os.PathLike`, `bytes`, `dict`, `biotite.structure.AtomArray`, `rdkit.Chem.Mol` or `ase.Atoms`):
                Data passed as input to AtomicStructure feature.

        Returns:
            `dict` with "path" and "bytes" fields, preserving source files; live objects are serialized as BinaryCIF.
        """
        if isinstance(value, (str, os.PathLike)):
            return {"path": os.fspath(value), "bytes": None}
        if isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        if isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            return {
                "path": os.fspath(value["path"]) if value.get("path") is not None else None,
                "bytes": bytes(value["bytes"]) if value.get("bytes") is not None else None,
            }
        if isinstance(value, _AtomicStructureModels):
            return dict(value._hf_encoded)
        if hasattr(value, "get_annotation_categories") and type(value).__module__.startswith("atomworks."):
            if "_hf_encoded" in value.get_annotation_categories(n_body=0):
                retained = value.get_annotation("_hf_encoded", n_body=0).item()
                if retained["owner"] == id(value):
                    return dict(retained["value"])
        if hasattr(value, "coord") and hasattr(value, "get_annotation_categories"):
            _require_atomworks()
            return {"path": None, "bytes": _write(value)}
        if type(value).__module__.startswith("rdkit."):
            _require_atomworks()
            from atomworks.io.tools.rdkit import atom_array_from_rdkit

            atoms = atom_array_from_rdkit(value, remove_hydrogens=False)
            atoms.chain_id[:] = "A"
            return {"path": None, "bytes": _write(atoms)}
        if type(value).__module__.startswith("ase.") and hasattr(value, "get_positions"):
            _require_atomworks()
            return {"path": None, "bytes": _write(_from_ase(value))}
        raise ValueError(
            "An atomic structure should be a file path, file bytes, a dict with 'path' or 'bytes', a biotite "
            f"AtomArray, an RDKit Mol or an ASE Atoms, but got {type(value)}."
        )

    def materialize(self, atoms) -> dict:
        """Serialize the supplied atoms as BinaryCIF, ignoring retained source bytes.

        Use this in ``Dataset.map`` after editing a decoded array. The input is not
        modified and no preparation is run. Arrays, stacks and nonempty lists of
        models are supported. Unsupported annotations raise instead of being lost.
        Decode the result with ``AtomicStructure()`` to avoid preparing it twice.
        """
        _require_atomworks()
        return {"path": None, "bytes": _write(atoms)}

    def decode_example(
        self, value: dict, token_per_repo_id=None
    ) -> Union["AtomArrayPlus", "AtomArrayPlusStack", list["AtomArrayPlus"]]:
        """Decode a structure into AtomWorks arrays, retaining all models by default.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with absolute or relative file path.
                - `bytes`: The bytes of the file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode files from private repositories on the Hub, you can pass a dictionary
                repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            An `AtomArrayPlus` for one model, an `AtomArrayPlusStack` for matching
            models, or a list of arrays for models with different atoms.
        """
        if not self.decode:
            raise RuntimeError(
                "Decoding is disabled for this feature. Please use AtomicStructure(decode=True) instead."
            )
        _require_atomworks()
        path, data = value.get("path"), value.get("bytes")
        if data is None:
            if path is None:
                raise ValueError(f"A structure should have one of 'path' or 'bytes' but both are None in {value}.")
            data = _read_file(path, token_per_repo_id)
        atoms = self._read(_decompress(data), path)
        if isinstance(atoms, list):
            return _AtomicStructureModels(atoms, {"path": path, "bytes": data})
        else:
            # Preserve even compressed input bytes when a decoded row is passed through Dataset.map.
            # A supported system annotation survives slicing without adding attributes to AtomArrayPlus.
            # The owner check makes copies and slices serialize their own atoms instead of the full source.
            atoms.set_annotation("_hf_encoded", {"owner": id(atoms), "value": {"path": path, "bytes": data}}, n_body=0)
        return atoms

    def flatten(self) -> Union["FeatureType", dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from .features import Value

        return (
            self
            if self.decode
            else {
                "bytes": Value("binary"),
                "path": Value("string"),
            }
        )

    def cast_storage(self, storage: Union[pa.StringArray, pa.BinaryArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the AtomicStructure arrow storage type.

        The Arrow types that can be converted to the AtomicStructure pyarrow storage type are:

        - `pa.null()` - an empty or all-missing column
        - `pa.string()` or `pa.large_string()` - paths of structure files
        - `pa.binary()` or `pa.large_binary()` - contents of structure files
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})` - file references, kept as they are.

        Args:
            storage (`Union[pa.StringArray, pa.BinaryArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the AtomicStructure arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if pa.types.is_null(storage.type):  # e.g. an empty or all-missing column
            return pa.nulls(len(storage), self.pa_type)
        if pa.types.is_string(storage.type) or pa.types.is_large_string(storage.type):
            paths, data = storage.cast(pa.string()), pa.nulls(len(storage), pa.binary())
        elif pa.types.is_binary(storage.type) or pa.types.is_large_binary(storage.type):
            paths, data = pa.nulls(len(storage), pa.string()), storage.cast(pa.binary())
        elif pa.types.is_struct(storage.type) and {"bytes", "path"} & {f.name for f in storage.type}:
            paths = (
                storage.field("path").cast(pa.string())
                if "path" in storage.type.names
                else pa.nulls(len(storage), pa.string())
            )
            data = (
                storage.field("bytes").cast(pa.binary())
                if "bytes" in storage.type.names
                else pa.nulls(len(storage), pa.binary())
            )
        else:
            raise TypeError(f"Can't cast {storage.type} to the AtomicStructure storage type.")
        return pa.StructArray.from_arrays([data, paths], ["bytes", "path"], mask=storage.is_null())

    def embed_storage(
        self, storage: pa.StructArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.StructArray:
        """Embed structure files into the Arrow array.

        Rows that already hold their bytes are kept as they are.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.
            token_per_repo_id (`dict`, optional):
                Dictionary repo_id -> token to fetch the files bytes.
            local_files (`bool`, defaults to `True`):
                Whether to embed local files data in the array.
            remote_files (`bool`, defaults to `True`):
                Whether to embed remote files data in the array.

        Returns:
            `pa.StructArray`: Array in the AtomicStructure arrow storage type.
        """
        data, paths = storage.field("bytes").to_pylist(), storage.field("path").to_pylist()
        embedded = []
        embedded_paths = []
        for bytes_, path in zip(data, paths):
            if bytes_ is None and path is not None and (local_files if is_local_path(path) else remote_files):
                bytes_ = _read_file(path, token_per_repo_id)
            embedded.append(bytes_)
            embedded_paths.append(
                os.path.basename(path.split("::")[0]) if path is not None and bytes_ is not None else path
            )
        paths = embedded_paths
        return pa.StructArray.from_arrays(
            [pa.array(embedded, type=pa.binary()), pa.array(paths, type=pa.string())],
            ["bytes", "path"],
            mask=storage.is_null(),
        )

    # ------------------------------------------------------------------------------------------- decoding

    def _read(self, data: bytes, path: Optional[str]):
        """Load atoms, then apply only the preparation the user requested."""
        from atomworks.io import parse, prepare_atom_array
        from atomworks.io.config import ParseConfig
        from biotite.structure import AtomArrayStack

        file_type = _detect_format(data, path)
        options = dict(self.parse_config or {})
        preset = options.pop("preset", "minimal")
        unsupported = {
            "build_assembly",
            "file_type",
            "cache_dir",
            "load_from_cache",
            "save_to_cache",
            "keep_cif_block",
            "return_atom_array_plus",
        } & options.keys()
        if unsupported:
            raise ValueError(
                f"Unsupported parse_config options: {sorted(unsupported)}. Use assembly= for assembly selection."
            )
        preparation = ParseConfig.from_preset(preset, return_atom_array_plus=True, **options)
        preparation = preparation.replace(
            file_type=file_type,
            build_assembly=[str(self.assembly)] if self.assembly is not None else None,
            return_atom_array_plus=True,
            keep_cif_block=True,
            extra_fields=options.get("extra_fields", "all"),
            load_standard_annotations=options.get(
                "load_standard_annotations",
                file_type in ("cif", "bcif")
                and not preparation.add_missing_atoms
                and not preparation.convert_mse_to_met,
            ),
            add_bond_types_from_struct_conn=options.get(
                "add_bond_types_from_struct_conn",
                ("covale", "disulf", "metalc") if preset == "minimal" else preparation.add_bond_types_from_struct_conn,
            ),
            struct_conn_distance_policy=options.get(
                "struct_conn_distance_policy",
                "keep" if preset == "minimal" else preparation.struct_conn_distance_policy,
            ),
        )
        if file_type in ("mol", "mol2"):
            if self.assembly is not None:
                raise ValueError("Biological assemblies require PDB or CIF inputs.")
            if {"model", "altloc", "altloc_seed", "extra_fields", "load_standard_annotations"} & options.keys():
                raise ValueError("Model/conformer loading options are supported only for PDB and CIF inputs.")
            from atomworks.io.utils.atom_array_plus import as_atom_array_plus

            atoms = as_atom_array_plus(_read_small_molecule(data, file_type))
            return prepare_atom_array(atoms, config=preparation) if self.parse_config is not None else atoms

        source = io.StringIO(data.decode("utf-8")) if file_type in ("cif", "pdb") else io.BytesIO(data)
        from biotite import InvalidFileError

        try:
            result = parse(source, config=preparation)
        except InvalidFileError:
            if file_type != "pdb" or preparation.model is not None:
                raise
            from biotite.structure.io.pdb import PDBFile

            # AtomWorks supports heterogeneous CIF models; PDB requires explicit model selection.
            n_models = PDBFile.read(io.StringIO(data.decode("utf-8"))).get_model_count()
            if n_models < 2:
                raise
            result = [
                parse(io.StringIO(data.decode("utf-8")), config=preparation.replace(model=i))
                for i in range(1, n_models + 1)
            ]

        def select(entry, model_index=0):
            if self.assembly is None:
                atoms = entry["asym_unit"]
            else:
                try:
                    atoms = entry["assemblies"][str(self.assembly)]
                except KeyError as error:
                    raise ValueError(f"Invalid assembly ID: {self.assembly}") from error
            if isinstance(atoms, AtomArrayStack) and atoms.stack_depth() == 1:
                atoms = atoms[0]
            # Restore the feature's explicit bonds/boxes only for minimally decoded storage.
            block = entry.get("cif_block")
            if block is not None and "hf_atomic_structure" in block and self.assembly is None:
                ids = list(dict.fromkeys(block["atom_site"]["pdbx_PDB_model_num"].as_array(int)))
                if preparation.model is not None:
                    ids = [ids[preparation.model - 1 if preparation.model > 0 else preparation.model]]
                if isinstance(result, list):
                    ids = [ids[model_index]]
                if preset == "minimal" and not options.keys() - {
                    "model",
                    "altloc",
                    "altloc_seed",
                    "extra_fields",
                    "load_standard_annotations",
                }:
                    _restore_bonds(atoms, block, ids)
            return atoms

        return [select(entry, i) for i, entry in enumerate(result)] if isinstance(result, list) else select(result)


# ----------------------------------------------------------------------------------------------- helpers


def _write(atoms) -> bytes:
    import numpy as np
    from atomworks.io import CIFWriteConfig, atom_array_to_file
    from atomworks.io.utils.atom_array_plus import AtomArrayPlus
    from atomworks.io.utils.standard_annotations import STANDARD_ANNOTATIONS
    from biotite.structure import AtomArray, AtomArrayStack, BondList

    models = list(atoms) if isinstance(atoms, (list, AtomArrayStack)) else [atoms]
    if not models or any(not isinstance(model, AtomArray) for model in models):
        raise ValueError("materialize expects an atom array, stack, or nonempty list of atom arrays.")
    registered = set(STANDARD_ANNOTATIONS.get_field_names(n_body=1, include_aliases=True))
    structures, metadata, bonds, boxes = [], [], [], []
    for number, model in enumerate(models, 1):
        model = model.copy()
        if isinstance(model, AtomArrayPlus):
            model.del_annotation("_hf_encoded", n_body=0)
        unsupported = [
            name
            for name in model.get_annotation_categories()
            if np.ndim(model.get_annotation(name)) != 1 and name not in registered
        ]
        for n_body in (0, 2):
            if isinstance(model, AtomArrayPlus):
                allowed = set(STANDARD_ANNOTATIONS.get_field_names(n_body=n_body, include_aliases=True))
                unsupported.extend(
                    name for name in model.get_annotation_categories(n_body=n_body) if name not in allowed
                )
        if unsupported:
            raise ValueError(
                f"AtomWorks cannot serialize these custom annotations losslessly: {sorted(unsupported)}. "
                "Keep the original file bytes or use registered StandardAnnotations."
            )
        for name in model.get_annotation_categories():
            values = model.get_annotation(name)
            if values.dtype.kind in "iu" and values.size and (values.min() < -(2**31) or values.max() >= 2**31):
                raise ValueError(f"Annotation {name!r} exceeds BinaryCIF's signed 32-bit integer range.")
        if model.array_length() == 0:
            raise ValueError(
                "AtomWorks cannot materialize an empty model. Filter empty structures before preparing storage."
            )
        structure = model
        metadata.append([2, number, model.array_length(), int(model.bonds is not None)])
        if model.bonds is not None:
            bonds.extend([[number, *edge] for edge in model.bonds.as_array().tolist()])
        else:
            structure.bonds = BondList(model.array_length())
        if model.box is not None:
            boxes.append([number, *model.box.flatten().tolist()])
        structures.append(structure)
    categories = {
        "hf_atomic_structure": dict(zip(("version", "model_num", "n_atoms", "has_bonds"), np.array(metadata).T)),
    }
    if bonds:
        categories["hf_atomic_structure_bond"] = dict(
            zip(("model_num", "atom_1", "atom_2", "type"), np.array(bonds).T)
        )
    if boxes:
        categories["hf_atomic_structure_box"] = {
            "model_num": [row[0] for row in boxes],
            **{f"v{i}": [row[i + 1] for row in boxes] for i in range(9)},
        }
    return atom_array_to_file(
        structures[0] if len(structures) == 1 else structures,
        file_type="bcif",
        config=CIFWriteConfig(
            extra_fields="all",
            extra_categories=categories,
            include_entity_categories=True,
            chem_comp_source="array",
            chain_disambiguation=(
                "transformation_id"
                if all("transformation_id" in model.get_annotation_categories() for model in models)
                else None
            ),
            coord_decimals=None,
            date="1970-01-01",
            time="00:00:00",
            author="datasets",
        ),
    )


def _restore_bonds(atoms, block, model_ids):
    """Restore explicit bonds and boxes without chemical inference, including selected models/atoms."""
    import numpy as np
    from biotite.structure import AtomArrayStack, BondList

    for array in atoms if isinstance(atoms, list) else [atoms]:
        if block is None or "hf_atomic_structure" not in block:
            continue
        metadata = block["hf_atomic_structure"]
        version = metadata["version"].as_array(int)[0]
        if version not in (1, 2):
            raise ValueError("Unsupported AtomicStructure BinaryCIF version.")
        number = model_ids[0]
        mask = metadata["model_num"].as_array(int) == number if version == 2 else np.array([True])
        if metadata["has_bonds"].as_array(int)[mask][0]:
            n_atoms = metadata["n_atoms"].as_array(int)[mask][0] if version == 2 else array.array_length()
            edges = np.empty((0, 3), dtype=int)
            if "hf_atomic_structure_bond" in block:
                category = block["hf_atomic_structure_bond"]
                edges = np.column_stack([category[name].as_array(int) for name in ("atom_1", "atom_2", "type")])
                if version == 2:
                    edges = edges[category["model_num"].as_array(int) == number]
            indices = (
                array.atom_array_index
                if "atom_array_index" in array.get_annotation_categories()
                else np.arange(array.array_length())
            )
            array.bonds = BondList(n_atoms, edges)[np.asarray(indices, dtype=int)]
        else:
            array.bonds = None
        if version == 2:
            array.box = None
            if "hf_atomic_structure_box" in block:
                category = block["hf_atomic_structure_box"]
                ids = category["model_num"].as_array(int)
                values = np.column_stack([category[f"v{i}"].as_array(float) for i in range(9)])
                chosen = model_ids if isinstance(array, AtomArrayStack) else [number]
                selected = [values[ids == model][0].reshape(3, 3) for model in chosen if np.any(ids == model)]
                if len(selected) == len(chosen):
                    array.box = np.array(selected) if isinstance(array, AtomArrayStack) else selected[0]


def _is_bcif(data: bytes) -> bool:
    """Whether `data` looks like BinaryCIF, which is a MessagePack map."""
    return bool(data[:1]) and (0x80 <= data[0] <= 0x8F or data[0] in (0xDE, 0xDF))


def _require_atomworks():
    if not config.ATOMWORKS_AVAILABLE:
        raise ImportError(
            "To decode or serialize atomic structures, please install 'atomworks>=3.1.0' (Python >=3.12)."
        )
    try:
        from atomworks.io import atom_array_from_file, atom_array_to_file, parse, prepare_atom_array  # noqa: F401
    except ImportError as error:
        raise ImportError(
            "AtomicStructure requires AtomWorks >=3.1.0 with the atom-array IO API. "
            "Install atomworks>=3.1.0 and let it select its compatible Biotite dependency. "
            f"Original import error: {error}"
        ) from error


def _read_small_molecule(data: bytes, file_type: str):
    from atomworks.io.tools.rdkit import atom_array_from_rdkit, sdf_to_rdkit
    from rdkit import Chem

    text = data.decode("utf-8")
    if file_type == "mol2":
        molecule = Chem.MolFromMol2Block(text, removeHs=False)
        if molecule is None:
            raise ValueError("RDKit could not read the Mol2 file.")
    else:
        molecule = sdf_to_rdkit(io.StringIO(text), remove_hydrogens=False)
    atoms = atom_array_from_rdkit(molecule, remove_hydrogens=False)
    atoms.chain_id[:] = "A"
    return atoms


def _from_ase(atoms):
    """ASE has no names for atoms and residues, which the standard categories need: use the element and a number."""
    import numpy as np
    from atomworks.io.utils.ase_conversions import ase_to_atom_array
    from biotite.structure import BondList

    array = ase_to_atom_array(atoms)
    n = array.array_length()
    array.set_annotation("atom_name", np.char.add(array.element.astype(str), np.arange(1, n + 1).astype(str)))
    array.set_annotation("res_name", np.full(n, "UNL"))
    array.set_annotation("chain_id", np.full(n, "A"))
    if array.bonds is None:
        array.bonds = BondList(n)
    return array


def _read_file(path: str, token_per_repo_id: Optional[dict] = None) -> bytes:
    if is_local_path(path):
        with open(path, "rb") as f:
            return f.read()
    download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id or {}))
    with xopen(path, "rb", download_config=download_config) as f:
        return f.read()


def _resolve_token(path: str, token_per_repo_id: dict) -> Optional[str]:
    """Return the token for the Hub repo that `path` points into, or `None`."""
    source_url = path.split("::")[-1]
    pattern = config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
    fields = string_to_dict(source_url, pattern)
    return token_per_repo_id.get(fields["repo_id"]) if fields is not None else None


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


_FILE_TYPE_BY_EXTENSION = {
    ".cif": "cif",
    ".mmcif": "cif",
    ".bcif": "bcif",
    ".pdb": "pdb",
    ".ent": "pdb",
    ".mol": "mol",
    ".sdf": "mol",
    ".mol2": "mol2",
}


def _detect_format(data: bytes, path: Optional[str]) -> str:
    """`file_type` of atomworks (`cif`, `bcif`, `pdb`) or `mol` / `mol2`, from the extension, else the content."""
    if path:
        name = path.split("::")[0].lower()
        for ext in _COMPRESSION_EXTENSIONS:
            name = name.removesuffix(ext)
        for ext, file_type in _FILE_TYPE_BY_EXTENSION.items():
            if name.endswith(ext):
                return file_type
    if _is_bcif(data):
        return "bcif"
    for line in data[:4096].splitlines():
        if line.startswith(b"data_"):
            return "cif"
        if line.strip() and not line.startswith(b"#"):
            break
    return "pdb"


def encode_atomic_structure(atoms: "biotite.structure.AtomArray") -> dict:
    """Encode a biotite `AtomArray` or `AtomArrayStack` (or an atomworks `AtomArrayPlus`) as `{"bytes", "path"}`."""
    return AtomicStructure().encode_example(atoms)
