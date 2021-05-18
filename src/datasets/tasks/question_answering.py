from dataclasses import dataclass
from typing import Dict

from ..features import Features, Sequence, Value
from .base import TaskTemplate


@dataclass(frozen=True)
class QuestionAnswering(TaskTemplate):
    task = "question-answering"
    input_schema = Features({"question": Value("string"), "context": Value("string")})
    label_schema = Features(
        {
            "answers": Sequence(
                {
                    "text": Value("string"),
                    "answer_start": Value("int32"),
                }
            )
        }
    )
    question_column: str = "question"
    context_column: str = "context"
    answers_column: str = "answers"

    def __post_init__(self):
        object.__setattr__(self, "question_column", self.question_column)
        object.__setattr__(self, "context_column", self.context_column)
        object.__setattr__(self, "answers_column", self.answers_column)

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {self.question_column: "question", self.context_column: "context", self.answers_column: "answers"}

    @classmethod
    def from_dict(cls, template_dict: dict) -> "QuestionAnswering":
        return cls(
            question_column=template_dict["question_column"],
            context_column=template_dict["context_column"],
            answers_column=template_dict["answers_column"],
        )
