from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Union

import numpy as np
import pyarrow as pa

from .. import config
from ..table import array_cast
from ..utils.file_utils import is_local_path
from ..utils.py_utils import first_non_null_value, no_op_if_value_is_null
from ..utils.streaming_download_manager import xopen


if TYPE_CHECKING:
    import PIL.Image


_IMAGE_COMPRESSION_FORMATS: Optional[List[str]] = None


@dataclass
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

    Args:
        decode (:obj:`bool`, default ``True``): Whether to decode the image data. If `False`,
            returns the underlying dictionary in the format {"path": image_path, "bytes": image_bytes}.
    """

    decode: bool = True
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "PIL.Image.Image"
    pa_type: ClassVar[Any] = pa.struct({"bytes": pa.binary(), "path": pa.string()})
    _type: str = field(default="Image", init=False, repr=False)

    def __call__(self):
        return self.pa_type

    def encode_example(self, value: Union[str, dict, np.ndarray, "PIL.Image.Image"]) -> dict:
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str`, :obj:`np.ndarray`, :obj:`PIL.Image.Image` or :obj:`dict`): Data passed as input to Image feature.

        Returns:
            :obj:`dict` with "path" and "bytes" fields
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
            return encode_pil_image(value)
        elif value.get("bytes") is not None or value.get("path") is not None:
            return {"bytes": value.get("bytes"), "path": value.get("path")}
        else:
            raise ValueError(
                f"An image sample should have one of 'path' or 'bytes' but they are missing or None in {value}."
            )

    def decode_example(self, value: dict) -> "PIL.Image.Image":
        """Decode example image file into image data.

        Args:
            value (obj:`str` or :obj:`dict`): a string with the absolute image file path, a dictionary with
                keys:

                - path: String with absolute or relative image file path.
                - bytes: The bytes of the image file.

        Returns:
            :obj:`PIL.Image.Image`
        """
        if not self.decode:
            raise RuntimeError("Decoding is disabled for this feature. Please use Image(decode=True) instead.")

        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("To support decoding images, please install 'Pillow'.")

        path, bytes_ = value["path"], value["bytes"]
        if bytes_ is None:
            if path is None:
                raise ValueError(f"An image should have one of 'path' or 'bytes' but both are None in {value}.")
            else:
                if is_local_path(path):
                    image = PIL.Image.open(path)
                else:
                    with xopen(path, "rb") as f:
                        bytes_ = BytesIO(f.read())
                    image = PIL.Image.open(bytes_)
        else:
            image = PIL.Image.open(BytesIO(bytes_))
        return image

    def cast_storage(self, storage: Union[pa.StringArray, pa.StructArray, pa.ListArray]) -> pa.StructArray:
        """Cast an Arrow array to the Image arrow storage type.
        The Arrow types that can be converted to the Image pyarrow storage type are:

        - pa.string() - it must contain the "path" data
        - pa.struct({"bytes": pa.binary()})
        - pa.struct({"path": pa.string()})
        - pa.struct({"bytes": pa.binary(), "path": pa.string()})  - order doesn't matter
        - pa.list(*) - it must contain the image array data

        Args:
            storage (Union[pa.StringArray, pa.StructArray, pa.ListArray]): [description]

        Returns:
            pa.StructArray: Array in the Image arrow storage type, that is
                pa.struct({"bytes": pa.binary(), "path": pa.string()})
        """
        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("To support encoding images, please install 'Pillow'.")

        if pa.types.is_string(storage.type):
            bytes_array = pa.array([None] * len(storage), type=pa.binary())
            storage = pa.StructArray.from_arrays([bytes_array, storage], ["bytes", "path"])
        elif pa.types.is_struct(storage.type):
            if storage.type.get_field_index("bytes") >= 0:
                bytes_array = storage.field("bytes")
            else:
                bytes_array = pa.array([None] * len(storage), type=pa.binary())
            if storage.type.get_field_index("path") >= 0:
                path_array = storage.field("path")
            else:
                path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])
        elif pa.types.is_list(storage.type):
            bytes_array = pa.array(
                [image_to_bytes(PIL.Image.fromarray(np.array(arr, np.uint8))) for arr in storage.to_pylist()],
                type=pa.binary(),
            )
            path_array = pa.array([None] * len(storage), type=pa.string())
            storage = pa.StructArray.from_arrays([bytes_array, path_array], ["bytes", "path"])
        return array_cast(storage, self.pa_type)


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


def encode_pil_image(image: "PIL.Image.Image") -> dict:
    if hasattr(image, "filename") and image.filename != "":
        return {"path": image.filename, "bytes": None}
    else:
        return {"path": None, "bytes": image_to_bytes(image)}


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
            obj_to_image_dict_func = no_op_if_value_is_null(encode_pil_image)
            return [obj_to_image_dict_func(obj) for obj in objs]
        else:
            return objs
    else:
        return objs
