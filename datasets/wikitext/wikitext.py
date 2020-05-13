"""TODO(wikitext): Add a description here."""

from __future__ import absolute_import, division, print_function

import os

import nlp


# TODO(wikitext): BibTeX citation
_CITATION = """\
@InProceedings{wikitext,
    author={Stephen, Merity and Caiming ,Xiong and James, Bradbury and Richard Socher}
    year=2016
}
"""

# TODO(wikitext):
_DESCRIPTION = """\
 The WikiText language modeling dataset is a collection of over 100 million tokens extracted from the set of verified 
 Good and Featured articles on Wikipedia. The dataset is available under the Creative Commons Attribution-ShareAlike License.
"""
_URL = "https://blog.einstein.ai/the-wikitext-long-term-dependency-language-modeling-dataset/"
_DATA_URL = "https://s3.amazonaws.com/research.metamind.io/wikitext"


class WikitextConfig(nlp.BuilderConfig):
    """BuilderConfig for GLUE."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for Wikitext

    Args:
      data_url: `string`, url to the dataset (word or raw level)
      **kwargs: keyword arguments forwarded to super.
    """
        super(WikitextConfig, self).__init__(version=nlp.Version("1.0.0",), **kwargs)
        self.data_url = data_url


class Wikitext(nlp.GeneratorBasedBuilder):
    """TODO(wikitext_103): Short description of my dataset."""

    # TODO(wikitext_103): Set up version.
    VERSION = nlp.Version("0.1.0")
    BUILDER_CONFIGS = [
        WikitextConfig(
            name="wikitext-103-raw-v1",
            data_url=_DATA_URL + "/" + "wikitext-103-raw-v1.zip",
            description="word level dataset. No processing is needed other than replacing newlines with <eos> tokens.",
        ),
        WikitextConfig(
            name="wikitext-2-raw-v1",
            data_url=_DATA_URL + "/" + "wikitext-2-raw-v1.zip",
            description="word level dataset. No processing is needed other than replacing newlines with <eos> tokens.",
        ),
        WikitextConfig(
            name="wikitext-103-v1",
            data_url=_DATA_URL + "/" + "wikitext-103-v1.zip",
            description="raw level dataset. The raw tokens before the addition of <unk> tokens. "
            "They should only be used for character level work or for creating newly derived datasets.",
        ),
        WikitextConfig(
            name="wikitext-2-v1",
            data_url=_DATA_URL + "/" + "wikitext-2-v1.zip",
            description="raw level dataset. The raw tokens before the addition of <unk> tokens. "
            "They should only be used for character level work or for creating newly derived datasets.",
        ),
    ]

    def _info(self):
        # TODO(wikitext): Specifies the nlp.DatasetInfo object
        return nlp.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # nlp.features.FeatureConnectors
            features=nlp.Features(
                {
                    "text": nlp.Value("string")
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
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(wikitext): Downloads the data and defines the splits
        # dl_manager is a nlp.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name == "wikitext-103-v1":
            data_file = dl_manager.download_and_extract(self.config.data_url)
            data_dir = os.path.join(data_file, "wikitext-103")
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    gen_kwargs={"data_file": os.path.join(data_dir, "wiki.test.tokens"), "split": "test"},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    gen_kwargs={"data_file": os.path.join(data_dir, "wiki.train.tokens"), "split": "train"},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.VALIDATION,
                    gen_kwargs={"data_file": os.path.join(data_dir, "wiki.valid.tokens"), "split": "valid"},
                ),
            ]
        else:
            if self.config.name == "wikitext-103-raw-v1":
                data_file = dl_manager.download_and_extract(self.config.data_url)
                data_dir = os.path.join(data_file, "wikitext-103-raw")
                return [
                    nlp.SplitGenerator(
                        name=nlp.Split.TEST,
                        gen_kwargs={"data_file": os.path.join(data_dir, "wiki.test.raw"), "split": "test"},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.TRAIN,
                        gen_kwargs={"data_file": os.path.join(data_dir, "wiki.train.raw"), "split": "train"},
                    ),
                    nlp.SplitGenerator(
                        name=nlp.Split.VALIDATION,
                        gen_kwargs={"data_file": os.path.join(data_dir, "wiki.valid.raw"), "split": "valid"},
                    ),
                ]
            else:
                if self.config.name == "wikitext-2-raw-v1":
                    data_file = dl_manager.download_and_extract(self.config.data_url)
                    data_dir = os.path.join(data_file, "wikitext-2-raw")
                    return [
                        nlp.SplitGenerator(
                            name=nlp.Split.TEST,
                            gen_kwargs={"data_file": os.path.join(data_dir, "wiki.test.raw"), "split": "test"},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.TRAIN,
                            gen_kwargs={"data_file": os.path.join(data_dir, "wiki.train.raw"), "split": "train"},
                        ),
                        nlp.SplitGenerator(
                            name=nlp.Split.VALIDATION,
                            gen_kwargs={"data_file": os.path.join(data_dir, "wiki.valid.raw"), "split": "valid"},
                        ),
                    ]
                else:
                    if self.config.name == "wikitext-2-v1":
                        data_file = dl_manager.download_and_extract(self.config.data_url)
                        data_dir = os.path.join(data_file, "wikitext-2")
                        return [
                            nlp.SplitGenerator(
                                name=nlp.Split.TEST,
                                gen_kwargs={"data_file": os.path.join(data_dir, "wiki.test.tokens"), "split": "test"},
                            ),
                            nlp.SplitGenerator(
                                name=nlp.Split.TRAIN,
                                gen_kwargs={
                                    "data_file": os.path.join(data_dir, "wiki.train.tokens"),
                                    "split": "train",
                                },
                            ),
                            nlp.SplitGenerator(
                                name=nlp.Split.VALIDATION,
                                gen_kwargs={
                                    "data_file": os.path.join(data_dir, "wiki.valid.tokens"),
                                    "split": "valid",
                                },
                            ),
                        ]

    def _generate_examples(self, data_file, split):

        """Yields examples."""
        # TODO(wikitext): Yields (key, example) tuples from the dataset
        # print(data_file)
        # print('=='*100)
        with open(data_file) as f:
            for idx, row in enumerate(f):
                if row.strip():
                    yield idx, {"text": row}
                else:
                    yield idx, {"text": ""}
