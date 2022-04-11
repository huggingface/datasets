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
"""CUAD: A dataset for legal contract review curated by the Atticus Project."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@article{hendrycks2021cuad,
      title={CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review},
      author={Dan Hendrycks and Collin Burns and Anya Chen and Spencer Ball},
      journal={arXiv preprint arXiv:2103.06268},
      year={2021}
}
"""

_DESCRIPTION = """\
Contract Understanding Atticus Dataset (CUAD) v1 is a corpus of more than 13,000 labels in 510
commercial legal contracts that have been manually labeled to identify 41 categories of important
clauses that lawyers look for when reviewing contracts in connection with corporate transactions.
"""

_HOMEPAGE = "https://www.atticusprojectai.org/cuad"

_LICENSE = "CUAD is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license."

_URL = "https://github.com/TheAtticusProject/cuad/raw/main/data.zip"


class CUAD(datasets.GeneratorBasedBuilder):
    """CUAD: A dataset for legal contract review curated by the Atticus Project."""

    VERSION = "1.0.0"

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "answers": datasets.features.Sequence(
                    {
                        "text": datasets.Value("string"),
                        "answer_start": datasets.Value("int32"),
                    }
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
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train_separate_questions.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.json"), "split": "test"},
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            cuad = json.load(f)
            for example in cuad["data"]:
                title = example.get("title", "").strip()
                for paragraph in example["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
