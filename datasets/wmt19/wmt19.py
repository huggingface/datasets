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
"""WMT19: Translate dataset."""

import nlp

from .wmt_utils import CWMT_SUBSET_NAMES, Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt19/translation-task.html"
# TODO(adarob): Update with citation of overview paper once it is published.
_CITATION = """
@ONLINE {wmt19translate,
    author = "Wikimedia Foundation",
    title  = "ACL 2019 Fourth Conference on Machine Translation (WMT19), Shared Task: Machine Translation of News",
    url    = "http://www.statmt.org/wmt19/translation-task.html"
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "fi", "gu", "kk", "lt", "ru", "zh"]] + [("fr", "de")]


class Wmt19(Wmt):
    """WMT 19 translation datasets for {(xx, "en")} + ("fr", "de") pairs."""

    # Version history:
    # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2019 %s-%s translation task dataset." % (l1, l2),
            url=_URL,
            citation=_CITATION,
            language_pair=(l1, l2),
            version=nlp.Version("1.0.0"),
        )
        for l1, l2 in _LANGUAGE_PAIRS
    ]

    @property
    def manual_download_instructions(self):
        if self.config.language_pair[1] in ["cs", "hi", "ru"]:
            return "Please download the data manually as explained. TODO(PVP)"

    @property
    def _subsets(self):
        return {
            nlp.Split.TRAIN: [
                "europarl_v9",
                "europarl_v7_frde",
                "paracrawl_v3",
                "paracrawl_v1_ru",
                "paracrawl_v3_frde",
                "commoncrawl",
                "commoncrawl_frde",
                "newscommentary_v14",
                "newscommentary_v14_frde",
                "czeng_17",
                "yandexcorpus",
                "wikititles_v1",
                "uncorpus_v1",
                "rapid_2016_ltfi",
                "rapid_2019",
            ]
            + CWMT_SUBSET_NAMES,
            nlp.Split.VALIDATION: ["euelections_dev2019", "newsdev2019", "newstest2018"],
        }
