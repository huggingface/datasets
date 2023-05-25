from __future__ import annotations

import os
from typing import Dict, Generic, List, TypeVar, Union

import numpy as np
import pandas as pd


T = TypeVar("T")

NestedDataStructureLike = Union[T, List[T], Dict[str, T]]
PathLike = Union[str, bytes, os.PathLike]


class NumpyNDArray(np.ndarray, Generic[T]):
    ...


class PandasExtensionArray(pd.core.arrays.base.ExtensionArray, Generic[T]):
    ...


class PandasIndex(pd.core.indexes.base.Index, Generic[T]):
    ...


class PandasSeries(pd.core.series.Series, Generic[T]):
    ...


ArrayLike = Union[NumpyNDArray[T], PandasExtensionArray[T]]
AnyArrayLike = Union[ArrayLike[T], PandasIndex[T], PandasSeries[T]]
ListLike = Union[AnyArrayLike[T], List[T]]
