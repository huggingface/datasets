from openexr_numpy import imwrite as exwrite
from openexr_numpy import imread as exload

import os
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union, Tuple

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict

if TYPE_CHECKING:
    from .features import FeatureType

@dataclass
class Exr:
    """Exr [`Feature`] to read Exr image data from an Exr file.

    Input: The Exr feature accepts as input:
    - A `str`: Absolute path to the Exr file (i.e., random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the Exr file to the archive file.
        - `bytes`: Bytes of the Exr file.

      This is useful for archived files with sequential access.

    - An `np.ndarray`: NumPy array representing the Exr image.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the Exr data. If `False`,
            returns the underlying dictionary in the format `{"path": exr_path, "bytes": exr_bytes}`.

    Example:

    ```py
    >>> from datasets import load_dataset, Exr
    >>> ds = load_dataset("my_dataset")
    >>> ds = ds.cast_column("exr_image", Exr())
    >>> ds[0]["exr_image"]
    {'array': array([...], dtype=float32),
     'path': '/path/to/file.exr'}
    ```
    """

    decode: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "np.ndarray"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Exr", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, dict, np.ndarray]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `np.ndarray` or `dict`):
                Data passed as input to Exr feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, bytes):
            return {"path": None, "bytes": value}
        elif isinstance(value, np.ndarray):
            # Convert the Exr array to bytes using the provided exwrite function
            buffer = BytesIO()
            exwrite(buffer, value)  # exwrite is your custom function to save Exr to bytes
            return {"path": None, "bytes": buffer.getvalue()}
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(f"An Exr sample should have one of 'path' or 'bytes' but they are missing or None in {value}.")

    def decode_example(self, value: Tuple[Dict, str], token_per_repo_id: Optional[Dict[str, Union[str, bool, None]]] = None) -> np.ndarray:
        """Decode example Exr file into image data.

        Args:
            value (`str` or `dict`):
                A string with the absolute Exr file path, a dictionary with keys:

                - `path`: String with absolute or relative Exr file path.
                - `bytes`: The bytes of the Exr file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode Exr files from private repositories on the Hub, you can pass
                a dictionary repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `np.ndarray`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Exr(decode=True) instead.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        if isinstance(value, str):
            path = value
            bytes_ = None
        else:
            path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"An Exr sample should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    array = exload(path)  # exload is your custom function to load Exr
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
                        bytes_ = BytesIO(f.read())
                    array = exload(bytes_)  # exload can handle file-like objects
        else:
            array = exload(BytesIO(bytes_))  # exload can handle file-like objects
        return array

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
        """Cast an Arrow array to the Exr arrow storage type.
        The Arrow types that can be converted to the Exr pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the Exr bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter
        - `pa.list(*)` - it must contain the Exr array data

        Args:
            storage (`Union[pa.StringArray, pa.StructArray, pa.ListArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Exr arrow storage type, that is
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
        elif pa.types.is_list(storage.type):
            bytes_array = pa.array(
                [self.encode_example(np.array(arr))["bytes"] if arr is not None else None for arr in storage.to_pylist()],
                type=pa.binary(),
            )
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays(
                [bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null()
            )
        return array_cast(storage, self.pa_type)

    def embed_storage(self, storage: pa.StructArray) -> pa.StructArray:
        """Embed Exr files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            `pa.StructArray`: Array in the Exr arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """

        @no_op_if_value_is_null
        def path_to_bytes(path):
            with xopen(path, "rb") as f:
                bytes_ = f.read()
            return bytes_

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
