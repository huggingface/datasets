from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..utils.file_utils import is_local_path
from ..utils.py_utils import first_non_null_value, no_op_if_value_is_null
from ..utils.streaming_download_manager import xopen
from .base_extension import BasePyarrowExtensionType


if TYPE_CHECKING:
    import PIL.Image


_IMAGE_COMPRESSION_FORMATS: Optional[List[str]] = None


class ImageExtensionType(BasePyarrowExtensionType):
    pa_storage_type = pa.struct({"bytes": pa.binary(), "path": pa.string()})

    def cast_storage(self, array: pa.Array) -> pa.ExtensionArray:
        if array.type == ImageExtensionType():
            return array
        elif array.type == pa.struct({"bytes": pa.binary(), "paths": pa.string()}):
            storage = array
        elif isinstance(array.type, pa.StructType):
            subarrays = {array.type[i].name: array.field(i) for i in range(array.type.num_fields)}
            bytes_array = (
                subarrays["bytes"].cast(pa.binary())
                if "bytes" in subarrays
                else pa.array([None] * len(array), type=pa.binary())
            )
            path_array = (
                subarrays["path"].cast(pa.string())
                if "path" in subarrays
                else pa.array([None] * len(array), type=pa.string())
            )
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])
        elif array.type == pa.string():
            bytes_array = pa.array([None] * len(array), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, array], ["bytes", "path"])
        else:
            raise TypeError(f"Can't convert array of type {array.type} to image type {type(self)}.")
        return pa.ExtensionArray.from_storage(self, storage)


@dataclass(unsafe_hash=True)
class Image:
    """Image feature to read image data from an image file.

    Input: The Image feature accepts as input:
    - A :obj:`str`: Absolute path to the image file (i.e. random access is allowed).
    - A :obj:`dict` with the keys:

        - path: String with relative path of the image file to the archive file.
        - bytes: Bytes of the image file.

      This is useful for archived files with sequential access.

    - An :obj:`np.ndarray`: NumPy array representing an image.
    - A :obj:`PIL.Image.Image`: PIL image object.
    """

    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "PIL.Image.Image"
    pa_type: ClassVar[Any] = ImageExtensionType
    _type: str = field(default="Image", init=False, repr=False)

    def __call__(self):
        return self.pa_type()

    def encode_example(self, value: Union[str, dict, np.ndarray, "PIL.Image.Image"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str`, :obj:`np.ndarray`, :obj:`PIL.Image.Image` or :obj:`dict`): Data passed as input to Image feature.

        Returns:
            :obj:`dict`
        """
        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("To support encoding images, please install 'Pillow'.")

        if isinstance(value, str):
            return {"path": value, "bytes": None}
        elif isinstance(value, np.ndarray):
            image = PIL.Image.fromarray(value.astype(np.uint8))
            return {"path": None, "bytes": image_to_bytes(image)}
        elif isinstance(value, PIL.Image.Image):
            if hasattr(value, "filename") and value.filename != "":
                return {"path": value.filename, "bytes": None}
            else:
                return {"path": None, "bytes": image_to_bytes(value)}
        else:
            return value

    def decode_example(self, value):
        """Decode example image file into image data.

        Args:
            value (obj:`str` or :obj:`dict`): a string with the absolute image file path, a dictionary with
                keys:
                - path: String with absolute or relative image file path.
                - bytes: The bytes of the image file.

        Returns:
            :obj:`PIL.Image.Image`
        """
        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("To support decoding images, please install 'Pillow'.")

        if isinstance(value, str):
            path, bytes_ = value, None
        else:
            path, bytes_ = value["path"], value["bytes"]

        if bytes_ is None:
            if isinstance(path, str):
                if is_local_path(path):
                    image = PIL.Image.open(path)
                else:
                    with xopen(path, "rb") as f:
                        bytes_ = BytesIO(f.read())
                    image = PIL.Image.open(bytes_)
        else:
            image = PIL.Image.open(BytesIO(bytes_))
        return image


def list_image_compression_formats() -> List[str]:
    if config.PIL_AVAILABLE:
        import PIL.Image
    else:
        raise ImportError("To support encoding images, please install 'Pillow'.")

    global _IMAGE_COMPRESSION_FORMATS
    if _IMAGE_COMPRESSION_FORMATS is None:
        PIL.Image.init()
        _IMAGE_COMPRESSION_FORMATS = list(set(PIL.Image.OPEN.keys()) & set(PIL.Image.SAVE.keys()))
    return _IMAGE_COMPRESSION_FORMATS


def image_to_bytes(image: "PIL.Image.Image") -> bytes:
    """Convert a PIL Image object to bytes using native compression if possible, otherwise use PNG compression."""
    buffer = BytesIO()
    format = image.format if image.format in list_image_compression_formats() else "PNG"
    image.save(buffer, format=format)
    return buffer.getvalue()


def objects_to_list_of_image_dicts(
    objs: Union[List[str], List[dict], List[np.ndarray], List["PIL.Image.Image"]]
) -> List[dict]:
    """Encode a list of objects into a format suitable for creating an extension array of type :obj:`ImageExtensionType`."""
    if config.PIL_AVAILABLE:
        import PIL.Image
    else:
        raise ImportError("To support encoding images, please install 'Pillow'.")

    if objs:
        _, obj = first_non_null_value(objs)
        if isinstance(obj, str):
            return [{"path": obj, "bytes": None} if obj is not None else None for obj in objs]
        if isinstance(obj, np.ndarray):
            return [
                {"path": None, "bytes": image_to_bytes(PIL.Image.fromarray(obj.astype(np.uint8)))}
                if obj is not None
                else None
                for obj in objs
            ]
        elif isinstance(obj, PIL.Image.Image):
            obj_to_image_dict_func = no_op_if_value_is_null(
                lambda obj: {"path": obj.filename, "bytes": None}
                if hasattr(obj, "filename") and obj.filename != ""
                else {"path": None, "bytes": image_to_bytes(obj)}
            )
            return [obj_to_image_dict_func(obj) for obj in objs]
        else:
            return objs
    else:
        return objs
