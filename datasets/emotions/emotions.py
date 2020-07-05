from __future__ import absolute_import, division, print_function

import pickle
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
Emotions is a dataset of English Twitter messages with eight basic emotions: anger, anticipation,
disgust, fear, joy, sadness, surprise, and trust. For more detailed information please refer to the
paper.
"""
_URL = "https://github.com/dair-ai/emotion_dataset"
_DATA_URL = "https://www.dropbox.com/s/607ptdakxuh5i4s/merged_training.pkl"


class EmotionsConfig(nlp.BuilderConfig):

    """BuilderConfig for Break"""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for BlogAuthorship

        Args:
          data_url: `string`, url to the dataset (word or raw level)
          **kwargs: keyword arguments forwarded to super.
        """
        super(EmotionsConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )
        self.data_url = data_url


class Emotions(nlp.GeneratorBasedBuilder):

    VERSION = nlp.Version("0.3.0")
    BUILDER_CONFIGS = [
        EmotionsConfig(
            name="emotions",
            data_url=_DATA_URL,
            description="Emotions classification dataset. Twitter messages are classified as either anger, anticipation, disgust, fear, joy, sadness, surprise, or trust",
        )
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "emotions": nlp.Value("string")
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        arch_path = dl_manager.download_and_extract(_DATA_URL)
        data_dir = os.path.join(arch_path, "emotions_data")
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"file_path": os.path.join(data_dir, "train")}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"file_path": os.path.join(data_dir, "test")})
        ]

    def _generate_examples(self, file_path):
        """Yields examples."""

        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            for row_id, row in enumerate(data):
                text, emotion = row
                yield "{}".format(row_id), {
                    "text": text,
                    "emotion": emotion
                }
