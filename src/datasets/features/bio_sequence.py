import os
from dataclasses import dataclass, field
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from Bio.SeqRecord import SeqRecord

    from .features import FeatureType


def encode_bio_seqrecord(record: "SeqRecord", format: str = "fasta") -> dict:
    """Serialize a ``SeqRecord`` back to the bytes of a single-record file."""
    from Bio import SeqIO

    buffer = StringIO()
    SeqIO.write(record, buffer, format)
    return {"path": None, "bytes": buffer.getvalue().encode("utf-8")}


def _resolve_token(path: str, token_per_repo_id: dict) -> Optional[str]:
    """Return the token for the Hub repo that ``path`` points into, or ``None``.

    ``string_to_dict`` returns ``None`` (it does not raise) when the URL is not a Hub
    dataset URL, so a plain https or s3 path resolves to "no token" instead of failing.
    """
    source_url = path.split("::")[-1]
    pattern = config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
    source_url_fields = string_to_dict(source_url, pattern)
    return token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None


@dataclass
class BioSequence:
    """
    **Experimental.**
    BioSequence [`Feature`] to read biological sequence records from a sequence file.

    A sequence file holds one or more records of residues with their identifiers and
    annotations. FASTA, FASTQ and GenBank are the same shape at this level, differing
    only in the parser used, so `format` selects the parser rather than the type.

    Input: The BioSequence feature accepts as input:
    - A `str`: Absolute path to the sequence file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the sequence file (i.e. random access is allowed).
    - A `dict` with the keys:
        - `path`: String with relative path of the sequence file in a dataset repository.
        - `bytes`: Bytes of the sequence file.
      This is useful for archived files with sequential access.

    - A `Bio.SeqRecord.SeqRecord`: biopython sequence record.

    Args:
        format (`str`, defaults to `"fasta"`):
            Name of the sequence format, as understood by `Bio.SeqIO`. Common values
            are `"fasta"`, `"fastq"` and `"genbank"`.
        decode (`bool`, defaults to `True`):
            Whether to decode the sequence data. If `False`,
            returns the underlying dictionary in the format `{"path": path, "bytes": bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, BioSequence
    >>> ds = Dataset.from_dict({"seq": ["path/to/sequences.fasta"]}).cast_column("seq", BioSequence())
    >>> ds.features["seq"]
    BioSequence(format='fasta', decode=True)
    >>> ds[0]["seq"]
    SeqRecord(seq=Seq('ACGT'), id='seq1', name='seq1', description='seq1', dbxrefs=[])
    >>> ds = ds.cast_column("seq", BioSequence(decode=False))
    >>> ds[0]["seq"]
    {'bytes': None,
    'path': 'path/to/sequences.fasta'}
    ```
    """

    format: str = "fasta"
    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "Bio.SeqRecord.SeqRecord"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="BioSequence", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict, "SeqRecord"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, `Bio.SeqRecord.SeqRecord` or `dict`):
                Data passed as input to BioSequence feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.BIOPYTHON_AVAILABLE:
            from Bio.SeqRecord import SeqRecord
        else:
            SeqRecord = None

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": bytes(value)}
        elif SeqRecord is not None and isinstance(value, SeqRecord):
            return encode_bio_seqrecord(value, self.format)
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A sequence sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "SeqRecord":
        """Decode example sequence file into a biopython record.

        A file may hold many records; this returns the first, because one row is one
        record. Use the packaged sequence loaders to expand a multi-record file into
        one row per record.

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
            `Bio.SeqRecord.SeqRecord`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use BioSequence(decode=True) instead.")

        if not config.BIOPYTHON_AVAILABLE:
            raise ImportError("To support decoding biological sequences, please install 'biopython'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A sequence should have one of 'path' or 'bytes' but both are None in {value}.")
            if is_local_path(path):
                with open(path, encoding="utf-8") as f:
                    return self._first_record(f, path)
            download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id))
            with xopen(path, "r", encoding="utf-8", download_config=download_config) as f:
                return self._first_record(f, path)
        else:
            with StringIO(bytes_.decode("utf-8")) as f:
                return self._first_record(f, path)

    def _first_record(self, handle, path: Optional[str]) -> "SeqRecord":
        """Return the first record in ``handle``, or raise if the file holds none."""
        from Bio import SeqIO

        for record in SeqIO.parse(handle, self.format):
            return record
        raise ValueError(f"No {self.format} record found in {path if path is not None else 'the given bytes'}.")

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
        """Cast an Arrow array to the BioSequence arrow storage type.
        The Arrow types that can be converted to the BioSequence pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the file bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`Union[pa.StringArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the BioSequence arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        return _cast_to_bytes_path_struct(storage, self.pa_type)

    def embed_storage(
        self, storage: pa.StructArray, token_per_repo_id=None, local_files: bool = True, remote_files: bool = True
    ) -> pa.StructArray:
        """Embed sequence files into the Arrow array.

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
            `pa.StructArray`: Array in the BioSequence arrow storage type.
        """
        return _embed_bytes_path_struct(
            storage, self.pa_type, token_per_repo_id, local_files=local_files, remote_files=remote_files
        )


def _cast_to_bytes_path_struct(storage, pa_type: pa.DataType) -> pa.StructArray:
    """Cast a string, binary or struct array to the shared ``struct<bytes, path>`` storage.

    BioSequence and BioStructure accept exactly the same inputs, so the conversion lives
    here rather than being written out twice.
    """
    if pa.types.is_string(storage.type):
        bytes_array = pa.array([None] * len(storage), type=pa.binary())
        storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
    elif pa.types.is_binary(storage.type):
        path_array = pa.array([None] * len(storage), type=pa.string())
        storage = pa.StructArray.from_arrays([storage, path_array], ["bytes", "path"], mask=storage.is_null())
    elif pa.types.is_struct(storage.type):
        if storage.type.get_field_index("bytes") >= 0:
            bytes_array = storage.field("bytes")
        else:
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
        if storage.type.get_field_index("path") >= 0:
            path_array = storage.field("path")
        else:
            path_array = pa.array([None] * len(storage), type=pa.string())
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
    return array_cast(storage, pa_type)


def _embed_bytes_path_struct(
    storage: pa.StructArray,
    pa_type: pa.DataType,
    token_per_repo_id=None,
    local_files: bool = True,
    remote_files: bool = True,
) -> pa.StructArray:
    """Read file contents into the ``bytes`` field, shared by both bio features."""
    if token_per_repo_id is None:
        token_per_repo_id = {}

    @no_op_if_value_is_null
    def path_to_bytes(path):
        download_config = DownloadConfig(token=_resolve_token(path, token_per_repo_id))
        with xopen(path, "rb", download_config=download_config) as f:
            return f.read()

    def should_embed(path: Optional[str]) -> bool:
        if path is None:
            return False
        return local_files if is_local_path(path) else remote_files

    bytes_array = pa.array(
        [
            (path_to_bytes(path) if should_embed(path) else bytes_)
            for bytes_, path in zip(storage.field("bytes").to_pylist(), storage.field("path").to_pylist())
        ],
        type=pa.binary(),
    )
    path_array = pa.array(
        [os.path.basename(path) if path is not None else None for path in storage.field("path").to_pylist()],
        type=pa.string(),
    )
    # Row nullness comes from the input row, not from whether bytes were embedded: a
    # path-only row with embedding disabled is still a valid row.
    storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=storage.is_null())
    return array_cast(storage, pa_type)
