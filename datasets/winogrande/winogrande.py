"""TODO(winogrande): Add a description here."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


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
_FORMATS = ["xs", "s", "m", "l", "xl", "debiased"]


class WinograndeConfig(datasets.BuilderConfig):

    """ BuilderConfig for Discofuse"""

    def __init__(self, data_size, **kwargs):
        """

        Args:
            data_size: the format of the training set we want to use (xs, s, m, l, xl, debiased)
            **kwargs: keyword arguments forwarded to super.
        """
        super(WinograndeConfig, self).__init__(version=datasets.Version("1.1.0", ""), **kwargs)
        self.data_size = data_size


class Winogrande(datasets.GeneratorBasedBuilder):
    """TODO(winogrande): Short description of my dataset."""

    # TODO(winogrande): Set up version.
    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        WinograndeConfig(name="winogrande_" + data_size, description="AI2 dataset", data_size=data_size)
        for data_size in _FORMATS
    ]

    def _info(self):
        # TODO(winogrande): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "option1": datasets.Value("string"),
                    "option2": datasets.Value("string"),
                    "answer": datasets.Value("string")
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "winogrande_1.1")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_{}.jsonl".format(self.config.data_size)),
                    # 'labelpath': os.path.join(data_dir, 'train_{}-labels.lst'.format(self.config.data_size)),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    # 'labelpath': os.path.join(data_dir, 'dev-labels.lst'),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # TODO(winogrande): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
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
#       with open(filepath, encoding="utf-8") as f:
#           for id_, row in enumerate(f):
#               data = json.loads(row)
#               yield id_,{
#                   'sentence': data['sentence'],
#                   'option1': data['option1'],
#                   'option2': data['option2'],
#                   'answer': None
#               }
