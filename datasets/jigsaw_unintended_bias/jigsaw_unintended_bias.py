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
"""Jigsaw Unintended Bias in Toxicity Classification dataset"""


import os

import pandas as pd

import datasets


_DESCRIPTION = """\
A collection of comments from the defunct Civil Comments platform that have been annotated for their toxicity.
"""

_HOMEPAGE = "https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/"

_LICENSE = "CC0 (both the dataset and underlying text)"


class JigsawUnintendedBias(datasets.GeneratorBasedBuilder):
    """A collection of comments from the defunct Civil Comments platform that have been annotated for their toxicity."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
            To use jigsaw_unintended_bias you have to download it manually from Kaggle: https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data
            You can manually download the data from it's homepage or use the Kaggle CLI tool (follow the instructions here: https://www.kaggle.com/docs/api)
            Please extract all files in one folder and then load the dataset with:
            `datasets.load_dataset('jigsaw_unintended_bias', data_dir='/path/to/extracted/data/')`"""

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "target": datasets.Value("float32"),
                    "comment_text": datasets.Value("string"),
                    "severe_toxicity": datasets.Value("float32"),
                    "obscene": datasets.Value("float32"),
                    "identity_attack": datasets.Value("float32"),
                    "insult": datasets.Value("float32"),
                    "threat": datasets.Value("float32"),
                    "asian": datasets.Value("float32"),
                    "atheist": datasets.Value("float32"),
                    "bisexual": datasets.Value("float32"),
                    "black": datasets.Value("float32"),
                    "buddhist": datasets.Value("float32"),
                    "christian": datasets.Value("float32"),
                    "female": datasets.Value("float32"),
                    "heterosexual": datasets.Value("float32"),
                    "hindu": datasets.Value("float32"),
                    "homosexual_gay_or_lesbian": datasets.Value("float32"),
                    "intellectual_or_learning_disability": datasets.Value("float32"),
                    "jewish": datasets.Value("float32"),
                    "latino": datasets.Value("float32"),
                    "male": datasets.Value("float32"),
                    "muslim": datasets.Value("float32"),
                    "other_disability": datasets.Value("float32"),
                    "other_gender": datasets.Value("float32"),
                    "other_race_or_ethnicity": datasets.Value("float32"),
                    "other_religion": datasets.Value("float32"),
                    "other_sexual_orientation": datasets.Value("float32"),
                    "physical_disability": datasets.Value("float32"),
                    "psychiatric_or_mental_illness": datasets.Value("float32"),
                    "transgender": datasets.Value("float32"),
                    "white": datasets.Value("float32"),
                    "created_date": datasets.Value("string"),
                    "publication_id": datasets.Value("int32"),
                    "parent_id": datasets.Value("float"),
                    "article_id": datasets.Value("int32"),
                    "rating": datasets.ClassLabel(names=["rejected", "approved"]),
                    "funny": datasets.Value("int32"),
                    "wow": datasets.Value("int32"),
                    "sad": datasets.Value("int32"),
                    "likes": datasets.Value("int32"),
                    "disagree": datasets.Value("int32"),
                    "sexual_explicit": datasets.Value("float"),
                    "identity_annotator_count": datasets.Value("int32"),
                    "toxicity_annotator_count": datasets.Value("int32"),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('jigsaw_unintended_bias', data_dir=...)`. Manual download instructions: {self.manual_download_instructions}"
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"path": os.path.join(data_dir, "train.csv"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split("test_private_leaderboard"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"path": os.path.join(data_dir, "test_private_expanded.csv"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split("test_public_leaderboard"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"path": os.path.join(data_dir, "test_public_expanded.csv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, split: str = "train", path: str = None):
        """Yields examples."""
        # This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        # Avoid loading everything into memory at once
        all_data = pd.read_csv(path, chunksize=50000)

        for data in all_data:
            if split != "train":
                data = data.rename(columns={"toxicity": "target"})

            for _, row in data.iterrows():
                example = row.to_dict()
                ex_id = example.pop("id")
                yield (ex_id, example)
