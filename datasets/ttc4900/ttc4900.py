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
"""TTC4900: A Benchmark Data for Turkish Text Categorization"""


import csv

import datasets
from datasets.tasks import TextClassification


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = """\
The data set is taken from kemik group
http://www.kemik.yildiz.edu.tr/
The data are pre-processed for the text categorization, collocations are found, character set is corrected, and so forth.
We named TTC4900 by mimicking the name convention of TTC 3600 dataset shared by the study http://journals.sagepub.com/doi/abs/10.1177/0165551515620551

If you use the dataset in a paper, please refer https://www.kaggle.com/savasy/ttc4900 as footnote and cite one of the papers as follows:

- A Comparison of Different Approaches to Document Representation in Turkish Language, SDU Journal of Natural and Applied Science, Vol 22, Issue 2, 2018
- A comparative analysis of text classification for Turkish language, Pamukkale University Journal of Engineering Science Volume 25 Issue 5, 2018
- A Knowledge-poor Approach to Turkish Text Categorization with a Comparative Analysis, Proceedings of CICLING 2014, Springer LNCS, Nepal, 2014.
"""

_CITATION = """\
@article{doi:10.5505/pajes.2018.15931,
author = {Yıldırım, Savaş and Yıldız, Tuğba},
title = {A comparative analysis of text classification for Turkish language},
journal = {Pamukkale Univ Muh Bilim Derg},
volume = {24},
number = {5},
pages = {879-886},
year = {2018},
doi = {10.5505/pajes.2018.15931},
note ={doi: 10.5505/pajes.2018.15931},

URL = {https://dx.doi.org/10.5505/pajes.2018.15931},
eprint = {https://dx.doi.org/10.5505/pajes.2018.15931}
}
"""

_LICENSE = "CC0: Public Domain"
_HOMEPAGE = "https://www.kaggle.com/savasy/ttc4900"
_DOWNLOAD_URL = "https://raw.githubusercontent.com/savasy/TurkishTextClassification/master"
_FILENAME = "7allV03.csv"


class TTC4900Config(datasets.BuilderConfig):
    """BuilderConfig for TTC4900"""

    def __init__(self, **kwargs):
        """BuilderConfig for TTC4900.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(TTC4900Config, self).__init__(**kwargs)


class TTC4900(datasets.GeneratorBasedBuilder):
    """TTC4900: A Benchmark Data for Turkish Text Categorization"""

    BUILDER_CONFIGS = [
        TTC4900Config(
            name="ttc4900",
            version=datasets.Version("1.0.0"),
            description="A Benchmark Data for Turkish Text Categorization",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "category": datasets.features.ClassLabel(
                        names=["siyaset", "dunya", "ekonomi", "kultur", "saglik", "spor", "teknoloji"]
                    ),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="category")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        urls_to_download = {
            "train": _DOWNLOAD_URL + "/" + _FILENAME,
        }
        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        ]

    def _generate_examples(self, filepath):
        """Generate TTC4900 examples."""
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter=",")
            next(rdr)
            rownum = 0
            for row in rdr:
                rownum += 1
                yield rownum, {
                    "category": row[0],
                    "text": row[1],
                }
