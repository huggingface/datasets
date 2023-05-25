import os
from typing import TYPE_CHECKING, Dict, List, TypeVar, Union


if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


T = TypeVar("T")

NestedDataStructureLike = Union[T, List[T], Dict[str, T]]
PathLike = Union[str, bytes, os.PathLike]


ArrayLike = Union["pandas.core.arrays.base.ExtensionArray", "np.ndarray"]
AnyArrayLike = Union[ArrayLike, "pd.core.indexes.base.Index", "pd.core.series.Series"]
ListLike = Union[AnyArrayLike, List, range]
