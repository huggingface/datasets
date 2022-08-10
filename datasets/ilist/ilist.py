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
"""Indo-Aryan Language Identification Shared Task Dataset"""


import datasets
from datasets.tasks import TextClassification


_CITATION = """\
@proceedings{ws-2018-nlp-similar,
    title = "Proceedings of the Fifth Workshop on {NLP} for Similar Languages, Varieties and Dialects ({V}ar{D}ial 2018)",
    editor = {Zampieri, Marcos  and
      Nakov, Preslav  and
      Ljube{\v{s}}i{\'c}, Nikola  and
      Tiedemann, J{\"o}rg  and
      Malmasi, Shervin  and
      Ali, Ahmed},
    month = aug,
    year = "2018",
    address = "Santa Fe, New Mexico, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-3900",
}
"""

_DESCRIPTION = """\
This dataset is introduced in a task which aimed at identifying 5 closely-related languages of Indo-Aryan language family –
Hindi (also known as Khari Boli), Braj Bhasha, Awadhi, Bhojpuri, and Magahi.
"""

_URL = "https://raw.githubusercontent.com/kmi-linguistics/vardial2018/master/dataset/{}.txt"


class Ilist(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "language_id": datasets.ClassLabel(names=["AWA", "BRA", "MAG", "BHO", "HIN"]),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/kmi-linguistics/vardial2018",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="language_id")],
        )

    def _split_generators(self, dl_manager):
        filepaths = dl_manager.download_and_extract(
            {
                "train": _URL.format("train"),
                "test": _URL.format("gold"),
                "dev": _URL.format("dev"),
            }
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepaths["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepaths["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepaths["dev"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, "r", encoding="utf-8") as file:
            for idx, row in enumerate(file):
                row = row.strip("\n").split("\t")
                if len(row) == 1:
                    continue
                yield idx, {"language_id": row[1], "text": row[0]}
