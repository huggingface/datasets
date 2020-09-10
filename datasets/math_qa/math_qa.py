"""TODO(math_qa): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(math_qa): BibTeX citation
_CITATION = """
"""

# TODO(math_qa):
_DESCRIPTION = """
Our dataset is gathered by using a new representation language to annotate over the AQuA-RAT dataset. AQuA-RAT has provided the questions, options, rationale, and the correct options.
"""
_URL = "https://math-qa.github.io/math-QA/data/MathQA.zip"


class MathQa(datasets.GeneratorBasedBuilder):
    """TODO(math_qa): Short description of my dataset."""

    # TODO(math_qa): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(math_qa): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "Problem": datasets.Value("string"),
                    "Rationale": datasets.Value("string"),
                    "options": datasets.Value("string"),
                    "correct": datasets.Value("string"),
                    "annotated_formula": datasets.Value("string"),
                    "linear_formula": datasets.Value("string"),
                    "category": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://math-qa.github.io/math-QA/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(math_qa): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_path, "train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_path, "test.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_path, "dev.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(math_qa): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, row in enumerate(data):
                yield id_, row
