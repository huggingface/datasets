import abc
from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Features


@dataclass(frozen=True)
class TaskTemplate(abc.ABC):
    task: ClassVar[str]
    input_schema: ClassVar[Features]
    label_schema: ClassVar[Features]

    @property
    def features(self) -> Features:
        return Features(**self.input_schema, **self.label_schema)

    @property
    @abc.abstractmethod
    def column_mapping(self) -> Dict[str, str]:
        return NotImplemented

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, template_dict: dict) -> "TaskTemplate":
        return NotImplemented
