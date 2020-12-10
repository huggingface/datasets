from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


csv.field_size_limit(int(1e6))  # to accommodate large fields


_CITATION = """\
@mastersthesis{chumpolsathien_2020,
    title={Using Knowledge Distillation from Keyword Extraction to Improve the Informativeness of Neural Cross-lingual Summarization},
    author={Chumpolsathien, Nakhun},
    year={2020},
    school={Beijing Institute of Technology}
"""

_DESCRIPTION = """\
ThaiSum is a large-scale corpus for Thai text summarization obtained from several online news websites namely Thairath,
ThaiPBS, Prachathai, and The Standard. This dataset consists of over 350,000 article and summary pairs
written by journalists.
"""


class ThaiSumConfig(datasets.BuilderConfig):
    """BuilderConfig for ThaiSum."""

    def __init__(self, **kwargs):
        """BuilderConfig for ThaiSum.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ThaiSumConfig, self).__init__(**kwargs)


class Thaisum(datasets.GeneratorBasedBuilder):
    """ThaiSum: The largest dataset for Thai text summarization"""

    _DOWNLOAD_URL = "https://archive.org/download/thaisum_datasets/data.zip"
    _TRAIN_FILE = "train.csv"
    _VAL_FILE = "valid.csv"
    _TEST_FILE = "test.csv"

    BUILDER_CONFIGS = [
        ThaiSumConfig(
            name="thaisum",
            version=datasets.Version("1.0.0"),
            description="ThaiSum: The largest dataset for Thai text summarization",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "summary": datasets.Value("string"),
                    "type": datasets.Value("string"),
                    "tags": datasets.Value("string"),
                    "url": datasets.Value("string"),
                }
            ),
            supervised_keys=("body", "summary"),
            homepage="https://github.com/nakhunchumpolsathien/ThaiSum",
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
            csv_reader = csv.reader(f)
            next(csv_reader)  # skip header
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "title": row[0],
                    "body": row[1],
                    "summary": row[2],
                    "type": row[3],
                    "tags": row[4],
                    "url": row[5],
                }
