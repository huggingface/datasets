from dataclasses import dataclass
from typing import ClassVar, Dict

from ..features import Features, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class LanguageModeling(TaskTemplate):
    task: str = "language-modeling"

    input_schema: ClassVar[Features] = Features({"text": Value("string")})
    label_schema: ClassVar[Features] = Features({})
    text_column: str = "text"

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.text_column: "text"}
