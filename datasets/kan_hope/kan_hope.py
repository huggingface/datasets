# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Kannada Hope Speech Dataset"""


import csv

import datasets


_CITATION = """\
@misc{hande2021hope,
      title={Hope Speech detection in under-resourced Kannada language},
      author={Adeep Hande and Ruba Priyadharshini and Anbukkarasi Sampath and Kingston Pal Thamburaj and Prabakaran Chandran and Bharathi Raja Chakravarthi},
      year={2021},
      eprint={2108.04616},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Numerous methods have been developed to monitor the spread of negativity in modern years by
eliminating vulgar, offensive, and fierce comments from social media platforms. However, there are relatively
lesser amounts of study that converges on embracing positivity, reinforcing supportive and reassuring content in online forums.
Consequently, we propose creating an English Kannada Hope speech dataset, KanHope and comparing several experiments to benchmark the dataset.
The dataset consists of 6,176 user generated comments in code mixed Kannada scraped from YouTube and manually annotated as bearing hope
speech or Not-hope speech.
This dataset was prepared for hope-speech text classification benchmark on code-mixed Kannada, an under-resourced language.
"""

_HOMEPAGE = "https://github.com/adeepH/kan_hope"

_LICENSE = "Creative Commons Attribution 4.0 International Licence"

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/adeepH/kan_hope/main/dataset/KanHope_train.csv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/adeepH/kan_hope/main/dataset/KanHope_test.csv"


class kan_hope(datasets.GeneratorBasedBuilder):
    """Code-Mixed Kannada Hope Speech Dataset"""

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["Not-Hope", "Hope"]),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
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
        """Generate Kannada Hope Speech examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            next(reader, None)
            for id_, row in enumerate(reader):
                dummy, text, label = row
                yield id_, {"text": text, "label": label}
