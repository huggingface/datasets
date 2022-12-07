import math
import os
import warnings
from dataclasses import dataclass, field
from fractions import Fraction
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple, Union

import numpy as np
import pyarrow as pa
from packaging import version

from .. import config
from ..download.streaming_download_manager import xopen
from ..table import array_cast
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


if TYPE_CHECKING:
    from .features import FeatureType


@dataclass
class Video:
    decode: bool = True

    fps: Optional[int] = None

    decode_audio: bool = True
    sampling_rate: Optional[int] = None
    mono: bool = True

    id: Optional[str] = None

    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Video", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, dict]) -> dict:
        try:
            import av  # av is needed to decode video files.
        except ImportError as err:
            raise ImportError("To support encoding audio data, please install 'av==9.2.0'.") from err

        if isinstance(value, str):
            return {"bytes": None, "path": value}

        # convert the video/audio arrays to video bytes
        elif "video_array" in value:
            if "fps" not in value:
                raise ValueError("FPS Not provided when array was")

            # This will be unpacked to encode video
            info = dict(video_fps=value.get("fps"))

            # Create a buffer for the video...have to add name as av will look for it
            buffer = BytesIO(bytes())
            buffer.name = "out.mp4"

            if "audio_array" in value:
                if "sampling_rate" not in value:
                    raise ValueError("Sampling rate not provided when arrays were")
                info["audio_sample_rate"] = value.get("sampling_rate")

            write_video_pyav(buffer, value.get("video_array"), audio_arr=value.get("audio_array", None), **info)
            return {"bytes": buffer.getvalue(), "path": None}

        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the audio bytes, and path is used to infer the audio format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"An video sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(
        self, value: dict, token_per_repo_id: Optional[Dict[str, Union[str, bool, None]]] = None
    ) -> dict:
        """Decode example audio file into audio data.

        Args:
            value (:obj:`dict`): a dictionary with keys:

                - path: String with relative audio file path.
                - bytes: Bytes of the audio file.
            token_per_repo_id (:obj:`dict`, optional): To access and decode
                audio files from private repositories on the Hub, you can pass
                a dictionary repo_id (str) -> token (bool or str)

        Returns:
            dict
        """
        try:
            import av  # av is needed to decode video files.
        except ImportError as err:
            raise ImportError("To support encoding audio data, please install 'av==9.2.0'.") from err

        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Video(decode=True) instead.")

        path, video_bytes = (
            (value["path"], BytesIO(value["bytes"])) if value["bytes"] is not None else (value["path"], None)
        )
        if path is None and video_bytes is None:
            raise ValueError(f"An video sample should have one of 'path' or 'bytes' but both are None in {value}.")

        if video_bytes:
            src = video_bytes
        else:
            # TODO - do the token_per_repo_id stuff here?
            src = path

        # Collect all available audio/video frames as numpy
        video_arr, audio_arr, info = read_video_pyav(src, 0, math.inf, decode_audio=self.decode_audio)
        return {"path": path, "video_array": video_arr, "audio_array": audio_arr, **info}

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
        """If in the decodable state, raise an error, otherwise flatten the feature into a dictionary."""
        from .features import Value

        if self.decode:
            raise ValueError("Cannot flatten a decoded Audio feature.")
        return {
            "bytes": Value("binary"),
            "path": Value("string"),
        }

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray]) -> pa.StructArray:
        """Cast an Arrow array to the Video arrow storage type.
        The Arrow types that can be converted to the Video pyarrow storage type are:

        - pa.string() - it must contain the "path" data
        - pa.struct({"bytes": pa.binary()})
        - pa.struct({"path": pa.string()})
        - pa.struct({"bytes": pa.binary(), "path": pa.string()})  - order doesn't matter

        Args:
            storage (Union[pa.StringArray, pa.StructArray]): PyArrow array to cast.

        Returns:
            pa.StructArray: Array in the Audio arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
        """
        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
        elif pa.types.is_struct(storage.type) and storage.type.get_all_field_indices("video_array"):
            storage = pa.array([Video().encode_example(x) if x is not None else None for x in storage.to_pylist()])
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

    def embed_storage(self, storage: pa.StructArray) -> pa.StructArray:
        """Embed video files into the Arrow array.

        Args:
            storage (pa.StructArray): PyArrow array to embed.

        Returns:
            pa.StructArray: Array in the Video arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
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


def _pyav_decode_stream(
    container: "av.container.input.InputContainer",
    start_sec: float,
    end_sec: float,
    stream: "av.video.stream.VideoStream",
    perform_seek: bool = True,
) -> Tuple[List, float]:
    """
    Decode the video with PyAV decoder.
    Args:
        container (container): PyAV container.
        start_sec (float): the starting second to fetch the frames.
        end_sec (float): the ending second of the decoded frames.
        stream (stream): PyAV stream.
    Returns:
        result (np.ndarray): np array of decoded frames.

    # TODO: Add support for resampling audio
    # https://pyav.org/docs/stable/api/audio.html#av.audio.resampler.AudioResampler
    """
    start_pts = math.ceil(start_sec / stream.time_base)
    end_pts = math.ceil(end_sec / stream.time_base)
    # NOTE:
    # Don't want to seek if iterating through a video due to slow-downs. I
    # believe this is some PyAV bug where seeking after a certain point causes
    # major slow-downs
    if perform_seek:
        # Seeking in the stream is imprecise. Thus, seek to an earlier pts by a
        # margin pts.
        margin = 1024
        seek_offset = max(start_pts - margin, 0)
        container.seek(int(seek_offset), any_frame=False, backward=True, stream=stream)

    frames = []
    stream_info = {"video": 0} if stream.type == "video" else {"audio": 0}
    for frame in container.decode(**stream_info):
        if frame.pts >= start_pts and frame.pts < end_pts:
            frames.append(frame)
        elif frame.pts >= end_pts:
            break

    if stream.type == "audio":
        return np.concatenate([x.to_ndarray() for x in frames], 1)
    else:
        return np.stack([x.to_ndarray(format="rgb24") for x in frames])


def read_video_pyav(file_or_bytes, start_sec, end_sec, decode_audio=True, perform_seek=True):
    import av

    container = av.open(file_or_bytes)

    # Handle video stream
    video_stream = container.streams.video[0]
    end_sec = min(float(video_stream.duration * video_stream.time_base), end_sec)
    info = dict(video_fps=video_stream.average_rate)
    video_arr = _pyav_decode_stream(container, start_sec, end_sec, video_stream, perform_seek)

    # Handle audio stream if desired
    audio_arr = None
    if decode_audio:
        audio_stream = container.streams.audio[0]
        info["audio_sample_rate"] = audio_stream.rate
        audio_arr = _pyav_decode_stream(container, start_sec, end_sec, audio_stream, perform_seek)

    return video_arr, audio_arr, info


def write_video_pyav(
    output_path,
    video_arr,  # np array of shape (T, H, W, C)
    audio_arr=None,
    video_fps=30,
    height=None,
    width=None,
    pix_fmt="yuv420p",
    codec="h264",
    audio_codec="aac",
    audio_sample_rate=44100,
    audio_options=None,
):
    # TODO - Look into the following lossless options
    # video_codec = "libx264rgb"
    # options = {"crf": "0"}

    try:
        import av  # av is needed to decode video files.
    except ImportError as err:
        raise ImportError("To support encoding audio data, please install 'av==9.2.0'.") from err

    # PyAV does not support floating point numbers with decimal point
    # and will throw OverflowException in case this is not the case
    if isinstance(video_fps, float):
        video_fps = np.round(video_fps)

    # video_arr is a np array of shape (T, H, W, C)
    with av.open(output_path, mode="w") as container:
        # Set up Video Stream
        video_stream = container.add_stream(codec, rate=video_fps)
        video_stream.width = width or video_arr.shape[2]
        video_stream.height = height or video_arr.shape[1]
        video_stream.pix_fmt = pix_fmt

        if audio_arr is not None:
            audio_stream = container.add_stream(audio_codec, rate=audio_sample_rate)
            audio_stream.channels = 2
            audio_stream.options = audio_options or {}
            audio_sample_fmt = container.streams.audio[0].format.name
            audio_format_dtypes = {
                "dbl": "<f8",
                "dblp": "<f8",
                "flt": "<f4",
                "fltp": "<f4",
                "s16": "<i2",
                "s16p": "<i2",
                "s32": "<i4",
                "s32p": "<i4",
                "u8": "u1",
                "u8p": "u1",
            }
            format_dtype = np.dtype(audio_format_dtypes[audio_sample_fmt])
            audio_arr = audio_arr.astype(format_dtype)

            num_channels = audio_arr.shape[0]
            audio_layout = "stereo" if num_channels > 1 else "mono"

            audio_frame = av.AudioFrame.from_ndarray(audio_arr, format=audio_sample_fmt, layout=audio_layout)
            audio_frame.sample_rate = audio_sample_rate
            audio_frame.pts = None
            audio_frame.time_base = Fraction(1, audio_sample_rate)

            for packet in audio_stream.encode(audio_frame):
                container.mux(packet)

            for packet in audio_stream.encode():
                container.mux(packet)

        for frame in video_arr:
            img = av.VideoFrame.from_ndarray(frame, format="rgb24")
            for packet in video_stream.encode(img):
                container.mux(packet)

        # Flush stream
        for packet in video_stream.encode():
            container.mux(packet)
