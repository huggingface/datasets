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
"""DKTC(Dataset of Korean Threatening Conversations) Dataset"""

import pandas as pd

import datasets


_CITATION = """
@misc{DKTC
  author       = {Cho, Soyoung and Ha, Sangchun and Ryu, Myeonghyeon and
                  Keum, Bitna and Park, Kyubyong},
  title        = {DKTC, Dataset of Korean Threatening Conversations},
  howpublished = {https://github.com/tunib-ai/DKTC},
  year         = {2022},
}
"""

_DESCRIPTION = """
It is a Korean dataset that classifies threatening conversation data into four threat situations. 

- 0: threat
- 1: extortion
- 2: workspace
- 3: etc
"""

_HOMEPAGE = "https://github.com/tunib-ai/DKTC"

_LICENSE = "CC-BY-NC-SA 4.0 License."

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/tunib-ai/DKTC/main/data/train.csv"


class Dktc(datasets.GeneratorBasedBuilder):
    """Dataset of Korean Threatening Conversations"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):

        features = datasets.Features(
            {
                "class": datasets.ClassLabel(names=["threat", "extortion", "workspace", "etc"]),
                "text": datasets.Value("string"),
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
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        convert_dict = {
            "협박 대화": 0,
            "갈취 대화": 1,
            "직장 내 괴롭힘 대화": 2,
            "기타 괴롭힘 대화": 3,
        }

        df = pd.read_csv(filepath, encoding="utf-8")

        for idx, (text, class_name) in enumerate(zip(df["conversation"], df["class"])):
            if pd.isna(text):
                continue
            yield idx, {
                "class": convert_dict[class_name],
                "text": text,
            }
