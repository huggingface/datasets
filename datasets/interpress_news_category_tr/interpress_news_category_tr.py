# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Lint as: python3
"""Turkish News Category Dataset (270K) - Interpress Media Monitoring Company"""


import csv
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = """\
It is a Turkish news data set consisting of 273601 news in 17 categories, compiled from print media and news websites between 2010 and 2017 by the Interpress (https://www.interpress.com/) media monitoring company.
"""

_CITATION = ""
_LICENSE = "unknown"
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
            name="270k",
            version=datasets.Version("1.0.0"),
            description="Turkish News Category Dataset (270K) - Interpress Media Monitoring Company",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
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
                    "categorycode": datasets.features.ClassLabel(num_classes=17),
                    "publishdatetime": datasets.Value("string"),
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
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                yield idx, {
                    "id": row["ID"],
                    "title": row["Title"],
                    "content": row["Content"],
                    "category": row["Category"],
                    "categorycode": row["CategoryCode"],
                    "publishdatetime": row["PublishDateTime"],
                }
