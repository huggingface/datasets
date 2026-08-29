import os
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict
from .bio_sequence import _cast_to_bytes_path_struct, _embed_bytes_path_struct


if TYPE_CHECKING:
    from Bio.PDB.Structure import Structure

    from .features import FeatureType


# Parser class name in Bio.PDB for each supported structure format.
_PARSERS: dict[str, str] = {"pdb": "PDBParser", "mmcif": "MMCIFParser"}


def encode_bio_structure(structure: "Structure", format: str = "pdb") -> dict:
    """Serialize a ``Structure`` back to the bytes of a structure file."""
    from Bio.PDB import MMCIFIO, PDBIO

    io = PDBIO() if format == "pdb" else MMCIFIO()
    io.set_structure(structure)
    buffer = StringIO()
    io.save(buffer)
    return {"path": None, "bytes": buffer.getvalue().encode("utf-8")}


@dataclass
class BioStructure:
    """
    **Experimental.**
    BioStructure [`Feature`] to read macromolecular structures from a structure file.

    A structure file holds the three-dimensional coordinates of a molecule's atoms,
    grouped into chains and residues. PDB and mmCIF describe the same objects and
    differ only in the parser used, so `format` selects the parser rather than the type.

    Input: The BioStructure feature accepts as input:
    - A `str`: Absolute path to the structure file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the structure file (i.e. random access is allowed).
    - A `dict` with the keys:
        - `path`: String with relative path of the structure file in a dataset repository.
        - `bytes`: Bytes of the structure file.
      This is useful for archived files with sequential access.

    - A `Bio.PDB.Structure.Structure`: biopython structure.

    Args:
        format (`str`, defaults to `"pdb"`):
            Structure format, either `"pdb"` or `"mmcif"`.
        decode (`bool`, defaults to `True`):
            Whether to decode the structure data. If `False`,
            returns the underlying dictionary in the format `{"path": path, "bytes": bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, BioStructure
    >>> ds = Dataset.from_dict({"st": ["path/to/1abc.pdb"]}).cast_column("st", BioStructure())
    >>> ds.features["st"]
    BioStructure(format='pdb', decode=True)
    >>> ds[0]["st"]
    <Structure id=1abc>
    >>> ds = ds.cast_column("st", BioStructure(decode=False))
    >>> ds[0]["st"]
    {'bytes': None,
    'path': 'path/to/1abc.pdb'}
    ```
    """

    format: str = "pdb"
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "Bio.PDB.Structure.Structure"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="BioStructure", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict, "Structure"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, `Bio.PDB.Structure.Structure` or `dict`):
                Data passed as input to BioStructure feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.BIOPYTHON_AVAILABLE:
            from Bio.PDB.Structure import Structure
        else:
            Structure = None

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        elif Structure is not None and isinstance(value, Structure):
            return encode_bio_structure(value, self.format)
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A structure sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "Structure":
        """Decode example structure file into a biopython structure.

        Args:
            value (`str` or `dict`):
                A string with the absolute file path, or a dictionary with
                keys:

                - `path`: String with absolute or relative file path.
                - `bytes`: The bytes of the file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode files from private repositories on
                the Hub, you can pass a dictionary
                repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `Bio.PDB.Structure.Structure`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use BioStructure(decode=True) instead.")

        if not config.BIOPYTHON_AVAILABLE:
            raise ImportError("To support decoding macromolecular structures, please install 'biopython'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        structure_id = os.path.splitext(os.path.basename(path))[0] if path else "structure"

        if bytes_ is None:
            if path is None:
                raise ValueError(f"A structure should have one of 'path' or 'bytes' but both are None in {value}.")
            if is_local_path(path):
                with open(path, encoding="utf-8") as f:
                    return self._parse(f, structure_id)
            source_url = path.split("::")[-1]
            pattern = (
                config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
            )
            try:
                repo_id = string_to_dict(source_url, pattern)["repo_id"]
                token = token_per_repo_id.get(repo_id)
            except ValueError:
                token = None
            download_config = DownloadConfig(token=token)
            with xopen(path, "r", download_config=download_config) as f:
                return self._parse(f, structure_id)
        else:
            with StringIO(bytes_.decode("utf-8")) as f:
                return self._parse(f, structure_id)

    def _parse(self, handle, structure_id: str) -> "Structure":
        """Parse ``handle`` with the parser for this feature's format."""
        import Bio.PDB

        try:
            parser_name = _PARSERS[self.format]
        except KeyError:
            raise ValueError(
                f"Unsupported structure format '{self.format}'. Supported formats are: {sorted(_PARSERS)}."
            ) from None
        # QUIET silences the discontinuity warnings that most real PDB entries trigger.
        parser = getattr(Bio.PDB, parser_name)(QUIET=True)
        return parser.get_structure(structure_id, handle)

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

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the BioStructure arrow storage type.
        The Arrow types that can be converted to the BioStructure pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the file bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`Union[pa.StringArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the BioStructure arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        return _cast_to_bytes_path_struct(storage, self.pa_type)

    def embed_storage(
        self, storage: pa.StructArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.StructArray:
        """Embed structure files into the Arrow array.

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
            `pa.StructArray`: Array in the BioStructure arrow storage type.
        """
        return _embed_bytes_path_struct(
            storage, self.pa_type, token_per_repo_id, local_files=local_files, remote_files=remote_files
        )
