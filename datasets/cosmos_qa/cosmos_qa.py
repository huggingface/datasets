"""TODO(cosmos_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json

import datasets


# TODO(cosmos_qa): BibTeX citation
_CITATION = """\
@inproceedings{cosmos,
    title={COSMOS QA: Machine Reading Comprehension
    with Contextual Commonsense Reasoning},
    author={Lifu Huang and Ronan Le Bras and Chandra Bhagavatula and Yejin Choi},
    booktitle ={arXiv:1909.00277v2},
    year={2019}
}
"""

# TODO(cosmos_qa):
_DESCRIPTION = """\
Cosmos QA is a large-scale dataset of 35.6K problems that require commonsense-based reading comprehension, formulated as multiple-choice questions. It focuses on reading between the lines over a diverse collection of people's everyday narratives, asking questions concerning on the likely causes or effects of events that require reasoning beyond the exact text spans in the context
"""

_URL = "https://github.com/wilburOne/cosmosqa/raw/master/data/"
_URLS = {
    "train": _URL + "train.csv",
    "test": _URL + "test.jsonl",
    "dev": _URL + "valid.csv",
}


class CosmosQa(datasets.GeneratorBasedBuilder):
    """TODO(cosmos_qa): Short description of my dataset."""

    # TODO(cosmos_qa): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(cosmos_qa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer0": datasets.Value("string"),
                    "answer1": datasets.Value("string"),
                    "answer2": datasets.Value("string"),
                    "answer3": datasets.Value("string"),
                    "label": datasets.Value("int32")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://wilburone.github.io/cosmos/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(cosmos_qa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = _URLS
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(cosmos_qa): Yields (key, example) tuples from the dataset
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
