import re
import tempfile
import unittest
from dataclasses import _MISSING_TYPE, asdict, fields
from pathlib import Path

from datasets.utils.metadata import (
    DatasetMetadata,
    metadata_dict_from_readme,
    tagset_validator,
    validate_metadata_type,
    yaml_block_from_readme,
)


def _dedent(string: str) -> str:
    indent_level = min(re.search("^ +", t).end() if t.startswith(" ") else 0 for t in string.splitlines())
    return "\n".join([line[indent_level:] for line in string.splitlines() if indent_level < len(line)])


README_YAML = """\
---
language:
- zh
- en
task_ids:
- sentiment-classification
---
# Begin of markdown

Some cool dataset card
"""

README_EMPTY_YAML = """\
---
---
# Begin of markdown

Some cool dataset card
"""


README_NO_YAML = """\
# Begin of markdown

Some cool dataset card
"""


class TestMetadataUtils(unittest.TestCase):
    def test_validate_metadata_type(self):
        metadata_dict = {
            "tag": ["list", "of", "values"],
            "another tag": ["Another", {"list"}, ["of"], 0x646D46736457567A],
        }
        with self.assertRaises(TypeError):
            validate_metadata_type(metadata_dict)

        metadata_dict = {"tag1": []}
        with self.assertRaises(TypeError):
            validate_metadata_type(metadata_dict)

        metadata_dict = {"tag1": None}
        with self.assertRaises(TypeError):
            validate_metadata_type(metadata_dict)

    def test_tagset_validator(self):
        name = "test_tag"
        url = "https://dummy.hf.co"

        items = ["tag1", "tag2", "tag2", "tag3"]
        reference_values = ["tag1", "tag2", "tag3"]
        returned_values, error = tagset_validator(items=items, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, items)
        self.assertIsNone(error)

        items = []
        reference_values = ["tag1", "tag2", "tag3"]
        items, error = tagset_validator(items=items, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(items, [])
        self.assertIsNone(error)

        items = []
        reference_values = []
        returned_values, error = tagset_validator(items=items, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, [])
        self.assertIsNone(error)

        items = ["tag1", "tag2", "tag2", "tag3", "unknown tag"]
        reference_values = ["tag1", "tag2", "tag3"]
        returned_values, error = tagset_validator(items=items, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, [])
        self.assertEqual(error, f"{['unknown tag']} are not registered tags for '{name}', reference at {url}")

        def predicate_fn(string):
            return "ignore" in string

        items = ["process me", "process me too", "ignore me"]
        reference_values = ["process me too"]
        returned_values, error = tagset_validator(
            items=items,
            reference_values=reference_values,
            name=name,
            url=url,
            escape_validation_predicate_fn=predicate_fn,
        )
        self.assertListEqual(returned_values, [])
        self.assertEqual(error, f"{['process me']} are not registered tags for '{name}', reference at {url}")

        items = ["process me", "process me too", "ignore me"]
        reference_values = ["process me too", "process me"]
        returned_values, error = tagset_validator(
            items=items,
            reference_values=reference_values,
            name=name,
            url=url,
            escape_validation_predicate_fn=predicate_fn,
        )
        self.assertListEqual(returned_values, items)
        self.assertIsNone(error)

        items = ["ignore me too", "ignore me"]
        reference_values = ["process me too"]
        returned_values, error = tagset_validator(
            items=items,
            reference_values=reference_values,
            name=name,
            url=url,
            escape_validation_predicate_fn=predicate_fn,
        )
        self.assertListEqual(returned_values, items)
        self.assertIsNone(error)

    def test_yaml_block_from_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"

            with open(path, "w+") as readme_file:
                readme_file.write(README_YAML)
            yaml_block = yaml_block_from_readme(path=path)
            self.assertEqual(
                yaml_block,
                _dedent(
                    """\
                    language:
                    - zh
                    - en
                    task_ids:
                    - sentiment-classification
                    """
                ),
            )

            with open(path, "w+") as readme_file:
                readme_file.write(README_EMPTY_YAML)
            yaml_block = yaml_block_from_readme(path=path)
            self.assertEqual(
                yaml_block,
                _dedent(
                    """\
                    """
                ),
            )

            with open(path, "w+") as readme_file:
                readme_file.write(README_NO_YAML)
            yaml_block = yaml_block_from_readme(path=path)
            self.assertIsNone(yaml_block)

    def test_metadata_dict_from_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"
            with open(path, "w+") as readme_file:
                readme_file.write(README_YAML)
            metadata_dict = metadata_dict_from_readme(path)
            self.assertDictEqual(metadata_dict, {"language": ["zh", "en"], "task_ids": ["sentiment-classification"]})

            with open(path, "w+") as readme_file:
                readme_file.write(README_EMPTY_YAML)
            metadata_dict = metadata_dict_from_readme(path)
            self.assertDictEqual(metadata_dict, {})

            with open(path, "w+") as readme_file:
                readme_file.write(README_NO_YAML)
            metadata_dict = metadata_dict_from_readme(path)
            self.assertIsNone(metadata_dict)

    def test_from_yaml_string(self):

        default_optional_keys = {
            field.name: field.default
            for field in fields(DatasetMetadata)
            if type(field.default) is not _MISSING_TYPE and field.name not in DatasetMetadata._DEPRECATED_YAML_KEYS
        }

        default_deprecated_keys = {
            field.name: field.default
            for field in fields(DatasetMetadata)
            if field.name in DatasetMetadata._DEPRECATED_YAML_KEYS
        }

        valid_yaml_string = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            """
        )
        DatasetMetadata.from_yaml_string(valid_yaml_string)

        valid_yaml_string_with_configs = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
              en:
              - en
              fr:
              - fr
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            """
        )
        DatasetMetadata.from_yaml_string(valid_yaml_string_with_configs)

        invalid_tag_yaml = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - some guys in Panama
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            """
        )
        with self.assertRaises(TypeError):
            metadata = DatasetMetadata.from_yaml_string(invalid_tag_yaml)
            metadata.validate()

        missing_tag_yaml = _dedent(
            """\
            annotations_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            """
        )
        with self.assertRaises(TypeError):
            metadata = DatasetMetadata.from_yaml_string(missing_tag_yaml)
            metadata.validate()

        duplicate_yaml_keys = _dedent(
            """\
            annotations_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            task_ids:
            - open-domain-qa
            """
        )
        with self.assertRaises(TypeError):
            metadata = DatasetMetadata.from_yaml_string(duplicate_yaml_keys)
            metadata.validate()

        valid_yaml_string_with_duplicate_configs = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
              en:
              - en
              en:
              - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            """
        )
        with self.assertRaises(TypeError):
            metadata = DatasetMetadata.from_yaml_string(valid_yaml_string_with_duplicate_configs)
            metadata.validate()

        valid_yaml_string_with_paperswithcode_id = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            paperswithcode_id: squad
            """
        )
        DatasetMetadata.from_yaml_string(valid_yaml_string_with_paperswithcode_id)

        valid_yaml_string_with_null_paperswithcode_id = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            paperswithcode_id: null
            """
        )
        DatasetMetadata.from_yaml_string(valid_yaml_string_with_null_paperswithcode_id)

        valid_yaml_string_with_list_paperswithcode_id = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - question-answering
            task_ids:
            - open-domain-qa
            paperswithcode_id:
            - squad
            """
        )
        with self.assertRaises(TypeError):
            metadata = DatasetMetadata.from_yaml_string(valid_yaml_string_with_list_paperswithcode_id)
            metadata.validate()

        valid_yaml_with_optional_keys = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            language:
            - en
            license:
            - unknown
            multilinguality:
            - monolingual
            pretty_name: Test Dataset
            size_categories:
            - 10K<n<100K
            source_datasets:
            - extended|other-yahoo-webscope-l6
            task_categories:
            - text-classification
            task_ids:
            - multi-class-classification
            paperswithcode_id:
            - squad
            configs:
            - en
            train-eval-index:
            - config: en
              task: text-classification
              task_id: multi_class_classification
              splits:
                train_split: train
                eval_split: test
              col_mapping:
                text: text
                label: target
              metrics:
                - type: accuracy
                  name: Accuracy
            extra_gated_prompt: |
              By clicking on “Access repository” below, you also agree to ImageNet Terms of Access:
              [RESEARCHER_FULLNAME] (the "Researcher") has requested permission to use the ImageNet database (the "Database") at Princeton University and Stanford University. In exchange for such permission, Researcher hereby agrees to the following terms and conditions:
              1. Researcher shall use the Database only for non-commercial research and educational purposes.
            extra_gated_fields:
              Company: text
              Country: text
              I agree to use this model for non-commerical use ONLY: checkbox
            """
        )

        metadata = DatasetMetadata.from_yaml_string(valid_yaml_with_optional_keys)
        metadata_dict = asdict(metadata)
        expected = {
            **default_optional_keys,
            **default_deprecated_keys,
            "annotations_creators": ["found"],
            "language_creators": ["found"],
            "language": ["en"],
            "license": ["unknown"],
            "multilinguality": ["monolingual"],
            "pretty_name": "Test Dataset",
            "size_categories": ["10K<n<100K"],
            "source_datasets": ["extended|other-yahoo-webscope-l6"],
            "task_categories": ["text-classification"],
            "task_ids": ["multi-class-classification"],
            "paperswithcode_id": ["squad"],
            "configs": ["en"],
            "train_eval_index": [
                {
                    "config": "en",
                    "task": "text-classification",
                    "task_id": "multi_class_classification",
                    "splits": {"train_split": "train", "eval_split": "test"},
                    "col_mapping": {"text": "text", "label": "target"},
                    "metrics": [{"type": "accuracy", "name": "Accuracy"}],
                },
            ],
            "extra_gated_prompt": (
                "By clicking on “Access repository” below, you also agree to ImageNet Terms of Access:\n"
                '[RESEARCHER_FULLNAME] (the "Researcher") has requested permission to use the ImageNet database '
                '(the "Database") at Princeton University and Stanford University. In exchange for such permission, '
                "Researcher hereby agrees to the following terms and conditions:\n"
                "1. Researcher shall use the Database only for non-commercial research and educational purposes.\n"
            ),
            "extra_gated_fields": {
                "Company": "text",
                "Country": "text",
                "I agree to use this model for non-commerical use ONLY": "checkbox",
            },
        }
        self.assertEqual(sorted(metadata_dict), sorted(expected))
        for key in expected:
            if key == "train_eval_index":
                self.assertEqual(len(metadata_dict[key]), len(expected[key]))
                for tei, expected_tei in zip(metadata_dict[key], expected[key]):
                    for subkey in expected_tei:
                        self.assertEqual(tei[subkey], expected_tei[subkey], msg=f"failed at {subkey}")
            else:
                self.assertEqual(metadata_dict[key], expected[key], msg=f"failed at {key}")
