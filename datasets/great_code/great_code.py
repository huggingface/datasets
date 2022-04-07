# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

# Lint as: python3
import json

import datasets


_DESCRIPTION = """\
The dataset for the variable-misuse task, described in the ICLR 2020 paper 'Global Relational Models of Source Code' [https://openreview.net/forum?id=B1lnbRNtwr]

This is the public version of the dataset used in that paper. The original, used to produce the graphs in the paper, could not be open-sourced due to licensing issues. See the public associated code repository [https://github.com/VHellendoorn/ICLR20-Great] for results produced from this dataset.

This dataset was generated synthetically from the corpus of Python code in the ETH Py150 Open dataset [https://github.com/google-research-datasets/eth_py150_open].
"""
_HOMEPAGE_URL = ""
_CITATION = """\
@inproceedings{DBLP:conf/iclr/HellendoornSSMB20,
  author    = {Vincent J. Hellendoorn and
               Charles Sutton and
               Rishabh Singh and
               Petros Maniatis and
               David Bieber},
  title     = {Global Relational Models of Source Code},
  booktitle = {8th International Conference on Learning Representations, {ICLR} 2020,
               Addis Ababa, Ethiopia, April 26-30, 2020},
  publisher = {OpenReview.net},
  year      = {2020},
  url       = {https://openreview.net/forum?id=B1lnbRNtwr},
  timestamp = {Thu, 07 May 2020 17:11:47 +0200},
  biburl    = {https://dblp.org/rec/conf/iclr/HellendoornSSMB20.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""
_TRAIN_URLS = [
    f"https://raw.githubusercontent.com/google-research-datasets/great/master/train/train__VARIABLE_MISUSE__SStuB.txt-{x:05d}-of-00300"
    for x in range(300)
]
_TEST_URLS = [
    f"https://raw.githubusercontent.com/google-research-datasets/great/master/eval/eval__VARIABLE_MISUSE__SStuB.txt-{x:05d}-of-00300"
    for x in range(300)
]
_VALID_URLS = [
    f"https://raw.githubusercontent.com/google-research-datasets/great/master/dev/dev__VARIABLE_MISUSE__SStuB.txt-{x:05d}-of-00300"
    for x in range(300)
]


class GreatCode(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "source_tokens": datasets.Sequence(datasets.Value("string")),
                    "has_bug": datasets.Value("bool"),
                    "error_location": datasets.Value("int32"),
                    "repair_candidates": datasets.Sequence(datasets.Value("string")),
                    "bug_kind": datasets.Value("int32"),
                    "bug_kind_name": datasets.Value("string"),
                    "repair_targets": datasets.Sequence(datasets.Value("int32")),
                    "edges": [
                        [
                            {
                                "before_index": datasets.Value("int32"),
                                "after_index": datasets.Value("int32"),
                                "edge_type": datasets.Value("int32"),
                                "edge_type_name": datasets.Value("string"),
                            }
                        ]
                    ],
                    "provenances": [
                        {
                            "datasetProvenance": {
                                "datasetName": datasets.Value("string"),
                                "filepath": datasets.Value("string"),
                                "license": datasets.Value("string"),
                                "note": datasets.Value("string"),
                            }
                        }
                    ],
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_URLS)
        valid_path = dl_manager.download_and_extract(_VALID_URLS)
        test_path = dl_manager.download_and_extract(_TEST_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "datapath": train_path,
                    "datatype": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "datapath": valid_path,
                    "datatype": "valid",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "datapath": test_path,
                    "datatype": "test",
                },
            ),
        ]

    def _generate_examples(self, datapath, datatype):
        for file_idx, dp in enumerate(datapath):
            with open(dp, "r", encoding="utf-8") as json_file:
                for example_counter, json_str in enumerate(json_file):
                    result = json.loads(json_str)
                    response = {
                        "id": example_counter,
                        "source_tokens": result["source_tokens"],
                        "has_bug": result["has_bug"],
                        "error_location": result["error_location"],
                        "repair_candidates": [str(x) for x in result["repair_candidates"]],
                        "bug_kind": result["bug_kind"],
                        "bug_kind_name": result["bug_kind_name"],
                        "repair_targets": result["repair_targets"],
                        "edges": [
                            [
                                {
                                    "before_index": result["edges"][x][0],
                                    "after_index": result["edges"][x][1],
                                    "edge_type": result["edges"][x][2],
                                    "edge_type_name": result["edges"][x][3],
                                }
                            ]
                            for x in range(len(result["edges"]))
                        ],
                        "provenances": result["provenances"],
                    }
                    yield f"{file_idx}_{example_counter}", response
