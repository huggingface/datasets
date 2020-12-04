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
import os

import datasets


_DESCRIPTION = """\
ToTTo is an open-domain English table-to-text dataset with over 120,000 training examples that proposes a controlled generation task: given a Wikipedia table and a set of highlighted table cells, produce a one-sentence description.
"""
_HOMEPAGE_URL = ""
_URL = "https://storage.googleapis.com/totto/totto_data.zip"
_CITATION = """\
@inproceedings{parikh2020totto,
  title={{ToTTo}: A Controlled Table-To-Text Generation Dataset},
  author={Parikh, Ankur P and Wang, Xuezhi and Gehrmann, Sebastian and Faruqui, Manaal and Dhingra, Bhuwan and Yang, Diyi and Das, Dipanjan},
  booktitle={Proceedings of EMNLP},
  year={2020}
 }
"""


class Totto(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "table_page_title": datasets.Value("string"),
                    "table_webpage_url": datasets.Value("string"),
                    "table_section_title": datasets.Value("string"),
                    "table_section_text": datasets.Value("string"),
                    "table": [
                        [
                            {
                                "column_span": datasets.Value("int32"),
                                "is_header": datasets.Value("bool"),
                                "row_span": datasets.Value("int32"),
                                "value": datasets.Value("string"),
                            }
                        ]
                    ],
                    "highlighted_cells": datasets.Sequence(datasets.Sequence(datasets.Value("int32"))),
                    "example_id": datasets.Value("string"),
                    "sentence_annotations": datasets.Sequence(
                        {
                            "original_sentence": datasets.Value("string"),
                            "sentence_after_deletion": datasets.Value("string"),
                            "sentence_after_ambiguity": datasets.Value("string"),
                            "final_sentence": datasets.Value("string"),
                        }
                    ),
                    "overlap_subset": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "datapath": os.path.join(path, "totto_data/totto_train_data.jsonl"),
                    "datatype": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "datapath": os.path.join(path, "totto_data/totto_dev_data.jsonl"),
                    "datatype": "valid",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "datapath": os.path.join(path, "totto_data/unlabeled_totto_test_data.jsonl"),
                    "datatype": "test",
                },
            ),
        ]

    def _generate_examples(self, datapath, datatype):
        with open(datapath, "r", encoding="utf-8") as json_file:
            json_list = list(json_file)

        for example_counter, json_str in enumerate(json_list):
            result = json.loads(json_str)
            response = {
                "id": example_counter,
                "table_page_title": result["table_page_title"],
                "table_webpage_url": result["table_webpage_url"],
                "table_section_title": result["table_section_title"],
                "table_section_text": result["table_section_text"],
                "table": result["table"],
                "highlighted_cells": result["highlighted_cells"],
                "example_id": str(result["example_id"]),
            }
            if datatype == "train":
                response["overlap_subset"] = "none"
            else:
                response["overlap_subset"] = str(result["overlap_subset"])

            if datatype == "test":
                response["sentence_annotations"] = [
                    {
                        "original_sentence": "none",
                        "sentence_after_deletion": "none",
                        "sentence_after_ambiguity": "none",
                        "final_sentence": "none",
                    }
                ]
            else:
                response["sentence_annotations"] = result["sentence_annotations"]
            yield example_counter, response
