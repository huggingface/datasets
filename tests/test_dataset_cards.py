# coding=utf-8
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

from datasets.utils.logging import get_logger
from datasets.utils.metadata import DatasetMetadata
from datasets.utils.readme import ReadMe

from .utils import slow


repo_path = Path.cwd()

logger = get_logger(__name__)


def get_changed_datasets(repo_path: Path) -> List[Path]:
    diff_output = check_output(["git", "diff", "--name-only", "HEAD..origin/master"], cwd=repo_path)
    changed_files = [Path(repo_path, f) for f in diff_output.decode().splitlines()]

    datasets_dir_path = repo_path / "datasets"

    changed_datasets = set(
        f.parent.name for f in changed_files if f.exists() and str(f.resolve()).startswith(str(datasets_dir_path))
    )

    return sorted(changed_datasets)


def get_all_datasets(repo_path: Path) -> List[Path]:
    return [path.parts[-1] for path in (repo_path / "datasets").iterdir()]


@pytest.mark.parametrize("dataset_name", get_changed_datasets(repo_path))
def test_changed_dataset_card(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert card_path.exists()
    error_messages = []
    try:
        ReadMe.from_readme(card_path)
    except Exception as readme_error:
        error_messages.append(f"The following issues have been found in the dataset cards:\nREADME:\n{readme_error}")
    try:
        DatasetMetadata.from_readme(card_path)
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
        ReadMe.from_readme(card_path)
    except Exception as readme_error:
        error_messages.append(f"The following issues have been found in the dataset cards:\nREADME:\n{readme_error}")
    try:
        DatasetMetadata.from_readme(card_path)
    except Exception as metadata_error:
        error_messages.append(
            f"The following issues have been found in the dataset cards:\nYAML tags:\n{metadata_error}"
        )

    if error_messages:
        raise ValueError("\n".join(error_messages))
