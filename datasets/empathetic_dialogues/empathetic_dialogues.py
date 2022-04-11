"""TODO(empathetic_dialogues): Add a description here."""


import csv

import datasets


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


class EmpatheticDialogues(datasets.GeneratorBasedBuilder):
    """TODO(empathetic_dialogues): Short description of my dataset."""

    # TODO(empathetic_dialogues): Set up version.
    VERSION = datasets.Version("0.1.0")

    def _info(self):
        # TODO(empathetic_dialogues): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "conv_id": datasets.Value("string"),
                    "utterance_idx": datasets.Value("int32"),
                    "context": datasets.Value("string"),
                    "prompt": datasets.Value("string"),
                    "speaker_idx": datasets.Value("int32"),
                    "utterance": datasets.Value("string"),
                    "selfeval": datasets.Value("string"),
                    "tags": datasets.Value("string")
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
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "empatheticdialogues/train.csv"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "empatheticdialogues/valid.csv"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "empatheticdialogues/test.csv"},
            ),
        ]

    def _generate_examples(self, files, split_file):
        """Yields examples."""
        for path, f in files:
            if split_file == path:
                data = csv.DictReader(line.decode("utf-8") for line in f)
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
                break
