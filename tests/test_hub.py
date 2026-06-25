from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import quote

import pytest
from huggingface_hub import CommitOperationAdd, CommitOperationDelete

import datasets
from datasets.config import METADATA_CONFIGS_FIELD
from datasets.hub import delete_from_hub
from datasets.utils.hub import hf_dataset_url


@pytest.mark.parametrize("repo_id", ["canonical_dataset_name", "org-name/dataset-name"])
@pytest.mark.parametrize("filename", ["filename.csv", "filename with blanks.csv"])
@pytest.mark.parametrize("revision", [None, "v2"])
def test_dataset_url(repo_id, filename, revision):
    url = hf_dataset_url(repo_id=repo_id, filename=filename, revision=revision)
    assert url == f"https://huggingface.co/datasets/{repo_id}/resolve/{revision or 'main'}/{quote(filename)}"


def test_delete_from_hub(temporary_repo, hf_api, hf_token, csv_path, ci_hub_config) -> None:
    with temporary_repo() as repo_id:
        hf_api.create_repo(repo_id, token=hf_token, repo_type="dataset")
        hf_api.upload_file(
            path_or_fileobj=str(csv_path),
            path_in_repo="cats/train/0000.csv",
            repo_id=repo_id,
            repo_type="dataset",
            token=hf_token,
        )
        hf_api.upload_file(
            path_or_fileobj=str(csv_path),
            path_in_repo="dogs/train/0000.csv",
            repo_id=repo_id,
            repo_type="dataset",
            token=hf_token,
        )
        hf_api.upload_file(
            token=hf_token,
            path_or_fileobj=dedent(
                f"""\
            ---
            {METADATA_CONFIGS_FIELD}:
            - config_name: cats
              data_files:
              - split: train
                path: cats/train/*
            - config_name: dogs
              data_files:
              - split: train
                path: dogs/train/*
            ---
            """
            ).encode(),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="dataset",
        )
        commit_info = SimpleNamespace(
            pr_url="https:///hub-ci.huggingface.co/datasets/__DUMMY_USER__/__DUMMY_DATASET__/refs%2Fpr%2F1"
        )
        with patch.object(datasets.hub.HfApi, "create_commit", return_value=commit_info) as mock_method:
            _ = delete_from_hub(repo_id, "dogs")
    assert mock_method.called
    assert mock_method.call_args.kwargs.get("commit_message") == "Delete 'dogs' config"
    assert mock_method.call_args.kwargs.get("create_pr")
    expected_readme = dedent(
        f"""\
        ---
        {METADATA_CONFIGS_FIELD}:
        - config_name: cats
          data_files:
          - split: train
            path: cats/train/*
        ---
        """
    ).encode()
    # Note: we compare operations attribute by attribute rather than relying on `==`. Since
    # huggingface_hub 1.20.0 (https://github.com/huggingface/huggingface_hub/pull/4331),
    # `CommitOperationAdd`/`CommitOperationDelete` no longer implement value equality, so two
    # operations with identical content are not considered equal.
    operations = mock_method.call_args.kwargs.get("operations")
    assert len(operations) == 2
    delete_operation, add_operation = operations
    assert isinstance(delete_operation, CommitOperationDelete)
    assert delete_operation.path_in_repo == "dogs/train/0000.csv"
    assert delete_operation.is_folder is False
    assert isinstance(add_operation, CommitOperationAdd)
    assert add_operation.path_in_repo == "README.md"
    assert add_operation.path_or_fileobj == expected_readme
