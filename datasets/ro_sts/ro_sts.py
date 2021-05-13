# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""RO-STS: The Romanian Semantic Textual Similarity Dataset"""


import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
Article under review
"""

# You can copy an official description
_DESCRIPTION = """\
The RO-STS (Romanian Semantic Textual Similarity) dataset contains 8628 pairs of sentences with their similarity score. It is a high-quality translation of the STS benchmark dataset.
"""

_HOMEPAGE = "https://github.com/dumitrescustefan/RO-STS/"

_LICENSE = "CC BY-SA 4.0 License"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/dumitrescustefan/RO-STS/master/dataset/text-similarity/"
_TRAINING_FILE = "RO-STS.train.tsv"
_TEST_FILE = "RO-STS.test.tsv"
_DEV_FILE = "RO-STS.dev.tsv"


class ROSTSConfig(datasets.BuilderConfig):
    """BuilderConfig for RO-STS dataset"""

    def __init__(self, **kwargs):
        super(ROSTSConfig, self).__init__(**kwargs)


class RoSts(datasets.GeneratorBasedBuilder):
    """RO-STS dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        ROSTSConfig(name="ro_sts", version=VERSION, description="RO-STS dataset"),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "score": datasets.Value("float"),
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
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

        urls_to_download = {"train": _URL + _TRAINING_FILE, "dev": _URL + _DEV_FILE, "test": _URL + _TEST_FILE}

        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["test"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": downloaded_files["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:

            reader = f.readlines()
            for idx, row in enumerate(reader):
                splits = row.strip().split("\t")
                yield idx, {
                    "score": splits[0],  # row["score"],
                    "sentence1": splits[1],  # row["sentence1"],
                    "sentence2": splits[2],  # row["sentence2"],
                }
