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
"""Qasper: A Dataset of Information-Seeking Questions and Answers Anchored in Research Papers."""


import json

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{Dasigi2021ADO,
  title={A Dataset of Information-Seeking Questions and Answers Anchored in Research Papers},
  author={Pradeep Dasigi and Kyle Lo and Iz Beltagy and Arman Cohan and Noah A. Smith and Matt Gardner},
  year={2021}
}
"""
_LICENSE = "CC BY 4.0"
_DESCRIPTION = """\
A dataset containing 1585 papers with 5049 information-seeking questions asked by regular readers of NLP papers, and answered by a separate set of NLP practitioners.
"""

_HOMEPAGE = "https://allenai.org/data/qasper"
_URL = "https://qasper-dataset.s3-us-west-2.amazonaws.com/qasper-train-dev-v0.1.tgz"
_DATA_FILES = {"train": "qasper-train-v0.1.json", "dev": "qasper-dev-v0.1.json"}

_VERSION = "0.1.0"


class Qasper(datasets.GeneratorBasedBuilder):
    """Qasper: A Dataset of Information-Seeking Q&A Anchored in Research Papers."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="qasper",
            version=datasets.Version(_VERSION),
            description=_DESCRIPTION,
        )
    ]

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "abstract": datasets.Value("string"),
                "full_text": datasets.features.Sequence(
                    {
                        "section_name": datasets.Value("string"),
                        "paragraphs": [datasets.Value("string")],
                    }
                ),
                "qas": datasets.features.Sequence(
                    {
                        "question": datasets.Value("string"),
                        "question_id": datasets.Value("string"),
                        "nlp_background": datasets.Value("string"),
                        "topic_background": datasets.Value("string"),
                        "paper_read": datasets.Value("string"),
                        "search_query": datasets.Value("string"),
                        "question_writer": datasets.Value("string"),
                        "answers": datasets.features.Sequence(
                            {
                                "answer": {
                                    "unanswerable": datasets.Value("bool"),
                                    "extractive_spans": datasets.features.Sequence(datasets.Value("string")),
                                    "yes_no": datasets.Value("bool"),
                                    "free_form_answer": datasets.Value("string"),
                                    "evidence": datasets.features.Sequence(datasets.Value("string")),
                                    "highlighted_evidence": datasets.features.Sequence(datasets.Value("string")),
                                },
                                "annotation_id": datasets.Value("string"),
                                "worker_id": datasets.Value("string"),
                            }
                        ),
                    }
                ),
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
        archive = dl_manager.download(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": _DATA_FILES["train"], "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": _DATA_FILES["dev"], "files": dl_manager.iter_archive(archive)},
            ),
        ]

    def _generate_examples(self, filepath, files):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        for path, f in files:
            if path == filepath:
                qasper = json.loads(f.read().decode("utf-8"))
                for id_ in qasper:
                    qasper[id_]["id"] = id_
                    yield id_, qasper[id_]
                break
