"""TODO(empathetic_dialogues): Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


_CITATION = """\
@inproceedings{rashkin2019towards,
  title = {Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset},
  author = {Hannah Rashkin and Eric Michael Smith and Margaret Li and Y-Lan Boureau},
  booktitle = {ACL},
  year = {2019},
}
"""

_DESCRIPTION = """\
PyTorch original implementation of Towards Empathetic Open-domain Conversation Models: a New Benchmark and Dataset
"""
_URL = "https://dl.fbaipublicfiles.com/parlai/empatheticdialogues/empatheticdialogues.tar.gz"


class EmpatheticDialogues(nlp.GeneratorBasedBuilder):
    """TODO(empathetic_dialogues): Short description of my dataset."""

    # TODO(empathetic_dialogues): Set up version.
    VERSION = nlp.Version("0.1.0")

    def _info(self):
        # TODO(empathetic_dialogues): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "conv_id": nlp.Value("string"),
                    "utterance_idx": nlp.Value("int32"),
                    "context": nlp.Value("string"),
                    "prompt": nlp.Value("string"),
                    "speaker_idx": nlp.Value("int32"),
                    "utterance": nlp.Value("string"),
                    "selfeval": nlp.Value("string"),
                    "tags": nlp.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/facebookresearch/EmpatheticDialogues",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(empathetic_dialogues): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "empatheticdialogues")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "train.csv")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "valid.csv")},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.csv")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(empathetic_dialogues): Yields (key, example) tuples from the dataset
        with open(filepath) as f:
            data = csv.DictReader(f)
            for id_, row in enumerate(data):
                utterance = row["utterance"]
                speaker_id = int(row["speaker_idx"])
                context = row["context"]
                conv_id = row["conv_id"]
                tags = row["tags"] if row["tags"] else ""
                selfeval = row["selfeval"] if row["selfeval"] else ""
                utterance_id = int(row["utterance_idx"])
                prompt = row["prompt"]
                yield id_, {
                    "utterance": utterance,
                    "utterance_idx": utterance_id,
                    "context": context,
                    "speaker_idx": speaker_id,
                    "conv_id": conv_id,
                    "selfeval": selfeval,
                    "prompt": prompt,
                    "tags": tags,
                }
