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
"""LIAR is a dataset for fake news detection with annotated claims."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{wang-2017-liar,
title = "{``}Liar, Liar Pants on Fire{''}: A New Benchmark Dataset for Fake News Detection",
author = "Wang, William Yang",
booktitle = "Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)",
month = jul,
year = "2017",
address = "Vancouver, Canada",
publisher = "Association for Computational Linguistics",
url = "https://www.aclweb.org/anthology/P17-2067",
doi = "10.18653/v1/P17-2067",
pages = "422--426",
abstract = "Automatic fake news detection is a challenging problem in deception detection, and it has tremendous real-world political and social impacts. However, statistical approaches to combating fake news has been dramatically limited by the lack of labeled benchmark datasets. In this paper, we present LIAR: a new, publicly available dataset for fake news detection. We collected a decade-long, 12.8K manually labeled short statements in various contexts from PolitiFact.com, which provides detailed analysis report and links to source documents for each case. This dataset can be used for fact-checking research as well. Notably, this new dataset is an order of magnitude larger than previously largest public fake news datasets of similar type. Empirically, we investigate automatic fake news detection based on surface-level linguistic patterns. We have designed a novel, hybrid convolutional neural network to integrate meta-data with text. We show that this hybrid approach can improve a text-only deep learning model.",
}
"""

_DESCRIPTION = """\
LIAR is a dataset for fake news detection with 12.8K human labeled short statements from politifact.com's API, and each statement is evaluated by a politifact.com editor for its truthfulness. The distribution of labels in the LIAR dataset is relatively well-balanced: except for 1,050 pants-fire cases, the instances for all other labels range from 2,063 to 2,638. In each case, the labeler provides a lengthy analysis report to ground each judgment.
"""

_HOMEPAGE = "https://www.aclweb.org/anthology/P17-2067"

_LICENSE = "Unknown"

_URL = "https://www.cs.ucsb.edu/~william/data/liar_dataset.zip"


class Liar(datasets.GeneratorBasedBuilder):
    """LIAR is a dataset for fake news detection with annotated claims."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "label": datasets.ClassLabel(
                        names=[
                            "false",
                            "half-true",
                            "mostly-true",
                            "true",
                            "barely-true",
                            "pants-fire",
                        ]
                    ),
                    "statement": datasets.Value("string"),
                    "subject": datasets.Value("string"),
                    "speaker": datasets.Value("string"),
                    "job_title": datasets.Value("string"),
                    "state_info": datasets.Value("string"),
                    "party_affiliation": datasets.Value("string"),
                    "barely_true_counts": datasets.Value("float"),
                    "false_counts": datasets.Value("float"),
                    "half_true_counts": datasets.Value("float"),
                    "mostly_true_counts": datasets.Value("float"),
                    "pants_on_fire_counts": datasets.Value("float"),
                    "context": datasets.Value("string"),
                }
            ),
            supervised_keys=("statement", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "test.tsv"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "valid.tsv"),
                    "split": "valid",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as tsv_file:
            reader = csv.reader(tsv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(reader):
                yield id_, {
                    "id": row[0],
                    "label": row[1],
                    "statement": row[2],
                    "subject": row[3],
                    "speaker": row[4],
                    "job_title": row[5],
                    "state_info": row[6],
                    "party_affiliation": row[7],
                    "barely_true_counts": row[8],
                    "false_counts": row[9],
                    "half_true_counts": row[10],
                    "mostly_true_counts": row[11],
                    "pants_on_fire_counts": row[12],
                    "context": row[13],
                }
