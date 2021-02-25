from abc import ABC, abstractmethod
from typing import Optional

from .. import DatasetInfo, NamedSplit
from ..arrow_dataset import Dataset
from ..utils.typing import PathLike


class AbstractDatasetReader(ABC):
    def __init__(
        self, path: PathLike, info: Optional[DatasetInfo] = None, split: Optional[NamedSplit] = None, **kwargs
    ):
        self.path = path
        self.info = info
        self.split = split
        self.kwargs = kwargs

    @abstractmethod
    def read(self) -> Dataset:
        pass
