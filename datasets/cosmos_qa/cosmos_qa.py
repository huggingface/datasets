"""TODO(cosmos_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import nlp


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
_TEST_FILE = "test.jsonl"
_TRAIN_FILE = "train.csv"
_DEV_FILE = "valid.csv"


class CosmosQa(nlp.GeneratorBasedBuilder):
    """TODO(cosmos_qa): Short description of my dataset."""

    # TODO(cosmos_qa): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(cosmos_qa): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answer0": nlp.Value("string"),
                    "answer1": nlp.Value("string"),
                    "answer2": nlp.Value("string"),
                    "answer3": nlp.Value("string"),
                    "label": nlp.Value("int32")
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
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {
            "train": os.path.join(_URL, _TRAIN_FILE),
            "test": os.path.join(_URL, _TEST_FILE),
            "dev": os.path.join(_URL, _DEV_FILE),
        }
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(cosmos_qa): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
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
