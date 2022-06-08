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
"""Passage, query, answers and answer classification with explanations."""


import json

import datasets


_CITATION = """
@unpublished{eraser2019,
    title = {ERASER: A Benchmark to Evaluate Rationalized NLP Models},
    author = {Jay DeYoung and Sarthak Jain and Nazneen Fatema Rajani and Eric Lehman and Caiming Xiong and Richard Socher and Byron C. Wallace}
}
@inproceedings{MultiRC2018,
    author = {Daniel Khashabi and Snigdha Chaturvedi and Michael Roth and Shyam Upadhyay and Dan Roth},
    title = {Looking Beyond the Surface:A Challenge Set for Reading Comprehension over Multiple Sentences},
    booktitle = {NAACL},
    year = {2018}
}
"""

_DESCRIPTION = """
Eraser Multi RC is a dataset for queries over multi-line passages, along with
answers and a rationalte. Each example in this dataset has the following 5 parts
1. A Mutli-line Passage
2. A Query about the passage
3. An Answer to the query
4. A Classification as to whether the answer is right or wrong
5. An Explanation justifying the classification
"""

_DOWNLOAD_URL = "http://www.eraserbenchmark.com/zipped/multirc.tar.gz"


class EraserMultiRc(datasets.GeneratorBasedBuilder):
    """Multi Sentence Reasoning with Explanations (Eraser Benchmark)."""

    VERSION = datasets.Version("0.1.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "passage": datasets.Value("string"),
                    "query_and_answer": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["False", "True"]),
                    "evidences": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="https://cogcomp.seas.upenn.edu/multirc/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        archive = dl_manager.download(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "multirc/train.jsonl"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "multirc/val.jsonl"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"files": dl_manager.iter_archive(archive), "split_file": "multirc/test.jsonl"},
            ),
        ]

    def _generate_examples(self, files, split_file):
        """Yields examples."""

        multirc_dir = "multirc/docs"
        docs = {}
        for path, f in files:
            docs[path] = f.read().decode("utf-8")
        for line in docs[split_file].splitlines():
            row = json.loads(line)
            evidences = []

            for evidence in row["evidences"][0]:
                docid = evidence["docid"]
                evidences.append(evidence["text"])

            passage_file = "/".join([multirc_dir, docid])
            passage_text = docs[passage_file]

            yield row["annotation_id"], {
                "passage": passage_text,
                "query_and_answer": row["query"],
                "label": row["classification"],
                "evidences": evidences,
            }
