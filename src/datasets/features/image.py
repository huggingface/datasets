from dataclasses import dataclass, field
from io import BytesIO
from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from pandas.api.extensions import ExtensionArray as PandasExtensionArray
from pandas.api.extensions import ExtensionDtype as PandasExtensionDtype

from .. import config
from ..utils.file_utils import is_local_path
from ..utils.streaming_download_manager import xopen


if TYPE_CHECKING:
    import PIL.Image


_IMAGE_COMPRESSION_FORMATS: Optional[List[str]] = None


class ImageExtensionType(pa.PyExtensionType):
    def __init__(self, storage_dtype):
        self.storage_dtype = storage_dtype
        if storage_dtype == "string":
            pa_type = pa.string()
        elif storage_dtype == "binary":
            pa_type = pa.binary()
        else:
            pa_type = pa.struct({"bytes": pa.binary(), "path": pa.string()})
        pa.PyExtensionType.__init__(self, pa_type)

    def __arrow_ext_class__(self):
        return ImageExtensionArray

    def __reduce__(self):
        return self.__class__, (self.storage_dtype,)

    def to_pandas_dtype(self):
        return PandasImageExtensionDtype()


class ImageExtensionArray(pa.ExtensionArray):
    def __array__(self):
        return self.to_numpy(zero_copy_only=False)

    def __getitem__(self, i):
        return self.storage[i]

    def to_pylist(self):
        return self.to_numpy(zero_copy_only=False).tolist()


class PandasImageExtensionDtype(PandasExtensionDtype):
    def __from_arrow__(self, array: Union[pa.Array, pa.ChunkedArray]):
        if isinstance(array, pa.ChunkedArray):
            numpy_arr = np.hstack([chunk.to_numpy(zero_copy_only=False) for chunk in array.chunks])
        else:
            numpy_arr = array.to_numpy(zero_copy_only=False)
        return PandasImageExtensionArray(numpy_arr)

    @classmethod
    def construct_array_type(cls):
        return PandasImageExtensionArray

    @property
    def type(self) -> type:
        # Expensive calls under the propery decorator are not a good practice, but it is what it is.
        if config.PIL_AVAILABLE:
            import PIL.Image
        else:
            raise ImportError("Pillow is not available.")
        return PIL.Image.Image

    @property
    def kind(self) -> str:
        return "O"

    @property
    def name(self) -> str:
        return "image"


class PandasImageExtensionArray(PandasExtensionArray):
    na_value = None

    def __init__(self, data: np.ndarray, copy: bool = False):
        self._data = data if not copy else np.array(data)
        self._dtype = PandasImageExtensionDtype()

    def __array__(self):
        return self._data

    def copy(self, deep: bool = False) -> "PandasImageExtensionArray":
        return PandasImageExtensionArray(self._data, copy=True)

    @classmethod
    def _from_sequence(
        cls, scalars, dtype: Optional[PandasImageExtensionDtype] = None, copy: bool = False
    ) -> "PandasImageExtensionArray":
        data = np.array(scalars, dtype=np.object, copy=copy)
        return cls(data, copy=copy)

    @classmethod
    def _concat_same_type(cls, to_concat: Sequence["PandasImageExtensionArray"]) -> "PandasImageExtensionArray":
        data = np.hstack([va._data for va in to_concat])
        return cls(data, copy=False)

    @property
    def dtype(self) -> PandasImageExtensionDtype:
        return self._dtype

    @property
    def nbytes(self) -> int:
        return self._data.nbytes

    def isna(self) -> np.ndarray:
        return np.array([pd.isna(arr).any() for arr in self._data])

    def __setitem__(self, key: Union[int, slice, np.ndarray], value: Any) -> None:
        raise NotImplementedError

    def __getitem__(self, item: Union[int, slice, np.ndarray]) -> Union[np.ndarray, "PandasImageExtensionArray"]:
        if isinstance(item, int):
            return self._data[item]
        return PandasImageExtensionArray(self._data[item], copy=False)

    def take(
        self, indices: Sequence[int], allow_fill: bool = False, fill_value: bool = None
    ) -> "PandasImageExtensionArray":
        indices: np.ndarray = np.asarray(indices, dtype=np.int)
        if allow_fill:
            fill_value = self.dtype.na_value if fill_value is None else np.asarray(fill_value, dtype=np.object)
            mask = indices == -1
            if (indices < -1).any():
                raise ValueError("Invalid value in `indices`, must be all >= -1 for `allow_fill` is True")
            elif len(self) > 0:
                pass
            elif not np.all(mask):
                raise IndexError("Invalid take for empty PandasImageExtensionArray, must be all -1.")
            else:
                data = np.array([fill_value] * len(indices), dtype=np.object)
                return PandasImageExtensionArray(data, copy=False)
        took = self._data.take(indices)
        if allow_fill and mask.any():
            took[mask] = [fill_value] * np.sum(mask)
        return PandasImageExtensionArray(took, copy=False)

    def map(self, mapper):
        # More info about this (undocumented) function can be found here:
        # https://github.com/pandas-dev/pandas/issues/23179
        return PandasImageExtensionArray(pd.Series(self._data).map(mapper).to_numpy())

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, other) -> np.ndarray:
        if not isinstance(other, PandasImageExtensionArray):
            raise NotImplementedError(f"Invalid type to compare to: {type(other)}")
        return (self._data == other._data).all()


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

    _storage_dtype: str = "string"
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Image", init=False, repr=False)

    def __call__(self):
        return ImageExtensionType(self._storage_dtype)

    def encode_example(self, value):
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
            self._storage_dtype = "string"
            return value
        elif isinstance(value, np.ndarray):
            self._storage_dtype = "binary"
            image = PIL.Image.fromarray(value.astype(np.uint8))
            return image_to_bytes(image)
        elif isinstance(value, PIL.Image.Image):
            if hasattr(value, "filename") and value.filename != "":
                self._storage_dtype = "string"
                return value.filename
            else:
                self._storage_dtype = "binary"
                return image_to_bytes(value)
        else:
            self._storage_dtype = "struct"
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

        if isinstance(value, str):
            path, bytes_ = value, None
        elif isinstance(value, bytes):
            path, bytes_ = None, BytesIO(value)
        else:
            path, bytes_ = value["path"], BytesIO(value["bytes"])

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


def objects_to_image_storage(objs) -> Tuple[pa.Array, ImageExtensionType]:
    """Encode a list of string, np.ndarray or PIL Image objects into image storage representation and deduce the image storage type.

    It checks only the first element to deduce the storage type.
    """
    if config.PIL_AVAILABLE:
        import PIL.Image
    else:
        raise ImportError("To support encoding images, please install 'Pillow'.")

    if objs:
        obj = objs[0]
        if isinstance(obj, str):
            return pa.array(objs, type=pa.string()), ImageExtensionType("string")
        elif isinstance(obj, bytes):
            return pa.array(objs, type=pa.binary()), ImageExtensionType("binary")
        elif isinstance(obj, PIL.Image.Image):
            # expensive, but can avoid unnecessary conversion to bytes
            if all(hasattr(obj, "filename") and obj.filename != "" for obj in objs):
                return pa.array([obj.filename for obj in objs], type=pa.string()), ImageExtensionType("string")
            return pa.array([image_to_bytes(obj) for obj in objs], type=pa.binary()), ImageExtensionType("binary")
        elif isinstance(obj, np.ndarray):
            return (
                pa.array(
                    [image_to_bytes(PIL.Image.fromarray(obj.astype(np.uint8))) for obj in objs],
                    type=pa.binary(),
                ),
                ImageExtensionType("binary"),
            )
        else:
            return (
                pa.array(objs, type=pa.struct({"bytes": pa.binary(), "path": pa.string()})),
                ImageExtensionType("struct"),
            )
    else:
        return pa.array(objs), ImageExtensionType("string")
