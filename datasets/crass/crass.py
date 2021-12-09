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
"""The CRASS (counterfactual reasoning assessment) dataset"""


import csv
import json
import os
import datasets




_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
author={huggingface, Inc.
},
year={2020}
}
"""

_DESCRIPTION = """\
The data consists of so-called PCTs (Premise-Counterfactual Tuples). They contrast a hypothetical situation using a counterfactual conditional against a base premise. In the fixed target mode there is one correct answer and two alternative incorrect answers.
"""

_HOMEPAGE = "https://www.crass.ai"
_LICENSE = "Apache License 2.0"
_URL = "https://github.com/apergo-ai/CRASS-data-set/blob/main/CRASS_FTM_main_data_set.csv"


class Crass(datasets.GeneratorBasedBuilder):
    """TODO: Premise-Questionized-Counterfactual-Conditional-Tuples in closed target mode"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features = datasets.Features(
                {
                    "PCTID": datasets.Value("int"),
                    "Premise": datasets.Value("string"),
                    "QCC": datasets.Value("string")
                    "CorrectAnswer": datasets.Value("string")
                    "Answer1": datasets.Value("string")
                    "Answer2": datasets.Value("string")            
                    "PossibleAnswer3": datasets.Value("string")                                                                                

                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
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
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test"
                },
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
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
