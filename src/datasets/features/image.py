from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional

import numpy as np
import pyarrow as pa

from .. import config
from ..utils.file_utils import is_local_path
from ..utils.streaming_download_manager import xopen


if TYPE_CHECKING:
    import PIL.Image


_IMAGE_COMPRESSION_FORMATS: Optional[List[str]] = None


class _ImageExtensionType(pa.PyExtensionType):
    def __init__(self):
        pa.PyExtensionType.__init__(self, pa.struct({"path": pa.string(), "bytes": pa.binary()}))

    def __reduce__(self):
        return self.__class__, ()


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
    """

    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Image", init=False, repr=False)

    def __call__(self):
        return _ImageExtensionType()

    def encode_example(self, value):
        """Encode example into a format for Arrow.

        Args:
            value (:obj:`str`, :obj:`np.ndarray` or :obj:`dict`): Data passed as input to Image feature.

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
        else:
            return value

    def decode_example(self, value):
        """Decode example image file into image data.

        Args:
            value (obj:`str` or :obj:`dict`): a string with the absolute image file path, an np.ndarray object or a dictionary with
                keys:
                - path: String with absolute or relative audio file path.
                - bytes: Optionally, the bytes of the audio file.

        Returns:
            :obj:`PIL.Image.Image`
        """
        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("To support decoding images, please install 'Pillow'.")

        if isinstance(value, np.ndarray):  # Allow casting np.ndarray objects to PIL.Image.Image objects
            image = PIL.Image.fromarray(value.astype(np.uint8))
        else:
            if isinstance(value, str):
                value = {"path": value, "bytes": None}

            path, bytes_ = (
                (value["path"], BytesIO(value["bytes"])) if value["bytes"] is not None else (value["path"], None)
            )
            if bytes_ is None:
                if isinstance(path, str):
                    if is_local_path(path):
                        image = PIL.Image.open(path)
                    else:
                        with xopen(path, "rb") as f:
                            bytes_ = BytesIO(f.read())
                        image = PIL.Image.open(bytes_)
            else:
                image = PIL.Image.open(bytes_)
        return image


def list_image_compression_formats():
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


def objects_to_images(objs):
    """Encode a list of string, np.ndarray or PIL Image objects into image representation."""
    if config.PIL_AVAILABLE:
        import PIL.Image
    else:
        raise ImportError("To support encoding images, please install 'Pillow'.")

    if objs:
        obj = objs[0]
        if isinstance(obj, str):
            return [{"path": obj, "bytes": None} for obj in objs]
        elif isinstance(obj, PIL.Image.Image):
            return [{"path": None, "bytes": image_to_bytes(obj)} for obj in objs]
        elif isinstance(obj, np.ndarray):
            return [{"path": None, "bytes": image_to_bytes(PIL.Image.fromarray(obj.astype(np.uint8)))} for obj in objs]
        else:
            return objs
    else:
        return objs
