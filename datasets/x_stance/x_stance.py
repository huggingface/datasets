"""TODO(x_stance): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


# TODO(x_stance): BibTeX citation
_CITATION = """\
@inproceedings{vamvas2020xstance,
    author    = "Vamvas, Jannis and Sennrich, Rico",
    title     = "{X-Stance}: A Multilingual Multi-Target Dataset for Stance Detection",
    booktitle = "Proceedings of the 5th Swiss Text Analytics Conference (SwissText) \\& 16th Conference on Natural Language Processing (KONVENS)",
    address   = "Zurich, Switzerland",
    year      = "2020",
    month     = "jun",
    url       = "http://ceur-ws.org/Vol-2624/paper9.pdf"
}
"""

# TODO(x_stance):
_DESCRIPTION = """\
The x-stance dataset contains more than 150 political questions, and 67k comments written by candidates on those questions.

It can be used to train and evaluate stance detection systems.

"""

_URL = "https://github.com/ZurichNLP/xstance/raw/v1.0.0/data/xstance-data-v1.0.zip"


class XStance(nlp.GeneratorBasedBuilder):
    """TODO(x_stance): Short description of my dataset."""

    # TODO(x_stance): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(x_stance): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "question": nlp.Value("string"),
                    "id": nlp.Value("int32"),
                    "question_id": nlp.Value("int32"),
                    "language": nlp.Value("string"),
                    "comment": nlp.Value("string"),
                    "label": nlp.Value("string"),
                    "numerical_label": nlp.Value("int32"),
                    "author": nlp.Value("string"),
                    "topic": nlp.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/ZurichNLP/xstance",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(x_stance): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "train.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "test.jsonl")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "valid.jsonl")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(x_stance): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)

                yield id_, {
                    "id": data["id"],
                    "question_id": data["question_id"],
                    "question": data["question"],
                    "comment": data["comment"],
                    "label": data["label"],
                    "author": data["author"],
                    "numerical_label": data["numerical_label"],
                    "topic": data["topic"],
                    "language": data["language"],
                }
