from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import quote

import pytest
from huggingface_hub import CommitOperationAdd, CommitOperationDelete

import datasets
from datasets.config import METADATA_CONFIGS_FIELD
from datasets.hub import _delete_files, delete_from_hub
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


def test_delete_from_hub_respects_revision_token_and_endpoint(tmp_path, monkeypatch) -> None:
    custom_endpoint = "https://custom-hub.example.org"
    monkeypatch.setattr(datasets.config, "HF_ENDPOINT", custom_endpoint)

    readme_path = tmp_path / "README.md"
    readme_path.write_text(
        dedent(
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
            Revision-specific body.
            """
        ),
        encoding="utf-8",
    )

    fake_builder = SimpleNamespace(
        config=SimpleNamespace(data_files={"train": ["hf://datasets/org/ds@dev/dogs/train/0000.csv"]})
    )
    fake_resolved = SimpleNamespace(repo_id="org/ds", path_in_repo="dogs/train/0000.csv")
    commit_info = SimpleNamespace(pr_url="https://custom-hub.example.org/datasets/org/ds/discussions/1")

    download_calls = []

    def fake_hf_hub_download(self, repo_id, filename, **kwargs):
        download_calls.append(
            {
                "endpoint": self.endpoint,
                "token": self.token,
                "repo_id": repo_id,
                "filename": filename,
                "kwargs": kwargs,
            }
        )
        return str(readme_path)

    with (
        patch("datasets.hub.HfFileSystem") as mock_fs_cls,
        patch("datasets.hub.load_dataset_builder", return_value=fake_builder),
        patch.object(datasets.hub.HfApi, "hf_hub_download", fake_hf_hub_download),
        patch.object(datasets.hub.HfApi, "create_commit", return_value=commit_info) as mock_commit,
    ):
        mock_fs_cls.return_value.resolve_path.return_value = fake_resolved
        result = delete_from_hub("org/ds", "dogs", revision="dev", token="hf_secret_token")

    assert result is commit_info
    assert len(download_calls) == 1
    assert download_calls[0] == {
        "endpoint": custom_endpoint,
        "token": "hf_secret_token",
        "repo_id": "org/ds",
        "filename": "README.md",
        "kwargs": {"repo_type": "dataset", "revision": "dev"},
    }
    assert mock_commit.call_args.kwargs["revision"] == "dev"
    assert mock_commit.call_args.kwargs["token"] == "hf_secret_token"
    operations = mock_commit.call_args.kwargs["operations"]
    assert len(operations) == 2
    delete_operation, add_operation = operations
    assert isinstance(delete_operation, CommitOperationDelete)
    assert delete_operation.path_in_repo == "dogs/train/0000.csv"
    assert isinstance(add_operation, CommitOperationAdd)
    assert add_operation.path_in_repo == "README.md"
    assert b"Revision-specific body." in add_operation.path_or_fileobj
    assert b"config_name: cats" in add_operation.path_or_fileobj
    assert b"config_name: dogs" not in add_operation.path_or_fileobj


def test_delete_files_passes_revision_to_list_repo_files() -> None:
    with (
        patch.object(
            datasets.hub.HfApi, "list_repo_files", return_value=["README.md", "dataset_infos.json", "train/0.parquet"]
        ) as mock_list,
        patch.object(datasets.hub.HfApi, "delete_file") as mock_delete,
    ):
        _delete_files("org/ds", revision="dev", token="hf_secret_token")

    mock_list.assert_called_once_with("org/ds", repo_type="dataset", revision="dev")
    assert mock_delete.call_count == 2
    for call in mock_delete.call_args_list:
        assert call.kwargs["revision"] == "dev"
