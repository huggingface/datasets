from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Tuple

from ..features import ClassLabel, Features, Image
from .base import TaskTemplate


@dataclass(frozen=True)
class ImageClassification(TaskTemplate):
    task: str = "image-classification"
    input_schema: ClassVar[Features] = Features({"image": Image()})
    label_schema: ClassVar[Features] = Features({"labels": ClassLabel})
    image_column: str = "image"
    label_column: str = "labels"
    labels: Optional[Tuple[str]] = None

    def __post_init__(self):
        if self.labels:
            if len(self.labels) != len(set(self.labels)):
                raise ValueError("Labels must be unique")
            # Cast labels to tuple to allow hashing
            self.__dict__["labels"] = tuple(sorted(self.labels))
            self.__dict__["label_schema"] = self.label_schema.copy()
            self.label_schema["labels"] = ClassLabel(names=self.labels)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.image_column: "image",
            self.label_column: "labels",
        }
