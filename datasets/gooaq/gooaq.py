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
"""GooAQ - Question-answers, collected from Google"""


import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{gooaq2021,
  title={GooAQ: Open Question Answering with Diverse Answer Types},
  author={Khashabi, Daniel and Ng, Amos and Khot, Tushar and Sabharwal, Ashish and Hajishirzi, Hannaneh and Callison-Burch, Chris},
  journal={arXiv preprint},
  year={2021}
}
"""

_DESCRIPTION = """\
GooAQ is a large-scale dataset with a variety of answer types. This dataset contains over
5 million questions and 3 million answers collected from Google. GooAQ questions are collected
semi-automatically from the Google search engine using its autocomplete feature. This results in
naturalistic questions of practical interest that are nonetheless short and expressed using simple
language. GooAQ answers are mined from Google's responses to our collected questions, specifically from
the answer boxes in the search results. This yields a rich space of answer types, containing both
textual answers (short and long) as well as more structured ones such as collections.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URL = "https://github.com/allenai/gooaq/blob/main/data/qoogle.jsonl?raw=true"


class GooAQ(datasets.GeneratorBasedBuilder):
    """GooAQ - Question-answers, collected from Google"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "short_answer": datasets.Value("string"),
                "answer": datasets.Value("string"),
                "answer_type": datasets.features.ClassLabel(
                    names=["feat_snip", "collection", "knowledge", "unit_conv", "time_conv", "curr_conv"]
                ),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "question": data["question"],
                    "short_answer": data["short_answer"],
                    "answer": data["answer"],
                    "answer_type": data["answer_type"],
                }
