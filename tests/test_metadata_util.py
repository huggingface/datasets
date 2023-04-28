import re
import tempfile
import unittest
from pathlib import Path

import pytest
from huggingface_hub import HfApi

from datasets.config import HF_ENDPOINT, METADATA_CONFIGS_FIELD
from datasets.data_files import DataFilesDict
from datasets.utils.metadata import DatasetMetadata, MetadataConfigs

from .test_load import SAMPLE_DATASET_TWO_CONFIG_IN_METADATA


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


README_METADATA_CONFIG_DEFAULT = f"""\
---
{METADATA_CONFIGS_FIELD}:
  data_dir: v1
  drop_labels: true
---
"""

README_METADATA_CONFIG_NONDEFAULT = f"""\
---
{METADATA_CONFIGS_FIELD}:
  config_name: custom
  data_dir: v1
  drop_labels: true
---
"""


README_METADATA_CONFIGS = f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: v1
    data_dir: v1
    drop_labels: true
  - config_name: v2
    data_dir: v2
    drop_labels: false
---
"""

EXPECTED_METADATA_CONFIG_DEFAULT = {"default": {"data_dir": "v1", "drop_labels": True}}
EXPECTED_METADATA_CONFIG_NONDEFAULT = {"custom": {"data_dir": "v1", "drop_labels": True}}
EXPECTED_METADATA_CONFIGS = {
    "v1": {"data_dir": "v1", "drop_labels": True},
    "v2": {"data_dir": "v2", "drop_labels": False},
}


@pytest.fixture
def data_dir_with_two_subdirs(tmp_path):
    data_dir = tmp_path / "data_dir_with_two_configs_in_metadata"
    cats_data_dir = data_dir / "cats"
    cats_data_dir.mkdir(parents=True)
    dogs_data_dir = data_dir / "dogs"
    dogs_data_dir.mkdir(parents=True)

    with open(cats_data_dir / "cat.jpg", "wb") as f:
        f.write(b"this_is_a_cat_image_bytes")
    with open(dogs_data_dir / "dog.jpg", "wb") as f:
        f.write(b"this_is_a_dog_image_bytes")

    return str(data_dir)


class TestMetadataUtils(unittest.TestCase):
    def test_metadata_dict_from_readme(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"
            with open(path, "w+") as readme_file:
                readme_file.write(README_YAML)
            metadata_dict = DatasetMetadata.from_readme(path)
            self.assertDictEqual(metadata_dict, {"language": ["zh", "en"], "task_ids": ["sentiment-classification"]})

            with open(path, "w+") as readme_file:
                readme_file.write(README_EMPTY_YAML)
            metadata_dict = DatasetMetadata.from_readme(path)
            self.assertDictEqual(metadata_dict, {})

            with open(path, "w+") as readme_file:
                readme_file.write(README_NO_YAML)
            metadata_dict = DatasetMetadata.from_readme(path)
            self.assertEqual(metadata_dict, {})

    def test_from_yaml_string(self):
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
        assert DatasetMetadata.from_yaml_string(valid_yaml_string)

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
            DatasetMetadata.from_yaml_string(duplicate_yaml_keys)

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
        assert DatasetMetadata.from_yaml_string(valid_yaml_with_optional_keys)

    def test_metadata_configs_dict_from_metadata_one_default_config(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"
            with open(path, "w+") as readme_file:
                readme_file.write(README_METADATA_CONFIG_DEFAULT)
            metadata_dict = DatasetMetadata.from_readme(path)
            metadata_configs_dict = MetadataConfigs.from_metadata(metadata_dict)
            self.assertDictEqual(metadata_configs_dict, {"default": {"data_dir": "v1", "drop_labels": True}})

    def test_metadata_configs_dict_from_metadata_one_nondefault_config(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"
            with open(path, "w+") as readme_file:
                readme_file.write(README_METADATA_CONFIG_NONDEFAULT)
            metadata_dict = DatasetMetadata.from_readme(path)
            metadata_configs_dict = MetadataConfigs.from_metadata(metadata_dict)
            self.assertDictEqual(metadata_configs_dict, {"custom": {"data_dir": "v1", "drop_labels": True}})

    def test_metadata_configs_dict_from_metadata_two_configs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "README.md"
            with open(path, "w+") as readme_file:
                readme_file.write(README_METADATA_CONFIGS)
            metadata_dict = DatasetMetadata.from_readme(path)
            metadata_configs_dict = MetadataConfigs.from_metadata(metadata_dict)
            self.assertDictEqual(
                metadata_configs_dict,
                {
                    "v1": {"data_dir": "v1", "drop_labels": True},
                    "v2": {"data_dir": "v2", "drop_labels": False},
                },
            )


@pytest.mark.parametrize(
    "readme_content, expected_metadata_configs_dict",
    [
        (README_METADATA_CONFIG_DEFAULT, EXPECTED_METADATA_CONFIG_DEFAULT),
        (README_METADATA_CONFIG_NONDEFAULT, EXPECTED_METADATA_CONFIG_NONDEFAULT),
        (README_METADATA_CONFIGS, EXPECTED_METADATA_CONFIGS),
    ],
)
def test_metadata_configs_from_metadata(readme_content, expected_metadata_configs_dict):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_content)
        metadata_dict = DatasetMetadata.from_readme(path)
        metadata_configs_dict = MetadataConfigs.from_metadata(metadata_dict)
        assert metadata_configs_dict == expected_metadata_configs_dict


def test_metadata_configs_resolve_data_files_locally(data_dir_with_two_subdirs):
    metadata_configs_dict = MetadataConfigs(
        {
            "cats": {"data_dir": "cats"},
            "dogs": {"data_dir": "dogs"},
        }
    )
    for config_name in metadata_configs_dict:
        config_data_files = metadata_configs_dict.resolve_data_files_locally(
            config_name, base_path=data_dir_with_two_subdirs, with_metadata_files=False, allowed_extensions=["jpg"]
        )
        assert isinstance(config_data_files, DataFilesDict)
        assert len(config_data_files) == 1  # there is a single split
        assert len(config_data_files["train"]) == 1
        if config_name == "cats":
            assert config_data_files["train"][0].name == "cat.jpg"
        else:
            assert config_data_files["train"][0].name == "dog.jpg"


@pytest.mark.parametrize("config_name, expected_train_samples, expected_test_samples", [("v1", 3, 3), ("v2", 2, 1)])
def test_metadata_configs_resolve_data_files_in_dataset_repository(
    config_name, expected_train_samples, expected_test_samples
):
    metadata_configs_dict = MetadataConfigs(
        {
            "v1": {"data_dir": "v1"},
            "v2": {"data_dir": "v2"},
        }
    )
    hfh_dataset_info = HfApi(HF_ENDPOINT).dataset_info(
        SAMPLE_DATASET_TWO_CONFIG_IN_METADATA,
        timeout=100.0,
    )
    config_data_files = metadata_configs_dict.resolve_data_files_in_dataset_repository(
        config_name, hfh_dataset_info, base_path="", with_metadata_files=False, allowed_extensions=["flac"]
    )
    assert isinstance(config_data_files, DataFilesDict)
    assert len(config_data_files["train"]) == expected_train_samples
    assert len(config_data_files["test"]) == expected_test_samples
    assert all(
        data_file.split("/")[-3] == config_name for data_file in config_data_files["train"] + config_data_files["test"]
    )


# TODO
README_YAML_WITH_CONFIG = """\
---
language:
- zh
- en
task_ids:
- sentiment-classification
configs_kwargs:
  config_name: custom
  data_dir: v1
  drop_labels: true
---
# Begin of markdown

Some cool dataset card
"""
