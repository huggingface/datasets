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
    from atomworks.io.utils.atom_array_plus import AtomArrayPlus

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
    Decoding uses ``atom_array_from_file`` for minimal loading: no chemical preparation,
    atom completion, water removal or assembly construction. Alternate conformers and
    insertion codes are retained. Live atom arrays, RDKit molecules and ASE structures
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
    with different atoms. Decoded arrays retain their original encoding in `source_info["_hf_encoded"]`,
    like Audio, so re-encoding them preserves the source. Remove that entry before
    encoding if you intentionally want to store edits to a decoded array.
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
        source_info = getattr(value, "source_info", {})
        if source_info.get("_hf_encoded_owner") == id(value) and "_hf_encoded" in source_info:
            return dict(source_info["_hf_encoded"])
        if hasattr(value, "coord") and hasattr(value, "get_annotation_categories"):
            _require_atomworks()
            return {"path": None, "bytes": _write(value)}
        if type(value).__module__.startswith("rdkit."):
            _require_atomworks()
            from atomworks.io.tools.rdkit import atom_array_from_rdkit

            return {"path": None, "bytes": _write(atom_array_from_rdkit(value, remove_hydrogens=False))}
        if type(value).__module__.startswith("ase.") and hasattr(value, "get_positions"):
            _require_atomworks()
            return {"path": None, "bytes": _write(_from_ase(value))}
        raise ValueError(
            "An atomic structure should be a file path, file bytes, a dict with 'path' or 'bytes', a biotite "
            f"AtomArray, an RDKit Mol or an ASE Atoms, but got {type(value)}."
        )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "AtomArrayPlus":
        """Decode example structure into an atomworks `AtomArrayPlus`.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with absolute or relative file path.
                - `bytes`: The bytes of the file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode files from private repositories on the Hub, you can pass a dictionary
                repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            The decoded structure, an atomworks `AtomArrayPlus`.
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
            atoms.source_info = {
                **atoms.source_info,
                "_hf_encoded": {"path": path, "bytes": data},
                "_hf_encoded_owner": id(atoms),
            }
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
        from atomworks.io import atom_array_from_file, build_assembly, prepare_atom_array
        from atomworks.io.config import ParseConfig, get_config

        file_type = _detect_format(data, path)
        options = dict(self.parse_config or {})
        preset = options.pop("preset", "minimal")
        # Assembly selection has its own feature argument; disk caches do not belong to decoding.
        unsupported = {
            "build_assembly",
            "file_type",
            "cache_dir",
            "load_from_cache",
            "save_to_cache",
            "keep_cif_block",
        } & options.keys()
        if unsupported:
            raise ValueError(
                f"Unsupported parse_config options: {sorted(unsupported)}. Use assembly= for assembly selection."
            )
        preparation = None
        if self.parse_config is not None or self.assembly is not None:
            preparation = get_config(
                preset,
                cls=ParseConfig,
                **{
                    "build_assembly": None,
                    "return_atom_array_plus": True,
                    "fix_ligands_at_symmetry_centers": False,
                    **options,
                },
            )
        if file_type in ("mol", "mol2"):
            if {"model", "altloc", "altloc_seed", "extra_fields", "load_standard_annotations"} & options.keys():
                raise ValueError("Model/conformer loading options are supported only for PDB and CIF inputs.")
            from atomworks.io.utils.atom_array_plus import as_atom_array_plus

            atoms = as_atom_array_plus(_read_small_molecule(data, file_type))
        else:
            source = io.StringIO(data.decode("utf-8")) if file_type in ("cif", "pdb") else io.BytesIO(data)
            # No config preserves all conformers and insertion codes. A config explicitly opts into parser selection.
            loading_fields = {"model", "altloc", "altloc_seed", "extra_fields", "load_standard_annotations"}
            loading_config = preparation if loading_fields & options.keys() else None
            atoms = atom_array_from_file(source, file_type, config=loading_config)
            _restore_bonds(atoms)

        def prepare(array):
            if preparation is not None:
                array = prepare_atom_array(array, config=preparation)
            if self.assembly is not None:
                array = build_assembly(
                    array,
                    str(self.assembly),
                    fix_ligands_at_symmetry_centers=preparation.fix_ligands_at_symmetry_centers,
                )
            return array

        return [prepare(array) for array in atoms] if isinstance(atoms, list) else prepare(atoms)


# ----------------------------------------------------------------------------------------------- helpers


def _write(atoms) -> bytes:
    import numpy as np
    from atomworks.io import CIFWriteConfig, atom_array_to_file
    from atomworks.io.utils.atom_array_plus import AtomArrayPlus, AtomArrayPlusStack
    from atomworks.io.utils.standard_annotations import STANDARD_ANNOTATIONS
    from biotite.structure import BondList

    # The development writer supports scalar atom fields and registered StandardAnnotations.
    registered = set(STANDARD_ANNOTATIONS.get_field_names(n_body=1, include_aliases=True))
    unsupported = [
        name
        for name in atoms.get_annotation_categories()
        if np.ndim(atoms.get_annotation(name)) != 1 and name not in registered
    ]
    for n_body in (0, 2):
        if isinstance(atoms, (AtomArrayPlus, AtomArrayPlusStack)):
            allowed = set(STANDARD_ANNOTATIONS.get_field_names(n_body=n_body, include_aliases=True))
            unsupported.extend(name for name in atoms.get_annotation_categories(n_body=n_body) if name not in allowed)
    if unsupported:
        raise ValueError(
            f"AtomWorks cannot serialize these custom annotations losslessly: {sorted(unsupported)}. "
            "Keep the original file bytes or use registered StandardAnnotations."
        )
    # Work on a copy: the writer needs a BondList even when the source has no bond information.
    structure = atoms.copy()
    bonds = structure.bonds
    edges = bonds.as_array() if bonds is not None else np.empty((0, 3), dtype=np.uint32)
    if bonds is None:
        structure.bonds = BondList(structure.array_length())
    categories = {
        "hf_atomic_structure": {"version": [1], "has_bonds": [int(bonds is not None)]},
    }
    if len(edges):
        categories["hf_atomic_structure_bond"] = {"atom_1": edges[:, 0], "atom_2": edges[:, 1], "type": edges[:, 2]}
    return atom_array_to_file(
        structure,
        file_type="bcif",
        config=CIFWriteConfig(
            extra_fields="all",
            extra_categories=categories,
            include_entity_categories=True,
            chem_comp_source="array",
            coord_decimals=None,
            date="1970-01-01",
            time="00:00:00",
            author="datasets",
        ),
    )


def _restore_bonds(atoms):
    """Restore explicit bonds for live arrays serialized by this feature, without chemical inference."""
    import numpy as np
    from biotite.structure import BondList

    for array in atoms if isinstance(atoms, list) else [atoms]:
        block = array.source_info.get("cif_block")
        if block is None or "hf_atomic_structure" not in block:
            continue
        metadata = block["hf_atomic_structure"]
        if metadata["version"].as_array(int)[0] != 1:
            raise ValueError("Unsupported AtomicStructure BinaryCIF version.")
        if metadata["has_bonds"].as_array(int)[0]:
            if "hf_atomic_structure_bond" in block:
                category = block["hf_atomic_structure_bond"]
                edges = np.column_stack([category[name].as_array(int) for name in ("atom_1", "atom_2", "type")])
                array.bonds = BondList(array.array_length(), edges)
            else:
                array.bonds = BondList(array.array_length())
        else:
            array.bonds = None


def _is_bcif(data: bytes) -> bool:
    """Whether `data` looks like BinaryCIF, which is a MessagePack map."""
    return bool(data[:1]) and (0x80 <= data[0] <= 0x8F or data[0] in (0xDE, 0xDF))


def _require_atomworks():
    if not config.ATOMWORKS_AVAILABLE:
        raise ImportError(
            "To decode or serialize atomic structures, please install 'atomworks' with the atom-array IO API (Python >=3.12)."
        )
    try:
        from atomworks.io import atom_array_from_file, atom_array_to_file, build_assembly, prepare_atom_array  # noqa: F401
    except ImportError as error:
        raise ImportError(
            "AtomicStructure requires AtomWorks with atom_array_from_file, prepare_atom_array and build_assembly. "
            "Install the supported development version and its pinned dependencies. "
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
        return atom_array_from_rdkit(molecule, remove_hydrogens=False)
    atoms = atom_array_from_rdkit(sdf_to_rdkit(io.StringIO(text), remove_hydrogens=False), remove_hydrogens=False)
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
