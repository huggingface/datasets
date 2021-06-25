from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class Summarization(TaskTemplate):
    # `task` is not a ClassVar since we want it to be part of the `asdict` output for JSON serialization
    task: str = "summarization"
    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    label_schema: ClassVar[Features] = Features({"summary": Value("string")})
    text_column: str = "text"
    summary_column: str = "summary"

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.text_column: "text", self.summary_column: "summary"}
