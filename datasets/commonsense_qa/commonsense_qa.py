"""TODO(commonsense_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


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
_URL = "https://s3.amazonaws.com/commensenseqa"
_TRAINING_FILE = "train_rand_split.jsonl"
_DEV_FILE = "dev_rand_split.jsonl"
_TEST_FILE = "test_rand_split_no_answers.jsonl"


class CommonsenseQa(nlp.GeneratorBasedBuilder):
    """TODO(commonsense_qa): Short description of my dataset."""

    # TODO(commonsense_qa): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # These are the features of your dataset like images, labels ...
        features = nlp.Features(
            {
                "answerKey": nlp.Value("string"),
                "question": nlp.Value("string"),
                "choices": nlp.features.Sequence({"label": nlp.Value("string"), "text": nlp.Value("string"),}),
            }
        )
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://www.tau-nlp.org/commonsenseqa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        download_urls = {
            "train": os.path.join(_URL, _TRAINING_FILE),
            "test": os.path.join(_URL, _TEST_FILE),
            "dev": os.path.join(_URL, _DEV_FILE),
        }

        downloaded_files = dl_manager.download_and_extract(download_urls)

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"], "split": "train"}
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"], "split": "dev",}
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"], "split": "test",}
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(commonsense_qa): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
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
