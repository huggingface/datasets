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
_URL = "https://raw.githubusercontent.com/apergo-ai/CRASS-data-set/main/CRASS_FTM_main_data_set.csv"


class Crass(datasets.GeneratorBasedBuilder):
    """TODO: Premise-Questionized-Counterfactual-Conditional-Tuples in closed target mode"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features = datasets.Features(
                {
                    "PCTID": datasets.Value("int8"),
                    "Premise": datasets.Value("string"),
                    "QCC": datasets.Value("string"),
                    "CorrectAnswer": datasets.Value("string"),
                    "Answer1": datasets.Value("string"),
                    "Answer2": datasets.Value("string") ,           
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
        test_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]



    def _generate_examples(self, filepath):
        """Generate crass dataset examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=";", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)            
            for id_, row in enumerate(csv_reader):
                yield id_, {
                    "PCTID": int(row[0]),
                    "Premise": str(row[2]),
                    "QCC": row[3],
                    "CorrectAnswer": row[4],
                    "Answer1": row[5],
                    "Answer2": row[6], 
                    "PossibleAnswer3": row[7]                      
                }

              