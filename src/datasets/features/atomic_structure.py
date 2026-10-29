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


@dataclass
class AtomicStructure:
    """AtomicStructure [`Feature`] for atomic structures: proteins, nucleic acids, small molecules and complexes.

    Structures are read with [`atomworks`](https://github.com/RosettaCommons/atomworks) when the dataset is created
    and stored as [BinaryCIF](https://github.com/molstar/BinaryCIF) files written by atomworks, so every row decodes
    the same way and without parsing. The file holds the usual categories (`atom_site`, `chem_comp`,
    `struct_conn`, ...), which any BinaryCIF reader (biotite, Mol*, PyMOL) opens, plus what atomworks needs to give the
    exact `AtomArrayPlus` back: every annotation with its dtype, bonds, box, and per-structure and per-pair
    annotations.

    Input: The AtomicStructure feature accepts as input:

    - A `str` or `pathlib.Path`: local path or URL of a PDBx/mmCIF (`.cif`, `.mmcif`), BinaryCIF (`.bcif`),
      PDB (`.pdb`, `.ent`), MOL/SDF (`.mol`, `.sdf`, first record) or Mol2 (`.mol2`) file, optionally gzip, bz2 or
      zstd compressed.
    - `bytes`: the content of such a file. MOL, SDF and Mol2 need a path or a `dict` with a `path`.
    - A `dict` with `path` and/or `bytes` keys, as above.
    - A `biotite.structure.AtomArray`, `AtomArrayStack`, or atomworks `AtomArrayPlus`, which is stored as it is.
    - An `rdkit.Chem.Mol` or an `ase.Atoms`.

    Output: an atomworks `AtomArrayPlus`, or `AtomArrayPlusStack` when there are several models. It is a biotite
    `AtomArray` that also carries per-structure and per-pair annotations.

    Args:
        parse_config (`dict`, *optional*):
            Options of the atomworks pipeline used to read files: a `preset` name (`"default"`, `"rcsb"`,
            `"lightweight"`, ...) and fields of `atomworks.io.config.ParseConfig`, e.g.
            `{"preset": "rcsb", "remove_waters": False}`.
        assembly (`str`, *optional*):
            Biological assembly to store, e.g. `"1"`. By default the asymmetric unit is stored.
        decode (`bool`, defaults to `True`):
            Whether to decode the structure. If `False`, returns the underlying dictionary in the format
            `{"path": path, "bytes": bytes}`.

    Example:

    ```py
    >>> from datasets import AtomicStructure, Dataset
    >>> ds = Dataset.from_dict({"structure": ["path/to/1abc.cif.gz"]}).cast_column("structure", AtomicStructure())
    >>> ds[0]["structure"]
    <atomworks.io.utils.atom_array_plus.AtomArrayPlus ...>
    ```
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
            `dict` with "path" and "bytes" fields, the bytes being the BinaryCIF file of the structure.
        """
        if not config.ATOMWORKS_AVAILABLE:
            raise ImportError("To support encoding atomic structures, please install 'atomworks'.")

        path = None
        if isinstance(value, (str, os.PathLike)):
            path = os.fspath(value)
            data = _read_file(path)
        elif isinstance(value, (bytes, bytearray)):
            data = bytes(value)
        elif isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            path = value.get("path")
            data = bytes(value["bytes"]) if value.get("bytes") is not None else _read_file(path)
        elif hasattr(value, "coord") and hasattr(value, "get_annotation_categories"):
            return {"path": None, "bytes": self._write(value)}
        elif type(value).__module__.startswith("rdkit."):
            from atomworks.io.tools.rdkit import atom_array_from_rdkit

            return {"path": None, "bytes": self._write(atom_array_from_rdkit(value))}
        elif type(value).__module__.startswith("ase.") and hasattr(value, "get_positions"):
            return {"path": None, "bytes": self._write(_from_ase(value))}
        else:
            raise ValueError(
                "An atomic structure should be a file path, file bytes, a dict with 'path' or 'bytes', a biotite "
                f"AtomArray, an RDKit Mol or an ASE Atoms, but got {type(value)}."
            )
        data = _decompress(data)
        if not _is_stored(data):
            data = self._write(self._read(data, path), _entry_id(path))
        return {"path": os.path.basename(path.split("::")[0]) if path else None, "bytes": data}

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
        if not config.ATOMWORKS_AVAILABLE:
            raise ImportError("To support decoding atomic structures, please install 'atomworks'.")

        path, data = value["path"], value["bytes"]
        if data is None:
            if path is None:
                raise ValueError(f"A structure should have one of 'path' or 'bytes' but both are None in {value}.")
            data = _read_file(path, token_per_repo_id)
        data = _decompress(data)
        if _is_stored(data):
            from atomworks.io import read_atom_array

            return read_atom_array(io.BytesIO(data), file_type="bcif")
        return self._read(data, path)  # a structure file that was not written by this feature, e.g. a path-only row

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
        - `pa.string()` or `pa.large_string()` - paths of structure files, which are read
        - `pa.binary()` or `pa.large_binary()` - contents of structure files, which are read
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})` - file references, which are read. Files
          written by this feature are kept as they are.

        Args:
            storage (`Union[pa.StringArray, pa.BinaryArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the AtomicStructure arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if pa.types.is_null(storage.type):  # e.g. an empty or all-missing column
            return pa.nulls(len(storage), self.pa_type)
        is_struct = pa.types.is_struct(storage.type)
        is_file_reference = is_struct and {"bytes", "path"} & {f.name for f in storage.type}
        if is_file_reference or any(
            check(storage.type)
            for check in (pa.types.is_string, pa.types.is_large_string, pa.types.is_binary, pa.types.is_large_binary)
        ):
            encoded = [None if value is None else self.encode_example(value) for value in storage.to_pylist()]
            return pa.array(encoded, type=self.pa_type)
        raise TypeError(f"Can't cast {storage.type} to the AtomicStructure storage type.")

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
        for bytes_, path in zip(data, paths):
            if bytes_ is None and path is not None and (local_files if is_local_path(path) else remote_files):
                bytes_ = _read_file(path, token_per_repo_id)
            embedded.append(bytes_)
        paths = [os.path.basename(p) if p is not None else None for p in paths]
        return pa.StructArray.from_arrays(
            [pa.array(embedded, type=pa.binary()), pa.array(paths, type=pa.string())],
            ["bytes", "path"],
            mask=storage.is_null(),
        )

    # ------------------------------------------------------------------------------------------- encoding

    def _read(self, data: bytes, path: Optional[str]):
        """A structure file -> atomworks `AtomArrayPlus` (or stack)."""
        file_type = _detect_format(data, path)
        if file_type in ("mol", "mol2"):
            return _read_small_molecule(data, file_type)
        from atomworks.io import parse
        from atomworks.io.config import ParseConfig, get_config

        options = dict(self.parse_config or {})
        preset = options.pop("preset", "default")
        options = {
            "file_type": file_type,
            "build_assembly": None if self.assembly is None else [str(self.assembly)],
            "return_atom_array_plus": True,
            **options,
        }
        source = io.StringIO(data.decode("utf-8")) if file_type in ("cif", "pdb") else io.BytesIO(data)
        result = parse(source, config=get_config(preset, cls=ParseConfig, **options))
        result = result[0] if isinstance(result, list) else result
        atoms = result["asym_unit"] if self.assembly is None else result["assemblies"][str(self.assembly)]
        return atoms[0] if hasattr(atoms, "stack_depth") and atoms.stack_depth() == 1 else atoms

    def _write(self, atoms, entry_id: str = "structure") -> bytes:
        from atomworks.io.utils.io_utils import CIFWriteConfig, to_cif_buffer

        write_config = CIFWriteConfig(
            id=entry_id,
            extra_fields="all",  # everything needed to read the array back exactly
            chem_comp_source="array",
            chain_disambiguation="transformation_id"
            if "transformation_id" in atoms.get_annotation_categories()
            else None,
        )
        return to_cif_buffer(atoms, as_bcif=True, config=write_config).getvalue()


# ----------------------------------------------------------------------------------------------- helpers


def _is_bcif(data: bytes) -> bool:
    """Whether `data` looks like BinaryCIF, which is a MessagePack map."""
    return bool(data[:1]) and (0x80 <= data[0] <= 0x8F or data[0] in (0xDE, 0xDF))


def _is_stored(data: bytes) -> bool:
    """Whether `data` is a BinaryCIF file written by atomworks with everything needed to read it back exactly."""
    return _is_bcif(data) and b"atomworks_annotation" in data  # category names are not compressed in BinaryCIF


def _read_small_molecule(data: bytes, file_type: str):
    from atomworks.io.tools.inference import sdf_to_annotated_atom_array
    from atomworks.io.tools.rdkit import atom_array_from_rdkit
    from rdkit import Chem

    text = data.decode("utf-8")
    if file_type == "mol2":
        molecule = Chem.MolFromMol2Block(text)
        if molecule is None:
            raise ValueError("RDKit could not read the Mol2 file.")
        return atom_array_from_rdkit(molecule)
    return sdf_to_annotated_atom_array(io.StringIO(text), chain_id="A")


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


def _entry_id(path: Optional[str]) -> str:
    if not path:
        return "structure"
    name = os.path.basename(path.split("::")[0])
    for ext in _COMPRESSION_EXTENSIONS:
        name = name.removesuffix(ext)
    return os.path.splitext(name)[0] or "structure"


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
