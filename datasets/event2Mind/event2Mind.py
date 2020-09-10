"""TODO(event2Mind): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# TODO(event2Mind): BibTeX citation
_CITATION = """\
@inproceedings{event2Mind,
    title={Event2Mind: Commonsense Inference on Events, Intents, and Reactions},
    author={Hannah Rashkin and Maarten Sap and Emily Allaway and Noah A. Smith† Yejin Choi},
    year={2018}
}
"""

# TODO(event2Mind):\

_DESCRIPTION = """\
In Event2Mind, we explore the task of understanding stereotypical intents and reactions to events. Through crowdsourcing, we create a large corpus with 25,000 events and free-form descriptions of their intents and reactions, both of the event's subject and (potentially implied) other participants.
"""
_URL = "https://uwnlp.github.io/event2mind/data/event2mind.zip"


class Event2mind(datasets.GeneratorBasedBuilder):
    """TODO(event2Mind): Short description of my dataset."""

    # TODO(event2Mind): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(event2Mind): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "Source": datasets.Value("string"),
                    "Event": datasets.Value("string"),
                    "Xintent": datasets.Value("string"),
                    "Xemotion": datasets.Value("string"),
                    "Otheremotion": datasets.Value("string"),
                    "Xsent": datasets.Value("string"),
                    "Osent": datasets.Value("string"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://uwnlp.github.io/event2mind/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(event2Mind): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "train.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "test.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(dl_dir, "dev.csv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(event2Mind): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f)
            for id_, row in enumerate(data):
                yield id_, {
                    "Source": row["Source"],
                    "Event": row["Event"],
                    "Xintent": row["Xintent"],
                    "Xemotion": row["Xemotion"],
                    "Otheremotion": row["Otheremotion"],
                    "Xsent": row["Xsent"],
                    "Osent": row["Osent"],
                }
