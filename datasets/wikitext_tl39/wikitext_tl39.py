"""TODO(wikitext): Add a description here."""


import os

import datasets


# TODO(wikitext): BibTeX citation
_CITATION = """\
@article{cruz2019evaluating,
  title={Evaluating Language Model Finetuning Techniques for Low-resource Languages},
  author={Cruz, Jan Christian Blaise and Cheng, Charibeth},
  journal={arXiv preprint arXiv:1907.00409},
  year={2019}
}
"""

# TODO(wikitext):
_DESCRIPTION = """\
Large scale, unlabeled text dataset with 39 Million tokens in the training set. Inspired by the original WikiText Long Term Dependency dataset (Merity et al., 2016). TL means "Tagalog." Originally published in Cruz & Cheng (2019).
"""
_URL = "https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks"
_LICENSE = "GPL-3.0"
_DATA_URL = "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/wikitext-tl-39"


class WikitextTl39Config(datasets.BuilderConfig):
    """BuilderConfig for WikiText."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for Wikitext

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(WikitextTl39Config, self).__init__(
            version=datasets.Version(
                "1.0.0",
            ),
            **kwargs,
        )
        self.data_url = data_url


class WikitextTl39(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        WikitextTl39Config(
            name="wikitext-tl-39",
            data_url=_DATA_URL + "/" + "wikitext-tl-39.zip",
            description=_DESCRIPTION,
        ),
    ]
    BUILDER_CONFIG_CLASS = WikitextTl39Config

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
        if self.config.name == "wikitext-tl-39":
            data_file = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(data_file, "wikitext-tl-39")
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"data_file": os.path.join(data_dir, "test.txt"), "split": "test"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"data_file": os.path.join(data_dir, "train.txt"), "split": "train"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"data_file": os.path.join(data_dir, "valid.txt"), "split": "valid"},
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
