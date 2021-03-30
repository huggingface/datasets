import abc
from typing import Dict, Union

from pydantic import BaseModel

from .. import Dataset, DatasetDict
from .base import AbstractTaskDataset


class ClassificationSingleLabelDataset(AbstractTaskDataset, metaclass=abc.ABCMeta):
    id = "classification_single_label"
    labels = ["classification", "nlp"]
    description = """
`classification_single_label` is a task that pairs a block of text with a label, drawn from an existing finite set of labels.
Classical instances of this task are:
- sentiment detection, which assigns a block of text with a label in ["positive", "negative"] set.
- topic classification, which assigns a block of text with a topic, e.g. in a set like ["sports", "politics", ...]
- fact checking, which assigns a block of text with a label in ["false", "true"]
    """

    class Input(BaseModel):
        text: str

    class Output(BaseModel):
        label_id: int

    input_schema = Input.schema_json()
    output_schema = Output.schema_json()

    @property
    @abc.abstractmethod
    def label2id(self) -> Dict[str, int]:
        raise NotImplementedError


class ClassificationSingleLabelDatasetBuilder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def cast_as_classification_single_label(
        self, dataset: Union[Dataset, DatasetDict]
    ) -> ClassificationSingleLabelDataset:
        """The table should have column names matching the input and output schemas laid out above."""
        raise NotImplementedError
