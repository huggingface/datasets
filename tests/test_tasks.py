from unittest.case import TestCase

from datasets.features import ClassLabel, Features, Sequence, Value
from datasets.tasks import (
    AutomaticSpeechRecognition,
    ImageClassification,
    QuestionAnsweringExtractive,
    Summarization,
    TextClassification,
)


class TextClassificationTest(TestCase):
    def setUp(self):
        self.labels = sorted(["pos", "neg"])

    def test_column_mapping(self):
        task = TextClassification(text_column="input_text", label_column="input_label", labels=self.labels)
        self.assertDictEqual({"input_text": "text", "input_label": "labels"}, task.column_mapping)

    def test_from_dict(self):
        input_schema = Features({"text": Value("string")})
        # Labels are cast to tuple during `TextClassification.__post_init__`, so we do the same here
        label_schema = Features({"labels": ClassLabel(names=tuple(self.labels))})
        template_dict = {"text_column": "input_text", "label_column": "input_labels", "labels": self.labels}
        task = TextClassification.from_dict(template_dict)
        self.assertEqual("text-classification", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)


class QuestionAnsweringTest(TestCase):
    def test_column_mapping(self):
        task = QuestionAnsweringExtractive(
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
            "context_column": "input_input_context",
            "question_column": "input_question",
            "answers_column": "input_answers",
        }
        task = QuestionAnsweringExtractive.from_dict(template_dict)
        self.assertEqual("question-answering-extractive", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)


class SummarizationTest(TestCase):
    def test_column_mapping(self):
        task = Summarization(text_column="input_text", summary_column="input_summary")
        self.assertDictEqual({"input_text": "text", "input_summary": "summary"}, task.column_mapping)

    def test_from_dict(self):
        input_schema = Features({"text": Value("string")})
        label_schema = Features({"summary": Value("string")})
        template_dict = {"text_column": "input_text", "summary_column": "input_summary"}
        task = Summarization.from_dict(template_dict)
        self.assertEqual("summarization", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)


class AutomaticSpeechRecognitionTest(TestCase):
    def test_column_mapping(self):
        task = AutomaticSpeechRecognition(
            audio_file_path_column="input_audio_file_path", transcription_column="input_transcription"
        )
        self.assertDictEqual(
            {"input_audio_file_path": "audio_file_path", "input_transcription": "transcription"}, task.column_mapping
        )

    def test_from_dict(self):
        input_schema = Features({"audio_file_path": Value("string")})
        label_schema = Features({"transcription": Value("string")})
        template_dict = {
            "audio_file_path_column": "input_audio_file_path",
            "transcription_column": "input_transcription",
        }
        task = AutomaticSpeechRecognition.from_dict(template_dict)
        self.assertEqual("automatic-speech-recognition", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)


class ImageClassificationTest(TestCase):
    def setUp(self):
        self.labels = sorted(["pos", "neg"])

    def test_column_mapping(self):
        task = ImageClassification(image_file_path_column="file_paths", label_column="input_label")
        self.assertDictEqual({"file_paths": "image_file_path", "input_label": "labels"}, task.column_mapping)

    def test_from_dict(self):
        input_schema = Features({"image_file_path": Value("string")})
        label_schema = Features({"labels": ClassLabel(names=tuple(self.labels))})
        template_dict = {
            "image_file_path_column": "input_image_file_path",
            "label_column": "input_label",
            "labels": self.labels,
        }
        task = ImageClassification.from_dict(template_dict)
        self.assertEqual("image-classification", task.task)
        self.assertEqual(input_schema, task.input_schema)
        self.assertEqual(label_schema, task.label_schema)
