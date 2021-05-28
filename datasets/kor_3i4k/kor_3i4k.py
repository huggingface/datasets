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
"""3i4K: Intonation-aided intention identification for Korean dataset"""


import csv

import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@article{cho2018speech,
    title={Speech Intention Understanding in a Head-final Language: A Disambiguation Utilizing Intonation-dependency},
    author={Cho, Won Ik and Lee, Hyeon Seung and Yoon, Ji Won and Kim, Seok Min and Kim, Nam Soo},
    journal={arXiv preprint arXiv:1811.04231},
    year={2018}
}
"""

_DESCRIPTION = """\
This dataset is designed to identify speaker intention based on real-life spoken utterance in Korean into one of
7 categories: fragment, description, question, command, rhetorical question, rhetorical command, utterances.
"""

_HOMEPAGE = "https://github.com/warnikchow/3i4k"

_LICENSE = "CC BY-SA-4.0"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/warnikchow/3i4k/master/data/train_val_test/fci_train_val.txt"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/warnikchow/3i4k/master/data/train_val_test/fci_test.txt"


class Kor_3i4k(datasets.GeneratorBasedBuilder):
    """Intonation-aided intention identification for Korean"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "label": datasets.features.ClassLabel(
                        names=[
                            "fragment",
                            "statement",
                            "question",
                            "command",
                            "rhetorical question",
                            "rhetorical command",
                            "intonation-dependent utterance",
                        ]
                    ),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators"""

        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generates 3i4K examples"""

        with open(filepath, encoding="utf-8") as csv_file:
            data = csv.reader(csv_file, delimiter="\t")
            for id_, row in enumerate(data):
                label, text = row
                yield id_, {"label": int(label), "text": text}
