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

_GIT_ARCHIVE_URL = (
    "https://github.com/wenhuchen/Table-Fact-Checking/archive/948b5560e2f7f8c9139bd91c7f093346a2bb56a8.zip"
)


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
        extracted_path = dl_manager.download_and_extract(_GIT_ARCHIVE_URL)

        repo_path = os.path.join(extracted_path, "Table-Fact-Checking-948b5560e2f7f8c9139bd91c7f093346a2bb56a8")
        all_csv_path = os.path.join(repo_path, "data", "all_csv")

        if self.config.name == "blind_test":
            test_file_path = os.path.join(repo_path, "challenge", "blind_test.json")
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"statements_file": test_file_path, "all_csv_path": all_csv_path},
                ),
            ]

        train_statements_file = os.path.join(repo_path, "tokenized_data", "train_examples.json")
        val_statements_file = os.path.join(repo_path, "tokenized_data", "val_examples.json")
        test_statements_file = os.path.join(repo_path, "tokenized_data", "test_examples.json")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"statements_file": train_statements_file, "all_csv_path": all_csv_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"statements_file": val_statements_file, "all_csv_path": all_csv_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"statements_file": test_statements_file, "all_csv_path": all_csv_path},
            ),
        ]

    def _generate_examples(self, statements_file, all_csv_path):
        with open(statements_file, encoding="utf-8") as f:
            examples = json.load(f)

        if self.config.name == "blind_test":
            test_examples = self._generate_blind_test_examples(examples, all_csv_path)
            for idx, example in test_examples:
                yield idx, example
        else:
            for i, (table_id, example) in enumerate(examples.items()):
                table_file_path = os.path.join(all_csv_path, table_id)
                with open(table_file_path, encoding="utf-8") as f:
                    tabel_text = f.read()

                statements, labels, caption = example

                for statement_idx, (statement, label) in enumerate(zip(statements, labels)):
                    yield f"{i}_{statement_idx}", {
                        "id": i,
                        "table_id": table_id,
                        "table_text": tabel_text,
                        "table_caption": caption,
                        "statement": statement,
                        "label": label,
                    }

    def _generate_blind_test_examples(self, examples, all_csv_path):
        for i, (test_id, example) in enumerate(examples.items()):
            statement, table_id, caption = example
            table_file_path = os.path.join(all_csv_path, table_id)
            with open(table_file_path, encoding="utf-8") as f:
                tabel_text = f.read()

            yield i, {
                "id": i,
                "test_id": test_id,
                "table_id": table_id,
                "table_text": tabel_text,
                "table_caption": caption,
                "statement": statement,
            }
