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
"""Dataset of 10065 tweets in Arabic for Emotion detection in Arabic text """


import csv

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@inbook{inbook,
author = {Al-Khatib, Amr and El-Beltagy, Samhaa},
year = {2018},
month = {01},
pages = {105-114},
title = {Emotional Tone Detection in Arabic Tweets: 18th International Conference, CICLing 2017, Budapest, Hungary, April 17–23, 2017, Revised Selected Papers, Part II},
isbn = {978-3-319-77115-1},
doi = {10.1007/978-3-319-77116-8_8}
}
"""


_DESCRIPTION = """\
Dataset of 10065 tweets in Arabic for Emotion detection in Arabic text"""


_HOMEPAGE = "https://github.com/AmrMehasseb/Emotional-Tone"


_DOWNLOAD_URL = "https://raw.githubusercontent.com/AmrMehasseb/Emotional-Tone/master/Emotional-Tone-Dataset.csv"


class EmotoneAr(datasets.GeneratorBasedBuilder):
    """Dataset of 10065 tweets in Arabic for Emotions detection in Arabic text"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tweet": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=["none", "anger", "joy", "sadness", "love", "sympathy", "surprise", "fear"]
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="tweet", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": data_dir})]

    def _generate_examples(self, filepath):
        """Generate labeled arabic tweets examples for emoptions detection."""
        with open(filepath, encoding="utf-8", mode="r") as csv_file:
            next(csv_file)  # skip header
            csv_reader = csv.reader(csv_file, quotechar='"', delimiter=",")

            for id_, row in enumerate(csv_reader):
                _, tweet, label = row
                yield id_, {"tweet": tweet, "label": label}
