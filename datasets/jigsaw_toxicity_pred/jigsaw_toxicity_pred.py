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
"""Comments from Jigsaw Toxic Comment Classification Kaggle Competition """


import os

import pandas as pd

import datasets


_DESCRIPTION = """\
This dataset consists of a large number of Wikipedia comments which have been labeled by human raters for toxic behavior.
"""

_HOMEPAGE = "https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data"

_LICENSE = 'The "Toxic Comment Classification" dataset is released under CC0, with the underlying comment text being governed by Wikipedia\'s CC-SA-3.0.'


class JigsawToxicityPred(datasets.GeneratorBasedBuilder):
    """This is a dataset of comments from Wikipedia’s talk page edits which have been labeled by human raters for toxic behavior."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
            To use jigsaw_toxicity_pred you have to download it manually from Kaggle: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data
            You can manually download the data from it's homepage or use the Kaggle CLI tool (follow the instructions here: https://www.kaggle.com/docs/api)
            Please extract all files in one folder and then load the dataset with:
            `datasets.load_dataset('jigsaw_toxicity_pred', data_dir='/path/to/extracted/data/')`"""

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "comment_text": datasets.Value("string"),
                    "toxic": datasets.ClassLabel(names=["false", "true"]),
                    "severe_toxic": datasets.ClassLabel(names=["false", "true"]),
                    "obscene": datasets.ClassLabel(names=["false", "true"]),
                    "threat": datasets.ClassLabel(names=["false", "true"]),
                    "insult": datasets.ClassLabel(names=["false", "true"]),
                    "identity_hate": datasets.ClassLabel(names=["false", "true"]),
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
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('jigsaw_toxicity_pred', data_dir=...)`. Manual download instructions: {self.manual_download_instructions}"
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"train_path": os.path.join(data_dir, "train.csv"), "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "test_text_path": os.path.join(data_dir, "test.csv"),
                    "test_labels_path": os.path.join(data_dir, "test_labels.csv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, split="train", train_path=None, test_text_path=None, test_labels_path=None):
        """Yields examples."""
        # This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        if split == "test":
            df1 = pd.read_csv(test_text_path)
            df2 = pd.read_csv(test_labels_path)
            df3 = df1.merge(df2)
            df4 = df3[df3["toxic"] != -1]

        elif split == "train":
            df4 = pd.read_csv(train_path)

        for _, row in df4.iterrows():
            example = {}
            example["comment_text"] = row["comment_text"]

            for label in ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]:
                if row[label] != -1:
                    example[label] = int(row[label])
            yield (row["id"], example)
