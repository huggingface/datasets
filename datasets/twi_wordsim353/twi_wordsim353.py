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
"""WordSim-353 for Yoruba"""


import csv

import datasets


_DESCRIPTION = """\
A translation of the word pair similarity dataset wordsim-353 to Twi.

The dataset was presented in the paper
Alabi et al.: Massive vs. Curated Embeddings for Low-Resourced
Languages: the Case of Yorùbá and Twi (LREC 2020).
"""

_CITATION = """\
@inproceedings{alabi-etal-2020-massive,
    title = "Massive vs. Curated Embeddings for Low-Resourced Languages: the Case of {Y}or{\\`u}b{\\'a} and {T}wi",
    author = "Alabi, Jesujoba  and
      Amponsah-Kaakyire, Kwabena  and
      Adelani, David  and
      Espa{\\~n}a-Bonet, Cristina",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.335",
    pages = "2754--2762",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

_DOWNLOAD_URL = "https://raw.githubusercontent.com/ajesujoba/YorubaTwi-Embedding/master/Twi/wordsim_tw.csv"


class TwiWordsim353(datasets.GeneratorBasedBuilder):
    """WordSim-353 for Yoruba."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "twi1": datasets.Value("string"),
                    "twi2": datasets.Value("string"),
                    "similarity": datasets.Value("float32"),
                }
            ),
            homepage="https://github.com/ajesujoba/YorubaTwi-Embedding",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        test_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate WordSim-353 for Yoruba examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "twi1": row["twi1"],
                    "twi2": row["twi2"],
                    "similarity": row["EngSim"],
                }
