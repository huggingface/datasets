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
"""The COmmonsense Dataset Adversarially-authored by Humans (CODAH)"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_CITATION = """\
@inproceedings{chen2019codah,
  title={CODAH: An Adversarially-Authored Question Answering Dataset for Common Sense},
  author={Chen, Michael and D'Arcy, Mike and Liu, Alisa and Fernandez, Jared and Downey, Doug},
  booktitle={Proceedings of the 3rd Workshop on Evaluating Vector Space Representations for NLP},
  pages={63--69},
  year={2019}
}
"""

_DESCRIPTION = """\
The COmmonsense Dataset Adversarially-authored by Humans (CODAH) is an evaluation set for commonsense \
question-answering in the sentence completion style of SWAG. As opposed to other automatically \
generated NLI datasets, CODAH is adversarially constructed by humans who can view feedback \
from a pre-trained model and use this information to design challenging commonsense questions. \
Our experimental results show that CODAH questions present a complementary extension to the SWAG dataset, testing additional modes of common sense.
"""

_URL = "https://raw.githubusercontent.com/Websail-NU/CODAH/master/data/"
_FULL_DATA_URL = _URL + "full_data.tsv"

QUESTION_CATEGORIES_MAPPING = {
    "i": "Idioms",
    "r": "Reference",
    "p": "Polysemy",
    "n": "Negation",
    "q": "Quantitative",
    "o": "Others",
}


class CodahConfig(datasets.BuilderConfig):
    """BuilderConfig for CODAH."""

    def __init__(self, fold=None, **kwargs):
        """BuilderConfig for CODAH.

        Args:
          fold: `string`, official cross validation fold.
          **kwargs: keyword arguments forwarded to super.
        """
        super(CodahConfig, self).__init__(**kwargs)
        self.fold = fold


class Codah(datasets.GeneratorBasedBuilder):
    """The COmmonsense Dataset Adversarially-authored by Humans (CODAH)"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        CodahConfig(name="codah", version=datasets.Version("1.0.0"), description="Full CODAH dataset", fold=None),
        CodahConfig(
            name="fold_0", version=datasets.Version("1.0.0"), description="Official CV split (fold_0)", fold="fold_0"
        ),
        CodahConfig(
            name="fold_1", version=datasets.Version("1.0.0"), description="Official CV split (fold_1)", fold="fold_1"
        ),
        CodahConfig(
            name="fold_2", version=datasets.Version("1.0.0"), description="Official CV split (fold_2)", fold="fold_2"
        ),
        CodahConfig(
            name="fold_3", version=datasets.Version("1.0.0"), description="Official CV split (fold_3)", fold="fold_3"
        ),
        CodahConfig(
            name="fold_4", version=datasets.Version("1.0.0"), description="Official CV split (fold_4)", fold="fold_4"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "question_category": datasets.features.ClassLabel(
                        names=["Idioms", "Reference", "Polysemy", "Negation", "Quantitative", "Others"]
                    ),
                    "question_propmt": datasets.Value("string"),
                    "candidate_answers": datasets.features.Sequence(datasets.Value("string")),
                    "correct_answer_idx": datasets.Value("int32"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/Websail-NU/CODAH",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "codah":
            data_file = dl_manager.download(_FULL_DATA_URL)
            return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_file": data_file})]

        base_url = f"{_URL}cv_split/{self.config.fold}/"
        _urls = {
            "train": base_url + "train.tsv",
            "dev": base_url + "dev.tsv",
            "test": base_url + "test.tsv",
        }
        downloaded_files = dl_manager.download_and_extract(_urls)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_file": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"data_file": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"data_file": downloaded_files["test"]}),
        ]

    def _generate_examples(self, data_file):
        with open(data_file, encoding="utf-8") as f:
            rows = csv.reader(f, delimiter="\t")
            for i, row in enumerate(rows):
                question_category = QUESTION_CATEGORIES_MAPPING[row[0]] if row[0] != "" else -1
                example = {
                    "id": i,
                    "question_category": question_category,
                    "question_propmt": row[1],
                    "candidate_answers": row[2:-1],
                    "correct_answer_idx": int(row[-1]),
                }
                yield i, example
