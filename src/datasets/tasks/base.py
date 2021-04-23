import abc
from dataclasses import dataclass
from typing import Dict, Optional

from ..features import Features


@dataclass
class TaskTemplate(abc.ABC):
    task: str
    input_schema: Features
    label_schema: Optional[Features]

    @property
    def features(self) -> Features:
        if not self.label_schema:
            return self.input_schema
        else:
            return Features(**self.input_schema, **self.label_schema)

    @property
    @abc.abstractmethod
    def column_mapping(self) -> Dict[str, str]:
        return NotImplemented

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, template_dict: dict) -> "TaskTemplate":
        return NotImplemented
