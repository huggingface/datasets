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
"""Introduction in a Romanian sentiment dataset."""

from __future__ import absolute_import, division, print_function

import csv
import logging

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = ""

_DESCRIPTION = """\
This new dataset is a Romanian sentiment analysis dataset.
"""

_HOMEPAGE = "https://github.com/katakonst/sentiment-analysis-tensorflow/tree/master/datasets"

_LICENSE = ""

_URL = (
    "https://raw.githubusercontent.com/dumitrescustefan/Romanian-Transformers/examples/examples/sentiment_analysis/ro/"
)
_TRAINING_FILE = "train.csv"
_TEST_FILE = "test.csv"


class ROSENTConfig(datasets.BuilderConfig):
    """BuilderConfig for ROSENT dataset"""

    def __init__(self, **kwargs):
        super(ROSENTConfig, self).__init__(**kwargs)


class ROSENTDataset(datasets.GeneratorBasedBuilder):
    """Romanian sentiment dataset."""

    VERSION = datasets.Version("1.0.0")
    DEFAULT_CONFIG_NAME = "rosent"

    BUILDER_CONFIGS = [
        ROSENTConfig(name=DEFAULT_CONFIG_NAME, version=VERSION, description="Romanian sentiment dataset."),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "sentence": datasets.Sequence(datasets.Value("string")),
                "label": datasets.Sequence(datasets.Value("int32")),
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

        urls_to_download_train = _URL + _TRAINING_FILE
        urls_to_download_test = _URL + _TEST_FILE

        train_path = dl_manager.download(urls_to_download_train)
        test_path = dl_manager.download(urls_to_download_test)
        print("FISIERE LUATE", train_path, test_path)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": test_path},
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """

        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            # data = pd.read_csv(filepath)
            data = csv.reader(f, delimiter=",", quotechar='"')

            next(data, None)
            for row_id, row in enumerate(data):
                print("ROW", row)
                id, txt, lbl = row
                yield "{}_{}".format(row_id, id), {
                    "id": id,
                    "sentence": [txt],
                    "label": [lbl],
                }
