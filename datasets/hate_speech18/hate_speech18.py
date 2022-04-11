# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""Hate speech dataset"""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{gibert2018hate,
    title = "{Hate Speech Dataset from a White Supremacy Forum}",
    author = "de Gibert, Ona  and
      Perez, Naiara  and
      Garcia-Pablos, Aitor  and
      Cuadros, Montse",
    booktitle = "Proceedings of the 2nd Workshop on Abusive Language Online ({ALW}2)",
    month = oct,
    year = "2018",
    address = "Brussels, Belgium",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-5102",
    doi = "10.18653/v1/W18-5102",
    pages = "11--20",
}
"""

_DESCRIPTION = """\
These files contain text extracted from Stormfront, a white supremacist forum. A random set of
forums posts have been sampled from several subforums and split into sentences. Those sentences
have been manually labelled as containing hate speech or not, according to certain annotation guidelines.
"""

_DATA_URL = "https://github.com/Vicomtech/hate-speech-dataset/archive/master.zip"


class HateSpeech18(datasets.GeneratorBasedBuilder):
    """Hate speech dataset"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "user_id": datasets.Value("int64"),
                    "subforum_id": datasets.Value("int64"),
                    "num_contexts": datasets.Value("int64"),
                    "label": datasets.features.ClassLabel(names=["noHate", "hate", "idk/skip", "relation"]),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/Vicomtech/hate-speech-dataset",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dl_dir, "hate-speech-dataset-master")}
            ),
        ]

    def _generate_examples(self, filepath):

        with open(os.path.join(filepath, "annotations_metadata.csv"), encoding="utf-8") as csv_file:

            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )

            next(csv_reader)

            for idx, row in enumerate(csv_reader):

                file_id, user_id, subforum_id, num_contexts, label = row

                all_files_path = os.path.join(filepath, "all_files")

                path = os.path.join(all_files_path, file_id + ".txt")

                with open(path, encoding="utf-8") as file:
                    text = file.read()

                yield idx, {
                    "text": text,
                    "user_id": user_id,
                    "subforum_id": subforum_id,
                    "num_contexts": num_contexts,
                    "label": label,
                }
