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


import csv
import os

import datasets


# no BibTeX citation
_CITATION = ""

_DESCRIPTION = """\
The Kannada news dataset contains only the headlines of news article in three categories:
Entertainment, Tech, and Sports.

The data set contains around 6300 news article headlines which collected from Kannada news websites.
The data set has been cleaned and contains train and test set using which can be used to benchmark
classification models in Kannada.
"""

_LICENSE = "CC BY-SA 4.0"
_TRAIN_FILENAME = "train.csv"
_VALID_FILENAME = "valid.csv"


class KannadaNews(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
    \n    You need to go to https://www.kaggle.com/disisbig/kannada-news-dataset,
    and manually download the dataset from Kaggle. Once it is completed,
    a folder named archive.zip will appear in your Downloads folder(
    or whichever folder your browser chooses to save files to). Unzip the folder to obtain
    a folder named "archive" having train.csv and valid.csv.

    You can then specify the path to this folder for the data_dir argument in the
    datasets.load_dataset(...) option.

    The <path/to/folder> can e.g. be "/Downloads/archive".
    The data can then be loaded using the following command `datasets.load_dataset("kannada_news", data_dir="/Downloads/archive")`.
    """

    def _info(self):
        class_names = ["sports", "tech", "entertainment"]
        features = datasets.Features(
            {
                "headline": datasets.Value("string"),
                "label": datasets.ClassLabel(names=class_names),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('kannada_news', data_dir=...)` that includes a file name {_TRAIN_FILENAME}. Manual download instructions: {self.manual_download_instructions})"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, _TRAIN_FILENAME),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, _VALID_FILENAME),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter=",")
            next(rdr)
            rownum = 0
            for row in rdr:
                rownum += 1
                yield rownum, {
                    "headline": row[0],
                    "label": row[1],
                }
