"""TODO(winogrande): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import nlp


# TODO(winogrande): BibTeX citation
_CITATION = """\
@InProceedings{ai2:winogrande,
title = {WinoGrande: An Adversarial Winograd Schema Challenge at Scale},
authors={Keisuke, Sakaguchi and Ronan, Le Bras and Chandra, Bhagavatula and Yejin, Choi
},
year={2019}
}
"""

# TODO(winogrande):
_DESCRIPTION = """\
WinoGrande is a new collection of 44k problems, inspired by Winograd Schema Challenge (Levesque, Davis, and Morgenstern
 2011), but adjusted to improve the scale and robustness against the dataset-specific bias. Formulated as a 
fill-in-a-blank task with binary options, the goal is to choose the right option for a given sentence which requires 
commonsense reasoning. 
"""

_URL = "https://storage.googleapis.com/ai2-mosaic/public/winogrande/winogrande_1.1.zip"
_SIZES = ["xs", "s", "m", "l", "xl"]


class WinograndeConfig(nlp.BuilderConfig):

    """ BuilderConfig for Discofuse"""

    def __init__(self, data_size, **kwargs):
        """

        Args:
            data_size: the size of the training set we want to us (xs, s, m, l, xl)
            **kwargs: keyword arguments forwarded to super.
        """
        super(WinograndeConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.data_size = data_size


class Winogrande(nlp.GeneratorBasedBuilder):
    """TODO(winogrande): Short description of my dataset."""

    # TODO(winogrande): Set up version.
    VERSION = nlp.Version("1.1.0")
    BUILDER_CONFIGS = [
        WinograndeConfig(name="winogrande_" + size, description="AI2 dataset", data_size=size) for size in _SIZES
    ]

    def _info(self):
        # TODO(winogrande): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "sentence": nlp.Value("string"),
                    "option1": nlp.Value("string"),
                    "option2": nlp.Value("string"),
                    "answer": nlp.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://leaderboard.allenai.org/winogrande/submissions/get-started",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(winogrande): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "winogrande_1.1")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_{}.jsonl".format(self.config.data_size)),
                    #'labelpath': os.path.join(data_dir, 'train_{}-labels.lst'.format(self.config.data_size)),
                    "split": "train",
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    #'labelpath': os.path.join(data_dir, 'dev-labels.lst'),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(winogrande): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if split == "test":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": "",
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "option2": data["option2"],
                        "answer": data["answer"],
                    }


# def _generate_test_example(filepath, split, labelpath=None):
#       with open(filepath) as f:
#           for id_, row in enumerate(f):
#               data = json.loads(row)
#               yield id_,{
#                   'sentence': data['sentence'],
#                   'option1': data['option1'],
#                   'option2': data['option2'],
#                   'answer': None
#               }
