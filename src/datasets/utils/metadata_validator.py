import json
from pathlib import Path
from typing import Dict, List, Tuple

import langcodes as lc
import yaml
from pydantic import BaseModel, validator


BASE_REF_URL = "https://github.com/huggingface/datasets/tree/master/src/datasets/utils"
this_url = f"{BASE_REF_URL}/{__file__}"


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


def tagset_validator(values: List[str], reference_values: List[str], name: str, url: str) -> List[str]:
    for v in values:
        if v not in reference_values:
            raise ValueError(f"'{v}' is not a registered tag for '{name}', reference at {url}")
    return values


class DatasetMetadata(BaseModel):
    annotations_creators: List[str]
    language_creators: List[str]
    languages: List[str]
    licenses: List[str]
    multilinguality: List[str]
    size_categories: List[str]
    source_datasets: List[str]
    task_categories: List[str]
    task_ids: List[str]

    @classmethod
    def from_readme(cls, f: Path) -> "DatasetMetadata":
        with f.open() as fi:
            content = [line.strip() for line in fi]

        if content[0] == "---" and "---" in content[1:]:
            yamlblock = "\n".join(content[1 : content[1:].index("---") + 1])
            metada_dict = yaml.safe_load(yamlblock) or dict()
            return cls(**metada_dict)
        else:
            raise ValueError(f"did not find a yaml block in '{f}'")

    @classmethod
    def from_yaml_string(cls, string: str) -> "DatasetMetadata":
        metada_dict = yaml.safe_load(string) or dict()
        return cls(**metada_dict)

    @classmethod
    def empty(cls) -> "DatasetMetadata":
        return cls(
            annotations_creators=list(),
            language_creators=list(),
            languages=list(),
            licenses=list(),
            multilinguality=list(),
            size_categories=list(),
            source_datasets=list(),
            task_categories=list(),
            task_ids=list(),
        )

    @validator("annotations_creators")
    def annotations_creators_must_be_in_known_set(cls, annotations_creators: List[str]) -> List[str]:
        return tagset_validator(annotations_creators, known_creators["annotations"], "annotations", known_creators_url)

    @validator("language_creators")
    def language_creators_must_be_in_known_set(cls, language_creators: List[str]) -> List[str]:
        return tagset_validator(language_creators, known_creators["language"], "annotations", known_creators_url)

    @validator("languages")
    def language_code_must_be_recognized(cls, languages: List[str]):
        for code in languages:
            try:
                lc.get(code)
            except lc.tag_parser.LanguageTagError:
                raise ValueError(
                    f"'{code}' is not recognised as a valid language code (BCP47 norm), you can refer to https://github.com/LuminosoInsight/langcodes"
                )
        return languages

    @validator("licenses")
    def licenses_must_be_in_known_set(cls, licenses: List[str]):
        return tagset_validator(licenses, list(known_licenses.keys()), "licenses", known_licenses_url)

    @validator("task_categories")
    def task_category_must_be_in_known_set(cls, task_categories: List[str]):
        return tagset_validator(task_categories, list(known_task_ids.keys()), "tasks_ids", known_task_ids_url)

    @validator("task_ids")
    def task_id_must_be_in_known_set(cls, task_ids: List[str]):
        return tagset_validator(
            task_ids,
            [tid for _cat, d in known_task_ids.items() for tid in d["options"]],
            "tasks_ids",
            known_task_ids_url,
        )

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
