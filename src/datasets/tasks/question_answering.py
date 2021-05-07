from typing import Dict

from ..features import Features, Value
from .base import TaskTemplate


class QuestionAnswering(TaskTemplate):
    task = "question_answering"
    input_schema = Features({"question": Value("string"), "context": Value("string")})
    label_schema = Features({"answer_start": Value("int32"), "answer_end": Value("int32")})

    def __init__(
        self,
        question_column: str = "question",
        context_column: str = "context",
        answer_start_column: str = "answer_start",
        answer_end_column: str = "answer_end",
    ):
        self.question_column = question_column
        self.context_column = context_column
        self.answer_start_column = answer_start_column
        self.answer_end_column = answer_end_column

    @property
    def column_mapping(self) -> Dict[str, str]:
        return {
            self.question_column: "question",
            self.context_column: "context",
            self.answer_start_column: "answer_start",
            self.answer_end_column: "answer_end",
        }

    @classmethod
    def from_dict(cls, template_dict: dict) -> "QuestionAnswering":
        return cls(
            question_column=template_dict["question_column"],
            context_column=template_dict["answer_column"],
            answer_start_column=template_dict["answer_start_column"],
            answer_end_column=template_dict["answer_end_column"],
        )
