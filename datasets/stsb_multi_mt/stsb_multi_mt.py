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
"""These are different multilingual translations and the English original of the STSbenchmark dataset."""


import csv

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset:stsb_multi_mt,
title = {Machine translated multilingual STS benchmark dataset.},
author={Philip May},
year={2021},
url={https://github.com/PhilipMay/stsb-multi-mt}
}
"""

_DESCRIPTION = """\
These are different multilingual translations and the English original of the STSbenchmark dataset. \
Translation has been done with deepl.com.
"""

_HOMEPAGE = "https://github.com/PhilipMay/stsb-multi-mt"

_LICENSE = "custom license - see project page"

_BASE_URL = "https://raw.githubusercontent.com/PhilipMay/stsb-multi-mt/main/data"


class StsbMultiMt(datasets.GeneratorBasedBuilder):
    """These are different multilingual translations and the English original of the STSbenchmark dataset.

    Translation has been done with deepl.com.
    """

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="en",
            version=VERSION,
            description="This is the original English STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="de",
            version=VERSION,
            description="This is the German STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="es",
            version=VERSION,
            description="This is the Spanish STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="fr",
            version=VERSION,
            description="This is the French STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="it",
            version=VERSION,
            description="This is the Italian STS benchmark data set.",
        ),
        # here seems to be an issue - see https://github.com/PhilipMay/stsb-multi-mt/issues/1
        # datasets.BuilderConfig(name="ja", version=VERSION, description="This is the Japanese STS benchmark data set."),
        datasets.BuilderConfig(
            name="nl",
            version=VERSION,
            description="This is the Dutch STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="pl",
            version=VERSION,
            description="This is the Polish STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="pt",
            version=VERSION,
            description="This is the Portuguese STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="ru",
            version=VERSION,
            description="This is the Russian STS benchmark data set.",
        ),
        datasets.BuilderConfig(
            name="zh",
            version=VERSION,
            description="This is the Chinese (simplified) STS benchmark data set.",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "similarity_score": datasets.Value("float"),
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
        urls_to_download = {
            "train": f"{_BASE_URL}/stsb-{self.config.name}-train.csv",
            "dev": f"{_BASE_URL}/stsb-{self.config.name}-dev.csv",
            "test": f"{_BASE_URL}/stsb-{self.config.name}-test.csv",
        }
        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.NamedSplit("dev"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                },
            ),
        ]

    def _generate_examples(
        self,
        filepath,  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            csv_dict_reader = csv.DictReader(
                csvfile,
                fieldnames=["sentence1", "sentence2", "similarity_score"],
                dialect="excel",
            )
            for id_, row in enumerate(csv_dict_reader):
                # do asserts
                assert "sentence1" in row
                assert isinstance(row["sentence1"], str)
                assert len(row["sentence1"].strip()) > 0
                assert "sentence2" in row
                assert isinstance(row["sentence2"], str)
                assert len(row["sentence2"].strip()) > 0
                assert "similarity_score" in row
                assert isinstance(row["similarity_score"], str)
                assert len(row["similarity_score"].strip()) > 0

                # convert similarity_score from str to float
                row["similarity_score"] = float(row["similarity_score"])

                # do more asserts
                assert row["similarity_score"] >= 0.0
                assert row["similarity_score"] <= 5.0

                yield id_, row
