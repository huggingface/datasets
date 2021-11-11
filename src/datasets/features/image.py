from collections import defaultdict
from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional

import pyarrow as pa


if TYPE_CHECKING:
    import PIL.Image


class _ImageExtensionType(pa.PyExtensionType):
    def __init__(self):
        pa.PyExtensionType.__init__(self, pa.struct({"bytes": pa.binary(), "path": pa.string()}))

    def __reduce__(self):
        return self.__class__, ()


@dataclass(unsafe_hash=True)
class Image:
    """Image Feature to read image data from an image file.

    Input: The Image feature accepts as input:
    - A :obj:`str`: Absolute path to the image file (i.e. random access is allowed).
    - A :obj:`dict` with the keys:

        - path: String with relative path of the image file to the archive file.
        - bytes: Bytes of the image file.

      This is useful for archived files with sequential access.
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
            value (:obj:`str` or :obj:`dict`): Data passed as input to Image feature.

        Returns:
            :obj:`dict`
        """
        if isinstance(value, str):
            return {"path": value}
        elif isinstance(value, bytes):
            return {"bytes": value}
        else:
            return value

    def decode_example(self, value):
        """Decode example image bytes into image data.

        Args:
            value (obj:`str` or :obj:`dict`): a string with the absolute image file path, the image bytes or a dictionary with
                keys:
                - path: String with absolute or relative image file path.
                - bytes: the bytes of the image file.

        Returns:
            dict
        """
        try:
            import PIL.Image
            import PIL.ImageOps
        except ImportError as err:
            raise ImportError("To support decoding images, please install 'Pillow'.") from err

        if isinstance(value, str):
            value = {"path": value, "bytes": None}
        elif isinstance(value, bytes):
            value = {"path": None, "bytes": value}

        if value["bytes"]:
            path = value["path"]
            file = BytesIO(value["bytes"])
        else:
            path = value["path"]
            file = path

        image = PIL.Image.open(file)
        # note: this operation removes the underlying plugin if there is one,
        # which also makes format-specific methods unavailable (e.g. get_format_mimetype, etc.)
        image = PIL.ImageOps.exif_transpose(image)
        return {"path": path, "image": image}

    def decode_batch(self, values):
        decoded_batch = defaultdict(list)
        for value in values:
            decoded_example = self.decode_example(value)
            for k, v in decoded_example.items():
                decoded_batch[k].append(v)
        return dict(decoded_batch)


def convert_pil_image_to_bytes(pil_image: "PIL.Image.Image") -> bytes:
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def list_of_pil_images_to_list_of_encoded_images(l_pil_images: List["PIL.Image.Image"]) -> List[Dict[str, Any]]:
    return [{"bytes": convert_pil_image_to_bytes(pil_image)} for pil_image in l_pil_images]


def list_of_image_dicts_to_list_of_encoded_images(l_image_dicts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def map_key_to_field(col):
        return col if col != "image" else "bytes"

    return [
        {map_key_to_field(k): v if k != "image" else convert_pil_image_to_bytes(v) for k, v in image_dict.items()}
        for image_dict in l_image_dicts
    ]


def list_of_images_to_list_of_encoded_images(data):
    import PIL.Image  # TODO(mario): add PIL_AVAILABLE to config.py

    is_non_empty_list = isinstance(data, list) and data
    if is_non_empty_list and isinstance(data[0], PIL.Image.Image):
        encoded_images = list_of_pil_images_to_list_of_encoded_images(data)
    elif is_non_empty_list and isinstance(data[0], dict):
        encoded_images = list_of_image_dicts_to_list_of_encoded_images(data)
    else:
        encoded_images = data
    return encoded_images
