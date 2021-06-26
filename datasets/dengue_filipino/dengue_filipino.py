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
"""Dengue Dataset Low-Resource Multiclass Text Classification Dataset in Filipino"""

import csv
import os

import datasets


_DESCRIPTION = """\
    Benchmark dataset for low-resource multiclass classification, with 4,015 training, 500 testing, and 500 validation examples, each labeled as part of five classes. Each sample can be a part of multiple classes. Collected as tweets.
"""

_CITATION = """\
    @INPROCEEDINGS{8459963,
      author={E. D. {Livelo} and C. {Cheng}},
      booktitle={2018 IEEE International Conference on Agents (ICA)},
      title={Intelligent Dengue Infoveillance Using Gated Recurrent Neural Learning and Cross-Label Frequencies},
      year={2018},
      volume={},
      number={},
      pages={2-7},
      doi={10.1109/AGENTS.2018.8459963}}
    }
"""

_HOMEPAGE = "https://github.com/jcblaisecruz02/Filipino-Text-Benchmarks"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

_URL = "https://s3.us-east-2.amazonaws.com/blaisecruz.com/datasets/dengue/dengue_raw.zip"


class DengueFilipino(datasets.GeneratorBasedBuilder):
    """Dengue Dataset Low-Resource Multiclass Text Classification Dataset in Filipino"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "absent": datasets.features.ClassLabel(names=["0", "1"]),
                "dengue": datasets.features.ClassLabel(names=["0", "1"]),
                "health": datasets.features.ClassLabel(names=["0", "1"]),
                "mosquito": datasets.features.ClassLabel(names=["0", "1"]),
                "sick": datasets.features.ClassLabel(names=["0", "1"]),
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
        data_dir = dl_manager.download_and_extract(_URL)
        train_path = os.path.join(data_dir, "dengue", "train.csv")
        test_path = os.path.join(data_dir, "dengue", "train.csv")
        validation_path = os.path.join(data_dir, "dengue", "valid.csv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": test_path,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": validation_path,
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                try:
                    text, absent, dengue, health, mosquito, sick = row
                    payload = {
                        "text": text,
                        "absent": absent,
                        "dengue": dengue,
                        "health": health,
                        "mosquito": mosquito,
                        "sick": sick,
                    }
                    yield id_, payload
                except ValueError:
                    pass
