import os
from typing import TypeVar, Union


T = TypeVar("T")

ListLike = Union[list[T], tuple[T, ...]]
NestedDataStructureLike = Union[T, list[T], dict[str, T]]
PathLike = Union[str, bytes, os.PathLike]
