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

"""The text2log dataset"""


import csv

import datasets


_CITATION = """\
@INPROCEEDINGS{9401852,  author={Levkovskyi, Oleksii and Li, Wei},  booktitle={SoutheastCon 2021},   title={Generating Predicate Logic Expressions from Natural Language},   year={2021},  volume={},  number={},  pages={1-8},  doi={10.1109/SoutheastCon45413.2021.9401852}}
"""

_DESCRIPTION = """\
The dataset contains about 100,000 simple English sentences selected and filtered from enTenTen15 and their translation into First Order Logic (FOL) Lambda Dependency-based Compositional Semantics using ccg2lambda.
"""

_HOMEPAGE = "https://github.com/alevkov/text2log"

_LICENSE = "none provided"


_URLS = {
    "csv": "https://raw.githubusercontent.com/apergo-ai/text2log/main/dat/text2log_clean.csv",
    "zip": "https://raw.githubusercontent.com/apergo-ai/text2log/main/dat/text2log_clean.zip",
}


class Text2log(datasets.GeneratorBasedBuilder):
    """Simple English sentences and FOL representations using LDbCS"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):

        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                "fol_translation": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            supervised_keys=None,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        test_path = dl_manager.download_and_extract(_URLS["csv"])
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate text2log dataset examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=";", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "sentence": str(row[0]),
                    "fol_translation": str(row[1]),
                }
