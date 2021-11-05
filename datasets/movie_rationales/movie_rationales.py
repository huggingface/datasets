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
"""Movie reviews with human annotated rationales."""


import json

import datasets


_CITATION = """
@unpublished{eraser2019,
    title = {ERASER: A Benchmark to Evaluate Rationalized NLP Models},
    author = {Jay DeYoung and Sarthak Jain and Nazneen Fatema Rajani and Eric Lehman and Caiming Xiong and Richard Socher and Byron C. Wallace}
}
@InProceedings{zaidan-eisner-piatko-2008:nips,
  author    =  {Omar F. Zaidan  and  Jason Eisner  and  Christine Piatko},
  title     =  {Machine Learning with Annotator Rationales to Reduce Annotation Cost},
  booktitle =  {Proceedings of the NIPS*2008 Workshop on Cost Sensitive Learning},
  month     =  {December},
  year      =  {2008}
}
"""

_DESCRIPTION = """
The movie rationale dataset contains human annotated rationales for movie
reviews.
"""

_DOWNLOAD_URL = "http://www.eraserbenchmark.com/zipped/movies.tar.gz"


class MovieRationales(datasets.GeneratorBasedBuilder):
    """Movie reviews with human annotated rationales."""

    VERSION = datasets.Version("0.1.0")
    test_dummy_data = False  # dummy data don't support having a specific order for the files in the archive

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "review": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["NEG", "POS"]),
                    "evidences": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="http://www.cs.jhu.edu/~ozaidan/rationales/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive = dl_manager.download(_DOWNLOAD_URL)
        data_dir = "movies/"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "reviews_dir": data_dir + "docs",
                    "filepath": data_dir + "train.jsonl",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "reviews_dir": data_dir + "docs",
                    "filepath": data_dir + "val.jsonl",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "reviews_dir": data_dir + "docs",
                    "filepath": data_dir + "test.jsonl",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, reviews_dir, filepath, files):
        """Yields examples."""
        reviews = {}
        for path, f in files:
            if path.startswith(reviews_dir):
                reviews[path.split("/")[-1]] = f.read().decode("utf-8")
            elif path == filepath:
                for line in f:
                    row = json.loads(line.decode("utf-8"))
                    doc_id = row["annotation_id"]
                    review_text = reviews[doc_id]

                    evidences = []
                    for evidence in row["evidences"]:
                        for e in evidence:
                            evidences.append(e["text"])

                    yield doc_id, {
                        "review": review_text,
                        "label": row["classification"],
                        "evidences": evidences,
                    }
                break
