from dataclasses import dataclass
from typing import ClassVar, Dict, List

from ..features import ClassLabel, Features, Value
from .base import TaskTemplate


class FeaturesWithLazyClassLabel:
    def __init__(self, features, label_column="labels"):
        assert label_column in features, f"Key '{label_column}' missing in features {features}"
        self._features = features
        self._label_column = label_column

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self._features

        assert hasattr(obj, self._label_column), f"Object has no attribute '{self._label_column}'"
        features = self._features.copy()
        features["labels"] = ClassLabel(names=getattr(obj, self._label_column))
        return features


@dataclass(frozen=True)
class TextClassification(TaskTemplate):
    task: ClassVar[str] = "text-classification"
    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    # TODO(lewtun): Find a more elegant approach without descriptors.
    label_schema: ClassVar[Features] = FeaturesWithLazyClassLabel(Features({"labels": ClassLabel}))
    labels: List[str]
    text_column: str = "text"
    label_column: str = "labels"

    def __post_init__(self):
        assert len(self.labels) == len(set(self.labels)), "Labels must be unique"
        # Cast labels to tuple to allow hashing
        self.__dict__["labels"] = tuple(sorted(self.labels))

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
