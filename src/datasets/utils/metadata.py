import os
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple, Type, Union

import huggingface_hub
import yaml

from ..config import METADATA_CONFIGS_FIELD
from ..data_files import (
    DEFAULT_PATTERNS_ALL,
    DataFilesDict,
    extend_data_files_with_metadata_files_in_dataset_repository,
    extend_data_files_with_metadata_files_locally,
    get_data_patterns_in_dataset_repository,
    get_data_patterns_locally,
    sanitize_patterns,
)
from ..utils.logging import get_logger


if TYPE_CHECKING:
    from ..builder import BuilderConfig


logger = get_logger(__name__)


class _NoDuplicateSafeLoader(yaml.SafeLoader):
    def _check_no_duplicates_on_constructed_node(self, node):
        keys = [self.constructed_objects[key_node] for key_node, _ in node.value]
        keys = [tuple(key) if isinstance(key, list) else key for key in keys]
        counter = Counter(keys)
        duplicate_keys = [key for key in counter if counter[key] > 1]
        if duplicate_keys:
            raise TypeError(f"Got duplicate yaml keys: {duplicate_keys}")

    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        self._check_no_duplicates_on_constructed_node(node)
        return mapping


def _split_yaml_from_readme(readme_content: str) -> Tuple[Optional[str], str]:
    full_content = list(readme_content.splitlines())
    if full_content and full_content[0] == "---" and "---" in full_content[1:]:
        sep_idx = full_content[1:].index("---") + 1
        yamlblock = "\n".join(full_content[1:sep_idx])
        return yamlblock, "\n".join(full_content[sep_idx + 1 :])

    return None, "\n".join(full_content)


class DatasetMetadata(dict):
    # class attributes
    _FIELDS_WITH_DASHES = {"train_eval_index"}  # train-eval-index in the YAML metadata

    @classmethod
    def from_readme(cls, path: Union[Path, str]) -> "DatasetMetadata":
        """Loads and validates the dataset metadata from its dataset card (README.md)

        Args:
            path (:obj:`Path`): Path to the dataset card (its README.md file)

        Returns:
            :class:`DatasetMetadata`: The dataset's metadata

        Raises:
            :obj:`TypeError`: If the dataset's metadata is invalid
        """
        with open(path, encoding="utf-8") as readme_file:
            yaml_string, _ = _split_yaml_from_readme(readme_file.read())
        if yaml_string is not None:
            return cls.from_yaml_string(yaml_string)
        else:
            return cls()

    def to_readme(self, path: Path):
        if path.exists():
            with open(path, encoding="utf-8") as readme_file:
                readme_content = readme_file.read()
        else:
            readme_content = None
        updated_readme_content = self._to_readme(readme_content)
        with open(path, "w", encoding="utf-8") as readme_file:
            readme_file.write(updated_readme_content)

    def _to_readme(self, readme_content: Optional[str] = None) -> str:
        if readme_content is not None:
            _, content = _split_yaml_from_readme(readme_content)
            full_content = "---\n" + self.to_yaml_string() + "---\n" + content
        else:
            full_content = "---\n" + self.to_yaml_string() + "---\n"
        return full_content

    @classmethod
    def from_yaml_string(cls, string: str) -> "DatasetMetadata":
        """Loads and validates the dataset metadata from a YAML string

        Args:
            string (:obj:`str`): The YAML string

        Returns:
            :class:`DatasetMetadata`: The dataset's metadata

        Raises:
            :obj:`TypeError`: If the dataset's metadata is invalid
        """
        metadata_dict = yaml.load(string, Loader=_NoDuplicateSafeLoader) or {}

        # Convert the YAML keys to DatasetMetadata fields
        metadata_dict = {
            (key.replace("-", "_") if key.replace("-", "_") in cls._FIELDS_WITH_DASHES else key): value
            for key, value in metadata_dict.items()
        }
        return cls(**metadata_dict)

    def to_yaml_string(self) -> str:
        return yaml.safe_dump(
            {
                (key.replace("_", "-") if key in self._FIELDS_WITH_DASHES else key): value
                for key, value in self.items()
            },
            sort_keys=False,
            allow_unicode=True,
            encoding="utf-8",
        ).decode("utf-8")


class MetadataConfigs(Dict[str, Dict[str, Any]]):
    """Should be in format {config_name: {**config_params}}."""

    FIELD_NAME: ClassVar[str] = METADATA_CONFIGS_FIELD

    @staticmethod
    def _raise_if_not_valid(metadata_config: dict):
        if isinstance(metadata_config.get("data_files"), dict):
            raise ValueError(
                f"Expected data_files in YAML to be a string or a list, but got {metadata_config['data_files']}\nExamples:\n"
                "    data_files: data.csv\n    data_files: data/*.png\n"
                "    data_files:\n    - part0/*\n    - part1/*\n"
                "    data_files:\n    - split: train\n      pattern: train/*\n    - split: test\n      pattern: test/*"
            )

    @classmethod
    def from_metadata(cls, dataset_metadata: DatasetMetadata) -> "MetadataConfigs":
        if dataset_metadata.get(cls.__configs_field_name):
            metadata_configs = dataset_metadata[cls.__configs_field_name]
            if isinstance(metadata_configs, dict):  # single configuration
                if "config_name" not in metadata_configs:
                    metadata_configs["config_name"] = "default"
                metadata_configs = [metadata_configs]
            elif not isinstance(metadata_configs, list):
                raise ValueError(
                    f"Expected {cls.__configs_field_name} to be a dict or a list, but got '{metadata_configs}'"
                )
            for metadata_config in metadata_configs:
                cls._raise_if_not_valid(metadata_config)
            return cls(
                {
                    config["config_name"]: {param: value for param, value in config.items() if param != "config_name"}
                    for config in metadata_configs
                }
            )
        return cls()

    def to_metadata(self, dataset_metadata: DatasetMetadata) -> None:
        if self:
            for metadata_config in self.values():
                self._raise_if_not_valid(metadata_config)
            current_metadata_configs = self.from_metadata(dataset_metadata)
            total_metadata_configs = dict(sorted({**current_metadata_configs, **self}.items()))
            if len(total_metadata_configs) > 1:
                for config_name, config_metadata in total_metadata_configs.items():
                    config_metadata.pop("config_name", None)
                dataset_metadata[self.__configs_field_name] = [
                    {"config_name": config_name, **config_metadata}
                    for config_name, config_metadata in total_metadata_configs.items()
                ]
            elif len(total_metadata_configs) == 1:
                metadata_config_name, metadata_config = next(iter(total_metadata_configs.items()))
                metadata_config = (
                    {"config_name": metadata_config_name, **metadata_config}
                    if metadata_config_name != "default"
                    else {**metadata_config}
                )
                dataset_metadata[self.__configs_field_name] = metadata_config

    def get_builder_config(
        self,
        config_name: str,
        builder_config_cls: Type["BuilderConfig"],
        data_files: Optional[DataFilesDict],
        data_dir: Optional[str],
        default_builder_kwargs: Dict[str, Any],
    ) -> "BuilderConfig":
        """Convert configurations parsed from metadata file to list of BuilderConfig objects."""
        meta_config = self[config_name]
        ignored_params = [
            param for param in meta_config if not hasattr(builder_config_cls, param) and param != "default"
        ]
        if ignored_params:
            logger.warning(
                f"Some datasets params were ignored: {ignored_params}. "
                "Make sure to use only valid params for the dataset builder and to have "
                "a up-to-date version of the `datasets` library."
            )
        return builder_config_cls(
            name=config_name,
            data_files=data_files,
            data_dir=data_dir,
            **{
                param: value
                for param, value in {**default_builder_kwargs, **meta_config}.items()
                if hasattr(builder_config_cls, param) and param not in ("default", "data_files", "data_dir")
            },
        )

    def get_default_config_name(self) -> Optional[str]:
        default_config_name = None
        for config_name, metadata_config in self.items():
            if config_name == "default" or metadata_config.get("default"):
                if default_config_name is None:
                    default_config_name = config_name
                else:
                    raise ValueError(
                        f"Dataset has several default configs: '{default_config_name}' and '{config_name}'."
                    )
        return default_config_name

    def resolve_data_files_locally(
        self,
        config_name: str,
        base_path: str,
        with_metadata_files: bool,
        allowed_extensions: List[str],
    ) -> DataFilesDict:
        """
        Find patterns and resolve data files for local datasets for each config in-place (i.e. modifying `self`).
        Drop initial `data_dir` and `data_files` values and set `data_files` to DataFilesDict object with resolved data files.
        """
        metadata_config = self[config_name]
        config_data_files = metadata_config.get("data_files")
        config_data_dir = metadata_config.get("data_dir")
        config_base_path = os.path.join(base_path, config_data_dir) if config_data_dir else base_path
        config_patterns = (
            sanitize_patterns(config_data_files)
            if config_data_files is not None
            else get_data_patterns_locally(config_base_path)
        )
        config_data_files_dict = DataFilesDict.from_local_or_remote(
            config_patterns,
            base_path=config_base_path,
            allowed_extensions=allowed_extensions,
        )
        if config_data_files is None and with_metadata_files and config_patterns != DEFAULT_PATTERNS_ALL:
            extend_data_files_with_metadata_files_locally(config_data_files_dict, base_path=config_base_path)
        return config_data_files_dict

    def resolve_data_files_in_dataset_repository(
        self,
        config_name: str,
        hfh_dataset_info: huggingface_hub.hf_api.DatasetInfo,
        base_path: str,
        with_metadata_files: bool,
        allowed_extensions: List[str],
    ) -> DataFilesDict:
        """
        Find patterns and resolve data files for Hub datasets for each config in-place (i.e. modifying `self`).
        Drop initial `data_dir` and `data_files` values and set `data_files` to DataFilesDict object with resolved data files.
        """
        metadata_config = self[config_name]
        config_data_files = metadata_config.get("data_files")
        config_data_dir = metadata_config.get("data_dir")
        config_base_path = os.path.join(base_path, config_data_dir) if config_data_dir else base_path
        config_patterns = (
            sanitize_patterns(config_data_files)
            if config_data_files is not None
            else get_data_patterns_in_dataset_repository(hfh_dataset_info, config_base_path)
        )
        config_data_files_dict = DataFilesDict.from_hf_repo(
            config_patterns,
            dataset_info=hfh_dataset_info,
            base_path=config_base_path,
            allowed_extensions=allowed_extensions,
        )
        if config_data_files is None and with_metadata_files and config_patterns != DEFAULT_PATTERNS_ALL:
            extend_data_files_with_metadata_files_in_dataset_repository(
                hfh_dataset_info, data_files=config_data_files_dict, base_path=config_base_path
            )
        return config_data_files_dict


# DEPRECATED - just here to support old versions of evaluate like 0.2.2
# To support new tasks on the Hugging Face Hub, please open a PR for this file:
# https://github.com/huggingface/hub-docs/blob/main/js/src/lib/interfaces/Types.ts
known_task_ids = {
    "image-classification": [],
    "translation": [],
    "image-segmentation": [],
    "fill-mask": [],
    "automatic-speech-recognition": [],
    "token-classification": [],
    "sentence-similarity": [],
    "audio-classification": [],
    "question-answering": [],
    "summarization": [],
    "zero-shot-classification": [],
    "table-to-text": [],
    "feature-extraction": [],
    "other": [],
    "multiple-choice": [],
    "text-classification": [],
    "text-to-image": [],
    "text2text-generation": [],
    "zero-shot-image-classification": [],
    "tabular-classification": [],
    "tabular-regression": [],
    "image-to-image": [],
    "tabular-to-text": [],
    "unconditional-image-generation": [],
    "text-retrieval": [],
    "text-to-speech": [],
    "object-detection": [],
    "audio-to-audio": [],
    "text-generation": [],
    "conversational": [],
    "table-question-answering": [],
    "visual-question-answering": [],
    "image-to-text": [],
    "reinforcement-learning": [],
    "voice-activity-detection": [],
    "time-series-forecasting": [],
    "document-question-answering": [],
}


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the yaml metadata block of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()

    readme_filepath = Path(args.readme_filepath)
    dataset_metadata = DatasetMetadata.from_readme(readme_filepath)
    print(dataset_metadata)
    dataset_metadata.to_readme(readme_filepath)
