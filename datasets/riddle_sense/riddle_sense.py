import json

import datasets


_CITATION = """\
@InProceedings{lin-etal-2021-riddlesense,
title={RiddleSense: Reasoning about Riddle Questions Featuring Linguistic Creativity and Commonsense Knowledge},
author={Lin, Bill Yuchen and Wu, Ziyi and Yang, Yichi and Lee, Dong-Ho and Ren, Xiang},
journal={Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021): Findings},
year={2021}
}
"""

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

_LICENSE = """\
The copyright of RiddleSense dataset is consistent with the terms of use of the fan websites and the intellectual
property and privacy rights of the original sources. All of our riddles and answers are from fan websites that can be
accessed freely. The website owners state that you may print and download material from the sites solely for non
commercial use provided that we agree not to change or delete any copyright or proprietary notices from the
materials. The dataset users must agree that they will only use the dataset for research purposes before they can
access the both the riddles and our annotations. We do not vouch for the potential bias or fairness issue that might
exist within the riddles. You do not have the right to redistribute them. Again, you must not use this dataset for any
commercial purposes.
"""

_URL = "https://inklab.usc.edu/RiddleSense/riddlesense_dataset/"
_URLS = {
    "train": _URL + "rs_train.jsonl",
    "dev": _URL + "rs_dev.jsonl",
    "test": _URL + "rs_test_hidden.jsonl",
}


class RiddleSense(datasets.GeneratorBasedBuilder):

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
            license=_LICENSE,
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
