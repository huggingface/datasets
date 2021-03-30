import abc
from typing import List, Union

from .. import Dataset, DatasetDict


class AbstractTaskDataset(Dataset, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def id(cls) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def labels(cls) -> List[str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def description(cls) -> List[str]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def input_schema(cls) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def output_schema(cls) -> str:
        raise NotImplementedError

    @classmethod
    def from_dataset(
        cls, dataset: Union[Dataset, DatasetDict]
    ) -> Union["AbstractTaskDataset", DatasetDict["AbstractTaskDataset"]]:
        if isinstance(dataset, Dataset):
            return cls(dataset._data, dataset.info, dataset.split, dataset._indices, dataset._fingerprint)
        elif isinstance(dataset, DatasetDict):
            return DatasetDict({key: cls.from_dataset(d) for key, d in dataset.items()})
        else:
            raise TypeError(f"Expected a Dataset or DatasetDict, received '{type(dataset)}'")
