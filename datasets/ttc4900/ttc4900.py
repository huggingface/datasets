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

from __future__ import absolute_import, division, print_function

import csv
import logging
import os

import datasets


_DESCRIPTION = """\
The data set is taken from kemik group
http://www.kemik.yildiz.edu.tr/
The data are pre-processed for the text categorization, collocations are found, character set is corrected, and so forth.
We named TTC4900 by mimicking the name convention of TTC 3600 dataset shared by the study http://journals.sagepub.com/doi/abs/10.1177/0165551515620551
"""

_CITATION = ""
_LICENSE = "CC0: Public Domain"
_HOMEPAGE = "https://www.kaggle.com/savasy/ttc4900"
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

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://www.kaggle.com/savasy/ttc4900,
    and manually download the ttc4900. Once it is completed,
    a file named archive.zip will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to. You then have
    to unzip the file and move 7allV03.csv under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    ttc4900 can then be loaded using the following command `datasets.load_dataset("ttc4900", data_dir="<path/to/folder>")`.
    """

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
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('ttc4900', data_dir=...)` that includes a file name {}. Manual download instructions: {})".format(
                    path_to_manual_file, _FILENAME, self.manual_download_instructions
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(path_to_manual_file, _FILENAME)}
            )
        ]

    def _generate_examples(self, filepath):
        """Generate TTC4900 examples."""
        logging.info("⏳ Generating examples from = %s", filepath)
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
