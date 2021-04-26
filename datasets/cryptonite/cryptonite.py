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


import json
import os

import datasets


_CITATION = """\
@misc{efrat2021cryptonite,
      title={Cryptonite: A Cryptic Crossword Benchmark for Extreme Ambiguity in Language},
      author={Avia Efrat and Uri Shaham and Dan Kilman and Omer Levy},
      year={2021},
      eprint={2103.01242},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Cryptonite: A Cryptic Crossword Benchmark for Extreme Ambiguity in Language
Current NLP datasets targeting ambiguity can be solved by a native speaker with relative ease. We present Cryptonite,
a large-scale dataset based on cryptic crosswords, which is both linguistically complex and naturally sourced. Each
example in Cryptonite is a cryptic clue, a short phrase or sentence with a misleading surface reading, whose solving
requires disambiguating semantic, syntactic, and phonetic wordplays, as well as world knowledge. Cryptic clues pose a
challenge even for experienced solvers, though top-tier experts can solve them with almost 100% accuracy. Cryptonite
is a challenging task for current models; fine-tuning T5-Large on 470k cryptic clues achieves only 7.6% accuracy, on
par with the accuracy of a rule-based clue solver (8.6%).
"""

_HOMEPAGE = "https://github.com/aviaefrat/cryptonite"

_LICENSE = "cc-by-nc-4.0"

_URL = "https://github.com/aviaefrat/cryptonite/blob/main/data/cryptonite-official-split.zip?raw=true"


class Cryptonite(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="cryptonite", version=VERSION),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "clue": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "enumeration": datasets.Value("string"),
                    "publisher": datasets.Value("string"),
                    "date": datasets.Value("int64"),
                    "quick": datasets.Value("bool"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "cryptonite-official-split/cryptonite-train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "cryptonite-official-split/cryptonite-val.jsonl"),
                    "split": "val",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "cryptonite-official-split/cryptonite-test.jsonl"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)

                publisher = data["publisher"]
                crossword_id = data["crossword_id"]
                number = data["number"]
                orientation = data["orientation"]
                d_id = f"{publisher}-{crossword_id}-{number}{orientation}"

                yield id_, {
                    "clue": data["clue"],
                    "answer": data["answer"],
                    "enumeration": data["enumeration"],
                    "publisher": publisher,
                    "date": data["date"],
                    "quick": data["quick"],
                    "id": d_id,
                }
