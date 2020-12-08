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
"""E2E Dataset: New Challenges For End-to-End Generation"""

import csv

import datasets


_CITATION = """\
@article{dusek.etal2020:csl,
  title = {Evaluating the {{State}}-of-the-{{Art}} of {{End}}-to-{{End Natural Language Generation}}: {{The E2E NLG Challenge}}},
  author = {Du{\v{s}}ek, Ond\v{r}ej and Novikova, Jekaterina and Rieser, Verena},
  year = {2020},
  month = jan,
  volume = {59},
  pages = {123--156},
  doi = {10.1016/j.csl.2019.06.009},
  archivePrefix = {arXiv},
  eprint = {1901.11528},
  eprinttype = {arxiv},
  journal = {Computer Speech & Language}
}
"""

_DESCRIPTION = """\
The E2E dataset is used for training end-to-end, data-driven natural language generation systems in the restaurant domain, which is ten times bigger than existing, frequently used datasets in this area.
The E2E dataset poses new challenges:
(1) its human reference texts show more lexical richness and syntactic variation, including discourse phenomena;
(2) generating from this set requires content selection. As such, learning from this dataset promises more natural, varied and less template-like system utterances.

E2E is released in the following paper where you can find more details and baseline results:
https://arxiv.org/abs/1706.09254
"""

_URL = "https://raw.githubusercontent.com/tuetschek/e2e-dataset/master/"
_TRAINING_FILE = "trainset.csv"
_DEV_FILE = "devset.csv"
_TEST_FILE = "testset_w_refs.csv"

_URLS = {
    "train": f"{_URL}{_TRAINING_FILE}",
    "dev": f"{_URL}{_DEV_FILE}",
    "test": f"{_URL}{_TEST_FILE}",
}


class E2eNLG(datasets.GeneratorBasedBuilder):
    """E2E dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "meaning_representation": datasets.Value("string"),
                    "human_reference": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="http://www.macs.hw.ac.uk/InteractionLab/E2E/#data",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        downloaded_files = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for example_idx, example in enumerate(reader):
                yield example_idx, {
                    "meaning_representation": example["mr"],
                    "human_reference": example["ref"],
                }
