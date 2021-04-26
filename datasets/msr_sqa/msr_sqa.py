# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors, The Google AI Language Team Authors and the current dataset script contributor.
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


import ast
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


def _load_table_data(table_file):
    """Load additional data from a csv table file.

    Args:
        table_file: Path to the csv file.

    Returns:
        header: a list of headers in the table.
        data: 2d array of data in the table.
    """
    with open(table_file, encoding="utf-8") as f:
        lines = f.readlines()
    header = lines[0].strip().split(",")
    data = [line.strip().split(",") for line in lines[1:]]
    return header, data


def _parse_answer_coordinates(answer_coordinate_str):
    """Parsing answer_coordinates field to a list of answer coordinates.
    The original code is from https://github.com/google-research/tapas.

    Args:
      answer_coordinate_str: A string representation of a Python list of tuple
        strings.
        For example: "['(1, 4)','(1, 3)', ...]"

    Returns:
      answer_coordinates: A list of answer cordinates.
    """
    try:
        answer_coordinates = []
        coords = ast.literal_eval(answer_coordinate_str)
        for row_index, column_index in sorted(ast.literal_eval(coord) for coord in coords):
            answer_coordinates.append({"row_index": row_index, "column_index": column_index})
        return answer_coordinates
    except SyntaxError:
        raise ValueError("Unable to evaluate %s" % answer_coordinate_str)


def _parse_answer_text(answer_text_str):
    """Parsing `answer_text` field to list of answers.
    The original code is from https://github.com/google-research/tapas.
    Args:
      answer_text_str: A string representation of a Python list of strings.
        For example: "[u'test', u'hello', ...]"

    Returns:
      answer_texts: A list of answers.
    """
    try:
        answer_texts = []
        for value in ast.literal_eval(answer_text_str):
            answer_texts.append(value)
        return answer_texts
    except SyntaxError:
        raise ValueError("Unable to evaluate %s" % answer_text_str)


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
                    "answer_coordinates": datasets.features.Sequence(
                        {"row_index": datasets.Value("int32"), "column_index": datasets.Value("int32")}
                    ),
                    "answer_text": datasets.features.Sequence(datasets.Value("string")),
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
                gen_kwargs={"filepath": os.path.join(data_dir, "train.tsv"), "data_dir": data_dir},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test.tsv"), "data_dir": data_dir},
            ),
        ]

    def _generate_examples(self, filepath, data_dir):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                item = dict(row)
                item["answer_text"] = _parse_answer_text(item["answer_text"])
                item["answer_coordinates"] = _parse_answer_coordinates(item["answer_coordinates"])
                header, table_data = _load_table_data(os.path.join(data_dir, item["table_file"]))
                item["table_header"] = header
                item["table_data"] = table_data
                yield item["id"], item
