from textwrap import dedent
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import quote

import pytest
from huggingface_hub import CommitOperationAdd, CommitOperationDelete
from packaging import version

import datasets
from datasets.config import METADATA_CONFIGS_FIELD, PYARROW_VERSION
from datasets.hub import convert_to_parquet, delete_from_hub
from datasets.utils.hub import hf_dataset_url


DUMMY_DATASET_SCRIPT = dedent("""\
import datasets


class NewDataset(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="first"),
        datasets.BuilderConfig(name="second"),
    ]
    DEFAULT_CONFIG_NAME = "first"

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features({"text": datasets.Value("string")}),
        )

    def _split_generators(self, dl_manager):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN)]

    def _generate_examples(self):
        for key in range(5):
            yield key, {"text": f"{self.config.name}-{key}"}
""")


@pytest.mark.parametrize("repo_id", ["canonical_dataset_name", "org-name/dataset-name"])
@pytest.mark.parametrize("filename", ["filename.csv", "filename with blanks.csv"])
@pytest.mark.parametrize("revision", [None, "v2"])
def test_dataset_url(repo_id, filename, revision):
    url = hf_dataset_url(repo_id=repo_id, filename=filename, revision=revision)
    assert url == f"https://huggingface.co/datasets/{repo_id}/resolve/{revision or 'main'}/{quote(filename)}"


def test_convert_to_parquet(temporary_repo, hf_api, hf_token, ci_hub_config, ci_hfh_hf_hub_url):
    with temporary_repo() as repo_id:
        hf_api.create_repo(repo_id, token=hf_token, repo_type="dataset")
        hf_api.upload_file(
            token=hf_token,
            path_or_fileobj=DUMMY_DATASET_SCRIPT.encode(),
            path_in_repo=f"{repo_id.split('/')[-1]}.py",
            repo_id=repo_id,
            repo_type="dataset",
        )
        commit_info = SimpleNamespace(
            pr_revision="refs/pr/1",  # "main", #
            pr_url="https:///hub-ci.huggingface.co/datasets/__DUMMY_USER__/__DUMMY_DATASET__/refs%2Fpr%2F1",
        )
        with patch.object(datasets.hub.HfApi, "create_commit", return_value=commit_info) as mock_create_commit:
            with patch.object(datasets.hub.HfApi, "create_branch") as mock_create_branch:
                with patch.object(datasets.hub.HfApi, "list_repo_tree", return_value=[]):  # not needed
                    with patch.object(datasets.hub.HfApi, "preupload_lfs_files", return_value=None):  # not needed
                        _ = convert_to_parquet(repo_id, token=hf_token, trust_remote_code=True)
    # mock_create_branch
    assert mock_create_branch.called
    assert mock_create_branch.call_count == 1
    assert mock_create_branch.call_args.kwargs.get("branch") == "script"
    # mock_create_commit
    assert mock_create_commit.called
    assert mock_create_commit.call_count == 2
    expected_readmes = [
        dedent(f"""\
        ---
        dataset_info:
          config_name: first
          features:
          - name: text
            dtype: string
          splits:
          - name: train
            num_bytes: 55
            num_examples: 5
          download_size: 725
          dataset_size: 55
        {METADATA_CONFIGS_FIELD}:
        - config_name: first
          data_files:
          - split: train
            path: first/train-*
          default: true
        ---
        """),
        dedent(f"""\
        ---
        dataset_info:
          config_name: second
          features:
          - name: text
            dtype: string
          splits:
          - name: train
            num_bytes: 60
            num_examples: 5
          download_size: 731
          dataset_size: 60
        {METADATA_CONFIGS_FIELD}:
        - config_name: second
          data_files:
          - split: train
            path: second/train-*
        ---
        """),
    ]
    if PYARROW_VERSION < version.parse("20.0.0"):
        expected_readmes[0] = expected_readmes[0].replace("download_size: 725", "download_size: 717")
        expected_readmes[1] = expected_readmes[1].replace("download_size: 731", "download_size: 723")
    if PYARROW_VERSION < version.parse("18.1.0"):
        expected_readmes[0] = expected_readmes[0].replace("download_size: 717", "download_size: 726")
        expected_readmes[1] = expected_readmes[1].replace("download_size: 723", "download_size: 732")
    if PYARROW_VERSION < version.parse("18.0.0"):
        expected_readmes[0] = expected_readmes[0].replace("download_size: 726", "download_size: 790")
        expected_readmes[1] = expected_readmes[1].replace("download_size: 732", "download_size: 798")
    for call_args, expected_commit_message, expected_create_pr, expected_readme, expected_parquet_path_in_repo in zip(
        mock_create_commit.call_args_list,
        ["Convert dataset to Parquet", "Add 'second' config data files"],
        [True, False],
        expected_readmes,
        ["first/train-00000-of-00001.parquet", "second/train-00000-of-00001.parquet"],
    ):
        assert call_args.kwargs.get("commit_message") == expected_commit_message
        assert call_args.kwargs.get("create_pr") is expected_create_pr
        operations = call_args.kwargs.get("operations")
        assert len(operations) == 2
        for operation in operations:
            if operation.path_in_repo == "README.md":
                assert operation.path_or_fileobj.decode() == expected_readme
            else:
                assert operation.path_in_repo == expected_parquet_path_in_repo


def test_delete_from_hub(temporary_repo, hf_api, hf_token, csv_path, ci_hub_config, ci_hfh_hf_hub_url) -> None:
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
            path_or_fileobj=dedent(f"""\
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
            """).encode(),
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
    expected_operations = [
        CommitOperationDelete(path_in_repo="dogs/train/0000.csv", is_folder=False),
        CommitOperationAdd(
            path_in_repo="README.md",
            path_or_fileobj=dedent(f"""\
            ---
            {METADATA_CONFIGS_FIELD}:
            - config_name: cats
              data_files:
              - split: train
                path: cats/train/*
            ---
            """).encode(),
        ),
    ]
    assert mock_method.call_args.kwargs.get("operations") == expected_operations
