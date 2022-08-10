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
"""Ascent KB: A Deep Commonsense Knowledge Base"""

import json

import datasets


_CITATION = """\
@InProceedings{nguyen2021www,
  title={Advanced Semantics for Commonsense Knowledge Extraction},
  author={Nguyen, Tuan-Phong and Razniewski, Simon and Weikum, Gerhard},
  year={2021},
  booktitle={The Web Conference 2021},
}
"""

_DESCRIPTION = """\
This dataset contains 8.9M commonsense assertions extracted by the Ascent pipeline (https://ascent.mpi-inf.mpg.de/).
"""

_HOMEPAGE = "https://ascent.mpi-inf.mpg.de/"

_LICENSE = "The Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/by/4.0/"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)

_URL = "https://nextcloud.mpi-klsb.mpg.de/index.php/s/dFLdTQHqiFrt3Q3/download"


# DONE: Name of the dataset usually match the script name with CamelCase instead of snake_case
class AscentKB(datasets.GeneratorBasedBuilder):
    """Ascent KB: A Deep Commonsense Knowledge Base. Version 1.0.0."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="canonical",
            version=VERSION,
            description="This KB contains <arg1 ; rel ; arg2> \
                               assertions where relations are canonicalized based on ConceptNet relations.",
        ),
        datasets.BuilderConfig(
            name="open",
            version=VERSION,
            description="This KB contains open assertions of the form \
                               <subject ; predicate ; object> extracted directly from web contents.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "canonical"

    def _info(self):
        if self.config.name == "canonical":
            features = datasets.Features(
                {
                    "arg1": datasets.Value("string"),
                    "rel": datasets.Value("string"),
                    "arg2": datasets.Value("string"),
                    "support": datasets.Value("int64"),
                    "facets": [
                        {
                            "value": datasets.Value("string"),
                            "type": datasets.Value("string"),
                            "support": datasets.Value("int64"),
                        }
                    ],
                    "source_sentences": [{"text": datasets.Value("string"), "source": datasets.Value("string")}],
                }
            )
        else:  # features for the "open" part
            features = datasets.Features(
                {
                    "subject": datasets.Value("string"),
                    "predicate": datasets.Value("string"),
                    "object": datasets.Value("string"),
                    "support": datasets.Value("int64"),
                    "facets": [
                        {
                            "value": datasets.Value("string"),
                            "type": datasets.Value("string"),
                            "support": datasets.Value("int64"),
                        }
                    ],
                    "source_sentences": [{"text": datasets.Value("string"), "source": datasets.Value("string")}],
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # my_urls = _URLs[self.config.name]
        # data_file = dl_manager.download_and_extract(my_urls)

        data_file = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file,
                    "split": "train",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "canonical":
                    data.pop("subject")
                    data.pop("predicate")
                    data.pop("object")
                    yield id_, data
                else:  # "open"
                    data.pop("arg1")
                    data.pop("rel")
                    data.pop("arg2")
                    yield id_, data
