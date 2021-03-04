from abc import ABC, abstractmethod
from typing import Optional

from .. import Features, NamedSplit
from ..arrow_dataset import Dataset
from ..utils.typing import PathLike


class AbstractDatasetReader(ABC):
    def __init__(
        self,
        path: PathLike,
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        self.path = path
        self.split = split
        self.features = features
        self.cache_dir = cache_dir
        self.keep_in_memory = keep_in_memory
        self.kwargs = kwargs

    @abstractmethod
    def read(self) -> Dataset:
        pass
