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
"""WMT14: Translate dataset."""

import datasets

from .wmt_utils import Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt14/translation-task.html"
_CITATION = """
@InProceedings{bojar-EtAl:2014:W14-33,
  author    = {Bojar, Ondrej  and  Buck, Christian  and  Federmann, Christian  and  Haddow, Barry  and  Koehn, Philipp  and  Leveling, Johannes  and  Monz, Christof  and  Pecina, Pavel  and  Post, Matt  and  Saint-Amand, Herve  and  Soricut, Radu  and  Specia, Lucia  and  Tamchyna, Ale\v{s}},
  title     = {Findings of the 2014 Workshop on Statistical Machine Translation},
  booktitle = {Proceedings of the Ninth Workshop on Statistical Machine Translation},
  month     = {June},
  year      = {2014},
  address   = {Baltimore, Maryland, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {12--58},
  url       = {http://www.aclweb.org/anthology/W/W14/W14-3302}
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "fr", "hi", "ru"]]


class Wmt14(Wmt):
    """WMT 14 translation datasets for all {xx, "en"} language pairs."""

    # Version history:
    # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2014 %s-%s translation task dataset." % (l1, l2),
            url=_URL,
            citation=_CITATION,
            language_pair=(l1, l2),
            version=datasets.Version("1.0.0"),
        )
        for l1, l2 in _LANGUAGE_PAIRS
    ]

    @property
    def manual_download_instructions(self):
        if self.config.language_pair[1] in ["cs", "hi", "ru"]:
            return "Please download the data manually as explained. TODO(PVP)"
        return None

    @property
    def _subsets(self):
        return {
            datasets.Split.TRAIN: [
                "europarl_v7",
                "commoncrawl",
                "multiun",
                "newscommentary_v9",
                "gigafren",
                "czeng_10",
                "yandexcorpus",
                "wikiheadlines_hi",
                "wikiheadlines_ru",
                "hindencorp_01",
            ],
            datasets.Split.VALIDATION: ["newsdev2014", "newstest2013"],
            datasets.Split.TEST: ["newstest2014"],
        }
