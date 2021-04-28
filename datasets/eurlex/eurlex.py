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
"""EURLEX57K contains 57k legislative documents in English from EUR-Lex portal, annotated with EUROVOC concepts."""


import json
import os

import datasets


_CITATION = """\
@inproceedings{chalkidis-etal-2019-large,
    title = "Large-Scale Multi-Label Text Classification on {EU} Legislation",
    author = "Chalkidis, Ilias  and Fergadiotis, Emmanouil  and Malakasiotis, Prodromos  and Androutsopoulos, Ion",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1636",
    doi = "10.18653/v1/P19-1636",
    pages = "6314--6322"
}
"""

_DESCRIPTION = """\
EURLEX57K contains 57k legislative documents in English from EUR-Lex portal, annotated with EUROVOC concepts.
"""

_HOMEPAGE = "http://nlp.cs.aueb.gr/software_and_datasets/EURLEX57K/"

_LICENSE = "CC BY-SA (Creative Commons / Attribution-ShareAlike)"

_URLs = {
    "eurlex57k": "http://archive.org/download/EURLEX57K/dataset.zip",
}


class EURLEX(datasets.GeneratorBasedBuilder):
    """EURLEX57K contains 57k legislative documents in English from EUR-Lex portal, annotated with EUROVOC concepts."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="eurlex57k", version=VERSION, description="EURLEX57K: Legal Multi-label Text Classification"
        ),
    ]

    DEFAULT_CONFIG_NAME = "eurlex57k"

    def _info(self):
        features = datasets.Features(
            {
                "celex_id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "text": datasets.Value("string"),
                "eurovoc_concepts": datasets.features.Sequence(datasets.Value("string")),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "celex_id": data["celex_id"],
                    "title": data["title"],
                    "text": "\n".join([data["header"], data["recitals"]] + data["main_body"]),
                    "eurovoc_concepts": data["eurovoc_concepts"],
                }
