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
SimpleQuestions is a dataset for simple QA, which consists
of a total of 108,442 questions written in natural language by human
English-speaking annotators each paired with a corresponding fact,
formatted as (subject, relationship, object), that provides the answer
but also a complete explanation.  Fast have been extracted from the
Knowledge Base Freebase (freebase.com).  We randomly shuffle these
questions and use 70% of them (75910) as training set, 10% as
validation set (10845), and the remaining 20% as test set.
"""
_HOMEPAGE_URL = "https://research.fb.com/downloads/babi/"
_CITATION = """\
@misc{bordes2015largescale,
      title={Large-scale Simple Question Answering with Memory Networks},
      author={Antoine Bordes and Nicolas Usunier and Sumit Chopra and Jason Weston},
      year={2015},
      eprint={1506.02075},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
"""

_URL = "https://www.dropbox.com/s/tohrsllcfy7rch4/SimpleQuestions_v2.tgz?dl=1"


class SimpleQuestionsV2Config(datasets.BuilderConfig):
    def __init__(self, *args, data_type=None, **kwargs):
        super().__init__(*args, version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_type = data_type


class SimpleQuestionsV2(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        SimpleQuestionsV2Config(name="annotated", data_type="annotated", description=f"Annotated dataset"),
        SimpleQuestionsV2Config(name="freebase2m", data_type="freebase2m", description=f"Freebase subset 2M"),
        SimpleQuestionsV2Config(name="freebase5m", data_type="freebase5m", description=f"Freebase subset 5M"),
    ]
    BUILDER_CONFIG_CLASS = SimpleQuestionsV2Config
    DEFAULT_CONFIG_NAME = "annotated"

    def _info(self):
        if self.config.data_type == "annotated":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "subject_entity": datasets.Value("string"),
                    "relationship": datasets.Value("string"),
                    "object_entity": datasets.Value("string"),
                    "question": datasets.Value("string"),
                },
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "subject_entity": datasets.Value("string"),
                    "relationship": datasets.Value("string"),
                    "object_entities": datasets.Sequence(datasets.Value("string")),
                },
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        if self.config.data_type == "annotated":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"datapath": os.path.join(path, "SimpleQuestions_v2", "annotated_fb_data_train.txt")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"datapath": os.path.join(path, "SimpleQuestions_v2", "annotated_fb_data_train.txt")},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"datapath": os.path.join(path, "SimpleQuestions_v2", "annotated_fb_data_train.txt")},
                ),
            ]
        elif self.config.data_type == "freebase2m":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datapath": os.path.join(
                            path,
                            "SimpleQuestions_v2",
                            "freebase-subsets",
                            "freebase-FB2M.txt",
                        )
                    },
                )
            ]
        elif self.config.data_type == "freebase5m":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "datapath": os.path.join(
                            path,
                            "SimpleQuestions_v2",
                            "freebase-subsets",
                            "freebase-FB5M.txt",
                        )
                    },
                )
            ]
        else:
            raise Exception("Unknown data type. Try one of: annotated, freebase2m and freebase5m")

    def _generate_examples(self, datapath):
        if self.config.data_type == "annotated":
            with open(datapath, encoding="utf-8") as f:
                for sentence_counter, row in enumerate(f):
                    row = row.split("\t")
                    result = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "subject_entity": row[0],
                            "relationship": row[1],
                            "object_entity": row[2],
                            "question": row[3],
                        },
                    )
                    yield result
        else:
            with open(datapath, encoding="utf-8") as f:
                for sentence_counter, row in enumerate(f):
                    row = row.split("\t")
                    result = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "subject_entity": row[0],
                            "relationship": row[1],
                            "object_entities": row[2].split(),
                        },
                    )
                    yield result
