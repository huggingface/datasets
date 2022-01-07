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
import json
import os

import datasets


_CITATION = """\
@INPROCEEDINGS{9401852,  author={Levkovskyi, Oleksii and Li, Wei},  booktitle={SoutheastCon 2021},   title={Generating Predicate Logic Expressions from Natural Language},   year={2021},  volume={},  number={},  pages={1-8},  doi={10.1109/SoutheastCon45413.2021.9401852}}
"""

_DESCRIPTION = """\
The dataset contains about 100,000 simple English sentences selected and filtered from enTenTen15 and their translation into First Order Logic (FOL) Lambda Dependency-based Compositional Semantics using ccg2lambda.
"""

_HOMEPAGE = "https://github.com/alevkov/text2log"

_LICENSE = "none provided"

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "clean": "https://github.com/alevkov/text2log/blob/main/dat/clean.tar.xz",
    "trans": "https://github.com/alevkov/text2log/blob/main/dat/trans.tar.xz",
}



class text2log(datasets.GeneratorBasedBuilder):
    """Simple English sentences and FOL representations using LDbCS"""

    VERSION = datasets.Version("1.0.0")


    def _info(self):

        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                #"fol_translation": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features, 
            # supervised_keys=("sentence", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        test_path = dl_manager.download_and_extract(_URLS["clean"])
        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    # def _generate_examples(self, filepath):
    #     # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
    #     # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
    #     with open(filepath, encoding="utf-8") as f:
    #         for key, row in enumerate(f):
    #             data = json.loads(row)
    #             yield key, {
    #                 "sentence": data["sentence"],
    #             }
              

    def _generate_examples(self, filepath):
        """Generate crass dataset examples."""
        with open(filepath, encoding="utf-8") as f:
            for idx, line in f:
                yield idx, {"sentence":line}