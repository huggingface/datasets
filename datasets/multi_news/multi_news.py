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
"""Multi-News dataset."""

import datasets


_HOMEPAGE = "https://github.com/Alex-Fabbri/Multi-News"

_LICENSE = "For non-commercial research and educational purposes only"

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

_REPO = "https://huggingface.co/datasets/multi_news/resolve/main/data"
_URLs = {
    "train": [
        f"{_REPO}/train.src.cleaned",
        f"{_REPO}/train.tgt",
    ],
    "val": [
        f"{_REPO}/val.src.cleaned",
        f"{_REPO}/val.tgt",
    ],
    "test": [
        f"{_REPO}/test.src.cleaned",
        f"{_REPO}/test.tgt",
    ],
}

_DOCUMENT = "document"
_SUMMARY = "summary"


class MultiNews(datasets.GeneratorBasedBuilder):
    """Multi-News dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({_DOCUMENT: datasets.Value("string"), _SUMMARY: datasets.Value("string")}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        files = dl_manager.download(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"src_file": files["train"][0], "tgt_file": files["train"][1]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"src_file": files["val"][0], "tgt_file": files["val"][1]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"src_file": files["test"][0], "tgt_file": files["test"][1]},
            ),
        ]

    def _generate_examples(self, src_file, tgt_file):
        """Yields examples."""
        with open(src_file, encoding="utf-8") as src_f, open(tgt_file, encoding="utf-8") as tgt_f:
            for i, (src_line, tgt_line) in enumerate(zip(src_f, tgt_f)):
                yield i, {
                    # In original file, each line has one example and natural newline
                    # tokens "\n" are being replaced with "NEWLINE_CHAR". Here restore
                    # the natural newline token to avoid special vocab "NEWLINE_CHAR".
                    _DOCUMENT: src_line.strip().replace("NEWLINE_CHAR", "\n"),
                    _SUMMARY: tgt_line.strip(),
                }
