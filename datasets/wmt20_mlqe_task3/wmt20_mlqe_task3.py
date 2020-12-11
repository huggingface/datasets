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
"""WMT MLQE Shared task 3."""

from __future__ import absolute_import, division, print_function

import csv
import glob
import os

import datasets


_CITATION = """
Not available.
"""

_DESCRIPTION = """\
This shared task (part of WMT20) will build on its previous editions
to further examine automatic methods for estimating the quality
of neural machine translation output at run-time, without relying
on reference translations. As in previous years, we cover estimation
at various levels. Important elements introduced this year include: a new
task where sentences are annotated with Direct Assessment (DA)
scores instead of labels based on post-editing; a new multilingual
sentence-level dataset mainly from Wikipedia articles, where the
source articles can be retrieved for document-wide context; the
availability of NMT models to explore system-internal information for the task.

The goal of this task 3 is to predict document-level quality scores as well as fine-grained annotations.
"""

_HOMEPAGE = "http://www.statmt.org/wmt20/quality-estimation-task.html"

_LICENSE = "Unknown"

_URLs = {
    "train+dev": "https://github.com/deep-spin/deep-spin.github.io/raw/master/docs/data/wmt2020_qe/qe-task3-enfr-traindev.tar.gz",
    "test": "https://github.com/deep-spin/deep-spin.github.io/raw/master/docs/data/wmt2020_qe/qe-enfr-blindtest.tar.gz",
}


_ANNOTATION_CATEGORIES = [
    "Addition",
    "Agreement",
    "Ambiguous Translation",
    "Capitalization",
    "Character Encoding",
    "Company Terminology",
    "Date/Time",
    "Diacritics",
    "Duplication",
    "False Friend",
    "Grammatical Register",
    "Hyphenation",
    "Inconsistency",
    "Lexical Register",
    "Lexical Selection",
    "Named Entity",
    "Number",
    "Omitted Auxiliary Verb",
    "Omitted Conjunction",
    "Omitted Determiner",
    "Omitted Preposition",
    "Omitted Pronoun",
    "Orthography",
    "Other POS Omitted",
    "Over-translation",
    "Overly Literal",
    "POS",
    "Punctuation",
    "Shouldn't Have Been Translated",
    "Shouldn't have been translated",
    "Spelling",
    "Tense/Mood/Aspect",
    "Under-translation",
    "Unidiomatic",
    "Unintelligible",
    "Unit Conversion",
    "Untranslated",
    "Whitespace",
    "Word Order",
    "Wrong Auxiliary Verb",
    "Wrong Conjunction",
    "Wrong Determiner",
    "Wrong Language Variety",
    "Wrong Preposition",
    "Wrong Pronoun",
]


class Wmt20MlqeTask3(datasets.GeneratorBasedBuilder):
    """WMT MLQE Shared task 3."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=f"plain_text",
            version=datasets.Version("1.1.0"),
            description=f"Plain text",
        )
    ]

    def _info(self):
        features = datasets.Features(
            {
                "document_id": datasets.Value("string"),
                "source_segments": datasets.Sequence(datasets.Value("string")),
                "source_tokenized": datasets.Sequence(datasets.Value("string")),
                "mt_segments": datasets.Sequence(datasets.Value("string")),
                "mt_tokenized": datasets.Sequence(datasets.Value("string")),
                "annotations": datasets.Sequence(
                    {
                        "segment_id": datasets.Sequence(datasets.Value("int32")),
                        "annotation_start": datasets.Sequence(datasets.Value("int32")),
                        "annotation_length": datasets.Sequence(datasets.Value("int32")),
                        "severity": datasets.ClassLabel(names=["minor", "major", "critical"]),
                        "severity_weight": datasets.Value("float32"),
                        "category": datasets.ClassLabel(names=_ANNOTATION_CATEGORIES),
                    }
                ),
                "token_annotations": datasets.Sequence(
                    {
                        "segment_id": datasets.Sequence(datasets.Value("int32")),
                        "first_token": datasets.Sequence(datasets.Value("int32")),
                        "last_token": datasets.Sequence(datasets.Value("int32")),
                        "token_after_gap": datasets.Sequence(datasets.Value("int32")),
                        "severity": datasets.ClassLabel(names=["minor", "major", "critical"]),
                        "category": datasets.ClassLabel(names=_ANNOTATION_CATEGORIES),
                    }
                ),
                "token_index": datasets.Sequence(datasets.Sequence(datasets.Sequence(datasets.Value("int32")))),
                "total_words": datasets.Value("int32"),
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
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train+dev"], "task3", "train"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["test"], "test-blind"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train+dev"], "task3", "dev"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        def open_and_read(fp):
            with open(fp, encoding="utf-8") as f:
                return f.read().splitlines()

        for id_, folder in enumerate(sorted(glob.glob(os.path.join(filepath, "*")))):
            source_segments = open_and_read(os.path.join(folder, "source.segments"))
            source_tokenized = open_and_read(os.path.join(folder, "source.tokenized"))
            mt_segments = open_and_read(os.path.join(folder, "mt.segments"))
            mt_tokenized = open_and_read(os.path.join(folder, "mt.tokenized"))

            if split in ["train", "dev"] and not os.path.exists(os.path.join(folder, "token_index")):
                token_index = []
            else:
                token_index = [
                    [idx.split(" ") for idx in line.split("\t")]
                    for line in open_and_read(os.path.join(folder, "token_index"))
                    if line != ""
                ]
            total_words = open_and_read(os.path.join(folder, "total_words"))[0]

            if split in ["train", "dev"]:
                with open(os.path.join(folder, "annotations.tsv"), encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter="\t")
                    annotations = [
                        {
                            "segment_id": row["segment_id"].split(" "),
                            "annotation_start": row["annotation_start"].split(" "),
                            "annotation_length": row["annotation_length"].split(" "),
                            "severity": row["severity"],
                            "severity_weight": row["severity_weight"],
                            "category": row["category"],
                        }
                        for row in reader
                    ]
                with open(os.path.join(folder, "token_annotations.tsv"), encoding="utf-8") as f:
                    reader = csv.DictReader(f, delimiter="\t")
                    token_annotations = [
                        {
                            "segment_id": row["segment_id"].split(" "),
                            "first_token": row["first_token"].replace("-", "-1").split(" "),
                            "last_token": row["last_token"].replace("-", "-1").split(" "),
                            "token_after_gap": row["token_after_gap"].replace("-", "-1").split(" "),
                            "severity": row["severity"],
                            "category": row["category"],
                        }
                        for row in reader
                    ]
            else:
                annotations = []
                token_annotations = []

            yield id_, {
                "document_id": os.path.basename(folder),
                "source_segments": source_segments,
                "source_tokenized": source_tokenized,
                "mt_segments": mt_segments,
                "mt_tokenized": mt_tokenized,
                "annotations": annotations,
                "token_annotations": token_annotations,
                "token_index": token_index,
                "total_words": total_words,
            }
