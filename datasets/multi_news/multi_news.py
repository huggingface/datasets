# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""Multi-News dataset."""

from __future__ import absolute_import, division, print_function

import os

import nlp


_CITATION = """
@misc{alex2019multinews,
    title={Multi-News: a Large-Scale Multi-Document Summarization Dataset and Abstractive Hierarchical Model},
    author={Alexander R. Fabbri and Irene Li and Tianwei She and Suyi Li and Dragomir R. Radev},
    year={2019},
    eprint={1906.01749},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
Multi-News, consists of news articles and human-written summaries
of these articles from the site newser.com.
Each summary is professionally written by editors and
includes links to the original articles cited.

There are two features:
  - document: text of news articles seperated by special token "|||||".
  - summary: news summary.
"""

_URL = "https://drive.google.com/uc?export=download&id=1vRY2wM6rlOZrf9exGTm5pXj5ExlVwJ0C"

_DOCUMENT = "document"
_SUMMARY = "summary"


class MultiNews(nlp.GeneratorBasedBuilder):
    """Multi-News dataset."""

    VERSION = nlp.Version("1.0.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({_DOCUMENT: nlp.Value("string"), _SUMMARY: nlp.Value("string")}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage="https://github.com/Alex-Fabbri/Multi-News",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        extract_path = os.path.join(dl_manager.download_and_extract(_URL), "multi-news-original")
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"path": os.path.join(extract_path, "train")},),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"path": os.path.join(extract_path, "val")},),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"path": os.path.join(extract_path, "test")},),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(os.path.join(path + ".src")) as src_f, open(os.path.join(path + ".tgt")) as tgt_f:
            for i, (src_line, tgt_line) in enumerate(zip(src_f, tgt_f)):
                yield i, {
                    # In original file, each line has one example and natural newline
                    # tokens "\n" are being replaced with "NEWLINE_CHAR". Here restore
                    # the natural newline token to avoid special vocab "NEWLINE_CHAR".
                    _DOCUMENT: src_line.strip().replace("NEWLINE_CHAR", "\n"),
                    # Remove the starting token "- " for every target sequence.
                    _SUMMARY: tgt_line.strip().lstrip("- "),
                }
