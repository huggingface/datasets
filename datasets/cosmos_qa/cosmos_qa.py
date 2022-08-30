"""Cosmos QA dataset."""


import csv
import json

import datasets


_HOMEPAGE = "https://wilburone.github.io/cosmos/"

_DESCRIPTION = """\
Cosmos QA is a large-scale dataset of 35.6K problems that require commonsense-based reading comprehension, formulated as multiple-choice questions. It focuses on reading between the lines over a diverse collection of people's everyday narratives, asking questions concerning on the likely causes or effects of events that require reasoning beyond the exact text spans in the context
"""

_CITATION = """\
@inproceedings{huang-etal-2019-cosmos,
    title = "Cosmos {QA}: Machine Reading Comprehension with Contextual Commonsense Reasoning",
    author = "Huang, Lifu  and
      Le Bras, Ronan  and
      Bhagavatula, Chandra  and
      Choi, Yejin",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1243",
    doi = "10.18653/v1/D19-1243",
    pages = "2391--2401",
}
"""

_LICENSE = "CC BY 4.0"

_URL = "https://github.com/wilburOne/cosmosqa/raw/master/data/"
_URLS = {
    "train": _URL + "train.csv",
    "test": _URL + "test.jsonl",
    "dev": _URL + "valid.csv",
}


class CosmosQa(datasets.GeneratorBasedBuilder):
    """Cosmos QA dataset."""

    VERSION = datasets.Version("0.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer0": datasets.Value("string"),
                    "answer1": datasets.Value("string"),
                    "answer2": datasets.Value("string"),
                    "answer3": datasets.Value("string"),
                    "label": datasets.Value("int32"),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": dl_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            if split == "test":
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    yield id_, {
                        "id": data["id"],
                        "context": data["context"],
                        "question": data["question"],
                        "answer0": data["answer0"],
                        "answer1": data["answer1"],
                        "answer2": data["answer2"],
                        "answer3": data["answer3"],
                        "label": int(data.get("label", -1)),
                    }
            else:
                data = csv.DictReader(f)
                for id_, row in enumerate(data):
                    yield id_, {
                        "id": row["id"],
                        "context": row["context"],
                        "question": row["question"],
                        "answer0": row["answer0"],
                        "answer1": row["answer1"],
                        "answer2": row["answer2"],
                        "answer3": row["answer3"],
                        "label": int(row.get("label", -1)),
                    }
