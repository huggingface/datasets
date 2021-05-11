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

import os
from pathlib import Path
from subprocess import check_output
from typing import List

from datasets.utils.logging import get_logger

import pytest
from datasets.utils.metadata import DatasetMetadata
from datasets.utils.readme import ReadMe

from .utils import slow

repo_path = Path.cwd()

logger = get_logger(__name__)


def get_changed_datasets(repo_path: Path) -> List[Path]:
    diff_output = check_output(["git", "diff", "--name-only", "HEAD..origin/master"], cwd=repo_path)
    changed_files = [Path(repo_path, f) for f in diff_output.decode().splitlines()]
    changed_datasets_unique = []
    changed_datasets = [f.parent.parts[-1] for f in changed_files if f.exists() and f.parent.parent.name == "datasets" and f.parent.parent.parent.name == "datasets"]

    for dataset_name in changed_datasets:
        if dataset_name not in changed_datasets_unique:
            changed_datasets_unique.append(dataset_name)

    return changed_datasets_unique


def get_all_datasets(repo_path: Path) -> List[Path]:
    return [x.parts[-1] for x in (repo_path / "datasets").iterdir()]


@slow
@pytest.mark.parametrize("dataset_name", get_all_datasets(repo_path))
def test_dataset_tags(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert os.path.exists(card_path)
    DatasetMetadata.from_readme(card_path)


@pytest.mark.parametrize("dataset_name", get_changed_datasets(repo_path))
def test_changed_dataset_tags(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert os.path.exists(card_path)
    DatasetMetadata.from_readme(card_path)


@slow
@pytest.mark.parametrize("dataset_name", get_all_datasets(repo_path))
def test_readme_content(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert os.path.exists(card_path)
    ReadMe.from_readme(card_path)


@pytest.mark.parametrize("dataset_name", get_changed_datasets(repo_path))
def test_changed_readme_content(dataset_name):
    card_path = repo_path / "datasets" / dataset_name / "README.md"
    assert os.path.exists(card_path)
    ReadMe.from_readme(card_path)
