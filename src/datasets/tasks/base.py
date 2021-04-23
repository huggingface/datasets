import abc
from dataclasses import dataclass
from typing import Optional

from ..features import Features


@dataclass
class TaskTemplate(abc.ABC):
    task: str
    input_schema: Features
    label_schema: Optional[Features]

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, template_dict: dict) -> "TaskTemplate":
        return NotImplemented
