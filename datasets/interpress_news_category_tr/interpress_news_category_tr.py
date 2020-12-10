# coding=utf-8
# Lint as: python3
"""Turkish News Category Dataset (270K) - Interpress Media Monitoring Company"""

from __future__ import absolute_import, division, print_function

import csv
import logging
import os

import datasets


_DESCRIPTION = """\
It is a Turkish news data set consisting of 273601 news in 17 categories, compiled from print media and news websites between 2010 and 2017 by the Interpress (https://www.interpress.com/) media monitoring company.
"""

_CITATION = ""

_HOMEPAGE = "https://www.interpress.com/"
_DOWNLOAD_URL = "https://www.interpress.com/downloads/interpress_news_category_tr_270k.zip"
_DATASET_URLS = {
    "train": "interpress_news_category_tr_270k_train.tsv",
    "test": "interpress_news_category_tr_270k_test.tsv",
}


class InterpressNewsCategoryTRConfig(datasets.BuilderConfig):
    """BuilderConfig for InterpressNewsCategoryTR."""

    def __init__(self, **kwargs):
        """BuilderConfig for InterpressNewsCategoryTR.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(InterpressNewsCategoryTRConfig, self).__init__(**kwargs)


class InterpressNewsCategoryTR(datasets.GeneratorBasedBuilder):
    """Turkish News Category Dataset (270K) - Interpress Media Monitoring Company"""

    BUILDER_CONFIGS = [
        InterpressNewsCategoryTRConfig(
<<<<<<< HEAD
            name="270k",
=======
            name="interpress_news_category_tr_270k",
>>>>>>> cb6d81ed8e525a403441d067f6246d4cfc070d95
            version=datasets.Version("1.0.0"),
            description="Turkish News Category Dataset (270K) - Interpress Media Monitoring Company",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
<<<<<<< HEAD
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
=======
>>>>>>> cb6d81ed8e525a403441d067f6246d4cfc070d95
                    "category": datasets.features.ClassLabel(
                        names=[
                            "aktuel",
                            "bilisim",
                            "egitim",
                            "ekonomi",
                            "gida",
                            "iletisim",
                            "kultursanat",
                            "magazin",
                            "saglik",
                            "savunma",
                            "seyahat",
                            "siyasi",
                            "spor",
                            "teknoloji",
                            "ticaret",
                            "turizm",
                            "yasam",
                        ]
                    ),
<<<<<<< HEAD
                    "categorycode": datasets.features.ClassLabel(
                        names=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
                    ),
                    "publishdatetime": datasets.Value("string"),
=======
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "publishdatetime": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "categorycode": datasets.Value("string"),
>>>>>>> cb6d81ed8e525a403441d067f6246d4cfc070d95
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_dir, _DATASET_URLS["train"])}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(dl_dir, _DATASET_URLS["test"])}
            ),
        ]

    def _generate_examples(self, filepath):
        """Generate InterpressNewsCategoryTR examples."""
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
<<<<<<< HEAD
=======
            csv.field_size_limit()
>>>>>>> cb6d81ed8e525a403441d067f6246d4cfc070d95
            for idx, row in enumerate(reader):
                yield idx, {
                    "id": row["ID"],
                    "title": row["Title"],
                    "content": row["Content"],
                    "category": row["Category"],
                    "categorycode": row["CategoryCode"],
                    "publishdatetime": row["PublishDateTime"],
                }
