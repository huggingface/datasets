from collections import Counter
from pathlib import Path
from typing import Optional, Tuple

import yaml


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
    def from_readme(cls, path: Path) -> "DatasetMetadata":
        """Loads and validates the dataset metadat from its dataset card (README.md)

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
