import os
from typing import Dict, List, TypeVar, Union


T = TypeVar("T")

NestedDataStructureLike = Union[T, List[T], Dict[str, T]]
PathLike = Union[str, bytes, os.PathLike]
