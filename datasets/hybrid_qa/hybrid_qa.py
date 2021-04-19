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


import json
import os

import datasets


_CITATION = """\
@article{chen2020hybridqa,
  title={HybridQA: A Dataset of Multi-Hop Question Answering over Tabular and Textual Data},
  author={Chen, Wenhu and Zha, Hanwen and Chen, Zhiyu and Xiong, Wenhan and Wang, Hong and Wang, William},
  journal={Findings of EMNLP 2020},
  year={2020}
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

_HOMEPAGE = "https://github.com/wenhuchen/HybridQA"

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
            "question_id": datasets.Value("string"),
            "question": datasets.Value("string"),
            "table_id": datasets.Value("string"),
            "answer_text": datasets.Value("string"),
            "question_postag": datasets.Value("string"),
            "table": {
                "url": datasets.Value("string"),
                "title": datasets.Value("string"),
                "header": datasets.Sequence(datasets.Value("string")),
                "data": [
                    {
                        "value": datasets.Value("string"),
                        "urls": [{"url": datasets.Value("string"), "summary": datasets.Value("string")}],
                    }
                ],
                "section_title": datasets.Value("string"),
                "section_text": datasets.Value("string"),
                "uid": datasets.Value("string"),
                "intro": datasets.Value("string"),
            },
        }
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        extracted_path = dl_manager.download_and_extract(_WIKI_TABLES_GIT_ARCHIVE_URL)
        downloaded_files = dl_manager.download(_URLS)

        repo_path = os.path.join(extracted_path, "WikiTables-WithLinks-f4ed68e54e25c495f63d309de0b89c0f97b3c508")
        tables_path = os.path.join(repo_path, "tables_tok")
        requests_path = os.path.join(repo_path, "request_tok")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "qa_filepath": downloaded_files["train"],
                    "tables_path": tables_path,
                    "requests_path": requests_path,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "qa_filepath": downloaded_files["dev"],
                    "tables_path": tables_path,
                    "requests_path": requests_path,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "qa_filepath": downloaded_files["test"],
                    "tables_path": tables_path,
                    "requests_path": requests_path,
                },
            ),
        ]

    def _generate_examples(self, qa_filepath, tables_path, requests_path):
        with open(qa_filepath, encoding="utf-8") as f:
            examples = json.load(f)

        for example in examples:
            table_id = example["table_id"]
            table_file_path = os.path.join(tables_path, f"{table_id}.json")
            url_data_path = os.path.join(requests_path, f"{table_id}.json")

            with open(table_file_path, encoding="utf-8") as f:
                table = json.load(f)
            with open(url_data_path, encoding="utf-8") as f:
                url_data = json.load(f)

            table["header"] = [header[0] for header in table["header"]]

            # here each row is a list with two elemets, the row value and list of urls for that row
            # convert it to list of dict with keys value and urls
            rows = []
            for row in table["data"]:
                for col in row:
                    new_row = {"value": col[0]}
                    urls = col[1]
                    new_row["urls"] = [{"url": url, "summary": url_data[url]} for url in urls]
                    rows.append(new_row)
            table["data"] = rows

            example["answer_text"] = example.pop("answer-text") if "answer-text" in example else ""
            example["table"] = table

            yield example["question_id"], example
