from itertools import chain
from typing import Optional, Union

from huggingface_hub import (
    CommitInfo,
    CommitOperationAdd,
    CommitOperationDelete,
    DatasetCard,
    DatasetCardData,
    HfApi,
    HfFileSystem,
)

from datasets import config
from datasets.info import DatasetInfosDict
from datasets.load import load_dataset_builder
from datasets.utils.metadata import MetadataConfigs


def delete_from_hub(
    repo_id: str,
    config_name: Optional[str] = None,
    commit_message: Optional[str] = None,
    commit_description: Optional[str] = None,
    create_pr: Optional[bool] = False,
    revision: Optional[str] = None,
    token: Optional[Union[bool, str]] = None,
) -> CommitInfo:
    operations = []
    # data_files
    fs = HfFileSystem(endpoint=config.HF_ENDPOINT, token=token)
    builder = load_dataset_builder(repo_id, config_name, revision=revision, token=token)
    for data_file in chain(*builder.config.data_files.values()):
        operations.append(CommitOperationDelete(path_in_repo=fs.resolve_path(data_file).path_in_repo))
    # README.md
    dataset_card = DatasetCard.load(repo_id)
    # config_names
    if "config_names" in dataset_card.data and config_name in dataset_card.data["config_names"]:
        dataset_card.data["config_names"].remove(config_name)
    # metadata_configs
    metadata_configs = MetadataConfigs.from_dataset_card_data(dataset_card.data)
    if metadata_configs:
        _ = metadata_configs.pop(config_name, None)
        dataset_card_data = DatasetCardData()
        metadata_configs.to_dataset_card_data(dataset_card_data)
        dataset_card.data[config.METADATA_CONFIGS_FIELD] = dataset_card_data[config.METADATA_CONFIGS_FIELD]
    # dataset_info
    dataset_infos: DatasetInfosDict = DatasetInfosDict.from_dataset_card_data(dataset_card.data)
    if dataset_infos:
        _ = dataset_infos.pop(config_name, None)
        dataset_card_data = DatasetCardData()
        dataset_infos.to_dataset_card_data(dataset_card_data)
        dataset_card.data["dataset_info"] = dataset_card_data["dataset_info"]
    # Commit
    operations.append(
        CommitOperationAdd(path_in_repo=config.REPOCARD_FILENAME, path_or_fileobj=str(dataset_card).encode())
    )
    commit_message = commit_message if commit_message is not None else "Delete dataset config"
    api = HfApi(endpoint=config.HF_ENDPOINT, token=token)
    commit_info = api.create_commit(
        repo_id,
        operations=operations,
        commit_message=commit_message,
        commit_description=commit_description,
        token=token,
        repo_type="dataset",
        revision=revision,
        create_pr=create_pr,
    )
    return commit_info
