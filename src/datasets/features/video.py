import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Literal, Optional, TypedDict, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..download.download_config import DownloadConfig
from ..table import array_cast
from ..utils.file_utils import is_local_path, xopen
from ..utils.py_utils import string_to_dict


if TYPE_CHECKING:
    import torch
    from torchcodec.decoders import VideoDecoder

    from .features import FeatureType


class Example(TypedDict):
    path: Optional[str]
    bytes: Optional[bytes]


@dataclass
class Video:
    """
    Video [`Feature`] to read video data from a video file.

    Input: The Video feature accepts as input:
    - A `str`: Absolute path to the video file (i.e. random access is allowed).
    - A `dict` with the keys:

        - `path`: String with relative path of the video file in a dataset repository.
        - `bytes`: Bytes of the video file.

      This is useful for parquet or webdataset files which embed video files.

    - A `torchcodec.decoders.VideoDecoder`: torchcodec video decoder object.

    Output: The Video features output data as `torchcodec.decoders.VideoDecoder` objects.

    Args:
        mode (`str`, *optional*):
            The mode to convert the video to. If `None`, the native mode of the video is used.
        decode (`bool`, defaults to `True`):
            Whether to decode the video data. If `False`,
            returns the underlying dictionary in the format `{"path": video_path, "bytes": video_bytes}`.
        stream_index (`int`, *optional*):
            The streaming index to use from the file. If `None` defaults to the "best" index.
        dimension_order (`str`, defaults to `NCHW`):
            The dimension order of the decoded frames.
            where N is the batch size, C is the number of channels,
            H is the height, and W is the width of the frames.
        num_ffmpeg_threads (`int`, defaults to `1`):
            The number of threads to use for decoding the video. (Recommended to keep this at 1)
        device (`str` or `torch.device`, defaults to `cpu`):
            The device to use for decoding the video.
        seek_mode (`str`, defaults to `exact`):
            Determines if frame access will be “exact” or “approximate”.
            Exact guarantees that requesting frame i will always return frame i, but doing so requires an initial scan of the file.
            Approximate is faster as it avoids scanning the file, but less accurate as it uses the file's metadata to calculate where i probably is.
            read more [here](https://docs.pytorch.org/torchcodec/stable/generated_examples/approximate_mode.html#sphx-glr-generated-examples-approximate-mode-py)

    Examples:

    ```py
    >>> from datasets import Dataset, Video
    >>> ds = Dataset.from_dict({"video":["path/to/Screen Recording.mov"]}).cast_column("video", Video())
    >>> ds.features["video"]
    Video(decode=True, id=None)
    >>> ds[0]["video"]
    <torchcodec.decoders._video_decoder.VideoDecoder object at 0x14a61e080>
    >>> video = ds[0]["video"]
    >>> video.get_frames_in_range(0, 10)
    FrameBatch:
    data (shape): torch.Size([10, 3, 50, 66])
    pts_seconds: tensor([0.4333, 0.4333, 0.4333, 0.4333, 0.4333, 0.4333, 0.4333, 0.4333, 0.4333,
            0.4333], dtype=torch.float64)
    duration_seconds: tensor([0.0167, 0.0167, 0.0167, 0.0167, 0.0167, 0.0167, 0.0167, 0.0167, 0.0167,
            0.0167], dtype=torch.float64)
    >>> ds.cast_column('video', Video(decode=False))[0]["video]
    {'bytes': None,
     'path': 'path/to/Screen Recording.mov'}
    ```
    """

    decode: bool = True
    stream_index: Optional[int] = None
    dimension_order: Literal["NCHW", "NHWC"] = "NCHW"
    num_ffmpeg_threads: int = 1
    device: Optional[Union[str, "torch.device"]] = "cpu"
    seek_mode: Literal["exact", "approximate"] = "exact"
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    dtype: ClassVar[str] = "torchcodec.decoders.VideoDecoder"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Video", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, bytes, bytearray, Example, np.ndarray, "VideoDecoder"]) -> Example:
        """Encode example into a format for Arrow.

        Args:
            value (`str`, `np.ndarray`, `bytes`, `bytearray`, `VideoDecoder` or `dict`):
                Data passed as input to Video feature.

        Returns:
            `dict` with "path" and "bytes" fields
        """
        if value is None:
            raise ValueError("value must be provided")

        if config.TORCHCODEC_AVAILABLE:
            from torchcodec.decoders import VideoDecoder
        else:
            VideoDecoder = None

        if isinstance(value, list):
            value = np.array(value)

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, (bytes, bytearray)):
            return {"path": None, "bytes": value}
        elif isinstance(value, np.ndarray):
            # convert the video array to bytes
            return encode_np_array(value)
        elif VideoDecoder is not None and isinstance(value, VideoDecoder):
            # convert the torchcodec video decoder to bytes
            return encode_torchcodec_video(value)
        elif isinstance(value, dict):
            path, bytes_ = value.get("path"), value.get("bytes")
            if path is not None and os.path.isfile(path):
                # we set "bytes": None to not duplicate the data if they're already available locally
                return {"bytes": None, "path": path}
            elif bytes_ is not None or path is not None:
                # store the video bytes, and path is used to infer the video format using the file extension
                return {"bytes": bytes_, "path": path}
            else:
                raise ValueError(
                    f"A video sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
                )
        else:
            raise TypeError(f"Unsupported encode_example type: {type(value)}")

    def decode_example(
        self,
        value: Union[str, Example],
        token_per_repo_id: Optional[dict[str, Union[bool, str]]] = None,
    ) -> "VideoDecoder":
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
            `torchcodec.decoders.VideoDecoder`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Video(decode=True) instead.")

        if config.TORCHCODEC_AVAILABLE:
            from torchcodec.decoders import VideoDecoder

        else:
            raise ImportError("To support decoding videos, please install 'torchcodec'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        if isinstance(value, str):
            path, bytes_ = value, None
        else:
            path, bytes_ = value["path"], value["bytes"]

        if bytes_ is None:
            if path is None:
                raise ValueError(f"A video should have one of 'path' or 'bytes' but both are None in {value}.")
            elif is_local_path(path):
                video = VideoDecoder(
                    path,
                    stream_index=self.stream_index,
                    dimension_order=self.dimension_order,
                    num_ffmpeg_threads=self.num_ffmpeg_threads,
                    device=self.device,
                    seek_mode=self.seek_mode,
                )
            else:
                video = hf_video_reader(
                    path,
                    token_per_repo_id=token_per_repo_id,
                    dimension_order=self.dimension_order,
                    num_ffmpeg_threads=self.num_ffmpeg_threads,
                    device=self.device,
                    seek_mode=self.seek_mode,
                )
        else:
            video = VideoDecoder(
                bytes_,
                stream_index=self.stream_index,
                dimension_order=self.dimension_order,
                num_ffmpeg_threads=self.num_ffmpeg_threads,
                device=self.device,
                seek_mode=self.seek_mode,
            )
        video._hf_encoded = {"path": path, "bytes": bytes_}
        video.metadata.path = path
        return video

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


def video_to_bytes(video: "VideoDecoder") -> bytes:
    """Convert a torchcodec Video object to bytes using native compression if possible"""
    raise NotImplementedError()


def encode_torchcodec_video(video: "VideoDecoder") -> Example:
    if hasattr(video, "_hf_encoded"):
        return video._hf_encoded
    else:
        raise NotImplementedError(
            "Encoding a VideoDecoder that doesn't come from datasets.Video.decode() is not implemented"
        )


def encode_np_array(array: np.ndarray) -> Example:
    raise NotImplementedError()


# No monkey patch needed!
# 1. store the encoded video data {"path": ..., "bytes": ...} in `video._hf_encoded``
# 2. add support for hf:// files


def hf_video_reader(
    path: str,
    token_per_repo_id: Optional[dict[str, Union[bool, str]]] = None,
    stream: str = "video",
    dimension_order: Literal["NCHW", "NHWC"] = "NCHW",
    num_ffmpeg_threads: int = 1,
    device: Optional[Union[str, "torch.device"]] = "cpu",
    seek_mode: Literal["exact", "approximate"] = "exact",
) -> "VideoDecoder":
    from torchcodec.decoders import VideoDecoder

    # Load the file from HF
    if token_per_repo_id is None:
        token_per_repo_id = {}
    source_url = path.split("::")[-1]
    pattern = config.HUB_DATASETS_URL if source_url.startswith(config.HF_ENDPOINT) else config.HUB_DATASETS_HFFS_URL
    source_url_fields = string_to_dict(source_url, pattern)
    token = token_per_repo_id.get(source_url_fields["repo_id"]) if source_url_fields is not None else None
    download_config = DownloadConfig(token=token)
    f = xopen(path, "rb", download_config=download_config)

    # Instantiate the VideoDecoder
    stream_id = 0 if len(stream.split(":")) == 1 else int(stream.split(":")[1])
    vd = VideoDecoder(
        f,
        stream_index=stream_id,
        dimension_order=dimension_order,
        num_ffmpeg_threads=num_ffmpeg_threads,
        device=device,
        seek_mode=seek_mode,
    )
    return vd
