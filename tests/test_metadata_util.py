import re
import tempfile
import unittest
from dataclasses import asdict
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
            languages:
              en:
              - en
              fr:
              - fr
            licenses:
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
            languages:
            - en
            licenses:
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
            languages:
            - en
            licenses:
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
            languages:
            - en
            licenses:
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
            languages:
              en:
              - en
              en:
              - en
            licenses:
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
            languages:
            - en
            licenses:
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
            languages:
            - en
            licenses:
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
            languages:
            - en
            licenses:
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

    def test_get_metadata_by_config_name(self):
        valid_yaml_with_multiple_configs = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            languages:
              en:
              - en
              fr:
              - fr
            licenses:
            - unknown
            multilinguality:
            - monolingual
            pretty_name:
              en: English Test Dataset
              fr: French Test Dataset
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

        metadata = DatasetMetadata.from_yaml_string(valid_yaml_with_multiple_configs)
        en_metadata = metadata.get_metadata_by_config_name("en")
        self.assertEqual(
            asdict(en_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["en"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "English Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )
        fr_metadata = metadata.get_metadata_by_config_name("fr")
        self.assertEqual(
            asdict(fr_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["fr"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "French Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )

        valid_yaml_with_single_configs = _dedent(
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

        metadata = DatasetMetadata.from_yaml_string(valid_yaml_with_single_configs)
        en_metadata = metadata.get_metadata_by_config_name("en")
        self.assertEqual(
            asdict(en_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["en"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )
        fr_metadata = metadata.get_metadata_by_config_name("fr")
        self.assertEqual(
            asdict(fr_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["en"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )

        invalid_yaml_with_multiple_configs = _dedent(
            """\
            annotations_creators:
            - found
            language_creators:
            - found
            languages:
              en:
              - en
              zh:
              - zh
            licenses:
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

        metadata = DatasetMetadata.from_yaml_string(invalid_yaml_with_multiple_configs)
        en_metadata = metadata.get_metadata_by_config_name("en")
        self.assertEqual(
            asdict(en_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["en"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )
        zh_metadata = metadata.get_metadata_by_config_name("zh")
        self.assertEqual(
            asdict(zh_metadata),
            {
                "annotations_creators": ["found"],
                "language_creators": ["found"],
                "languages": ["zh"],
                "licenses": ["unknown"],
                "multilinguality": ["monolingual"],
                "pretty_name": "Test Dataset",
                "size_categories": ["10K<n<100K"],
                "source_datasets": ["extended|other-yahoo-webscope-l6"],
                "task_categories": ["question-answering"],
                "task_ids": ["open-domain-qa"],
                "paperswithcode_id": ["squad"],
            },
        )
        with self.assertRaises(TypeError):
            fr_metadata = metadata.get_metadata_by_config_name("fr")
