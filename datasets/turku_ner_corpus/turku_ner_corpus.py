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
import os

import datasets


_DESCRIPTION = """\
An open, broad-coverage corpus for Finnish named entity recognition presented in Luoma et al. (2020) A Broad-coverage Corpus for Finnish Named Entity Recognition.
"""
_HOMEPAGE_URL = "https://turkunlp.org/fin-ner.html"
_URL = "https://github.com/TurkuNLP/turku-ner-corpus/archive/v1.0.tar.gz"
_CITATION = """\
@inproceedings{luoma-etal-2020-broad,
title = "A Broad-coverage Corpus for {F}innish Named Entity Recognition",
author = {Luoma, Jouni and Oinonen, Miika and Pyyk{\"o}nen, Maria and Laippala, Veronika and Pyysalo, Sampo},
booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
year = "2020",
url = "https://www.aclweb.org/anthology/2020.lrec-1.567",
pages = "4615--4624",
}
"""


class TurkuNERCorpus(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-DATE",
                                "B-EVENT",
                                "B-LOC",
                                "B-ORG",
                                "B-PER",
                                "B-PRO",
                                "I-DATE",
                                "I-EVENT",
                                "I-LOC",
                                "I-ORG",
                                "I-PER",
                                "I-PRO",
                                "O",
                            ]
                        )
                    ),
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
                gen_kwargs={"data_path": path, "data_type": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_path": path, "data_type": "valid"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_path": path, "data_type": "test"},
            ),
        ]

    def _generate_examples(self, data_path, data_type):
        if data_type == "train":
            data_path = os.path.join(data_path, "turku-ner-corpus-1.0/data/conll/train.tsv")
        elif data_type == "valid":
            data_path = os.path.join(data_path, "turku-ner-corpus-1.0/data/conll/dev.tsv")
        elif data_type == "test":
            data_path = os.path.join(data_path, "turku-ner-corpus-1.0/data/conll/test.tsv")
        else:
            raise Exception("data_type not understood")

        sentence_counter = 0
        with open(data_path, encoding="utf-8") as f:
            current_words = []
            current_labels = []
            for row in f:
                row = row.rstrip()
                row_split = row.split("\t")
                if len(row_split) == 2:
                    token, label = row_split
                    current_words.append(token)
                    current_labels.append(label)
                else:
                    if not current_words:
                        continue
                    assert len(current_words) == len(current_labels), "word len doesnt match label length"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_words,
                            "ner_tags": current_labels,
                        },
                    )
                    sentence_counter += 1
                    current_words = []
                    current_labels = []
                    yield sentence

            # if something remains:
            if current_words:
                sentence = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "tokens": current_words,
                        "ner_tags": current_labels,
                    },
                )
                yield sentence
