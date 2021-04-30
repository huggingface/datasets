from typing import Optional

from .base import TaskTemplate
from .question_answering import QuestionAnswering
from .text_classification import TextClassification


__all__ = ["TaskTemplate", "QuestionAnswering", "TextClassification"]


NAME2TEMPLATE = {QuestionAnswering.task: QuestionAnswering, TextClassification.task: TextClassification}


def task_template_from_dict(task_template_dict: dict) -> Optional[TaskTemplate]:
    task_name = task_template_dict.get("name")
    if task_name is None:
        return None
    template = NAME2TEMPLATE.get(task_name)
    if template is None:
        return None
    return template.from_dict(task_template_dict)
