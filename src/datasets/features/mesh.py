import os
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from typing import Any, ClassVar, Optional, Union

import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict


@dataclass
class Mesh:
    """Mesh [`Feature`] to read 3D mesh data from a file.

    Input: The Mesh feature accepts as input:
    - A `str`: Absolute path to the mesh file (i.e. random access is allowed).
    - A `pathlib.Path`: path to the mesh file (i.e. random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the mesh file to the archive file.
        - `bytes`: Bytes of the mesh file.

      This is useful for parquet or webdataset files which embed mesh files.

    Output: The Mesh features output data as a dictionary `{"path": ..., "bytes": ...}` by default.

    Args:
        decode (`bool`, defaults to `True`):
            Whether to decode the mesh data. If `False`,
            returns the underlying dictionary in the format `{"path": mesh_path, "bytes": mesh_bytes}`.
            Note: Decoding is currently a no-op that returns the raw dictionary, matching the no-decode behavior, but allows future extensions.
    """

    decode: bool = True
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Mesh", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, dict]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `bytes`, or `dict`):
                Data passed as input to Mesh feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, Path):
            return {"path": str(value.absolute()), "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": value}
        elif isinstance(value, dict) and value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif isinstance(value, dict) and (value.get("bytes") is not None or value.get("path") is not None):
            # store the mesh bytes, and path is used to infer the mesh format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A mesh sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> dict:
        """Decode example mesh file.

        Args:
            value (`dict`):
                A dictionary with keys:

                - `path`: String with absolute or relative mesh file path.
                - `bytes`: The bytes of the mesh file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode
                mesh files from private repositories on the Hub, you can pass
                a dictionary repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `dict` containing "path" and "bytes" of the Mesh.
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Mesh(decode=True) instead.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A mesh should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    with open(path, "rb") as f:
                        bytes_ = f.read()
                else:
                    source_url = path.split("::")[-1]
                    pattern = (
                        config.HUB_DATASETS_URL
                        if source_url.startswith(config.HF_ENDPOINT)
                        else config.HUB_DATASETS_HFFS_URL
                    )
                    source_url_fields = string_to_dict(source_url, pattern)
                    token = (
                        token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None
                    )
                    download_config = DownloadConfig(token=token)
                    with xopen(path, "rb", download_config=download_config) as f:
                        bytes_ = f.read()

        # Currently we just return the raw bytes and path for 3D data.
        # This matches the dictionary structure and defers rendering to the user or dataset viewer
        return {"path": path, "bytes": bytes_}

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
        """Cast an Arrow array to the Mesh arrow storage type.
        The Arrow types that can be converted to the Mesh pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.large_string()` - it must contain the "path" data (will be cast to string if possible)
        - `pa.binary()` - it must contain the mesh bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter

        Args:
            storage (`Union[pa.StringArray, pa.StructArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Mesh arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if pa.types.is_large_string(storage.type):
            try:
                storage = storage.cast(pa.string())
            except pa.ArrowInvalid as e:
                raise ValueError(
                    f"Failed to cast large_string to string for Mesh feature. "
                    f"This can happen if string values exceed 2GB. "
                    f"Original error: {e}"
                ) from e
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_large_binary(storage.type):
            storage = array_cast(
                storage, pa.binary()
            )  # this can fail in case of big meshes, paths should be used instead
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([storage, path_array], ["bytes", "path"], mask=storage.is_null())
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
        """Embed mesh files into the Arrow array.

        Args:
            storage (`pa.StructArray`):
                PyArrow array to embed.

        Returns:
            `pa.StructArray`: Array in the Mesh arrow storage type, that is
                `pa.struct({"bytes": pa.binary(), "path": pa.string()})`.
        """
        if token_per_repo_id is None:
            token_per_repo_id = {}

        def path_to_bytes(path):
            if path is None:
                return None
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
