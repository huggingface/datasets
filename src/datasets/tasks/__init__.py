from typing import Optional

from ..utils.logging import get_logger
from .base import TaskTemplate
from .question_answering import QuestionAnsweringExtractive
from .text_classification import TextClassification


__all__ = ["TaskTemplate", "QuestionAnsweringExtractive", "TextClassification"]

logger = get_logger(__name__)


NAME2TEMPLATE = {
    QuestionAnsweringExtractive.task: QuestionAnsweringExtractive,
    TextClassification.task: TextClassification,
}


def task_template_from_dict(task_template_dict: dict) -> Optional[TaskTemplate]:
    """Create one of the supported task templates in :py:mod:`datasets.tasks` from a dictionary."""
    task_name = task_template_dict.get("task")
    if task_name is None:
        logger.warning(f"Couldn't find template for task '{task_name}'. Available templates: {list(NAME2TEMPLATE)}")
        return None
    template = NAME2TEMPLATE.get(task_name)
    return template.from_dict(task_template_dict)
