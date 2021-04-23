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
"""Korean pairwise question binary classification dataset"""


import datasets


_CITATION = """\
@misc{Song:2018,
  title     = "Paired Question v.2",
  authors   = "Youngsook Song",
  publisher = "GitHub",
  year      = "2018"
}
"""


_DESCRIPTION = """\
This is a Korean paired question dataset containing labels indicating whether two questions in a given pair are semantically identical. This dataset was used to evaluate the performance of [KoGPT2](https://github.com/SKT-AI/KoGPT2#subtask-evaluations) on a phrase detection downstream task.
"""


_HOMEPAGE = "https://github.com/songys/Question_pair"

_LICENSE = "The MIT License (MIT)"

_URL = "https://raw.githubusercontent.com/songys/Question_pair/master/"
_URLs = {key: f"{_URL}{key}.txt" for key in ("train", "test", "validation")}


class KorQpair(datasets.GeneratorBasedBuilder):
    """Korean pairwise question classification dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "question1": datasets.Value("string"),
                    "question2": datasets.Value("string"),
                    "is_duplicate": datasets.ClassLabel(names=["0", "1"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        downloaded_files = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_files["validation"],
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            next(f)
            for id_, row in enumerate(f):
                row = row.strip().split("\t")
                yield id_, {
                    "question1": row[0],
                    "question2": row[1],
                    "is_duplicate": row[2],
                }
