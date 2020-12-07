"""TODO(wikitext): Add a description here."""

from __future__ import absolute_import, division, print_function

import os

import datasets


# TODO(wikitext): BibTeX citation
_CITATION = """\
@article{cruz2020investigating,
  title={Investigating the True Performance of Transformers in Low-Resource Languages: A Case Study in Automatic Corpus Creation},
  author={Jan Christian Blaise Cruz and Jose Kristian Resabal and James Lin and Dan John Velasco and Charibeth Cheng},
  journal={arXiv preprint arXiv:2010.11574},
  year={2020}
}
"""

# TODO(wikitext):
_DESCRIPTION = """\
Large-scale dataset of Filipino news articles. Sourced for the NewsPH-NLI Project (Cruz et al., 2020).
"""
_URL = "https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks"
_LICENSE = "GPL-3.0"
_DATA_URL = "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/newsph"


class NewsPHConfig(datasets.BuilderConfig):
    """BuilderConfig for WikiText."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for Wikitext

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(NewsPHConfig, self).__init__(
            version=datasets.Version(
                "1.0.0",
            ),
            **kwargs,
        )
        self.data_url = data_url


class NewsPH(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        NewsPHConfig(
            name="newsph",
            data_url=_DATA_URL + "/" + "newsph.zip",
            description=_DESCRIPTION,
        ),
    ]

    def _info(self):
        # TODO(wikitext): Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "text": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_URL,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(wikitext): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name == "newsph":
            data_file = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(data_file, "newsph")
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"data_file": os.path.join(data_dir, "train.txt"), "split": "train"},
                ),
            ]

    def _generate_examples(self, data_file, split):

        """Yields examples."""
        # TODO(wikitext): Yields (key, example) tuples from the dataset
        with open(data_file, encoding="utf-8") as f:
            for idx, row in enumerate(f):
                if row.strip():
                    yield idx, {"text": row}
                else:
                    yield idx, {"text": ""}
