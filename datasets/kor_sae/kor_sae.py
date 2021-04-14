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
"""Structured Argument Extraction for Korean"""


import csv

import datasets


_CITATION = """\
@article{cho2019machines,
  title={Machines Getting with the Program: Understanding Intent Arguments of Non-Canonical Directives},
  author={Cho, Won Ik and Moon, Young Ki and Moon, Sangwhan and Kim, Seok Min and Kim, Nam Soo},
  journal={arXiv preprint arXiv:1912.00342},
  year={2019}
}
"""

_DESCRIPTION = """\
This new dataset is designed to extract intent from non-canonical directives which will help dialog managers
extract intent from user dialog that may have no clear objective or are paraphrased forms of utterances.
"""

_HOMEPAGE = "https://github.com/warnikchow/sae4k"

_LICENSE = "CC-BY-SA-4.0"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/warnikchow/sae4k/master/data/sae4k_v1.txt"


class KorSae(datasets.GeneratorBasedBuilder):
    """Structured Argument Extraction for Korean"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "intent_pair1": datasets.Value("string"),
                    "intent_pair2": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "yes/no",
                            "alternative",
                            "wh- questions",
                            "prohibitions",
                            "requirements",
                            "strong requirements",
                        ]
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate KorSAE examples"""

        with open(filepath, encoding="utf-8") as csv_file:
            data = csv.reader(csv_file, delimiter="\t")
            for id_, row in enumerate(data):
                intent_pair1, intent_pair2, label = row
                yield id_, {"intent_pair1": intent_pair1, "intent_pair2": intent_pair2, "label": int(label)}
