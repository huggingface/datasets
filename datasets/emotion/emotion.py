from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


_CITATION = """\
@inproceedings{saravia-etal-2018-carer,
    title = "{CARER}: Contextualized Affect Representations for Emotion Recognition",
    author = "Saravia, Elvis  and
      Liu, Hsien-Chi Toby  and
      Huang, Yen-Hao  and
      Wu, Junlin  and
      Chen, Yi-Shin",
    booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
    month = oct # "-" # nov,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D18-1404",
    doi = "10.18653/v1/D18-1404",
    pages = "3687--3697",
    abstract = "Emotions are expressed in nuanced ways, which varies by collective or individual experiences, knowledge, and beliefs. Therefore, to understand emotion, as conveyed through text, a robust mechanism capable of capturing and modeling different linguistic nuances and phenomena is needed. We propose a semi-supervised, graph-based algorithm to produce rich structural descriptors which serve as the building blocks for constructing contextualized affect representations from text. The pattern-based representations are further enriched with word embeddings and evaluated through several emotion recognition tasks. Our experimental results demonstrate that the proposed method outperforms state-of-the-art techniques on emotion recognition tasks.",
}
"""

_DESCRIPTION = """\
Emotion is a dataset of English Twitter messages with eight basic emotions: anger, anticipation,
disgust, fear, joy, sadness, surprise, and trust. For more detailed information please refer to the
paper.
"""
_URL = "https://github.com/dair-ai/emotion_dataset"
# use dl=1 to force browser to download data instead of displaying it
_TRAIN_DOWNLOAD_URL = "https://www.dropbox.com/s/1pzkadrvffbqw6o/train.txt?dl=1"
_VALIDATION_DOWNLOAD_URL = "https://www.dropbox.com/s/2mzialpsgf9k5l3/val.txt?dl=1"
_TEST_DOWNLOAD_URL = "https://www.dropbox.com/s/ikkqxfdbdec3fuj/test.txt?dl=1"


class Emotion(nlp.GeneratorBasedBuilder):
    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"text": nlp.Value("string"), "label": nlp.Value("string")}),
            supervised_keys=("text", "label"),
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        valid_path = dl_manager.download_and_extract(_VALIDATION_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate examples."""
        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=";")
            for id_, row in enumerate(csv_reader):
                text, label = row
                yield id_, {"text": text, "label": label}
