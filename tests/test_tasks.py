from unittest.case import TestCase

from datasets.features import ClassLabel, Features, Sequence, Value
from datasets.tasks import QuestionAnswering, TextClassification


class TextClassificationTest(TestCase):
    def setUp(self):
        self.labels = sorted(["pos", "neg"])

    def test_column_mapping(self):
        task = TextClassification(text_column="input_text", label_column="input_label", labels=self.labels)
        self.assertDictEqual({"input_text": "text", "input_label": "labels"}, task.column_mapping)

    def test_from_dict(self):
        input_schema = Features({"text": Value("string")})
        label_schema = Features({"labels": ClassLabel(names=self.labels)})
        template_dict = {"text_column": "input_text", "label_column": "input_labels", "labels": self.labels}
        task = TextClassification.from_dict(template_dict)
        self.assertEqual("text_classification", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)


class QuestionAnsweringTest(TestCase):
    def test_column_mapping(self):
        task = QuestionAnswering(
            context_column="input_context", question_column="input_question", answers_column="input_answers"
        )
        self.assertDictEqual(
            {"input_context": "context", "input_question": "question", "input_answers": "answers"}, task.column_mapping
        )

    def test_from_dict(self):
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
        template_dict = {
            "context_column": "input_input_contexttext",
            "question_column": "input_question",
            "answers_column": "input_answers",
        }
        task = QuestionAnswering.from_dict(template_dict)
        self.assertEqual("question_answering", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)
