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
"""Neural-Code-Search-Evaluation-Dataset presents an evaluation dataset consisting of natural language query and code snippet pairs"""


import json
from itertools import chain

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title         = {Neural Code Search Evaluation Dataset},
authors       = {Hongyu Li, Seohyun Kim and Satish Chandra},
journal       = {arXiv e-prints},
year          = 2018,
eid           = {arXiv:1908.09804 [cs.SE]},
pages         = {arXiv:1908.09804 [cs.SE]},
archivePrefix = {arXiv},
eprint        = {1908.09804},
}
"""

_DESCRIPTION = """\
Neural-Code-Search-Evaluation-Dataset presents an evaluation dataset \
consisting of natural language query and code snippet pairs and a search corpus \
consisting of code snippets collected from the most popular Android repositories \
on GitHub.
"""

_HOMEPAGE = "https://github.com/facebookresearch/Neural-Code-Search-Evaluation-Dataset/tree/master/data"

_LICENSE = "CC-BY-NC 4.0 (Attr Non-Commercial Inter.)"

_BASE_URL = "https://raw.githubusercontent.com/facebookresearch/Neural-Code-Search-Evaluation-Dataset/master/data/"
_URLs = {
    "evaluation_dataset": _BASE_URL + "287_android_questions.json",
    "search_corpus_1": _BASE_URL + "search_corpus_1.tar.gz",
    "search_corpus_2": _BASE_URL + "search_corpus_2.tar.gz",
}


class NeuralCodeSearch(datasets.GeneratorBasedBuilder):
    """Neural Code Search Evaluation Dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="evaluation_dataset",
            version=VERSION,
            description="The evaluation dataset is composed of \
            287 Stack Overflow question and answer pairs",
        ),
        datasets.BuilderConfig(
            name="search_corpus",
            version=VERSION,
            description="The search corpus is indexed using all \
            method bodies parsed from the 24,549 GitHub repositories.",
        ),
    ]

    FILENAME_MAP = {
        "evaluation_dataset": "287_android_questions.json",
        "search_corpus": "search_corpus_1.jsonl",
    }

    def _info(self):
        if self.config.name == "evaluation_dataset":
            features = datasets.Features(
                {
                    "stackoverflow_id": datasets.Value("int32"),
                    "question": datasets.Value("string"),
                    "question_url": datasets.Value("string"),
                    "question_author": datasets.Value("string"),
                    "question_author_url": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "answer_url": datasets.Value("string"),
                    "answer_author": datasets.Value("string"),
                    "answer_author_url": datasets.Value("string"),
                    "examples": datasets.features.Sequence(datasets.Value("int32")),
                    "examples_url": datasets.features.Sequence(datasets.Value("string")),
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "filepath": datasets.Value("string"),
                    "method_name": datasets.Value("string"),
                    "start_line": datasets.Value("int32"),
                    "end_line": datasets.Value("int32"),
                    "url": datasets.Value("string"),
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
        if self.config.name == "evaluation_dataset":
            filepath = dl_manager.download_and_extract(_URLs[self.config.name])
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"filepath": filepath},
                ),
            ]
        else:
            my_urls = [url for config, url in _URLs.items() if config.startswith(self.config.name)]
            archives = dl_manager.download(my_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "files": chain(*(dl_manager.iter_archive(archive) for archive in archives)),
                    },
                ),
            ]

    def _generate_examples(self, filepath=None, files=None):
        """Yields examples."""
        id_ = 0
        if self.config.name == "evaluation_dataset":
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                for row in data:
                    yield id_, {
                        "stackoverflow_id": row["stackoverflow_id"],
                        "question": row["question"],
                        "question_url": row["question_url"],
                        "question_author": row["question_author"],
                        "question_author_url": row["question_author_url"],
                        "answer": row["answer"],
                        "answer_url": row["answer_url"],
                        "answer_author": row["answer_author"],
                        "answer_author_url": row["answer_author_url"],
                        "examples": row["examples"],
                        "examples_url": row["examples_url"],
                    }
                    id_ += 1
        else:
            for _, f in files:
                for row in f:
                    data_dict = json.loads(row.decode("utf-8"))
                    yield id_, {
                        "id": data_dict["id"],
                        "filepath": data_dict["filepath"],
                        "method_name": data_dict["method_name"],
                        "start_line": data_dict["start_line"],
                        "end_line": data_dict["end_line"],
                        "url": data_dict["url"],
                    }
                    id_ += 1
