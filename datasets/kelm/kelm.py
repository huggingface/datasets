# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Corpus for Knowledge-Enhanced Language Model Pre-training (KELM)"""

from __future__ import absolute_import, division, print_function

import csv

import datasets


_DESCRIPTION = """\
Data-To-Text Generation involves converting knowledge graph (KG) triples of the form (subject, relation, object) into
a natural language sentence(s). This dataset consists of English KG data converted into paired natural language text.
The generated corpus consists of ∼18M sentences spanning ∼45M triples with ∼1500 distinct relations.
"""

_CITATION = """\
@misc{agarwal2020large,
      title={Large Scale Knowledge Graph Based Synthetic Corpus Generation for Knowledge-Enhanced Language Model Pre-training},
      author={Oshin Agarwal and Heming Ge and Siamak Shakeri and Rami Al-Rfou},
      year={2020},
      eprint={2010.12688},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DOWNLOAD_URL = "https://storage.googleapis.com/gresearch/kelm-corpus/quadruples-{}.tsv"
_WEBPAGE = "https://github.com/google-research-datasets/KELM-corpus"


class KELM(datasets.GeneratorBasedBuilder):
    """Corpus for Knowledge-Enhanced Language Model Pre-training (KELM)"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "triple": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                }
            ),
            homepage=_WEBPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("train"))
        validation_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("validation"))
        test_path = dl_manager.download_and_extract(_DOWNLOAD_URL.format("test"))

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": validation_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, "r", encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter="\t", fieldnames=["triple", "sentence"])
            for irow, row in enumerate(csv_reader):
                yield irow, row
