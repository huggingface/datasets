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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This dataset is used to train models for Natural Language Inference Tasks in Low-Resource Languages like Hindi.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/midas-research/hindi-nli-data"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = """
MIT License

Copyright (c) 2019 MIDAS, IIIT Delhi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/midas-research/hindi-nli-data/master/Textual_Entailment/BBC/BBC_recasted_train.tsv"
_VALID_DOWNLOAD_URL = "https://raw.githubusercontent.com/midas-research/hindi-nli-data/master/Textual_Entailment/BBC/BBC_recasted_dev.tsv"
_TEST_DOWNLOAD_URL = "https://raw.githubusercontent.com/midas-research/hindi-nli-data/master/Textual_Entailment/BBC/BBC_recasted_test.tsv"


class BBC_Hindi_NLI(datasets.GeneratorBasedBuilder):
    """BBC Hindi NLI dataset -- Dataset providing textual-entailment pairs for NLI tasks in Hindi"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "Context": datasets.Value("string"),
                    "Hypothesis": datasets.Value("string"),
                    "Entailment_Label": datasets.Value("string"),
                    "Topic_Label": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        valid_path = dl_manager.download_and_extract(_VALID_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """

        with open(filepath, encoding="utf-8") as tsv_file:
            tsv_reader = csv.reader(tsv_file, delimiter="\t")
            for id_, row in enumerate(tsv_reader):
                (context, hypothesis, entailment_label, topic_label) = row
                yield id_, {
                    "Context": context,
                    "Hypothesis": hypothesis,
                    "Entailment_Label": entailment_label,
                    "Topic_Label": topic_label,
                }
