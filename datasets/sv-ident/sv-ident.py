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
"""Survey Variable Identification (SV-Ident) Corpus."""

import csv
import random

import datasets


# TODO: Add BibTeX citation
# _CITATION = ""

_DESCRIPTION = """\
The SV-Ident corpus (version 0.3) is a collection of 4,248 expert-annotated English
and German sentences from social science publications, supporting the task of
multi-label text classification.
"""

_HOMEPAGE = "https://github.com/vadis-project/sv-ident"

# TODO: Add the licence
# _LICENSE = ""

_URLS = {
    "train": "https://raw.githubusercontent.com/vadis-project/sv-ident/9962c3274444ce84c59d42e2a6f8c0958ed15a26/data/train/data.tsv",
    "trial": "https://github.com/vadis-project/sv-ident/tree/9962c3274444ce84c59d42e2a6f8c0958ed15a26/data/trial",
}


class SVIdent(datasets.GeneratorBasedBuilder):
    """Survey Variable Identification (SV-Ident) Corpus."""

    VERSION = datasets.Version("0.3.0")

    def _info(self):
        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                "is_variable": datasets.ClassLabel(names=["0", "1"]),
                "variable": datasets.Sequence(datasets.Value(dtype="string")),
                "research_data": datasets.Sequence(datasets.Value(dtype="string")),
                "doc_id": datasets.Value("string"),
                "uuid": datasets.Value("string"),
                "lang": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=("sentence", "is_variable"),
            homepage=_HOMEPAGE,
            # license=_LICENSE,
            # citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        filepath = dl_manager.download(_URLS["train"])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": filepath,
                },
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        data = []
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t")
            next(reader, None)  # skip the headers
            for row in reader:
                data.append(row)

        seed = 42
        random.seed(seed)
        random.shuffle(data)

        for id_, example in enumerate(data):
            sentence = example[0]
            is_variable = example[1]
            variable = example[2] if example[2] != "" else []
            if variable:
                variable = variable.split(";") if ";" in variable else [variable]
            research_data = example[3] if example[3] != "" else []
            if research_data:
                research_data = research_data.split(";") if ";" in research_data else [research_data]
            doc_id = example[4]
            uuid = example[5]
            lang = example[6]

            yield id_, {
                "sentence": sentence,
                "is_variable": is_variable,
                "variable": variable,
                "research_data": research_data,
                "doc_id": doc_id,
                "uuid": uuid,
                "lang": lang,
            }
