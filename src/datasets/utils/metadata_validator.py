import json
from pathlib import Path
from typing import Dict, List

import langcodes as lc
import yaml
from pydantic import BaseModel, validator


def load_json_resource(resource: str) -> Dict:
    utils_dir = Path(__file__).parent
    with open(utils_dir / "resources" / resource) as fi:
        return json.load(fi)


known_licenses: Dict[str, str] = load_json_resource("licenses.json")
known_task_ids: Dict[str, Dict] = load_json_resource("tasks.json")
creator_set: Dict[str, List[str]] = load_json_resource("creators.json")
known_size_categories = ["unknown", "n<1K", "1K<n<10K", "10K<n<100K", "100K<n<1M", "n>1M"]
multilinguality_set = {
    "monolingual": "contains a single language",
    "multilingual": "contains multiple languages",
    "translation": "contains translated or aligned text",
    "other": "other type of language distribution",
}


def tagset_validator(values: List[str], reference_values: List[str], name: str) -> List[str]:
    for v in values:
        if v not in reference_values:
            raise ValueError(f"'{v}' is not a registered tag for {name}.")
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

    @validator("annotations_creators")
    def annotations_creators_must_be_in_known_set(cls, annotations_creators: List[str]) -> List[str]:
        return tagset_validator(annotations_creators, creator_set["annotations"], "annotations")

    @validator("language_creators")
    def language_creators_must_be_in_known_set(cls, language_creators: List[str]) -> List[str]:
        return tagset_validator(language_creators, creator_set["language"], "annotations")

    @validator("languages")
    def language_code_must_be_recognized(cls, languages: List[str]):
        for code in languages:
            try:
                lc.get(code)
            except lc.tag_parser.LanguageTagError:
                raise ValueError(f"'{code}' is not recognised as a valid language code")
        return languages

    @validator("licenses")
    def licenses_must_be_in_known_set(cls, licenses: List[str]):
        return tagset_validator(licenses, list(known_licenses.keys()), "licenses")

    @validator("task_categories")
    def task_category_must_be_in_known_set(cls, task_categories: List[str]):
        return tagset_validator(task_categories, list(known_task_ids.keys()), "taks_ids")

    @validator("task_ids")
    def task_id_must_be_in_known_set(cls, task_ids: List[str]):
        return tagset_validator(
            task_ids, [tid for _cat, d in known_task_ids.items() for tid in d["options"]], "taks_ids"
        )


if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(usage="Validate the yaml metadata block of a README.md file.")
    ap.add_argument("readme_filepath")
    args = ap.parse_args()

    readme_filepath = Path(args.readme_filepath)
    DatasetMetadata.from_readme(readme_filepath)
