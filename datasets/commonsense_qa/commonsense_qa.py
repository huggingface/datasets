"""TODO(commonsense_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json

import datasets


# TODO(commonsense_qa): BibTeX citation
_CITATION = """\
@InProceedings{commonsense_QA,
title={COMMONSENSEQA: A Question Answering Challenge Targeting Commonsense Knowledge},
author={Alon, Talmor and Jonathan, Herzig and Nicholas, Lourie and Jonathan ,Berant},
journal={arXiv preprint arXiv:1811.00937v2},
year={2019}

"""

# TODO(commonsense_qa):
_DESCRIPTION = """\
CommonsenseQA is a new multiple-choice question answering dataset that requires different types of commonsense knowledge
 to predict the correct answers . It contains 12,102 questions with one correct answer and four distractor answers.
 The dataset is provided in two major training/validation/testing set splits: "Random split" which is the main evaluation
  split, and "Question token split", see paper for details.
"""

_URL = "https://s3.amazonaws.com/commensenseqa/"
_URLS = {
    "train": _URL + "train_rand_split.jsonl",
    "dev": _URL + "dev_rand_split.jsonl",
    "test": _URL + "test_rand_split_no_answers.jsonl",
}


class CommonsenseQa(datasets.GeneratorBasedBuilder):
    """TODO(commonsense_qa): Short description of my dataset."""

    # TODO(commonsense_qa): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # These are the features of your dataset like images, labels ...
        features = datasets.Features(
            {
                "answerKey": datasets.Value("string"),
                "question": datasets.Value("string"),
                "choices": datasets.features.Sequence(
                    {
                        "label": datasets.Value("string"),
                        "text": datasets.Value("string"),
                    }
                ),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://www.tau-datasets.org/commonsenseqa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        download_urls = _URLS

        downloaded_files = dl_manager.download_and_extract(download_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(commonsense_qa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                question = data["question"]
                choices = question["choices"]
                labels = [label["label"] for label in choices]
                texts = [text["text"] for text in choices]
                stem = question["stem"]
                if split == "test":
                    answerkey = ""
                else:
                    answerkey = data["answerKey"]

                yield id_, {
                    "answerKey": answerkey,
                    "question": stem,
                    "choices": {"label": labels, "text": texts},
                }
