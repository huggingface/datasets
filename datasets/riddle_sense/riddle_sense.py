"""TODO(commonsense_qa): Add a description here."""


import json

import datasets


# TODO(commonsense_qa): BibTeX citation
_CITATION = """\
@InProceedings{lin-etal-2021-riddlesense,
title={RiddleSense: Reasoning about Riddle Questions Featuring Linguistic Creativity and Commonsense Knowledge},
author={Lin, Bill Yuchen and Wu, Ziyi and Yang, Yichi and Lee, Dong-Ho and Ren, Xiang},
journal={Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021): Findings},
year={2021}

"""

# TODO(commonsense_qa):
_DESCRIPTION = """\
Answering such a riddle-style question is a challenging cognitive process, in that it requires
complex commonsense reasoning abilities, an understanding of figurative language, and counterfactual reasoning
skills, which are all important abilities for advanced natural language understanding (NLU). However,
there is currently no dedicated datasets aiming to test these abilities. Herein, we present RiddleSense,
a new multiple-choice question answering task, which comes with the first large dataset (5.7k examples) for answering
riddle-style commonsense questions. We systematically evaluate a wide range of models over the challenge,
and point out that there is a large gap between the best-supervised model and human performance — suggesting
intriguing future research in the direction of higher-order commonsense reasoning and linguistic creativity towards
building advanced NLU systems.

"""

_URL = "https://inklab.usc.edu/RiddleSense/riddlesense_dataset/"
_URLS = {
    "train": _URL + "rs_train.jsonl",
    "dev": _URL + "rs_dev.jsonl",
    "test": _URL + "rs_test_hidden.jsonl",
}


class RiddleSense(datasets.GeneratorBasedBuilder):
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
            homepage="https://inklab.usc.edu/RiddleSense/",
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
