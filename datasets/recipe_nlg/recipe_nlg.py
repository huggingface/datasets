# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors
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
import ast
import csv
import os

import datasets


_CITATION = """\
@inproceedings{bien-etal-2020-recipenlg,
title = "{R}ecipe{NLG}: A Cooking Recipes Dataset for Semi-Structured Text Generation",
author = "Bie{'n}, Micha{l}  and
  Gilski, Micha{l}  and
  Maciejewska, Martyna  and
  Taisner, Wojciech  and
  Wisniewski, Dawid  and
  Lawrynowicz, Agnieszka",
booktitle = "Proceedings of the 13th International Conference on Natural Language Generation",
month = dec,
year = "2020",
address = "Dublin, Ireland",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/2020.inlg-1.4",
pages = "22--28"
}
"""

_DESCRIPTION = """\
The dataset contains 2231142 cooking recipes (>2 millions). It's processed in more careful way and provides more samples than any other dataset in the area.
"""

_HOMEPAGE = "https://recipenlg.cs.put.poznan.pl/"

_FILENAME = "full_dataset.csv"


class RecipeNlg(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://recipenlg.cs.put.poznan.pl/,
    and manually download the dataset. Once it is completed,
    a file named dataset.zip will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to. You then have
    to unzip the file and move full_dataset.csv under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    recipe_nlg can then be loaded using the following command `datasets.load_dataset("recipe_nlg", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "title": datasets.Value("string"),
                "ingredients": datasets.Sequence(datasets.Value("string")),
                "directions": datasets.Sequence(datasets.Value("string")),
                "link": datasets.Value("string"),
                "source": datasets.ClassLabel(names=["Gathered", "Recipes1M"]),
                "ner": datasets.Sequence(datasets.Value("string")),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('recipe_nlg', data_dir=...)` that includes file name {_FILENAME}. Manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, "full_dataset.csv"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    continue
                resp = {
                    "id": row[0],
                    "title": row[1],
                    "ingredients": ast.literal_eval(row[2]),
                    "directions": ast.literal_eval(row[3]),
                    "link": row[4],
                    "source": row[5],
                    "ner": ast.literal_eval(row[6]),
                }
                yield idx, resp
