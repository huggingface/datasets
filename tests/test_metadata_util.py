import re
import sys
import tempfile
import unittest
from pathlib import Path

import pytest
import yaml
from huggingface_hub import DatasetCard, DatasetCardData

from datasets.config import METADATA_CONFIGS_FIELD
from datasets.utils.metadata import MetadataConfigs


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


README_METADATA_CONFIG_INCORRECT_FORMAT = f"""\
---
{METADATA_CONFIGS_FIELD}:
  data_dir: v1
  drop_labels: true
---
"""


README_METADATA_SINGLE_CONFIG = f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: custom
    data_dir: v1
    drop_labels: true
---
"""


README_METADATA_TWO_CONFIGS_WITH_DEFAULT_FLAG = f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: v1
    data_dir: v1
    drop_labels: true
  - config_name: v2
    data_dir: v2
    drop_labels: false
    default: true
---
"""


README_METADATA_TWO_CONFIGS_WITH_DEFAULT_NAME = f"""\
---
{METADATA_CONFIGS_FIELD}:
  - config_name: custom
    data_dir: custom
    drop_labels: true
  - config_name: default
    data_dir: data
    drop_labels: false
---
"""


EXPECTED_METADATA_SINGLE_CONFIG = {"custom": {"data_dir": "v1", "drop_labels": True}}
EXPECTED_METADATA_TWO_CONFIGS_DEFAULT_FLAG = {
    "v1": {"data_dir": "v1", "drop_labels": True},
    "v2": {"data_dir": "v2", "drop_labels": False, "default": True},
}
EXPECTED_METADATA_TWO_CONFIGS_DEFAULT_NAME = {
    "custom": {"data_dir": "custom", "drop_labels": True},
    "default": {"data_dir": "data", "drop_labels": False},
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
            dataset_card_data = DatasetCard.load(path).data
            self.assertDictEqual(
                dataset_card_data.to_dict(), {"language": ["zh", "en"], "task_ids": ["sentiment-classification"]}
            )

            with open(path, "w+") as readme_file:
                readme_file.write(README_EMPTY_YAML)
            if (
                sys.platform != "win32"
            ):  # there is a bug on windows, see https://github.com/huggingface/huggingface_hub/issues/1546
                dataset_card_data = DatasetCard.load(path).data
                self.assertDictEqual(dataset_card_data.to_dict(), {})

            with open(path, "w+") as readme_file:
                readme_file.write(README_NO_YAML)
            dataset_card_data = DatasetCard.load(path).data
            self.assertEqual(dataset_card_data.to_dict(), {})

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
        assert DatasetCardData(**yaml.safe_load(valid_yaml_string)).to_dict()

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
        assert DatasetCardData(**yaml.safe_load(valid_yaml_with_optional_keys)).to_dict()


@pytest.mark.parametrize(
    "readme_content, expected_metadata_configs_dict, expected_default_config_name",
    [
        (README_METADATA_SINGLE_CONFIG, EXPECTED_METADATA_SINGLE_CONFIG, None),
        (README_METADATA_TWO_CONFIGS_WITH_DEFAULT_FLAG, EXPECTED_METADATA_TWO_CONFIGS_DEFAULT_FLAG, "v2"),
        (README_METADATA_TWO_CONFIGS_WITH_DEFAULT_NAME, EXPECTED_METADATA_TWO_CONFIGS_DEFAULT_NAME, "default"),
    ],
)
def test_metadata_configs_dataset_card_data(
    readme_content, expected_metadata_configs_dict, expected_default_config_name
):
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(readme_content)
        dataset_card_data = DatasetCard.load(path).data
        metadata_configs_dict = MetadataConfigs.from_dataset_card_data(dataset_card_data)
        assert metadata_configs_dict == expected_metadata_configs_dict
        assert metadata_configs_dict.get_default_config_name() == expected_default_config_name


def test_metadata_configs_incorrect_yaml():
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = Path(tmp_dir) / "README.md"
        with open(path, "w+") as readme_file:
            readme_file.write(README_METADATA_CONFIG_INCORRECT_FORMAT)
        dataset_card_data = DatasetCard.load(path).data
        with pytest.raises(ValueError):
            _ = MetadataConfigs.from_dataset_card_data(dataset_card_data)
