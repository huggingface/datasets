# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Arabic Wiki Question Answering corpus."""


import csv

import datasets


_CITATION = """\
@InProceedings{YangYihMeek:EMNLP2015:WikiQA,
       author = {{Yi}, Yang and {Wen-tau},  Yih and {Christopher} Meek},
        title = "{WikiQA: A Challenge Dataset for Open-Domain Question Answering}",
      journal = {Association for Computational Linguistics},
         year = 2015,
          doi = {10.18653/v1/D15-1237},
        pages = {2013–2018},
}
"""

_DESCRIPTION = """\
Arabic Version of WikiQA by automatic automatic machine translators \
and crowdsourced the selection of the best one to be incorporated into the corpus
"""

_URL = "https://raw.githubusercontent.com/qcri/WikiQAar/master/"
_URL_FILES = {
    "train": _URL + "WikiQAar-train.tsv",
    "dev": _URL + "WikiQAar-dev.tsv",
    "test": _URL + "WikiQAar-test.tsv",
}


class WikiQaArConfig(datasets.BuilderConfig):
    """BuilderConfig for WikiQaAr."""

    def __init__(self, **kwargs):
        """BuilderConfig for WikiQaAr.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(WikiQaArConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class WikiQaAr(datasets.GeneratorBasedBuilder):
    """WikiQaAr dataset."""

    BUILDER_CONFIGS = [
        WikiQaArConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "question_id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "document_id": datasets.Value("string"),
                    "answer_id": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(num_classes=2),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/qcri/WikiQAar",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URL_FILES)

        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": dl_dir["test"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": dl_dir["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dl_dir["train"]}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for _id, row in enumerate(reader):

                # ignore some entries with errors
                if len(row) > 6 or len(row["Label"]) == 0:
                    continue

                yield str(_id), {
                    "question_id": row["QuestionID"],
                    "question": row["Question"],
                    "document_id": row["DocumentID"],
                    "answer_id": row["SentenceID"],
                    "answer": row["Sentence"],
                    "label": row["Label"],
                }
