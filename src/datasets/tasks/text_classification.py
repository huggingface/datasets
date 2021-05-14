from dataclasses import dataclass
from typing import Dict, List

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class TextClassification(TaskTemplate):
    task = "text-classification"
    input_schema = Features({"text": Value("string")})
    label_schema = Features({"labels": ClassLabel})
    labels: List[str]
    text_column: str = "text"
    label_column: str = "labels"

    def __post_init__(self):
        assert sorted(set(self.labels)) == sorted(self.labels), "Labels must be unique"
        # Cast labels to tuple to allow hashing
        object.__setattr__(self, "labels", tuple(sorted(self.labels)))
        object.__setattr__(self, "text_column", self.text_column)
        object.__setattr__(self, "label_column", self.label_column)
        self.label_schema["labels"] = ClassLabel(names=self.labels)
        object.__setattr__(self, "label2id", {label: idx for idx, label in enumerate(self.labels)})
        object.__setattr__(self, "id2label", {idx: label for label, idx in self.label2id.items()})

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
