"""Allocine Dataset: A Large-Scale French Movie Reviews Dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


_CITATION = """\
@misc{blard2019allocine,
  author = {Blard, Theophile},
  title = {french-sentiment-analysis-with-bert},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished={\\url{https://github.com/TheophileBlard/french-sentiment-analysis-with-bert}},
}
"""

_DESCRIPTION = """\
 Allocine Dataset: A Large-Scale French Movie Reviews Dataset.
 This is a dataset for binary sentiment classification, made of user reviews scraped from Allocine.fr.
 It contains 100k positive and 100k negative reviews divided into 3 balanced splits: train (160k reviews), val (20k) and test (20k).
"""


class AllocineConfig(nlp.BuilderConfig):
    """BuilderConfig for Allocine."""

    def __init__(self, **kwargs):
        """BuilderConfig for Allocine.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(AllocineConfig, self).__init__(**kwargs)


class AllocineDataset(nlp.GeneratorBasedBuilder):
    """Allocine Dataset: A Large-Scale French Movie Reviews Dataset."""

    _DOWNLOAD_URL = "https://github.com/TheophileBlard/french-sentiment-analysis-with-bert/raw/master/allocine_dataset/data.tar.bz2"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "val.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        AllocineConfig(
            name="allocine",
            version=nlp.Version("1.0.0"),
            description="Allocine Dataset: A Large-Scale French Movie Reviews Dataset",
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {"review": nlp.Value("string"), "label": nlp.features.ClassLabel(names=["neg", "pos"]),}
            ),
            supervised_keys=None,
            homepage="https://github.com/TheophileBlard/french-sentiment-analysis-with-bert",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)}
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(data_dir, self._VAL_FILE)}
            ),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FILE)}),
        ]

    def _generate_examples(self, filepath):
        """Generate Allocine examples."""
        with open(filepath) as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                review = data["review"]
                label = "neg" if data["polarity"] == 0 else "pos"
                yield id_, {"review": review, "label": label}
