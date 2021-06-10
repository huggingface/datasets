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
"""A Benchmark Dataset for Understanding Disfluencies in Question Answering"""


import json

import datasets


_CITATION = """\
@inproceedings{gupta-etal-2021-disflqa,
    title = "{Disfl-QA: A Benchmark Dataset for Understanding Disfluencies in Question Answering}",
    author = "Gupta, Aditya and Xu, Jiacheng and Upadhyay, Shyam and Yang, Diyi and Faruqui, Manaal",
    booktitle = "Findings of ACL",
    year = "2021"
}

"""

_DESCRIPTION = """\
Disfl-QA is a targeted dataset for contextual disfluencies in an information seeking setting,
namely question answering over Wikipedia passages. Disfl-QA builds upon the SQuAD-v2 (Rajpurkar et al., 2018)
dataset, where each question in the dev set is annotated to add a contextual disfluency using the paragraph as
a source of distractors.

The final dataset consists of ~12k (disfluent question, answer) pairs. Over 90% of the disfluencies are
corrections or restarts, making it a much harder test set for disfluency correction. Disfl-QA aims to fill a
major gap between speech and NLP research community. We hope the dataset can serve as a benchmark dataset for
testing robustness of models against disfluent inputs.

Our expriments reveal that the state-of-the-art models are brittle when subjected to disfluent inputs from
Disfl-QA. Detailed experiments and analyses can be found in our paper.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/disfl-qa"

_LICENSE = "Disfl-QA dataset is licensed under CC BY 4.0"

_URL = "https://raw.githubusercontent.com/google-research-datasets/Disfl-QA/main/"


class DisflQA(datasets.GeneratorBasedBuilder):
    """A Benchmark Dataset for Understanding Disfluencies in Question Answering"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "squad_v2_id": datasets.Value("string"),
                "original": datasets.Value("string"),
                "disfluent": datasets.Value("string"),
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
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dl_manager.download_and_extract(_URL + "train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_manager.download_and_extract(_URL + "test.json"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": dl_manager.download_and_extract(_URL + "dev.json"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            glob_id = 0
            for id_, row in enumerate(f):
                data = json.loads(row)
                for i in data:
                    yield glob_id, {
                        "squad_v2_id": i,
                        "original": data[i]["original"],
                        "disfluent": data[i]["disfluent"],
                    }
                    glob_id += 1
