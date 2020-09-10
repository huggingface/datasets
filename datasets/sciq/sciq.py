"""TODO(sciQ): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


# TODO(sciQ): BibTeX citation
_CITATION = """\
@inproceedings{SciQ,
    title={Crowdsourcing Multiple Choice Science Questions},
    author={Johannes Welbl, Nelson F. Liu, Matt Gardner},
    year={2017},
    journal={arXiv:1707.06209v1}
}
"""

# TODO(sciQ):
_DESCRIPTION = """\
The SciQ dataset contains 13,679 crowdsourced science exam questions about Physics, Chemistry and Biology, among others. The questions are in multiple-choice format with 4 answer options each. For the majority of the questions, an additional paragraph with supporting evidence for the correct answer is provided.

"""
_URL = "https://s3-us-west-2.amazonaws.com/ai2-website/data/SciQ.zip"


class Sciq(datasets.GeneratorBasedBuilder):
    """TODO(sciQ): Short description of my dataset."""

    # TODO(sciQ): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(sciQ): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "question": datasets.Value("string"),
                    "distractor3": datasets.Value("string"),
                    "distractor1": datasets.Value("string"),
                    "distractor2": datasets.Value("string"),
                    "correct_answer": datasets.Value("string"),
                    "support": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://allenai.org/data/sciq",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(sciQ): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "SciQ dataset-2 3")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "valid.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(sciQ): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, row in enumerate(data):
                yield id_, row
