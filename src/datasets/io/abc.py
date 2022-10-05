from abc import ABC, abstractmethod
from typing import Optional, Union

from .. import Dataset, DatasetDict, Features, IterableDataset, IterableDatasetDict, NamedSplit
from ..utils.typing import NestedDataStructureLike, PathLike


class AbstractDatasetReader(ABC):
    def __init__(
        self,
        path_or_paths: NestedDataStructureLike[PathLike],
        split: Optional[NamedSplit] = None,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        streaming: bool = False,
        **kwargs,
    ):
        self.path_or_paths = path_or_paths
        self.split = split if split or isinstance(path_or_paths, dict) else "train"
        self.features = features
        self.cache_dir = cache_dir
        self.keep_in_memory = keep_in_memory
        self.streaming = streaming
        self.kwargs = kwargs

    @abstractmethod
    def read(self) -> Union[Dataset, DatasetDict, IterableDataset, IterableDatasetDict]:
        pass


class AbstractDatasetInputStream(ABC):
    def __init__(
        self,
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        streaming: bool = False,
        **kwargs,
    ):
        self.features = features
        self.cache_dir = cache_dir
        self.keep_in_memory = keep_in_memory
        self.streaming = streaming
        self.kwargs = kwargs

    @abstractmethod
    def read(self) -> Union[Dataset, IterableDataset]:
        pass
