import pytest


DATASET_LOADING_SCRIPT_NAME = "__dummy_dataset1__"

DATASET_LOADING_SCRIPT_CODE = """
import json
import os

import datasets


REPO_URL = "https://huggingface.co/datasets/hf-internal-testing/raw_jsonl/resolve/main/"
URLS = {"train": REPO_URL + "wikiann-bn-train.jsonl", "validation": REPO_URL + "wikiann-bn-validation.jsonl"}


class __DummyDataset1__(datasets.GeneratorBasedBuilder):

    def _info(self):
        features = datasets.Features(
            {
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-PER",
                            "I-PER",
                            "B-ORG",
                            "I-ORG",
                            "B-LOC",
                            "I-LOC",
                        ]
                    )
                ),
                "langs": datasets.Sequence(datasets.Value("string")),
                "spans": datasets.Sequence(datasets.Value("string")),
            }
        )
        return datasets.DatasetInfo(features=features)

    def _split_generators(self, dl_manager):
        dl_path = dl_manager.download(URLS)
        return [
            datasets.SplitGenerator(datasets.Split.TRAIN, gen_kwargs={"filepath": dl_path["train"]}),
            datasets.SplitGenerator(datasets.Split.VALIDATION, gen_kwargs={"filepath": dl_path["validation"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                yield i, json.loads(line)
"""


@pytest.fixture
def dataset_loading_script_name():
    return DATASET_LOADING_SCRIPT_NAME


@pytest.fixture
def dataset_loading_script_code():
    return DATASET_LOADING_SCRIPT_CODE


@pytest.fixture
def dataset_loading_script_dir(dataset_loading_script_name, dataset_loading_script_code, tmp_path):
    script_name = dataset_loading_script_name
    script_dir = tmp_path / "datasets" / script_name
    script_dir.mkdir(parents=True)
    script_path = script_dir / f"{script_name}.py"
    with open(script_path, "w") as f:
        f.write(dataset_loading_script_code)
    return str(script_dir)
