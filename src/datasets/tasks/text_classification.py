from dataclasses import dataclass
from typing import ClassVar, Dict, List

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class TextClassification(TaskTemplate):
    task: ClassVar[str] = "text-classification"
    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    # TODO(lewtun): Since we update this in __post_init__ do we need to set a default? We'll need it for __init__ so
    # investigate if there's a more elegant approach.
    label_schema: ClassVar[Features] = Features({"labels": ClassLabel})
    labels: List[str]
    text_column: str = "text"
    label_column: str = "labels"

    def __post_init__(self):
        assert len(self.labels) == len(set(self.labels)), "Labels must be unique"
        # Cast labels to tuple to allow hashing
        self.__dict__["labels"] = tuple(sorted(self.labels))
        self.label_schema["labels"] = ClassLabel(names=self.labels)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.text_column: "text",
            self.label_column: "labels",
        }

    @property
    def label2id(self):
        return {label: idx for idx, label in enumerate(self.labels)}

    @property
    def id2label(self):
        return {idx: label for idx, label in enumerate(self.labels)}
