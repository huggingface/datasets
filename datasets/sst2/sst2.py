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
"""SST-2 (Stanford Sentiment Treebank v2) dataset."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{socher2013recursive,
  title={Recursive deep models for semantic compositionality over a sentiment treebank},
  author={Socher, Richard and Perelygin, Alex and Wu, Jean and Chuang, Jason and Manning, Christopher D and Ng, Andrew and Potts, Christopher},
  booktitle={Proceedings of the 2013 conference on empirical methods in natural language processing},
  pages={1631--1642},
  year={2013}
}
"""

_DESCRIPTION = """\
The Stanford Sentiment Treebank consists of sentences from movie reviews and
human annotations of their sentiment. The task is to predict the sentiment of a
given sentence. We use the two-way (positive/negative) class split, and use only
sentence-level labels.
"""

_HOMEPAGE = "https://nlp.stanford.edu/sentiment/"

_LICENSE = "Unknown"

_URL = "https://dl.fbaipublicfiles.com/glue/data/SST-2.zip"


class Sst2(datasets.GeneratorBasedBuilder):
    """SST-2 dataset."""

    VERSION = datasets.Version("2.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "idx": datasets.Value("int32"),
                "sentence": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["negative", "positive"]),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "file_paths": dl_manager.iter_files(dl_dir),
                    "data_filename": "train.tsv",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "file_paths": dl_manager.iter_files(dl_dir),
                    "data_filename": "dev.tsv",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "file_paths": dl_manager.iter_files(dl_dir),
                    "data_filename": "test.tsv",
                },
            ),
        ]

    def _generate_examples(self, file_paths, data_filename):
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            if filename == data_filename:
                with open(file_path, encoding="utf8") as f:
                    reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                    for idx, row in enumerate(reader):
                        yield idx, {
                            "idx": row["index"] if "index" in row else idx,
                            "sentence": row["sentence"],
                            "label": int(row["label"]) if "label" in row else -1,
                        }
