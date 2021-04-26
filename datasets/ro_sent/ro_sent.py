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


import csv

import datasets
from datasets.builder import BuilderConfig


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """
@article{dumitrescu2020birth,
  title={The birth of Romanian BERT},
  author={Dumitrescu, Stefan Daniel and Avram, Andrei-Marius and Pyysalo, Sampo},
  journal={arXiv preprint arXiv:2009.08712},
  year={2020}
}
"""

_DESCRIPTION = """\
This dataset is a Romanian Sentiment Analysis dataset.
It is present in a processed form, as used by the authors of `Romanian Transformers`
in their examples and based on the original data present in
`https://github.com/katakonst/sentiment-analysis-tensorflow`. The original dataset is collected
from product and movie reviews in Romanian.
"""

_HOMEPAGE = "https://github.com/dumitrescustefan/Romanian-Transformers/tree/examples/examples/sentiment_analysis"

_LICENSE = ""

_URL = (
    "https://raw.githubusercontent.com/dumitrescustefan/Romanian-Transformers/examples/examples/sentiment_analysis/ro/"
)
_URLs = {"train": _URL + "train.csv", "test": _URL + "test.csv"}


class RoSent(datasets.GeneratorBasedBuilder):
    """Romanian Sentiment Analysis dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        BuilderConfig(
            name="default",
            version=VERSION,
            description="This configuration handles all of Romanian Sentiment Analysis dataset.",
        ),
    ]

    def _info(self):

        features = datasets.Features(
            {
                "original_id": datasets.Value("string"),
                "id": datasets.Value("string"),
                "sentence": datasets.Value("string"),
                "label": datasets.ClassLabel(names=["negative", "positive"]),  # 0 is negative
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
            supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        paths = dl_manager.download(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": paths["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": paths["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter=",", quotechar='"')

            for row_id, row in enumerate(data):
                yield row_id, {
                    "original_id": row["index"] if "index" in row.keys() else row[""],  # test has no 'index' key
                    "id": str(row_id),  # this is needed because indices are repeated in the files.
                    "sentence": row["text"],
                    "label": int(row["label"]),
                }
