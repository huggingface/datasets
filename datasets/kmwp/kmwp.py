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
"""KMWP (Korean Math Word Problems) Dataset"""

import pandas as pd

import datasets


_CITATION = """
@misc{KMWP
  author       = {Keum, Bitna and Ryu, Myeonghyeon and Ham, Yoseph and Seo, Minsuh and 
                  Jo, Heechang and Kim, Hangyeol and Park, Kyubyong},
  title        = {KMWP, Korean Math Word Problems},
  howpublished = {https://github.com/tunib-ai/KMWP},
  year         = {2022},
}
"""

_DESCRIPTION = """\
A dataset in which Python codes corresponding to math problems and solutions in Korean are paired.
It consists of 8 types, see https://github.com/tunib-ai/KMWP for more information.
"""

_HOMEPAGE = "https://github.com/tunib-ai/KMWP"

_LICENSE = "CC-BY-NC-SA 4.0 License."

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/tunib-ai/KMWP/main/data/train.csv"


class Kmwp(datasets.GeneratorBasedBuilder):
    """Korean Math Word Problems"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):

        features = datasets.Features(
            {
                "class": datasets.Value("int32"),
                "problem": datasets.Value("string"),
                "code": datasets.Value("string"),
                "answer": datasets.Value("string"),
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
        df = pd.read_csv(filepath, encoding="utf-8")

        for id_, (class_, problem, code, answer) in enumerate(
            zip(df["class"], df["problem"], df["code"], df["answer"])
        ):
            yield id_, {"class": class_, "problem": problem, "code": code, "answer": answer}
