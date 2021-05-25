from typing import Optional

from .base import TaskTemplate
from .question_answering import QuestionAnswering
from .text_classification import TextClassification


__all__ = ["TaskTemplate", "QuestionAnswering", "TextClassification"]


NAME2TEMPLATE = {QuestionAnswering.task: QuestionAnswering, TextClassification.task: TextClassification}


def task_template_from_dict(task_template_dict: dict) -> Optional[TaskTemplate]:
    """Create one of the supported task templates in :py:mod:`datasets.tasks` from a dictionary."""
    task_name = task_template_dict.get("task")
    if task_name is None:
        return None
    template = NAME2TEMPLATE.get(task_name)
    if template is None:
        return None
    return template.from_dict(task_template_dict)
