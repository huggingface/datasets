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
"""HybridQA: A Dataset of Multi-Hop Question Answering over Tabular and Textual Data"""

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
Existing question answering datasets focus on dealing with homogeneous information, based either only on text or \
KB/Table information alone. However, as human knowledge is distributed over heterogeneous forms, \
using homogeneous information alone might lead to severe coverage problems. \
To fill in the gap, we present HybridQA, a new large-scale question-answering dataset that \
requires reasoning on heterogeneous information. Each question is aligned with a Wikipedia table \
and multiple free-form corpora linked with the entities in the table. The questions are designed \
to aggregate both tabular information and text information, i.e., \
lack of either form would render the question unanswerable.
"""

_HOMEPAGE = "https://tabfact.github.io/"

_WIKI_TABLES_GIT_ARCHIVE_URL = (
    "https://github.com/wenhuchen/WikiTables-WithLinks/archive/f4ed68e54e25c495f63d309de0b89c0f97b3c508.zip"
)

_QA_DATA_BASE_URL = "https://raw.githubusercontent.com/wenhuchen/HybridQA/master/released_data"
_URLS = {
    "train": f"{_QA_DATA_BASE_URL}/train.json",
    "dev": f"{_QA_DATA_BASE_URL}/dev.json",
    "test": f"{_QA_DATA_BASE_URL}/test.json",
}


class HybridQa(datasets.GeneratorBasedBuilder):
    """HybridQA: A Dataset of Multi-Hop Question Answering over Tabular and Textual Data"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="hybrid_qa",
            version=datasets.Version("1.0.0"),
        ),
    ]

    def _info(self):
        features = {
            "question_id": datasets.Value("int32"),
            "question": datasets.Value("string"),
            "table_id": datasets.Value("string"),
            "answer-text": datasets.Value("string"),
            "question_postag": datasets.Value("string"),
            "table": {
                "url": datasets.Value("string"),
                "title": datasets.Value("string"),
                "headers": datasets.Sequence(datasets.Value("string")),
                "data": [
                    {
                        "value": datasets.Value("string"),
                        "urls": [
                            "url": datasets.Value("string"),
                            "summary": datasets.Value("string")
                        ]
                    }
                ],
                "section_title": datasets.Value("string"),
                "section_text": datasets.Value("string"),
                "uid": datasets.Value("string"),
                "intro": datasets.Value("string")
            }
        }
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_path = dl_manager.download_and_extract(_GIT_ARCHIVE_URL)
        downloaded_files = dl_manager.download(_URLS)

        repo_path = os.path.join(extracted_path, "WikiTables-WithLinks-f4ed68e54e25c495f63d309de0b89c0f97b3c508")
        tables_path = os.path.join(repo_path, "tables_tok")
        requests_paths = os.path.join(repo_path, "requests_tok")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"qa_filepath": downloaded_files["train"], "tables_path": requests_paths, "tables_path": tables_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"qa_filepath": downloaded_files["dev"], "tables_path": requests_paths, "tables_path": tables_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"qa_filepath": downloaded_files["test"], "tables_path": requests_paths, "tables_path": tables_path},
            ),
        ]

    def _generate_examples(self, qa_filepath, tables_path, tables_path):
        with open(qa_filepath, encoding="utf-8") as f:
            examples = json.load(f)

        
        for i, (table_id, example) in enumerate(examples.items()):
            table_file_path = os.path.join(tables_path, f"{table_id}.json")
            with open(table_file_path, encoding="utf-8") as f:
                tabel_text = f.read()

            statements, labels, caption = example

            for statement, label in zip(statements, labels):
                yield i, {
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