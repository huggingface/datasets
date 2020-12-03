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
"""Dataset for explainable fake news detection of public health claims."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{kotonya-toni-2020-explainable,
    title = "Explainable Automated Fact-Checking for Public Health Claims",
    author = "Kotonya, Neema and Toni, Francesca",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods
    in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.623",
    pages = "7740--7754",
}
"""

_DESCRIPTION = """\
PUBHEALTH is a comprehensive dataset for explainable automated fact-checking of
public health claims. Each instance in the PUBHEALTH dataset has an associated
veracity label (true, false, unproven, mixture). Furthermore each instance in the
dataset has an explanation text field. The explanation is a justification for which
the claim has been assigned a particular veracity label.

The dataset was created to explore fact-checking of difficult to verify claims i.e.,
those which require expertise from outside of the journalistics domain, in this case
biomedical and public health expertise.

It was also created in response to the lack of fact-checking datasets which provide
gold standard natural language explanations for verdicts/labels.

NOTE: There are missing labels in the dataset and we have replaced them with -1.
"""

_DATA_URL = "https://drive.google.com/uc?export=download&id=1eTtRs5cUlBP5dXsx-FTAlmXuB6JQi2qj"
_TEST_FILE_NAME = "PUBHEALTH/test.tsv"
_TRAIN_FILE_NAME = "PUBHEALTH/train.tsv"
_VAL_FILE_NAME = "PUBHEALTH/dev.tsv"


class HealthFact(datasets.GeneratorBasedBuilder):
    """Dataset for explainable fake news detection of public health claims."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "claim_id": datasets.Value("string"),
                    "claim": datasets.Value("string"),
                    "date_published": datasets.Value("string"),
                    "explanation": datasets.Value("string"),
                    "fact_checkers": datasets.Value("string"),
                    "main_text": datasets.Value("string"),
                    "sources": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["false", "mixture", "true", "unproven"]),
                    "subjects": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/neemakot/Health-Fact-Checking/blob/master/data/DATASHEET.md",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, _TRAIN_FILE_NAME),
                    "split": datasets.Split.TRAIN,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, _TEST_FILE_NAME),
                    "split": datasets.Split.TEST,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, _VAL_FILE_NAME),
                    "split": datasets.Split.VALIDATION,
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf-8") as f:
            label_list = ["false", "mixture", "true", "unproven"]
            data = csv.reader(f, delimiter="\t")
            next(data, None)  # skip the headers
            for row_id, row in enumerate(data):
                row = [x if x != "nan" else "" for x in row]  # nan values changed to empty string
                if split != "test":
                    if len(row) <= 9:
                        elements = ["" for x in range(9 - len(row))]
                        row = row + elements
                    (
                        claim_id,
                        claim,
                        date_published,
                        explanation,
                        fact_checkers,
                        main_text,
                        sources,
                        label,
                        subjects,
                    ) = row
                    if label not in label_list:  # remove stray labels in dev.tsv, train.tsv
                        label = -1
                else:
                    if len(row) <= 10:
                        elements = ["" for x in range(10 - len(row))]
                        row = row + elements
                    (
                        _,
                        claim_id,
                        claim,
                        date_published,
                        explanation,
                        fact_checkers,
                        main_text,
                        sources,
                        label,
                        subjects,
                    ) = row
                    if label not in label_list:  # remove stray labels in test.tsv
                        label = -1
                if label == "":
                    label = -1
                yield row_id, {
                    "claim_id": claim_id,
                    "claim": claim,
                    "date_published": date_published,
                    "explanation": explanation,
                    "fact_checkers": fact_checkers,
                    "main_text": main_text,
                    "sources": sources,
                    "label": label,
                    "subjects": subjects,
                }
