from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import ClassLabel, Features, Image
from .base import TaskTemplate

@dataclass(frozen=True)
class ImageClassification(TaskTemplate):
    task: str = "image-classification"
    input_schema: ClassVar[Features] = Features({"image": Image()})
    label_schema: ClassVar[Features] = Features({"labels": ClassLabel})
    image_column: str = "image"
    label_column: str = "labels"

    def _align_with_features(self, features):
        if self.label_column not in features:
            raise ValueError(f"Column {self.label_column} is not present in features.")
        if not isinstance(features[self.label_column], ClassLabel):
            raise ValueError(f"Column {self.label_column} is not a ClassLabel.")
        task_template = self.copy()
        task_template.label_schema["labels"] = features[self.label_column]
        return task_template

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.image_column: "image",
            self.label_column: "labels",
        }
