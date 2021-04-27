import tempfile
import unittest
from pathlib import Path

from datasets.utils.metadata import (
    DatasetMetadata,
    escape_validation_for_predicate,
    metadata_dict_from_readme,
    tagset_validator,
    validate_metadata_type,
    yaml_block_from_readme,
)


def _dedent(string: str) -> str:
    return "\n".join([line.lstrip() for line in string.splitlines()])


README_YAML = """\
---
languages:
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

        values = ["tag1", "tag2", "tag2", "tag3"]
        reference_values = ["tag1", "tag2", "tag3"]
        returned_values, error = tagset_validator(values=values, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, values)
        self.assertIsNone(error)

        values = []
        reference_values = ["tag1", "tag2", "tag3"]
        returned_values, error = tagset_validator(values=values, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, values)
        self.assertIsNone(error)

        values = []
        reference_values = []
        returned_values, error = tagset_validator(values=values, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, values)
        self.assertIsNone(error)

        values = ["tag1", "tag2", "tag2", "tag3", "unknown tag"]
        reference_values = ["tag1", "tag2", "tag3"]
        returned_values, error = tagset_validator(values=values, reference_values=reference_values, name=name, url=url)
        self.assertListEqual(returned_values, [])
        self.assertEqual(error, f"{['unknown tag']} are not registered tags for '{name}', reference at {url}")

    def test_escape_validation_for_predicate(self):
        def predicate_fn(string: str) -> bool:
            return "ignore" in string

        values = ["process me", "process me too", "ignore me"]
        to_ignore, to_validate = escape_validation_for_predicate(values=values, predicate_fn=predicate_fn)
        self.assertListEqual(to_ignore, ["ignore me"])
        self.assertListEqual(to_validate, ["process me", "process me too"])

        values = ["process me", "process me too"]
        to_ignore, to_validate = escape_validation_for_predicate(values=values, predicate_fn=predicate_fn)
        self.assertListEqual(to_ignore, [])
        self.assertListEqual(to_validate, values)

        values = ["this value will be ignored", "ignore this one two"]
        to_ignore, to_validate = escape_validation_for_predicate(values=values, predicate_fn=predicate_fn)
        self.assertListEqual(to_ignore, values)
        self.assertListEqual(to_validate, [])

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
                    languages:
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
            self.assertDictEqual(metadata_dict, {"languages": ["zh", "en"], "task_ids": ["sentiment-classification"]})

            with open(path, "w+") as readme_file:
                readme_file.write(README_EMPTY_YAML)
            metadata_dict = metadata_dict_from_readme(path)
            self.assertDictEqual(metadata_dict, {})

            with open(path, "w+") as readme_file:
                readme_file.write(README_NO_YAML)
            metadata_dict = metadata_dict_from_readme(path)
            self.assertIsNone(metadata_dict)

    def test_from_yaml_string(self):
        valid_yaml_string = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            languages:
            - en
            licenses:
            - unknown
            multilinguality:
            - monolingual
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

        invalid_tag_yaml = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - some guys in Panama
            languages:
            - en
            licenses:
            - unknown
            multilinguality:
            - monolingual
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
            DatasetMetadata.from_yaml_string(invalid_tag_yaml)

        missing_tag_yaml = _dedent(
            """\
            annotations_creators:
            - found
            languages:
            - en
            licenses:
            - unknown
            multilinguality:
            - monolingual
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
            DatasetMetadata.from_yaml_string(missing_tag_yaml)
