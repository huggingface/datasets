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
"""EURegIR: Regulatory Compliance IR (EU/UK)"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{chalkidis-etal-2021-regir,
    title = "Regulatory Compliance through Doc2Doc Information Retrieval: A case study in EU/UK legislation where text similarity has limitations",
    author = "Chalkidis, Ilias  and Fergadiotis, Emmanouil and Manginas, Nikos and Katakalou, Eva,  and Malakasiotis, Prodromos",
    booktitle = "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL 2021)",
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/2101.10726",
}
"""

_DESCRIPTION = """\
EURegIR: Regulatory Compliance IR (EU/UK)
"""

_HOMEPAGE = "https://archive.org/details/eacl2021_regir_dataset"

_LICENSE = "CC BY-SA (Creative Commons / Attribution-ShareAlike)"

_URLs = {
    "eu2uk": "https://archive.org/download/eacl2021_regir_datasets/eu2uk.zip",
    "uk2eu": "https://archive.org/download/eacl2021_regir_datasets/uk2eu.zip",
}


class EuRegulatoryIr(datasets.GeneratorBasedBuilder):
    """EURegIR: Regulatory Compliance IR (EU/UK)"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="eu2uk", version=VERSION, description="EURegIR: Regulatory Compliance IR (EU2UK)"),
        datasets.BuilderConfig(name="uk2eu", version=VERSION, description="EURegIR: Regulatory Compliance IR (UK2EU)"),
    ]

    def _info(self):
        if self.config.name == "eu2uk":
            features = datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "publication_year": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "relevant_documents": datasets.features.Sequence(datasets.Value("string")),
                }
            )
        else:
            features = datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "publication_year": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "relevant_documents": datasets.features.Sequence(datasets.Value("string")),
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
            datasets.SplitGenerator(
                name=f"{self.config.name.split('2')[1]}_corpus",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "corpus.jsonl"),
                    "split": f"{self.config.name.split('2')[1]}_corpus",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "document_id": data["document_id"],
                    "text": data["text"],
                    "publication_year": data["publication_year"],
                    "relevant_documents": data["relevant_documents"]
                    if split != f"{self.config.name.split('2')[1]}_corpus"
                    else [],
                }
