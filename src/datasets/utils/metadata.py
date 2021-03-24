import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import langcodes as lc
import yaml
from pydantic import BaseModel, conlist, validator


BASE_REF_URL = "https://github.com/huggingface/datasets/tree/master/src/datasets/utils"
this_url = f"{BASE_REF_URL}/{__file__}"
logger = logging.getLogger(__name__)


def load_json_resource(resource: str) -> Tuple[Dict, str]:
    utils_dir = Path(__file__).parent
    with open(utils_dir / "resources" / resource) as fi:
        return json.load(fi), f"{BASE_REF_URL}/resources/{resource}"


known_licenses, known_licenses_url = load_json_resource("licenses.json")
known_task_ids, known_task_ids_url = load_json_resource("tasks.json")
known_creators, known_creators_url = load_json_resource("creators.json")
known_size_categories = ["unknown", "n<1K", "1K<n<10K", "10K<n<100K", "100K<n<1M", "n>1M"]
known_multilingualities = {
    "monolingual": "contains a single language",
    "multilingual": "contains multiple languages",
    "translation": "contains translated or aligned text",
    "other": "other type of language distribution",
}


def dict_from_readme(f: Path) -> Optional[Dict[str, List[str]]]:
    with f.open() as fi:
        content = [line.strip() for line in fi]

    if content[0] == "---" and "---" in content[1:]:
        yamlblock = "\n".join(content[1 : content[1:].index("---") + 1])
        metada_dict = yaml.safe_load(yamlblock) or dict()
        return metada_dict


def tagset_validator(values: List[str], reference_values: List[str], name: str, url: str) -> List[str]:
    invalid_values = [v for v in values if v not in reference_values]
    if len(invalid_values) > 0:
        raise ValueError(f"{invalid_values} are not registered tags for '{name}', reference at {url}")
    return values


def splitter(values: List[Any], predicate_fn: Callable[[Any], bool]) -> Tuple[List[Any], List[Any]]:
    trues, falses = list(), list()
    for v in values:
        if predicate_fn(v):
            trues.append(v)
        else:
            falses.append(v)
    return trues, falses


class DatasetMetadata(BaseModel):
    annotations_creators: conlist(str, min_items=1)
    language_creators: conlist(str, min_items=1)
    languages: conlist(str, min_items=1)
    licenses: conlist(str, min_items=1)
    multilinguality: conlist(str, min_items=1)
    size_categories: conlist(str, min_items=1)
    source_datasets: conlist(str, min_items=1)
    task_categories: conlist(str, min_items=1)
    task_ids: conlist(str, min_items=1)

    @classmethod
    def from_readme(cls, f: Path) -> "DatasetMetadata":
        metadata_dict = dict_from_readme(f)
        if metadata_dict is not None:
            return cls(**metadata_dict)
        else:
            raise ValueError(f"did not find a yaml block in '{f}'")

    @classmethod
    def from_yaml_string(cls, string: str) -> "DatasetMetadata":
        metada_dict = yaml.safe_load(string) or dict()
        return cls(**metada_dict)

    @validator("annotations_creators")
    def annotations_creators_must_be_in_known_set(cls, annotations_creators: List[str]) -> List[str]:
        return tagset_validator(annotations_creators, known_creators["annotations"], "annotations", known_creators_url)

    @validator("language_creators")
    def language_creators_must_be_in_known_set(cls, language_creators: List[str]) -> List[str]:
        return tagset_validator(language_creators, known_creators["language"], "annotations", known_creators_url)

    @validator("languages")
    def language_code_must_be_recognized(cls, languages: List[str]):
        invalid_values = []
        for code in languages:
            try:
                lc.get(code)
            except lc.tag_parser.LanguageTagError:
                invalid_values.append(code)
        if len(invalid_values) > 0:
            raise ValueError(
                f"{invalid_values} are not recognised as valid language codes (BCP47 norm), you can refer to https://github.com/LuminosoInsight/langcodes"
            )
        return languages

    @validator("licenses")
    def licenses_must_be_in_known_set(cls, licenses: List[str]):
        return tagset_validator(licenses, list(known_licenses.keys()), "licenses", known_licenses_url)

    @validator("task_categories")
    def task_category_must_be_in_known_set(cls, task_categories: List[str]):
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = list(known_task_ids.keys())
        others, to_validate = splitter(task_categories, lambda e: e.startswith("other"))
        return [*tagset_validator(to_validate, known_set, "tasks_ids", known_task_ids_url), *others]

    @validator("task_ids")
    def task_id_must_be_in_known_set(cls, task_ids: List[str]):
        # TODO: we're currently ignoring all values starting with 'other' as our task taxonomy is bound to change
        #   in the near future and we don't want to waste energy in tagging against a moving taxonomy.
        known_set = [tid for _cat, d in known_task_ids.items() for tid in d["options"]]
        others, to_validate = splitter(task_ids, lambda e: e.startswith("other"))
        return [*tagset_validator(to_validate, known_set, "tasks_ids", known_task_ids_url), *others]

    @validator("multilinguality")
    def multilinguality_must_be_in_known_set(cls, multilinguality: List[str]):
        return tagset_validator(multilinguality, list(known_multilingualities.keys()), "multilinguality", this_url)

    @validator("size_categories")
    def size_categories_must_be_in_known_set(cls, size_cats: List[str]):
        return tagset_validator(size_cats, known_size_categories, "size_categories", this_url)


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the yaml metadata block of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()

    readme_filepath = Path(args.readme_filepath)
    DatasetMetadata.from_readme(readme_filepath)
