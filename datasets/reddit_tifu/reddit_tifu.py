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
"""Reddit TIFU dataset using tifu or tldr from subreddit tifu."""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """
@misc{kim2018abstractive,
    title={Abstractive Summarization of Reddit Posts with Multi-level Memory Networks},
    author={Byeongchang Kim and Hyunwoo Kim and Gunhee Kim},
    year={2018},
    eprint={1811.00783},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
Reddit dataset, where TIFU denotes the name of subbreddit /r/tifu.
As defined in the publication, styel "short" uses title as summary and
"long" uses tldr as summary.

Features includes:
  - document: post text without tldr.
  - tldr: tldr line.
  - title: trimmed title without tldr.
  - ups: upvotes.
  - score: score.
  - num_comments: number of comments.
  - upvote_ratio: upvote ratio.
"""

_URL = "https://drive.google.com/uc?export=download&id=1ffWfITKFMJeqjT8loC8aiCLRNJpc_XnF"

_DOCUMENT = "documents"
_TITLE = "title"
_TLDR = "tldr"
_ADDITIONAL_FEATURES = ["ups", "num_comments", "score", "upvote_ratio"]


class RedditTifuConfig(datasets.BuilderConfig):
    """BuilderConfig for RedditTifu."""

    def __init__(self, summary_key=None, **kwargs):
        """BuilderConfig for RedditTifu.

        Args:
          summary_key: key string of summary in downloaded json file.
          **kwargs: keyword arguments forwarded to super.
        """
        # Version 1.1.0 remove empty document and summary strings.
        super(RedditTifuConfig, self).__init__(version=datasets.Version("1.1.0"), **kwargs)
        self.summary_key = summary_key


class RedditTifu(datasets.GeneratorBasedBuilder):
    """Reddit TIFU Dataset."""

    BUILDER_CONFIGS = [
        RedditTifuConfig(
            name="short",
            summary_key=_TITLE,
            description="Using title as summary.",
        ),
        RedditTifuConfig(
            name="long",
            summary_key=_TLDR,
            description="Using TLDR as summary.",
        ),
    ]

    def _info(self):
        features = {
            "ups": datasets.Value("float32"),
            "num_comments": datasets.Value("float32"),
            "upvote_ratio": datasets.Value("float32"),
            "score": datasets.Value("float32"),
        }
        features.update({k: datasets.Value("string") for k in [_DOCUMENT, _TLDR, _TITLE]})
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=(_DOCUMENT, self.config.summary_key),
            homepage="https://github.com/ctr4si/MMN",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"path": dl_path},
            )
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, "rb") as f:
            for i, line in enumerate(f):
                # keys are 'title_tokenized','permalink','title','url','num_comments',
                #   'tldr'(optional),'created_utc','trimmed_title_tokenized','ups',
                #   'selftext_html','score','upvote_ratio','tldr_tokenized'(optional),
                #   'selftext','trimmed_title','selftext_without_tldr_tokenized',
                #   'id','selftext_without_tldr'
                d = json.loads(line)
                r = {
                    _DOCUMENT: d["selftext_without_tldr"].strip(),
                    _TITLE: d["trimmed_title"].strip(),
                    _TLDR: (d["tldr"] or "").strip(),
                }
                r.update({k: d[k] for k in _ADDITIONAL_FEATURES})
                # skip if document or summary is empty
                if r[_DOCUMENT] and r[self.config.summary_key]:
                    yield i, r
