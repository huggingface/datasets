import os
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, TypedDict, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict


class DicomDict(TypedDict):
    bytes: Optional[bytes]
    path: Optional[str]


if TYPE_CHECKING:
    import pydicom

    from .features import FeatureType


@dataclass
class Dicom:
    """
    **Experimental.**
    Dicom [`Feature`] to read DICOM medical imaging files.

    Input: The Dicom feature accepts as input:
    - A `str`: Absolute path to the DICOM file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the DICOM file (i.e. random access is allowed).
    - A `dict` with the keys:
        - `path`: String with relative path of the DICOM file in a dataset repository.
        - `bytes`: Bytes of the DICOM file.
      This is useful for archived files with sequential access.

    - A `pydicom.FileDataset`: pydicom dataset object.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the DICOM data. If `False`,
            returns the underlying dictionary in the format `{"path": dicom_path, "bytes": dicom_bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, Dicom
    >>> ds = Dataset.from_dict({"dicom": ["path/to/file.dcm"]}).cast_column("dicom", Dicom())
    >>> ds.features["dicom"]
    Dicom(decode=True, id=None)
    >>> ds[0]["dicom"]
    <pydicom.dataset.FileDataset object at 0x7f8a1c2d8f40>
    >>> ds = ds.cast_column("dicom", Dicom(decode=False))
    >>> ds[0]["dicom"]
    {'bytes': None,
    'path': 'path/to/file.dcm'}
    ```
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)

    # Automatically constructed
    dtype: ClassVar[str] = "pydicom.dataset.FileDataset"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Dicom", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict, "pydicom.FileDataset"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, `pydicom.FileDataset` or `dict`):
                Data passed as input to Dicom feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.PYDICOM_AVAILABLE:
            import pydicom
        else:
            pydicom = None

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": value}
        elif pydicom is not None and isinstance(value, pydicom.dataset.FileDataset):
            # pydicom FileDataset object - try to get path or convert to bytes
            return encode_pydicom_dataset(value)
        elif isinstance(value, dict):
            if value.get("path") is not None and os.path.isfile(value["path"]):
                # we set "bytes": None to not duplicate the data if they're already available locally
                return {"bytes": None, "path": value.get("path")}
            elif value.get("bytes") is not None or value.get("path") is not None:
                # store the dicom bytes, and path is used to infer the format using the file extension
                return {"bytes": value.get("bytes"), "path": value.get("path")}
            else:
                raise ValueError(
                    f"A dicom sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
                )
        else:
            raise ValueError(
                f"A dicom sample should be a string, bytes, Path, pydicom FileDataset, or dict, but got {type(value)}."
            )

    def decode_example(
        self, value: DicomDict, token_per_repo_id: Optional[Dict[str, Union[str, bool]]] = None
    ) -> "pydicom.FileDataset":
        """Decode example DICOM file into pydicom FileDataset object.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with absolute or relative DICOM file path.
                - `bytes`: The bytes of the DICOM file.

            token_per_repo_id (`dict`, *optional*):
                To access and decode DICOM files from private repositories on
                the Hub, you can pass a dictionary
                repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `pydicom.FileDataset` objects
        """
        if not self.decode:
            raise NotImplementedError("Decoding is disabled for this feature. Please use Dicom(decode=True) instead.")

        if config.PYDICOM_AVAILABLE:
            import pydicom
        else:
            raise ImportError("To support decoding DICOM files, please install 'pydicom'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A dicom should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    dicom = pydicom.dcmread(path)
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
                    with xopen(path, "rb", download_config=download_config) as f:
                        dicom = pydicom.dcmread(f)
        else:
            bytesio = BytesIO(bytes_)
            dicom = pydicom.dcmread(bytesio)

        return dicom

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

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray, pa.BinaryArray]) -> pa.StructArray:
        """Cast an Arrow array to the Dicom arrow storage type.
        The Arrow types that can be converted to the Dicom pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the DICOM bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`Union[pa.StringArray, pa.StructArray, pa.BinaryArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Dicom arrow storage type, that is
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


def encode_pydicom_dataset(dicom_ds: "pydicom.FileDataset") -> dict[str, Optional[Union[str, bytes]]]:
    """
    Encode a pydicom FileDataset object into a dictionary.

    If the dataset has an associated file path, returns the path. Otherwise, serializes
    the dataset content into bytes.

    Args:
        dicom_ds: A pydicom FileDataset object.

    Returns:
        dict: A dictionary with "path" or "bytes" field.
    """
    if hasattr(dicom_ds, "filename") and dicom_ds.filename:
        return {"path": dicom_ds.filename, "bytes": None}

    # Serialize to bytes
    buffer = BytesIO()
    dicom_ds.save_as(buffer, write_like_original=False)
    return {"path": None, "bytes": buffer.getvalue()}
