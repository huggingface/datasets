import json
import logging
import re
from collections import Counter
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union


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
known_source_datasets, known_source_datasets_url = ["original", "extended", r"extended\|.*"], this_url


class NoDuplicateSafeLoader(yaml.SafeLoader):
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


def yaml_block_from_readme(path: Path) -> Optional[str]:
    with open(path, encoding="utf-8") as readme_file:
        content = [line.rstrip("\n") for line in readme_file]

    if content[0] == "---" and "---" in content[1:]:
        yamlblock = "\n".join(content[1 : content[1:].index("---") + 1])
        return yamlblock

    return None


def metadata_dict_from_readme(path: Path) -> Optional[Dict[str, List[str]]]:
    """Loads a dataset's metadata from the dataset card (REAMDE.md), as a Python dict"""
    yaml_block = yaml_block_from_readme(path=path)
    if yaml_block is None:
        return None
    metada_dict = yaml.load(yaml_block, Loader=NoDuplicateSafeLoader) or dict()
    return metada_dict


ValidatorOutput = Tuple[List[str], Optional[str]]


def tagset_validator(
    items: Union[List[str], Dict[str, List[str]]],
    reference_values: List[str],
    name: str,
    url: str,
    escape_validation_predicate_fn: Optional[Callable[[Any], bool]] = None,
) -> ValidatorOutput:
    reference_values = re.compile("^(?:" + "|".join(reference_values) + ")$")
    if isinstance(items, list):
        if escape_validation_predicate_fn is not None:
            invalid_values = [
                v for v in items if not reference_values.match(v) and escape_validation_predicate_fn(v) is False
            ]
        else:
            invalid_values = [v for v in items if not reference_values.match(v)]

    else:
        invalid_values = []
        if escape_validation_predicate_fn is not None:
            for config_name, values in items.items():
                invalid_values += [
                    v for v in values if not reference_values.match(v) and escape_validation_predicate_fn(v) is False
                ]
        else:
            for config_name, values in items.items():
                invalid_values += [v for v in values if not reference_values.match(v)]

    if len(invalid_values) > 0:
        return [], f"{invalid_values} are not registered tags for '{name}', reference at {url}"
    return items, None


def validate_type(value: Any, expected_type: Type):
    error_string = ""
    NoneType = type(None)
    if expected_type == NoneType:
        if not isinstance(value, NoneType):
            return f"Expected `{NoneType}`. Found value: `{value}` of type `{type(value)}`.\n"
        else:
            return error_string
    if expected_type == str:
        if not isinstance(value, str):
            return f"Expected `{str}`. Found value: `{value}` of type: `{type(value)}`.\n"

        elif isinstance(value, str) and len(value) == 0:
            return (
                f"Expected `{str}` with length > 0. Found value: `{value}` of type: `{type(value)}` with length: 0.\n"
            )
        else:
            return error_string
    # Add more `elif` statements if primitive type checking is needed
    else:
        expected_type_origin = expected_type.__origin__
        expected_type_args = expected_type.__args__

        if expected_type_origin == Union:
            for type_arg in expected_type_args:
                temp_error_string = validate_type(value, type_arg)
                if temp_error_string == "":  # at least one type is successfully validated
                    return temp_error_string
                else:
                    if error_string == "":
                        error_string = "(" + temp_error_string + ")"
                    else:
                        error_string += "\nOR\n" + "(" + temp_error_string + ")"

        else:
            # Assuming `List`/`Dict`/`Tuple`
            if not isinstance(value, expected_type_origin) or len(value) == 0:
                return f"Expected `{expected_type_origin}` with length > 0. Found value of type: `{type(value)}`, with length: {len(value)}.\n"

            if expected_type_origin == Dict:
                key_type, value_type = expected_type_args
                key_error_string = ""
                value_error_string = ""
                for k, v in value.items():
                    key_error_string += validate_type(k, key_type)
                    value_error_string += validate_type(v, value_type)
                if key_error_string != "" or value_error_string != "":
                    return f"Typing errors with keys:\n {key_error_string} and values:\n {value_error_string}"

            else:  # `List`/`Tuple`
                value_type = expected_type_args[0]
                value_error_string = ""
                for v in value:
                    value_error_string += validate_type(v, value_type)
                if value_error_string != "":
                    return f"Typing errors with values:\n {value_error_string}"

        return error_string


def validate_metadata_type(metadata_dict: dict):
    field_types = {field.name: field.type for field in fields(DatasetMetadata)}

    typing_errors = {}
    for field_name, field_value in metadata_dict.items():
        field_type_error = validate_type(
            metadata_dict[field_name], field_types.get(field_name, Union[List[str], Dict[str, List[str]]])
        )
        if field_type_error != "":
            typing_errors[field_name] = field_type_error
    if len(typing_errors) > 0:
        raise TypeError(f"The following typing errors are found: {typing_errors}")


@dataclass
class DatasetMetadata:
    annotations_creators: Union[List[str], Dict[str, List[str]]]
    language_creators: Union[List[str], Dict[str, List[str]]]
    languages: Union[List[str], Dict[str, List[str]]]
    licenses: Union[List[str], Dict[str, List[str]]]
    multilinguality: Union[List[str], Dict[str, List[str]]]
    pretty_name: Union[str, Dict[str, str]]
    size_categories: Union[List[str], Dict[str, List[str]]]
    source_datasets: Union[List[str], Dict[str, List[str]]]
    task_categories: Union[List[str], Dict[str, List[str]]]
    task_ids: Union[List[str], Dict[str, List[str]]]
    paperswithcode_id: Optional[str] = None

    def validate(self):
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
        self.paperswithcode_id, paperswithcode_id_errors = self.validate_paperswithcode_id_errors(
            self.paperswithcode_id
        )

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
            "paperswithcode_id": paperswithcode_id_errors,
        }

        exception_msg_dict = dict()
        for field, errs in errors.items():
            if errs is not None:
                exception_msg_dict[field] = errs
        if len(exception_msg_dict) > 0:
            raise TypeError(
                "Could not validate the metadata, found the following errors:\n"
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
            raise TypeError(f"Unable to find a yaml block in '{path}'")

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
        metada_dict = yaml.load(string, Loader=NoDuplicateSafeLoader) or dict()
        return cls(**metada_dict)

    @staticmethod
    def validate_annotations_creators(annotations_creators: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        return tagset_validator(
            annotations_creators, known_creators["annotations"], "annotations_creators", known_creators_url
        )

    @staticmethod
    def validate_language_creators(language_creators: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        return tagset_validator(language_creators, known_creators["language"], "language_creators", known_creators_url)

    @staticmethod
    def validate_language_codes(languages: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        return tagset_validator(
            languages,
            known_language_codes.keys(),
            "languages",
            known_language_codes_url,
            lambda lang: lang == "unknown",
        )

    @staticmethod
    def validate_licences(licenses: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        validated, error = tagset_validator(
            licenses,
            list(known_licenses.keys()),
            "licenses",
            known_licenses_url,
            lambda e: "-other-" in e or e.startswith("other-"),
        )
        return validated, error

    @staticmethod
    def validate_task_categories(task_categories: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = list(known_task_ids.keys())
        validated, error = tagset_validator(
            task_categories, known_set, "task_categories", known_task_ids_url, lambda e: e.startswith("other-")
        )
        return validated, error

    @staticmethod
    def validate_task_ids(task_ids: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = [tid for _cat, d in known_task_ids.items() for tid in d["options"]]
        validated, error = tagset_validator(
            task_ids, known_set, "task_ids", known_task_ids_url, lambda e: "-other-" in e or e.startswith("other-")
        )
        return validated, error

    @staticmethod
    def validate_mulitlinguality(multilinguality: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        validated, error = tagset_validator(
            multilinguality,
            list(known_multilingualities.keys()),
            "multilinguality",
            known_size_categories_url,
            lambda e: e.startswith("other-"),
        )
        return validated, error

    @staticmethod
    def validate_size_catgeories(size_cats: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        return tagset_validator(size_cats, known_size_categories, "size_categories", known_size_categories_url)

    @staticmethod
    def validate_source_datasets(sources: Union[List[str], Dict[str, List[str]]]) -> ValidatorOutput:
        return tagset_validator(sources, known_source_datasets, "source_datasets", known_source_datasets_url)

    @staticmethod
    def validate_paperswithcode_id_errors(paperswithcode_id: Optional[str]) -> ValidatorOutput:
        if paperswithcode_id is None:
            return paperswithcode_id, None
        else:
            if " " in paperswithcode_id or paperswithcode_id.lower() != paperswithcode_id:
                return (
                    None,
                    f"The paperswithcode_id must be lower case and not contain spaces but got {paperswithcode_id}. You can find the paperswithcode_id in the URL of the dataset page on paperswithcode.com.",
                )
            else:
                return paperswithcode_id, None

    @staticmethod
    def validate_pretty_name(pretty_name: Union[str, Dict[str, str]]):
        if isinstance(pretty_name, str):
            if len(pretty_name) == 0:
                return None, "The pretty name must have a length greater than 0 but got an empty string."
        else:
            error_string = ""
            for key, value in pretty_name.items():
                if len(value) == 0:
                    error_string += f"The pretty name must have a length greater than 0 but got an empty string for config: {key}.\n"

            if error_string == "":
                return None, error_string
            else:
                return pretty_name, None

    def get_metadata_by_config_name(self, name: str) -> "DatasetMetadata":
        metadata_dict = asdict(self)
        config_name_hit = []
        has_multi_configs = []
        result_dict = {}
        for tag_key, tag_value in metadata_dict.items():
            if isinstance(tag_value, str) or isinstance(tag_value, list):
                result_dict[tag_key] = tag_value
            elif isinstance(tag_value, dict):
                has_multi_configs.append(tag_key)
                for config_name, value in tag_value.items():
                    if config_name == name:
                        result_dict[tag_key] = value
                        config_name_hit.append(tag_key)

        if len(has_multi_configs) > 0 and has_multi_configs != config_name_hit:
            raise TypeError(
                f"The following tags have multiple configs: {has_multi_configs} but the config `{name}`  was found only in: {config_name_hit}."
            )
        if config_name_hit == 0:
            logger.warning(
                "No matching config names found in the metadata, using the common values to create metadata."
            )

        return DatasetMetadata(**result_dict)


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the yaml metadata block of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()

    readme_filepath = Path(args.readme_filepath)
    dataset_metadata = DatasetMetadata.from_readme(readme_filepath)
    dataset_metadata.validate()
