from dataclasses import dataclass
from typing import Dict, List

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class TextClassification(TaskTemplate):
    task = "text-classification"
    input_schema = Features({"text": Value("string")})
    # TODO(lewtun): Since we update this in __post_init__ do we need to set a default? We'll need it for __init__ so
    # investigate if there's a more elegant approach.
    label_schema = Features({"labels": ClassLabel})
    labels: List[str] = None
    text_column: str = "text"
    label_column: str = "labels"

    def __post_init__(self):
        object.__setattr__(self, "labels", self.labels)
        object.__setattr__(self, "text_column", self.text_column)
        object.__setattr__(self, "label_column", self.label_column)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.text_column: "text",
            self.label_column: "labels",
        }

    @classmethod
    def from_dict(cls, template_dict: dict) -> "TextClassification":
        return cls(
            text_column=template_dict["text_column"],
            label_column=template_dict["label_column"],
            labels=template_dict["labels"],
        )

    @property
    def label2id(self):
        return {label: idx for idx, label in enumerate(self.labels)}

    @property
    def id2label(self):
        return {idx: label for idx, label in enumerate(self.labels)}
