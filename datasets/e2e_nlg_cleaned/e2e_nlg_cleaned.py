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
"""E2E Dataset: New Challenges For End-to-End Generation, cleaned version"""

import csv

import datasets


_CITATION = """\
@inproceedings{dusek-etal-2019-semantic,
    title = "Semantic Noise Matters for Neural Natural Language Generation",
    author = "Du{\v{s}}ek, Ond{\v{r}}ej  and
      Howcroft, David M.  and
      Rieser, Verena",
    booktitle = "Proceedings of the 12th International Conference on Natural Language Generation",
    month = oct # "{--}" # nov,
    year = "2019",
    address = "Tokyo, Japan",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-8652",
    doi = "10.18653/v1/W19-8652",
    pages = "421--426"
}
"""

_DESCRIPTION = """\
An update release of E2E NLG Challenge data with cleaned MRs and scripts, accompanying the following paper:

Ondřej Dušek, David M. Howcroft, and Verena Rieser (2019): Semantic Noise Matters for Neural Natural Language Generation. In INLG, Tokyo, Japan.
"""

_URL = "https://github.com/tuetschek/e2e-cleaning/raw/master/cleaned-data/"
_TRAINING_FILE = "train-fixed.no-ol.csv"
_DEV_FILE = "devel-fixed.no-ol.csv"
_TEST_FILE = "test-fixed.csv"

_URLS = {
    "train": f"{_URL}{_TRAINING_FILE}",
    "dev": f"{_URL}{_DEV_FILE}",
    "test": f"{_URL}{_TEST_FILE}",
}


class E2eNLGCleaned(datasets.GeneratorBasedBuilder):
    """E2E dataset, cleaned version."""

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
            homepage="https://github.com/tuetschek/e2e-cleaning",
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
