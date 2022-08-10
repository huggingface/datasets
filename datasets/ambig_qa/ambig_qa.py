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

"""AmbigQA: Answering Ambiguous Open-domain Questions"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{ min2020ambigqa,
    title={ {A}mbig{QA}: Answering Ambiguous Open-domain Questions },
    author={ Min, Sewon and Michael, Julian and Hajishirzi, Hannaneh and Zettlemoyer, Luke },
    booktitle={ EMNLP },
    year={2020}
}
"""

_DESCRIPTION = """\
AmbigNQ, a dataset covering 14,042 questions from NQ-open, an existing open-domain QA benchmark. We find that over half of the questions in NQ-open are ambiguous. The types of ambiguity are diverse and sometimes subtle, many of which are only apparent after examining evidence provided by a very large text corpus.  AMBIGNQ, a dataset with
14,042 annotations on NQ-OPEN questions containing diverse types of ambiguity.
We provide two distributions of our new dataset AmbigNQ: a full version with all annotation metadata and a light version with only inputs and outputs.
"""
_HOMEPAGE = "https://nlp.cs.washington.edu/ambigqa/"
_LICENSE = "CC BY-SA 3.0"

_URL = "https://nlp.cs.washington.edu/ambigqa/data/"
_URLS = {
    "light": _URL + "ambignq_light.zip",
    "full": _URL + "ambignq.zip",
}


class AmbigQa(datasets.GeneratorBasedBuilder):
    """AmbigQA dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="light",
            version=VERSION,
            description="AmbigNQ light version with only inputs and outputs",
        ),
        datasets.BuilderConfig(
            name="full",
            version=VERSION,
            description="AmbigNQ full version with all annotation metadata",
        ),
    ]
    DEFAULT_CONFIG_NAME = "full"

    def _info(self):
        features_dict = {
            "id": datasets.Value("string"),
            "question": datasets.Value("string"),
            "annotations": datasets.features.Sequence(
                {
                    "type": datasets.Value("string"),  # datasets.ClassLabel(names = ["singleAnswer","multipleQAs"])
                    "answer": datasets.features.Sequence(datasets.Value("string")),
                    "qaPairs": datasets.features.Sequence(
                        {
                            "question": datasets.Value("string"),
                            "answer": datasets.features.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            ),
        }
        if self.config.name == "full":

            detail_features = {
                "viewed_doc_titles": datasets.features.Sequence(datasets.Value("string")),
                "used_queries": datasets.features.Sequence(
                    {
                        "query": datasets.Value("string"),
                        "results": datasets.features.Sequence(
                            {
                                "title": datasets.Value("string"),
                                "snippet": datasets.Value("string"),
                            }
                        ),
                    }
                ),
                "nq_answer": datasets.features.Sequence(datasets.Value("string")),
                "nq_doc_title": datasets.Value("string"),
            }
            features_dict.update(detail_features)

        features = datasets.Features(features_dict)

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
        # download and extract URLs
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        train_file_name = "train.json" if self.config.name == "full" else "train_light.json"
        dev_file_name = "dev.json" if self.config.name == "full" else "dev_light.json"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(downloaded_files[self.config.name], train_file_name)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(downloaded_files[self.config.name], dev_file_name)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for example in data:
                id_ = example["id"]
                annotations = example["annotations"]
                # Add this because we cannot have None values (all keys in the schema should be present)
                for an in annotations:
                    if "qaPairs" not in an:
                        an["qaPairs"] = []
                    if "answer" not in an:
                        an["answer"] = []

                yield id_, example
