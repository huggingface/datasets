import os
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    import pdfplumber

    from .features import FeatureType


def pdf_to_bytes(pdf: "pdfplumber.pdf.PDF") -> bytes:
    """Convert a pdfplumber.pdf.PDF object to bytes."""
    with BytesIO() as buffer:
        for page in pdf.pages:
            buffer.write(page.pdf.stream)
        return buffer.getvalue()


@dataclass
class Pdf:
    """
    **Experimental.**
    Pdf [`Feature`] to read pdf documents from a pdf file.

    Input: The Pdf feature accepts as input:
    - A `str`: Absolute path to the pdf file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the pdf file (i.e. random access is allowed).
    - A `dict` with the keys:
        - `path`: String with relative path of the pdf file in a dataset repository.
        - `bytes`: Bytes of the pdf file.
      This is useful for archived files with sequential access.

    - A `pdfplumber.pdf.PDF`: pdfplumber pdf object.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the pdf data. If `False`,
            returns the underlying dictionary in the format `{"path": pdf_path, "bytes": pdf_bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, Pdf
    >>> ds = Dataset.from_dict({"pdf": ["path/to/pdf/file.pdf"]}).cast_column("pdf", Pdf())
    >>> ds.features["pdf"]
    Pdf(decode=True, id=None)
    >>> ds[0]["pdf"]
    <pdfplumber.pdf.PDF object at 0x7f8a1c2d8f40>
    >>> ds = ds.cast_column("pdf", Pdf(decode=False))
    >>> ds[0]["pdf"]
    {'bytes': None,
    'path': 'path/to/pdf/file.pdf'}
    ```
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "pdfplumber.pdf.PDF"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Pdf", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict, "pdfplumber.pdf.PDF"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, `pdfplumber.pdf.PDF` or `dict`):
                Data passed as input to Pdf feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.PDFPLUMBER_AVAILABLE:
            import pdfplumber
        else:
            pdfplumber = None

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": value}
        elif pdfplumber is not None and isinstance(value, pdfplumber.pdf.PDF):
            # convert the pdfplumber.pdf.PDF to bytes
            return encode_pdfplumber_pdf(value)
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the pdf bytes, and path is used to infer the pdf format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A pdf sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "pdfplumber.pdf.PDF":
        """Decode example pdf file into pdf data.

        Args:
            value (`str` or `dict`):
                A string with the absolute pdf file path, a dictionary with
                keys:

                - `path`: String with absolute or relative pdf file path.
                - `bytes`: The bytes of the pdf file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode pdf files from private repositories on
                the Hub, you can pass a dictionary
                repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `pdfplumber.pdf.PDF`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Pdf(decode=True) instead.")

        if config.PDFPLUMBER_AVAILABLE:
            import pdfplumber
        else:
            raise ImportError("To support decoding pdfs, please install 'pdfplumber'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A pdf should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    pdf = pdfplumber.open(path)
                else:
                    source_url = path.split("::")[-1]
                    pattern = (
                        config.HUB_DATASETS_URL
                        if source_url.startswith(config.HF_ENDPOINT)
                        else config.HUB_DATASETS_HFFS_URL
                    )
                    try:
                        repo_id = string_to_dict(source_url, pattern)["repo_id"]
                        token = token_per_repo_id.get(repo_id)
                    except ValueError:
                        token = None
                    download_config = DownloadConfig(token=token)
                    f = xopen(path, "rb", download_config=download_config)
                    return pdfplumber.open(f)
        else:
            with pdfplumber.open(BytesIO(bytes_)) as p:
                pdf = p

        return pdf

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
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

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray, pa.ListArray]) -> pa.StructArray:
        """Cast an Arrow array to the Pdf arrow storage type.
        The Arrow types that can be converted to the Pdf pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the image bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter
        - `pa.list(*)` - it must contain the pdf array data

        Args:
            storage (`Union[pa.StringArray, pa.StructArray, pa.ListArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Pdf arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
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
        return array_cast(storage, self.pa_type)

    def embed_storage(self, storage: pa.StructArray, token_per_repo_id=None) -> pa.StructArray:
        """Embed PDF files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            `pa.StructArray`: Array in the PDF arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if token_per_repo_id is None:
            token_per_repo_id = {}

        @no_op_if_value_is_null
        def path_to_bytes(path):
            source_url = path.split("::")[-1]
            pattern = (
                config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
            )
            source_url_fields = string_to_dict(source_url, pattern)
            token = token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None
            download_config = DownloadConfig(token=token)
            with xopen(path, "rb", download_config=download_config) as f:
                return f.read()

        bytes_array = pa.array(
            [
                (path_to_bytes(x["path"]) if x["bytes"] is None else x["bytes"]) if x is not None else None
                for x in storage.to_pylist()
            ],
            type=pa.binary(),
        )
        path_array = pa.array(
            [os.path.basename(path) if path is not None else None for path in storage.field("path").to_pylist()],
            type=pa.string(),
        )
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)


def encode_pdfplumber_pdf(pdf: "pdfplumber.pdf.PDF") -> dict:
    """
    Encode a pdfplumber.pdf.PDF object into a dictionary.

    If the PDF has an associated file path, returns the path. Otherwise, serializes
    the PDF content into bytes.

    Args:
        pdf (pdfplumber.pdf.PDF): A pdfplumber PDF object.

    Returns:
        dict: A dictionary with "path" or "bytes" field.
    """
    if hasattr(pdf, "stream") and hasattr(pdf.stream, "name") and pdf.stream.name:
        # Return the path if the PDF has an associated file path
        return {"path": pdf.stream.name, "bytes": None}
    else:
        # Convert the PDF to bytes if no path is available
        return {"path": None, "bytes": pdf_to_bytes(pdf)}
