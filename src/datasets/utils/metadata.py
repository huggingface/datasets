import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# loading package files: https://stackoverflow.com/a/20885799
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import yaml

from . import resources


BASE_REF_URL = "https://github.com/huggingface/datasets/tree/master/src/datasets/utils"
this_url = f"{BASE_REF_URL}/{__file__}"
logger = logging.getLogger(__name__)


def load_json_resource(resource: str) -> Tuple[Any, str]:
    content = pkg_resources.read_text(resources, resource)
    return json.loads(content), f"{BASE_REF_URL}/resources/{resource}"


# Source of languages.json:
# https://datahub.io/core/language-codes/r/ietf-language-tags.csv
# Language names were obtained with langcodes: https://github.com/LuminosoInsight/langcodes
known_language_codes, known_language_codes_url = load_json_resource("languages.json")
known_licenses, known_licenses_url = load_json_resource("licenses.json")
known_task_ids, known_task_ids_url = load_json_resource("tasks.json")
known_creators, known_creators_url = load_json_resource("creators.json")
known_size_categories, known_size_categories_url = load_json_resource("size_categories.json")
known_multilingualities, known_multilingualities_url = load_json_resource("multilingualities.json")


def yaml_block_from_readme(path: Path) -> Optional[str]:
    with path.open() as readme_file:
        content = [line.strip() for line in readme_file]

    if content[0] == "---" and "---" in content[1:]:
        yamlblock = "\n".join(content[1 : content[1:].index("---") + 1])
        return yamlblock

    return None


def metadata_dict_from_readme(path: Path) -> Optional[Dict[str, List[str]]]:
    """ "Loads a dataset's metadata from the dataset card (REAMDE.md), as a Python dict"""
    yaml_block = yaml_block_from_readme(path=path)
    if yaml_block is None:
        return None
    metada_dict = yaml.safe_load(yaml_block) or dict()
    return metada_dict


ValidatorOutput = Tuple[List[str], Optional[str]]


def tagset_validator(values: List[str], reference_values: List[str], name: str, url: str) -> ValidatorOutput:
    invalid_values = [v for v in values if v not in reference_values]
    if len(invalid_values) > 0:
        return [], f"{invalid_values} are not registered tags for '{name}', reference at {url}"
    return values, None


def escape_validation_for_predicate(
    values: List[Any], predicate_fn: Callable[[Any], bool]
) -> Tuple[List[Any], List[Any]]:
    trues, falses = list(), list()
    for v in values:
        if predicate_fn(v):
            trues.append(v)
        else:
            falses.append(v)
    if len(trues) > 0:
        logger.warning(f"The following values will escape validation: {trues}")
    return trues, falses


def validate_metadata_type(metadata_dict: dict):
    basic_typing_errors = {
        name: value
        for name, value in metadata_dict.items()
        if not isinstance(value, list) or len(value) == 0 or not isinstance(value[0], str)
    }
    if len(basic_typing_errors) > 0:
        raise TypeError(f"Found fields that are not non-empty list of strings: {basic_typing_errors}")


@dataclass
class DatasetMetadata:
    annotations_creators: List[str]
    language_creators: List[str]
    languages: List[str]
    licenses: List[str]
    multilinguality: List[str]
    size_categories: List[str]
    source_datasets: List[str]
    task_categories: List[str]
    task_ids: List[str]

    def __post_init__(self):
        validate_metadata_type(metadata_dict=vars(self))

        self.annotations_creators, annotations_creators_errors = self.validate_annotations_creators(
            self.annotations_creators
        )
        self.language_creators, language_creators_errors = self.validate_language_creators(self.language_creators)
        self.languages, languages_errors = self.validate_language_codes(self.languages)
        self.licenses, licenses_errors = self.validate_licences(self.licenses)
        self.multilinguality, multilinguality_errors = self.validate_mulitlinguality(self.multilinguality)
        self.size_categories, size_categories_errors = self.validate_size_catgeories(self.size_categories)
        self.source_datasets, source_datasets_errors = self.validate_source_datasets(self.source_datasets)
        self.task_categories, task_categories_errors = self.validate_task_categories(self.task_categories)
        self.task_ids, task_ids_errors = self.validate_task_ids(self.task_ids)

        errors = {
            "annotations_creators": annotations_creators_errors,
            "language_creators": language_creators_errors,
            "licenses": licenses_errors,
            "multilinguality": multilinguality_errors,
            "size_categories": size_categories_errors,
            "source_datasets": source_datasets_errors,
            "task_categories": task_categories_errors,
            "task_ids": task_ids_errors,
            "languages": languages_errors,
        }

        exception_msg_dict = dict()
        for field, errs in errors.items():
            if errs is not None:
                exception_msg_dict[field] = errs
        if len(exception_msg_dict) > 0:
            raise TypeError(
                "Could not validate the metada, found the following errors:\n"
                + "\n".join(f"* field '{fieldname}':\n\t{err}" for fieldname, err in exception_msg_dict.items())
            )

    @classmethod
    def from_readme(cls, path: Path) -> "DatasetMetadata":
        """Loads and validates the dataset metadat from its dataset card (README.md)

        Args:
            path (:obj:`Path`): Path to the dataset card (its README.md file)

        Returns:
            :class:`DatasetMetadata`: The dataset's metadata

        Raises:
            :obj:`TypeError`: If the dataset card has no metadata (no YAML header)
            :obj:`TypeError`: If the dataset's metadata is invalid
        """
        yaml_string = yaml_block_from_readme(path)
        if yaml_string is not None:
            return cls.from_yaml_string(yaml_string)
        else:
            raise TypeError(f"did not find a yaml block in '{path}'")

    @classmethod
    def from_yaml_string(cls, string: str) -> "DatasetMetadata":
        """Loads and validates the dataset metadat from a YAML string

        Args:
            string (:obj:`str`): The YAML string

        Returns:
            :class:`DatasetMetadata`: The dataset's metadata

        Raises:
            :obj:`TypeError`: If the dataset's metadata is invalid
        """
        metada_dict = yaml.safe_load(string) or dict()
        return cls(**metada_dict)

    @staticmethod
    def validate_annotations_creators(annotations_creators: List[str]) -> ValidatorOutput:
        return tagset_validator(
            annotations_creators, known_creators["annotations"], "annotations_creators", known_creators_url
        )

    @staticmethod
    def validate_language_creators(language_creators: List[str]) -> ValidatorOutput:
        return tagset_validator(language_creators, known_creators["language"], "language_creators", known_creators_url)

    @staticmethod
    def validate_language_codes(languages: List[str]) -> ValidatorOutput:
        return tagset_validator(
            values=languages,
            reference_values=known_language_codes.keys(),
            name="languages",
            url=known_language_codes_url,
        )

    @staticmethod
    def validate_licences(licenses: List[str]) -> ValidatorOutput:
        others, to_validate = escape_validation_for_predicate(licenses, lambda e: "-other-" in e)
        validated, error = tagset_validator(to_validate, list(known_licenses.keys()), "licenses", known_licenses_url)
        return [*validated, *others], error

    @staticmethod
    def validate_task_categories(task_categories: List[str]) -> ValidatorOutput:
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = list(known_task_ids.keys())
        others, to_validate = escape_validation_for_predicate(task_categories, lambda e: e.startswith("other"))
        validated, error = tagset_validator(to_validate, known_set, "task_categories", known_task_ids_url)
        return [*validated, *others], error

    @staticmethod
    def validate_task_ids(task_ids: List[str]) -> ValidatorOutput:
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = [tid for _cat, d in known_task_ids.items() for tid in d["options"]]
        others, to_validate = escape_validation_for_predicate(task_ids, lambda e: "-other-" in e)
        validated, error = tagset_validator(to_validate, known_set, "task_ids", known_task_ids_url)
        return [*validated, *others], error

    @staticmethod
    def validate_mulitlinguality(multilinguality: List[str]) -> ValidatorOutput:
        others, to_validate = escape_validation_for_predicate(multilinguality, lambda e: e.startswith("other"))
        validated, error = tagset_validator(
            to_validate, list(known_multilingualities.keys()), "multilinguality", known_size_categories_url
        )
        return [*validated, *others], error

    @staticmethod
    def validate_size_catgeories(size_cats: List[str]) -> ValidatorOutput:
        return tagset_validator(size_cats, known_size_categories, "size_categories", known_size_categories_url)

    @staticmethod
    def validate_source_datasets(sources: List[str]) -> ValidatorOutput:
        invalid_values = []
        for src in sources:
            is_ok = src in ["original", "extended"] or src.startswith("extended|")
            if not is_ok:
                invalid_values.append(src)
        if len(invalid_values) > 0:
            return (
                [],
                f"'source_datasets' has invalid values: {invalid_values}, refer to source code to understand {this_url}",
            )

        return sources, None


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the yaml metadata block of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()

    readme_filepath = Path(args.readme_filepath)
    DatasetMetadata.from_readme(readme_filepath)
