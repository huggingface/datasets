# Copyright 2021 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from subprocess import check_output
from typing import List

import pytest

from datasets.packaged_modules import _PACKAGED_DATASETS_MODULES
from datasets.utils.logging import get_logger
from datasets.utils.metadata import DatasetMetadata
from datasets.utils.readme import ReadMe

from .utils import slow


repo_path = Path.cwd()

logger = get_logger(__name__)


def get_changed_datasets(repo_path: Path) -> List[Path]:
    diff_output = check_output(["git", "diff", "--name-only", "origin/master...HEAD"], cwd=repo_path)
    changed_files = [Path(repo_path, f) for f in diff_output.decode().splitlines()]

    datasets_dir_path = repo_path / "datasets"

    changed_datasets = {
        f.resolve().relative_to(datasets_dir_path).parts[0]
        for f in changed_files
        if f.exists() and str(f.resolve()).startswith(str(datasets_dir_path)) and not f.name == "dummy_data.zip"
    }

    return sorted(dataset_name for dataset_name in changed_datasets if dataset_name not in _PACKAGED_DATASETS_MODULES)


def get_all_datasets(repo_path: Path) -> List[Path]:
    dataset_names = [path.parts[-1] for path in (repo_path / "datasets").iterdir()]
    return [dataset_name for dataset_name in dataset_names if dataset_name not in _PACKAGED_DATASETS_MODULES]


@pytest.mark.parametrize("dataset_name", get_changed_datasets(repo_path))
def test_changed_dataset_card(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert card_path.exists()
    error_messages = []
    try:
        readme = ReadMe.from_readme(card_path)
    except Exception as readme_parsing_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nREADME Parsing:\n{readme_parsing_error}"
        )
    try:
        readme = ReadMe.from_readme(card_path, suppress_parsing_errors=True)
        readme.validate()
    except Exception as readme_validation_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nREADME Validation:\n{readme_validation_error}"
        )
    try:
        metadata = DatasetMetadata.from_readme(card_path)
        metadata.validate()
    except Exception as metadata_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nYAML tags:\n{metadata_error}"
        )

    if error_messages:
        raise ValueError("\n".join(error_messages))


@slow
@pytest.mark.parametrize("dataset_name", get_all_datasets(repo_path))
def test_dataset_card(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert card_path.exists()
    error_messages = []
    try:
        readme = ReadMe.from_readme(card_path)
    except Exception as readme_parsing_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nREADME Parsing:\n{readme_parsing_error}"
        )
    try:
        readme = ReadMe.from_readme(card_path, suppress_parsing_errors=True)
        readme.validate()
    except Exception as readme_validation_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nREADME Validation:\n{readme_validation_error}"
        )
    try:
        metadata = DatasetMetadata.from_readme(card_path)
        metadata.validate()
    except Exception as metadata_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nYAML tags:\n{metadata_error}"
        )

    if error_messages:
        raise ValueError("\n".join(error_messages))
