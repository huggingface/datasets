"""`prachathai-67k`: News Article Corpus and Multi-label Text Classificdation from Prachathai.com"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{prachathai67k,
  author = {cstorm125, lukkiddd },
  title = {prachathai67k},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished={\\url{https://github.com/PyThaiNLP/prachathai-67k}},
}
"""

_DESCRIPTION = """\
`prachathai-67k`: News Article Corpus and Multi-label Text Classificdation from Prachathai.com
The prachathai-67k dataset was scraped from the news site Prachathai.
We filtered out those articles with less than 500 characters of body text, mostly images and cartoons.
It contains 67,889 articles wtih 12 curated tags from August 24, 2004 to November 15, 2018.
The dataset was originally scraped by @lukkiddd and cleaned by @cstorm125.
You can also see preliminary exploration at https://github.com/PyThaiNLP/prachathai-67k/blob/master/exploration.ipynb
"""


class Prachathai67kConfig(datasets.BuilderConfig):
    """BuilderConfig for Prachathai."""

    def __init__(self, **kwargs):
        """BuilderConfig for Prachathai.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Prachathai67kConfig, self).__init__(**kwargs)


class Prachathai67k(datasets.GeneratorBasedBuilder):
    """`prachathai-67k`: News Article Corpus and Multi-label Text Classificdation from Prachathai.com"""

    _DOWNLOAD_URL = "https://github.com/PyThaiNLP/prachathai-67k/raw/master/data.zip"
    _TRAIN_FILE = "train.jsonl"
    _VAL_FILE = "valid.jsonl"
    _TEST_FILE = "test.jsonl"

    BUILDER_CONFIGS = [
        Prachathai67kConfig(
            name="prachathai67k",
            version=datasets.Version("1.1.0"),
            description="`prachathai-67k`: News Article Corpus and Multi-label Text Classificdation from Prachathai.com",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "url": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "body_text": datasets.Value("string"),
                    "politics": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "human_rights": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "quality_of_life": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "international": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "social": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "environment": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "economics": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "culture": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "labor": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "national_security": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "ict": datasets.features.ClassLabel(names=["neg", "pos"]),
                    "education": datasets.features.ClassLabel(names=["neg", "pos"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/PyThaiNLP/prachathai-67k/",
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
        """Generate examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "url": data["url"],
                    "date": data["date"],
                    "title": data["title"],
                    "body_text": data["body_text"],
                    "politics": data["politics"],
                    "human_rights": data["human_rights"],
                    "quality_of_life": data["quality_of_life"],
                    "international": data["international"],
                    "social": data["social"],
                    "environment": data["environment"],
                    "economics": data["economics"],
                    "culture": data["culture"],
                    "labor": data["labor"],
                    "national_security": data["national_security"],
                    "ict": data["ict"],
                    "education": data["education"],
                }
