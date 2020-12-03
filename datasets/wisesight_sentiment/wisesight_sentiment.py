"""Wisesight Sentiment Corpus: Social media messages in Thai language with sentiment category (positive, neutral, negative, question)"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@software{bact_2019_3457447,
  author       = {Suriyawongkul, Arthit and
                  Chuangsuwanich, Ekapol and
                  Chormai, Pattarawat and
                  Polpanumas, Charin},
  title        = {PyThaiNLP/wisesight-sentiment: First release},
  month        = sep,
  year         = 2019,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.3457447},
  url          = {https://doi.org/10.5281/zenodo.3457447}
}
"""

_DESCRIPTION = """\
Wisesight Sentiment Corpus: Social media messages in Thai language with sentiment category (positive, neutral, negative, question)
* Released to public domain under Creative Commons Zero v1.0 Universal license.
* Category (Labels): {"pos": 0, "neu": 1, "neg": 2, "q": 3}
* Size: 26,737 messages
* Language: Central Thai
* Style: Informal and conversational. With some news headlines and advertisement.
* Time period: Around 2016 to early 2019. With small amount from other period.
* Domains: Mixed. Majority are consumer products and services (restaurants, cosmetics, drinks, car, hotels), with some current affairs.
* Privacy:
    * Only messages that made available to the public on the internet (websites, blogs, social network sites).
    * For Facebook, this means the public comments (everyone can see) that made on a public page.
    * Private/protected messages and messages in groups, chat, and inbox are not included.
* Alternations and modifications:
    * Keep in mind that this corpus does not statistically represent anything in the language register.
    * Large amount of messages are not in their original form. Personal data are removed or masked.
    * Duplicated, leading, and trailing whitespaces are removed. Other punctuations, symbols, and emojis are kept intact.
    (Mis)spellings are kept intact.
    * Messages longer than 2,000 characters are removed.
    * Long non-Thai messages are removed. Duplicated message (exact match) are removed.
* More characteristics of the data can be explore: https://github.com/PyThaiNLP/wisesight-sentiment/blob/master/exploration.ipynb
"""


class WisesightSentimentConfig(datasets.BuilderConfig):
    """BuilderConfig for WisesightSentiment."""

    def __init__(self, **kwargs):
        """BuilderConfig for WisesightSentiment.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(WisesightSentimentConfig, self).__init__(**kwargs)


class WisesightSentiment(datasets.GeneratorBasedBuilder):
    """Wisesight Sentiment Corpus: Social media messages in Thai language with sentiment category (positive, neutral, negative, question)"""

    _DOWNLOAD_URL = "https://github.com/PyThaiNLP/wisesight-sentiment/raw/master/huggingface/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "valid.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        WisesightSentimentConfig(
            name="wisesight_sentiment",
            version=datasets.Version("1.0.0"),
            description="Wisesight Sentiment Corpus: Social media messages in Thai language with sentiment category (positive, neutral, negative, question)",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "texts": datasets.Value("string"),
                    "category": datasets.features.ClassLabel(names=["pos", "neu", "neg", "q"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/PyThaiNLP/wisesight-sentiment",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(self._DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TRAIN_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, self._VAL_FILE)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, self._TEST_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate WisesightSentiment examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                texts = data["texts"]
                category = data["category"]
                yield id_, {"texts": texts, "category": category}
