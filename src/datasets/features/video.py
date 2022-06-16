import os
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional, Union

import numpy as np
import pyarrow as pa

import datasets

from .. import config
from ..download.streaming_download_manager import xopen
from ..table import array_cast
from ..utils.file_utils import is_local_path
from ..utils.py_utils import no_op_if_value_is_null, string_to_dict


@dataclass
class Video:
    decode: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Video", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, dict, np.ndarray, "encoded_video.EncodedVideo"]) -> dict:
        """Encode example into a format for Arrow.
        Args:
            value (:obj:`str`, :obj:`encoded_video.EncodedVideo` or :obj:`dict`): Data passed as input to video feature.
        Returns:
            :obj:`dict` with "path" and "bytes" fields
        """
        if config.ENCODED_VIDEO_AVAILABLE:
            import encoded_video
        else:
            raise ImportError("To support encoding videos, please install 'encoded_video'.")

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, encoded_video.EncodedVideo):
            # convert the video to bytes
            return encode_video(value)
        elif value.get("path") is not None and os.path.isfile(value["path"]):
            # we set "bytes": None to not duplicate the data if they're already available locally
            return {"bytes": None, "path": value.get("path")}
        elif value.get("bytes") is not None or value.get("path") is not None:
            # store the video bytes, and path is used to infer the video format using the file extension
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"An video sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict, token_per_repo_id=None) -> "encoded_video.EncodedVideo":
        """Decode example video file into video data.
        Args:
            value (obj:`str` or :obj:`dict`): a string with the absolute video file path, a dictionary with
                keys:
                - path: String with absolute or relative video file path.
                - bytes: The bytes of the video file.
            token_per_repo_id (:obj:`dict`, optional): To access and decode
                video files from private repositories on the Hub, you can pass
                a dictionary repo_id (str) -> token (bool or str)
        Returns:
            :obj:`encoded_video.EncodedVideo`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Video(decode=True) instead.")

        if config.ENCODED_VIDEO_AVAILABLE:
            import encoded_video
        else:
            raise ImportError("To support decoding videos, please install 'encoded_video'.")

        if token_per_repo_id is None:
            token_per_repo_id = {}

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"An video should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    with open(path, "rb") as f:
                        bytes_ = f.read()
                    bytes_ = BytesIO(bytes_)
                    bytes.name = path
                    video = encoded_video.EncodedVideo(bytes_)  # TODO does this need to happen below?
                else:
                    source_url = path.split("::")[-1]
                    try:
                        repo_id = string_to_dict(source_url, config.HUB_DATASETS_URL)["repo_id"]
                        use_auth_token = token_per_repo_id.get(repo_id)
                    except ValueError:
                        use_auth_token = None
                    with xopen(path, "rb", use_auth_token=use_auth_token) as f:
                        bytes_ = BytesIO(f.read())
                    video = encoded_video.EncodedVideo(bytes_)
        else:
            video = encoded_video.EncodedVideo(BytesIO(bytes_))

        return video

    def flatten(self) -> Union["FeatureType", Dict[str, "FeatureType"]]:
        """If in the decodable state, return the feature itself, otherwise flatten the feature into a dictionary."""
        from datasets.features import Value

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
        The Arrow types that can be converted to the video pyarrow storage type are:
        - pa.string() - it must contain the "path" data
        - pa.struct({"bytes": pa.binary()})
        - pa.struct({"path": pa.string()})
        - pa.struct({"bytes": pa.binary(), "path": pa.string()})  - order doesn't matter
        - pa.list(*) - it must contain the video array data
        Args:
            storage (Union[pa.StringArray, pa.StructArray, pa.ListArray]): PyArrow array to cast.
        Returns:
            pa.StructArray: Array in the video arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
        """
        if config.ENCODED_VIDEO_AVAILABLE:
            import encoded_video
        else:
            raise ImportError("To support encoding videos, please install 'encoded_video'.")

        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"], mask=storage.is_null())
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

    def embed_storage(self, storage: pa.StructArray, drop_paths: bool = True) -> pa.StructArray:
        """Embed video files into the Arrow array.
        Args:
            storage (pa.StructArray): PyArrow array to embed.
            drop_paths (bool, default ``True``): If True, the paths are set to None.
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
        path_array = pa.array([None] * len(storage), type=pa.string()) if drop_paths else storage.field("path")
        storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"], mask=bytes_array.is_null())
        return array_cast(storage, self.pa_type)


def encode_video(video: "encoded_video.EncodedVideo") -> dict:

    if hasattr(video._container.file.file, "name") and video._container.file.file.name != "":
        return {"path": video._container.file.file.name, "bytes": None}
    else:
        return {"path": None, "bytes": video._container.file.file.getvalue()}
