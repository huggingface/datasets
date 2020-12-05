# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""TabFact: A Large-scale Dataset for Table-based Fact Verification"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{2019TabFactA,
  title={TabFact : A Large-scale Dataset for Table-based Fact Verification},
  author={Wenhu Chen, Hongmin Wang, Jianshu Chen, Yunkai Zhang, Hong Wang, Shiyang Li, Xiyou Zhou and William Yang Wang},
  booktitle = {International Conference on Learning Representations (ICLR)},
  address = {Addis Ababa, Ethiopia},
  month = {April},
  year = {2020}
}
"""

_DESCRIPTION = """\
The problem of verifying whether a textual hypothesis holds the truth based on the given evidence, \
also known as fact verification, plays an important role in the study of natural language \
understanding and semantic representation. However, existing studies are restricted to \
dealing with unstructured textual evidence (e.g., sentences and passages, a pool of passages), \
while verification using structured forms of evidence, such as tables, graphs, and databases, remains unexplored. \
TABFACT is large scale dataset with 16k Wikipedia tables as evidence for 118k human annotated statements \
designed for fact verification with semi-structured evidence. \
The statements are labeled as either ENTAILED or REFUTED. \
TABFACT is challenging since it involves both soft linguistic reasoning and hard symbolic reasoning.
"""

_HOMEPAGE = "https://tabfact.github.io/"

_CSV_BASE_URL = "https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/master/data"
_ALL_CSV_IDS_URL = _BASE_URL + "/all_csv_ids.json"

_STATEMENTS_BASE_URL = "https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/master/tokenized_data/"
_URLS = {
    "train": _STATEMENTS_BASE_URL + "train_examples.json",
    "dev": _STATEMENTS_BASE_URL + "val_examples.json",
    "test": _STATEMENTS_BASE_URL + "test_examples.json",
}

_BLIND_TEST_URL = "https://raw.githubusercontent.com/wenhuchen/Table-Fact-Checking/master/challenge/blind_test.json"


class TabFact(datasets.GeneratorBasedBuilder):
    """TabFact: A Large-scale Dataset for Table-based Fact Verification"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="tab_fact",
            version=datasets.Version("1.0.0"),
        ),
        datasets.BuilderConfig(
            name="blind_test",
            version=datasets.Version("1.0.0"),
            description="Blind test dataset",
        ),
    ]

    def _info(self):
        features = {
            "id": datasets.Value("int32"),
            "table_id": datasets.Value("string"),
            "table_text": datasets.Value("string"),
            "table_caption": datasets.Value("string"),
            "statement": datasets.Value("string"),
        }
        if self.config.name == "tab_fact":
            features["label"] = datasets.ClassLabel(names=["refuted", "entailed"])
        else:
            features["test_id"] = datasets.Value("string")

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        ids_file = dl_manager.download(_ALL_CSV_IDS_URL)
        ids = json.load(open(ids_file))

        csv_urls = {id_: f"{_BASE_URL}/all_csv/{id_}" for id_ in ids}
        csv_files = dl_manager.download(csv_urls)

        if self.config.name == "blind_test":
            test_file = dl_manager.download(_BLIND_TEST_URL)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"statements_file": test_file, "csv_files": csv_files, "split": "test"},
                ),
            ]

        statements_files = dl_manager.download(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"statements_file": statements_files["train"], "csv_files": csv_files, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"statements_file": statements_files["dev"], "csv_files": csv_files, "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"statements_file": statements_files["test"], "csv_files": csv_files, "split": "test"},
            ),
        ]

    def _generate_examples(self, statements_file, csv_files, split):
        with open(statements_file, encoding="utf-8") as f:
            examples = json.load(f)

        if self.config.name == "blind_test":
            test_examples = self._generate_blind_test_examples(examples, csv_files)
            for idx, example in test_examples:
                yield idx, example
        else:
            counter = 0
            for table_id, example in examples.items():
                with open(csv_files[table_id], encoding="utf-8") as f:
                    tabel_text = f.read()

                statements, labels, caption = example

                for statement, label in zip(statements, labels):
                    yield counter, {
                        "id": counter,
                        "table_id": table_id,
                        "table_text": tabel_text,
                        "table_caption": caption,
                        "statement": statement,
                        "label": label,
                    }
                    counter += 1

    def _generate_blind_test_examples(self, examples, csv_files):
        for i, (test_id, example) in enumerate(examples.items()):
            statement, table_id, caption = example
            with open(csv_files[table_id], encoding="utf-8") as f:
                tabel_text = f.read()

            yield i, {
                "id": i,
                "test_id": test_id,
                "table_id": table_id,
                "table_text": tabel_text,
                "table_caption": caption,
                "statement": statement,
            }
