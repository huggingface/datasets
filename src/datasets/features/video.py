import os
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict


if TYPE_CHECKING:
    from decord import VideoReader

    from .features import FeatureType


@dataclass
class Video:
    """
    **Experimental.** Video [`Feature`] to read video data from a video file.

    Input: The Video feature accepts as input:
    - A `str`: Absolute path to the video file (i.e. random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the video file in a dataset repository.
        - `bytes`: Bytes of the video file.

      This is useful for archived files with sequential access.

    - A `decord.VideoReader`: decord video reader object.

    Args:
        mode (`str`, *optional*):
            The mode to convert the video to. If `None`, the native mode of the video is used.
        decode (`bool`, defaults to `True`):
            Whether to decode the video data. If `False`,
            returns the underlying dictionary in the format `{"path": video_path, "bytes": video_bytes}`.

    Examples:

    ```py
    >>> from datasets import Dataset, Video
    >>> ds = Dataset.from_dict({"video":["path/to/Screen Recording.mov"]}).cast_column("video", Video())
    >>> ds.features["video"]
    Video(decode=True, id=None)
    >>> ds[0]["video"]
    <decord.video_reader.VideoReader at 0x105525c70>
    >>> ds = ds.cast_column('video', Video(decode=False))
    {'bytes': None,
     'path': 'path/to/Screen Recording.mov'}
    ```
    """

    decode: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "decord.VideoReader"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Video", init=False, repr=False)

    def __post_init__(self):
        if config.DECORD_AVAILABLE:
            patch_decord()

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, dict, np.ndarray, "VideoReader"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `np.ndarray`, `VideoReader` or `dict`):
                Data passed as input to Video feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if config.DECORD_AVAILABLE:
            from decord import VideoReader

        else:
            VideoReader = None

        if isinstance(value, list):
            value = np.array(value)

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, bytes):
            return {"path": None, "bytes": value}
        elif isinstance(value, np.ndarray):
            # convert the video array to bytes
            return encode_np_array(value)
        elif VideoReader and isinstance(value, VideoReader):
            # convert the decord video reader to bytes
            return encode_decord_video(value)
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the video bytes, and path is used to infer the video format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"A video sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "VideoReader":
        """Decode example video file into video data.

        Args:
            value (`str` or `dict`):
                A string with the absolute video file path, a dictionary with
                keys:

                - `path`: String with absolute or relative video file path.
                - `bytes`: The bytes of the video file.
            token_per_repo_id (`dict`, *optional*):
                To access and decode
                video files from private repositories on the Hub, you can pass
                a dictionary repo_id (`str`) -> token (`bool` or `str`).

        Returns:
            `decord.VideoReader`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Video(decode=True) instead.")

        if config.DECORD_AVAILABLE:
            from decord import VideoReader

        else:
            raise ImportError("To support decoding videos, please install 'decord'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"A video should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    video = VideoReader(path)
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
                    video = VideoReader(bytes_)
        else:
            video = VideoReader(BytesIO(bytes_))
        return video

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
        """Cast an Arrow array to the Video arrow storage type.
        The Arrow types that can be converted to the Video pyarrow storage type are:

        - `pa.string()` - it must contain the "path" data
        - `pa.binary()` - it must contain the video bytes
        - `pa.struct({"bytes": pa.binary()})`
        - `pa.struct({"path": pa.string()})`
        - `pa.struct({"bytes": pa.binary(), "path": pa.string()})`  - order doesn't matter
        - `pa.list(*)` - it must contain the video array data

        Args:
            storage (`Union[pa.StringArray, pa.StructArray, pa.ListArray]`):
                PyArrow array to cast.

        Returns:
            `pa.StructArray`: Array in the Video arrow storage type, that is
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
                [encode_np_array(np.array(arr))["bytes"] if arr is not None else None for arr in storage.to_pylist()],
                type=pa.binary(),
            )
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays(
                [bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null()
            )
        return array_cast(storage, self.pa_type)


def video_to_bytes(video: "VideoReader") -> bytes:
    """Convert a decord Video object to bytes using native compression if possible"""
    raise NotImplementedError()


def encode_decord_video(video: "VideoReader") -> dict:
    if hasattr(video, "_hf_encoded"):
        return video._hf_encoded
    else:
        raise NotImplementedError(
            "Encoding a decord video is not implemented. "
            "Please call `datasets.features.video.patch_decord()` before loading videos to enable this."
        )


def encode_np_array(array: np.ndarray) -> dict:
    raise NotImplementedError()


# Patching decord a little bit to:
# 1. store the encoded video data {"path": ..., "bytes": ...} in `video._hf_encoded``
# 2. set the decord bridge to numpy/torch/tf/jax using `video._hf_bridge_out` (per video instance) instead of decord.bridge.bridge_out (global)
# This doesn't affect the normal usage of decord.


def _patched_init(self: "VideoReader", uri: Union[str, BytesIO], *args, **kwargs) -> None:
    from decord.bridge import bridge_out

    if hasattr(uri, "read"):
        self._hf_encoded = {"bytes": uri.read(), "path": None}
        uri.seek(0)
    elif isinstance(uri, str):
        self._hf_encoded = {"bytes": None, "path": uri}
    self._hf_bridge_out = bridge_out
    self._original_init(uri, *args, **kwargs)


def _patched_next(self: "VideoReader", *args, **kwargs):
    return self._hf_bridge_out(self._original_next(*args, **kwargs))


def _patched_get_batch(self: "VideoReader", *args, **kwargs):
    return self._hf_bridge_out(self._original_get_batch(*args, **kwargs))


def patch_decord():
    # We need to import torch first, otherwise later it can cause issues
    # e.g. "RuntimeError: random_device could not be read"
    # when running `torch.tensor(value).share_memory_()`
    # Same for duckdb which crashes on import
    if config.TORCH_AVAILABLE:
        import torch  # noqa
    if config.DUCKDB_AVAILABLE:
        import duckdb  # noqa
    import decord.video_reader
    from decord import VideoReader

    if not hasattr(VideoReader, "_hf_patched"):
        decord.video_reader.bridge_out = lambda x: x
        VideoReader._original_init = VideoReader.__init__
        VideoReader.__init__ = _patched_init
        VideoReader._original_next = VideoReader.next
        VideoReader.next = _patched_next
        VideoReader._original_get_batch = VideoReader.get_batch
        VideoReader.get_batch = _patched_get_batch
        VideoReader._hf_patched = True
