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
"""The Text REtrieval Conference (TREC) Question Classification dataset."""


import datasets


_DESCRIPTION = """\
The Text REtrieval Conference (TREC) Question Classification dataset contains 5500 labeled questions in training set and another 500 for test set.

The dataset has 6 coarse class labels and 50 fine class labels. Average length of each sentence is 10, vocabulary size of 8700.

Data are collected from four sources: 4,500 English questions published by USC (Hovy et al., 2001), about 500 manually constructed questions for a few rare classes, 894 TREC 8 and TREC 9 questions, and also 500 questions from TREC 10 which serves as the test set. These questions were manually labeled.
"""

_HOMEPAGE = "https://cogcomp.seas.upenn.edu/Data/QA/QC/"

_CITATION = """\
@inproceedings{li-roth-2002-learning,
    title = "Learning Question Classifiers",
    author = "Li, Xin  and
      Roth, Dan",
    booktitle = "{COLING} 2002: The 19th International Conference on Computational Linguistics",
    year = "2002",
    url = "https://www.aclweb.org/anthology/C02-1150",
}
@inproceedings{hovy-etal-2001-toward,
    title = "Toward Semantics-Based Answer Pinpointing",
    author = "Hovy, Eduard  and
      Gerber, Laurie  and
      Hermjakob, Ulf  and
      Lin, Chin-Yew  and
      Ravichandran, Deepak",
    booktitle = "Proceedings of the First International Conference on Human Language Technology Research",
    year = "2001",
    url = "https://www.aclweb.org/anthology/H01-1069",
}
"""

_URLs = {
    "train": "https://cogcomp.seas.upenn.edu/Data/QA/QC/train_5500.label",
    "test": "https://cogcomp.seas.upenn.edu/Data/QA/QC/TREC_10.label",
}

_COARSE_LABELS = ["ABBR", "ENTY", "DESC", "HUM", "LOC", "NUM"]

_FINE_LABELS = [
    "ABBR:abb",
    "ABBR:exp",
    "ENTY:animal",
    "ENTY:body",
    "ENTY:color",
    "ENTY:cremat",
    "ENTY:currency",
    "ENTY:dismed",
    "ENTY:event",
    "ENTY:food",
    "ENTY:instru",
    "ENTY:lang",
    "ENTY:letter",
    "ENTY:other",
    "ENTY:plant",
    "ENTY:product",
    "ENTY:religion",
    "ENTY:sport",
    "ENTY:substance",
    "ENTY:symbol",
    "ENTY:techmeth",
    "ENTY:termeq",
    "ENTY:veh",
    "ENTY:word",
    "DESC:def",
    "DESC:desc",
    "DESC:manner",
    "DESC:reason",
    "HUM:gr",
    "HUM:ind",
    "HUM:title",
    "HUM:desc",
    "LOC:city",
    "LOC:country",
    "LOC:mount",
    "LOC:other",
    "LOC:state",
    "NUM:code",
    "NUM:count",
    "NUM:date",
    "NUM:dist",
    "NUM:money",
    "NUM:ord",
    "NUM:other",
    "NUM:period",
    "NUM:perc",
    "NUM:speed",
    "NUM:temp",
    "NUM:volsize",
    "NUM:weight",
]


class Trec(datasets.GeneratorBasedBuilder):
    """The Text REtrieval Conference (TREC) Question Classification dataset."""

    VERSION = datasets.Version("2.0.0", description="Fine label contains 50 classes instead of 47.")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS),
                    "fine_label": datasets.ClassLabel(names=_FINE_LABELS),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_files = dl_manager.download(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": dl_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": dl_files["test"],
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, "rb") as f:
            for id_, row in enumerate(f):
                # One non-ASCII byte: sisterBADBYTEcity. We replace it with a space
                fine_label, _, text = row.replace(b"\xf0", b" ").strip().decode().partition(" ")
                coarse_label = fine_label.split(":")[0]
                yield id_, {
                    "text": text,
                    "coarse_label": coarse_label,
                    "fine_label": fine_label,
                }
