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
"""Bengali Hate Speech Dataset"""


import csv

import datasets


_CITATION = """\
@misc{karim2020classification,
      title={Classification Benchmarks for Under-resourced Bengali Language based on Multichannel Convolutional-LSTM Network},
      author={Md. Rezaul Karim and Bharathi Raja Chakravarthi and John P. McCrae and Michael Cochez},
      year={2020},
      eprint={2004.07807},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The Bengali Hate Speech Dataset is a collection of Bengali articles collected from Bengali news articles,
news dump of Bengali TV channels, books, blogs, and social media. Emphasis was placed on Facebook pages and
newspaper sources because they attract close to 50 million followers and is a common source of opinions
and hate speech. The raw text corpus contains 250 million articles and the full dataset is being prepared
for release. This is a subset of the full dataset.

This dataset was prepared for hate-speech text classification benchmark on Bengali, an under-resourced language.
"""

_HOMEPAGE = "https://github.com/rezacsedu/Bengali-Hate-Speech-Dataset"

_LICENSE = "MIT License"

_URL = "https://raw.githubusercontent.com/rezacsedu/Bengali-Hate-Speech-Dataset/main/bengali_%20hate_v1.0.csv"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class BnHateSpeech(datasets.GeneratorBasedBuilder):
    """Bengali Hate Speech Dataset"""

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "label": datasets.features.ClassLabel(
                    names=["Personal", "Political", "Religious", "Geopolitical", "Gender abusive"]
                ),
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
        """Returns SplitGenerators."""

        train_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Bengali Hate Speech examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file, delimiter="\t")
            next(reader, None)
            for id_, row in enumerate(reader):
                text, label = row
                yield id_, {"text": text, "label": label}
