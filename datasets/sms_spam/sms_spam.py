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
"""SMS Spam Collection Data Set"""


import os

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@inproceedings{Almeida2011SpamFiltering,
  title={Contributions to the Study of SMS Spam Filtering: New Collection and Results},
  author={Tiago A. Almeida and Jose Maria Gomez Hidalgo and Akebo Yamakami},
  year={2011},
  booktitle = "Proceedings of the 2011 ACM Symposium on Document Engineering (DOCENG'11)",
}
"""

_DESCRIPTION = """\
The SMS Spam Collection v.1 is a public set of SMS labeled messages that have been collected for mobile phone spam research.
It has one collection composed by 5,574 English, real and non-enconded messages, tagged according being legitimate (ham) or spam.
"""

_DATA_URL = "http://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"


class SmsSpam(datasets.GeneratorBasedBuilder):
    """SMS Spam Collection Data Set"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of SMS Spam Collection Data Set",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sms": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["ham", "spam"]),
                }
            ),
            supervised_keys=("sms", "label"),
            homepage="http://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="sms", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_dir, "SMSSpamCollection")}
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""

        with open(filepath, encoding="utf-8") as sms_file:
            for idx, line in enumerate(sms_file):
                fields = line.split("\t")

                if fields[0] == "ham":
                    label = 0
                else:
                    label = 1

                yield idx, {
                    "sms": fields[1],
                    "label": label,
                }
