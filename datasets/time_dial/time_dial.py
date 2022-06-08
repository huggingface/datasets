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
"""Temporal Commonsense Reasoning in Dialog"""


import json

import datasets


_CITATION = """\
@inproceedings{qin-etal-2021-timedial,
    title = "{TimeDial: Temporal Commonsense Reasoning in Dialog}",
    author = "Qin, Lianhui and Gupta, Aditya and Upadhyay, Shyam and He, Luheng and Choi, Yejin and Faruqui, Manaal",
    booktitle = "Proc. of ACL",
    year = "2021"
}
"""

_DESCRIPTION = """\
TimeDial presents a crowdsourced English challenge set, for temporal commonsense reasoning, formulated
as a multiple choice cloze task with around 1.5k carefully curated dialogs. The dataset is derived from
the DailyDialog (Li et al., 2017), which is a multi-turn dialog corpus.

In order to establish strong baselines and provide information on future model development, we
conducted extensive experiments with state-of-the-art LMs. While humans can easily answer these
questions (97.8%), the best T5 model variant struggles on this challenge set (73%). Moreover, our
qualitative error analyses show that the models often rely on shallow, spurious features (particularly text
matching), instead of truly doing reasoning over the context.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/timedial"

_LICENSE = "TimeDial dataset is licensed under CC BY-NC-SA 4.0"

_URL = "https://raw.githubusercontent.com/google-research-datasets/TimeDial/main/test.json"


class TimeDial(datasets.GeneratorBasedBuilder):
    """Temporal Commonsense Reasoning in Dialog"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("int32"),
                "conversation": datasets.features.Sequence(datasets.Value("string")),
                "correct1": datasets.Value("string"),
                "correct2": datasets.Value("string"),
                "incorrect1": datasets.Value("string"),
                "incorrect1_rule": datasets.Value("string"),
                "incorrect2": datasets.Value("string"),
                "incorrect2_rule": datasets.Value("string"),
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

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_manager.download_and_extract(_URL), "split": "test"},
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            glob_id = 0
            row = json.load(f)
            for data in row:
                yield glob_id, {
                    "id": data["id"],
                    "conversation": data["conversation"],
                    "correct1": data["correct1"],
                    "correct2": data["correct2"],
                    "incorrect1": data["incorrect1"],
                    "incorrect1_rule": data["incorrect1_rule"],
                    "incorrect2": data["incorrect2"],
                    "incorrect2_rule": data["incorrect2_rule"],
                }
                glob_id += 1
