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
"""TODO: Add a description here."""


import json

import datasets


_CITATION = """\
@inproceedings{swapnil2020,
    title={An Annotated Dataset of Discourse Modes in Hindi Stories},
    author={Swapnil Dhanwal, Hritwik Dutta, Hitesh Nankani, Nilay Shrivastava, Yaman Kumar, Junyi Jessy Li, Debanjan Mahata, Rakesh Gosangi, Haimin Zhang, Rajiv Ratn Shah, Amanda Stent},
    booktitle={Proceedings of the 12th Conference on Language Resources and Evaluation (LREC 2020)},
    volume={12},
    pages={1191–1196},
    year={2020}
"""

_DESCRIPTION = """\
The Hindi Discourse Analysis dataset is a corpus for analyzing discourse modes present in its sentences.
It contains sentences from stories written by 11 famous authors from the 20th Century.
4-5 stories by each author have been selected which were available in the public domain resulting
in a collection of 53 stories. Most of these short stories were originally written in Hindi
but some of them were written in other Indian languages and later translated to Hindi.
"""


_DOWNLOAD_URL = "https://raw.githubusercontent.com/midas-research/hindi-discourse/master/discourse_dataset.json"


class HindiDiscourse(datasets.GeneratorBasedBuilder):
    """Hindi Discourse Dataset - dataset of discourse modes in Hindi stories."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        # This method pecifies the datasets.DatasetInfo object which contains informations and typings for the dataset

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "Story_no": datasets.Value("int32"),
                    "Sentence": datasets.Value("string"),
                    "Discourse Mode": datasets.ClassLabel(
                        names=["Argumentative", "Descriptive", "Dialogue", "Informative", "Narrative", "Other"]
                    ),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/midas-research/hindi-discourse",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dataset_path = dl_manager.download_and_extract(_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dataset_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            hindiDiscourse = json.load(f)

            for sentence, rowData in hindiDiscourse.items():
                yield sentence, {
                    "Story_no": rowData["Story_no"],
                    "Sentence": rowData["Sentence"],
                    "Discourse Mode": rowData["Discourse Mode"],
                }
