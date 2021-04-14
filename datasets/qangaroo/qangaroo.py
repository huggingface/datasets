"""TODO(qangaroo): Add a description here."""


import json
import os

import datasets


# TODO(qangaroo): BibTeX citation

_CITATION = """
"""

# TODO(quangaroo):
_DESCRIPTION = """\
  We have created two new Reading Comprehension datasets focussing on multi-hop (alias multi-step) inference.

Several pieces of information often jointly imply another fact. In multi-hop inference, a new fact is derived by combining facts via a chain of multiple steps.

Our aim is to build Reading Comprehension methods that perform multi-hop inference on text, where individual facts are spread out across different documents.

The two QAngaroo datasets provide a training and evaluation resource for such methods.
"""

_MEDHOP_DESCRIPTION = """\
  With the same format as WikiHop, this dataset is based on research paper abstracts from PubMed, and the queries are about interactions between pairs of drugs.
  The correct answer has to be inferred by combining information from a chain of reactions of drugs and proteins.
  """
_WIKIHOP_DESCRIPTION = """\
  With the same format as WikiHop, this dataset is based on research paper abstracts from PubMed, and the queries are about interactions between pairs of drugs.
   The correct answer has to be inferred by combining information from a chain of reactions of drugs and proteins.
  """

_URL = "https://drive.google.com/uc?export=download&id=1ytVZ4AhubFDOEL7o7XrIRIyhU8g9wvKA"


class QangarooConfig(datasets.BuilderConfig):
    def __init__(self, data_dir, **kwargs):
        """BuilderConfig for qangaroo dataset

        Args:
          data_dir: directory for the given dataset name
          **kwargs: keyword arguments forwarded to super.

        """

        super(QangarooConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)

        self.data_dir = data_dir


class Qangaroo(datasets.GeneratorBasedBuilder):
    """TODO(qangaroo): Short description of my dataset."""

    # TODO(qangaroo): Set up version.
    VERSION = datasets.Version("0.1.0")
    BUILDER_CONFIGS = [
        QangarooConfig(name="medhop", description=_MEDHOP_DESCRIPTION, data_dir="medhop"),
        QangarooConfig(name="masked_medhop", description=_MEDHOP_DESCRIPTION, data_dir="medhop"),
        QangarooConfig(name="wikihop", description=_WIKIHOP_DESCRIPTION, data_dir="wikihop"),
        QangarooConfig(name="masked_wikihop", description=_WIKIHOP_DESCRIPTION, data_dir="wikihop"),
    ]

    def _info(self):
        # TODO(qangaroo): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    # These are the features of your dataset like images, labels ...
                    "query": datasets.Value("string"),
                    "supports": datasets.features.Sequence(datasets.Value("string")),
                    "candidates": datasets.features.Sequence(datasets.Value("string")),
                    "answer": datasets.Value("string"),
                    "id": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://qangaroo.cs.ucl.ac.uk/index.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(qangaroo): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "qangaroo_v1.1")
        train_file = "train.masked.json" if "masked" in self.config.name else "train.json"
        dev_file = "dev.masked.json" if "masked" in self.config.name else "dev.json"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, self.config.data_dir, train_file)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, self.config.data_dir, dev_file)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        # TODO(quangaroo): Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for example in data:
                id_ = example["id"]
                yield id_, {
                    "id": example["id"],
                    "query": example["query"],
                    "supports": example["supports"],
                    "candidates": example["candidates"],
                    "answer": example["answer"],
                }
