from typing import Any, Optional, Sequence, Union

import numpy as np
import pandas as pd
import pyarrow as pa
from pandas.api.extensions import ExtensionArray as PandasExtensionArray
from pandas.api.extensions import ExtensionDtype as PandasExtensionDtype


class PandasBaseExtensionDtype(PandasExtensionDtype):
    pd_extension_array = None

    def __from_arrow__(self, array: Union[pa.Array, pa.ChunkedArray]):
        if isinstance(array, pa.ChunkedArray):
            numpy_arr = np.hstack([chunk.to_numpy(zero_copy_only=False) for chunk in array.chunks])
        else:
            numpy_arr = array.to_numpy(zero_copy_only=False)
        return self.construct_array_type()(numpy_arr)

    @classmethod
    def construct_array_type(cls):
        return cls.pd_extension_array

    @property
    def type(self) -> type:
        return object

    @property
    def kind(self) -> str:
        return "O"

    @property
    def name(self) -> str:
        return self.__class__.__name__.split("Pandas", 1)[-1].split("ExtensionDtype", 1)[0] + "Type"


class PandasBaseExtensionArray(PandasExtensionArray):
    pd_type = None

    def __init__(self, data: np.ndarray, copy: bool = False):
        self._data = data if not copy else np.array(data)

    def __array__(self):
        return self._data

    def copy(self, deep: bool = False) -> "PandasBaseExtensionArray":
        return self.__class__(self._data, copy=True)

    @classmethod
    def _from_sequence(
        cls, scalars, dtype: Optional[PandasBaseExtensionDtype] = None, copy: bool = False
    ) -> "PandasBaseExtensionArray":
        data = np.array(scalars, dtype=np.object, copy=copy)
        return cls(data, copy=copy)

    @classmethod
    def _concat_same_type(cls, to_concat: Sequence["PandasBaseExtensionArray"]) -> "PandasBaseExtensionArray":
        data = np.hstack([va._data for va in to_concat])
        return cls(data, copy=False)

    @property
    def dtype(self) -> PandasBaseExtensionDtype:
        return self.pd_type()

    @property
    def nbytes(self) -> int:
        return self._data.nbytes

    def isna(self) -> np.ndarray:
        return np.array([pd.isna(x) for x in self._data])

    def __setitem__(self, key: Union[int, slice, np.ndarray], value: Any) -> None:
        raise NotImplementedError

    def __getitem__(self, item: Union[int, slice, np.ndarray]) -> Union[np.ndarray, "PandasBaseExtensionArray"]:
        if isinstance(item, int):
            return self._data[item]
        return self.__class__(self._data[item], copy=False)

    def take(
        self, indices: Sequence[int], allow_fill: bool = False, fill_value: bool = None
    ) -> "PandasBaseExtensionArray":
        indices: np.ndarray = np.asarray(indices, dtype=np.int)
        if allow_fill:
            fill_value = self.dtype.na_value if fill_value is None else np.asarray(fill_value, dtype=np.object)
            mask = indices == -1
            if (indices < -1).any():
                raise ValueError("Invalid value in `indices`, must be all >= -1 for `allow_fill` is True")
            elif len(self) > 0:
                pass
            elif not np.all(mask):
                raise IndexError("Invalid take for empty PandasBaseExtensionArray, must be all -1.")
            else:
                data = np.array([fill_value] * len(indices), dtype=np.object)
                return self.__class__(data, copy=False)
        took = self._data.take(indices)
        if allow_fill and mask.any():
            took[mask] = [fill_value] * np.sum(mask)
        return self.__class__(took, copy=False)

    def map(self, mapper):
        # More info about this (undocumented) function can be found here:
        # https://github.com/pandas-dev/pandas/issues/23179
        return self.__class__(pd.Series(self._data).map(mapper).to_numpy())

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, other) -> np.ndarray:
        if not isinstance(other, self.__class__):
            raise NotImplementedError(f"Invalid type to compare to: {type(other)}")
        return (self._data == other._data).all()


def create_pd_type(pa_type_cls):
    feature_name = pa_type_cls.__name__.rsplit("Type", 1)[0]
    pd_type = type(
        "Pandas" + feature_name + "ExtensionDtype", (PandasBaseExtensionDtype,), {"py_type": int}
    )  # TODO set py_type
    pd_type.pd_extension_array = type(
        "Pandas" + feature_name + "ExtensionArray", (PandasBaseExtensionArray,), {"pd_type": pd_type}
    )
    return pd_type


class _WatchAndAutomaticallyCreatePandasDtype(type):
    def __init__(cls, name, bases, clsdict):
        if len(cls.mro()) > len(pa.PyExtensionType.mro()) + 1 and cls._pd_type is None:
            cls._pd_type = create_pd_type(cls)
        super(_WatchAndAutomaticallyCreatePandasDtype, cls).__init__(name, bases, clsdict)


class BasePyarrowExtensionType(pa.PyExtensionType, metaclass=_WatchAndAutomaticallyCreatePandasDtype):
    pa_storage_type = None
    _pd_type = None  # automatically created

    def __init__(self):
        pa.PyExtensionType.__init__(self, self.pa_storage_type)

    def __reduce__(self):
        return self.__class__, ()

    def to_pandas_dtype(self):
        return self._pd_type()

    def cast_storage(self, array: pa.Array) -> pa.Array:
        return array.cast(self.pa_storage_type)

    def wrap_array(self, storage: pa.Array) -> pa.ExtensionArray:
        return pa.ExtensionArray.from_storage(self, self.cast_storage(storage))
