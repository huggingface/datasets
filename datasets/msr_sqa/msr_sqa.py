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
"""Microsoft Research Sequential Question Answering (SQA) Dataset"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{iyyer2017search,
  title={Search-based neural structured learning for sequential question answering},
  author={Iyyer, Mohit and Yih, Wen-tau and Chang, Ming-Wei},
  booktitle={Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={1821--1831},
  year={2017}
}
"""

_DESCRIPTION = """\
Recent work in semantic parsing for question answering has focused on long and complicated questions, \
many of which would seem unnatural if asked in a normal conversation between two humans. \
In an effort to explore a conversational QA setting, we present a more realistic task: \
answering sequences of simple but inter-related questions. We created SQA by asking crowdsourced workers \
to decompose 2,022 questions from WikiTableQuestions (WTQ), which contains highly-compositional questions about \
tables from Wikipedia. We had three workers decompose each WTQ question, resulting in a dataset of 6,066 sequences \
that contain 17,553 questions in total. Each question is also associated with answers in the form of cell \
locations in the tables.
"""

_HOMEPAGE = "https://msropendata.com/datasets/b25190ed-0f59-47b1-9211-5962858142c2"

_LICENSE = "Microsoft Research Data License Agreement"

_URL = "https://download.microsoft.com/download/1/D/C/1DC270D2-1B53-4A61-A2E3-88AB3E4E6E1F/SQA%20Release%201.0.zip"


class MsrSQA(datasets.GeneratorBasedBuilder):
    """Microsoft Research Sequential Question Answering (SQA) Dataset"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "annotator": datasets.Value("int32"),
                    "position": datasets.Value("int32"),
                    "question": datasets.Value("string"),
                    "table_file": datasets.Value("string"),
                    "table_header": datasets.features.Sequence(datasets.Value("string")),
                    "table_data": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                    "answer_coordinates": datasets.features.Sequence(datasets.Value("string")),
                    "answer_text": datasets.features.Sequence(datasets.Value("string"))
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.join(dl_manager.download_and_extract(_URL), "SQA Release 1.0")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "data_dir": data_dir
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.tsv"),
                    "data_dir": data_dir
                },
            )
        ]

    def _generate_examples(self, filepath, data_dir):
        """ Yields examples. """

        def load_table_data(table_file):
            with open(table_file, encoding="utf-8") as f:
                lines = f.readlines()
            header = lines[0].strip().split(",")
            data = [line.strip().split(",") for line in lines[1:]]
            return header, data

        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                item = dict(row)
                item["answer_text"] = eval(item["answer_text"])
                item["answer_coordinates"] = eval(item["answer_coordinates"])
                header, table_data = load_table_data(os.path.join(data_dir, item["table_file"]))
                item["table_header"] = header
                item["table_data"] = table_data
                yield item["id"], item
