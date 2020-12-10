# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Hotel Reviews in Arabic language"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_DESCRIPTION = """\
This dataset contains 93700 hotel reviews in Arabic language.\
The hotel reviews were collected from Booking.com website during June/July 2016.\
The reviews are expressed in Modern Standard Arabic as well as dialectal Arabic.\
The following table summarize some tatistics on the HARD Dataset.
"""

_CITATION = """\
@incollection{elnagar2018hotel,
  title={Hotel Arabic-reviews dataset construction for sentiment analysis applications},
  author={Elnagar, Ashraf and Khalifa, Yasmin S and Einea, Anas},
  booktitle={Intelligent Natural Language Processing: Trends and Applications},
  pages={35--52},
  year={2018},
  publisher={Springer}
}
"""

_DOWNLOAD_URL = "https://raw.githubusercontent.com/elnagara/HARD-Arabic-Dataset/master/data/balanced-reviews.zip"


class HardConfig(datasets.BuilderConfig):
    """BuilderConfig for Hard."""

    def __init__(self, **kwargs):
        """BuilderConfig for Hard.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(HardConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Hard(datasets.GeneratorBasedBuilder):
    """Hard dataset."""

    BUILDER_CONFIGS = [
        HardConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "1",
                            "2",
                            "3",
                            "4",
                            "5",
                        ]
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/elnagara/HARD-Arabic-Dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "balanced-reviews.txt")}
            ),
        ]

    def _generate_examples(self, directory):
        """Generate examples."""
        with open(directory, mode="r", encoding="utf-16") as file:
            for id_, line in enumerate(file.read().splitlines()[1:]):
                _, _, rating, _, _, _, review_text = line.split("\t")
                yield str(id_), {"text": review_text, "label": rating}
