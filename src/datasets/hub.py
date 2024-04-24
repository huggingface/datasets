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
    revision: Optional[str] = None,
    token: Optional[Union[bool, str]] = None,
) -> CommitInfo:
    operations = []
    # data_files
    fs = HfFileSystem(endpoint=config.HF_ENDPOINT, token=token)
    builder = load_dataset_builder(repo_id, config_name, revision=revision, token=token, trust_remote_code=False)
    for data_file in chain(*builder.config.data_files.values()):
        operations.append(CommitOperationDelete(path_in_repo=fs.resolve_path(data_file).path_in_repo))
    # README.md
    dataset_card = DatasetCard.load(repo_id)
    # config_names
    if dataset_card.data.get("config_names", None) and config_name in dataset_card.data["config_names"]:
        dataset_card.data["config_names"].remove(config_name)
    # metadata_configs
    metadata_configs = MetadataConfigs.from_dataset_card_data(dataset_card.data)
    if metadata_configs:
        _ = metadata_configs.pop(config_name, None)
        dataset_card_data = DatasetCardData()
        metadata_configs.to_dataset_card_data(dataset_card_data)
        if config.METADATA_CONFIGS_FIELD in dataset_card_data:
            dataset_card.data[config.METADATA_CONFIGS_FIELD] = dataset_card_data[config.METADATA_CONFIGS_FIELD]
        else:
            _ = dataset_card.data.pop(config.METADATA_CONFIGS_FIELD, None)
    # dataset_info
    dataset_infos: DatasetInfosDict = DatasetInfosDict.from_dataset_card_data(dataset_card.data)
    if dataset_infos:
        _ = dataset_infos.pop(config_name, None)
        dataset_card_data = DatasetCardData()
        dataset_infos.to_dataset_card_data(dataset_card_data)
        if "dataset_info" in dataset_card_data:
            dataset_card.data["dataset_info"] = dataset_card_data["dataset_info"]
        else:
            _ = dataset_card.data.pop("dataset_info", None)
    # Commit
    operations.append(
        CommitOperationAdd(path_in_repo=config.REPOCARD_FILENAME, path_or_fileobj=str(dataset_card).encode())
    )
    api = HfApi(endpoint=config.HF_ENDPOINT, token=token)
    commit_info = api.create_commit(
        repo_id,
        operations=operations,
        commit_message=f"Delete '{config_name}' config",
        commit_description=f"Delete '{config_name}' config.",
        token=token,
        repo_type="dataset",
        revision=revision,
        create_pr=True,
    )
    print(f"You can find your PR to delete the dataset config at: {commit_info.pr_url}")
    return commit_info
