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
"""WMT15: Translate dataset."""

import nlp

from .wmt_utils import Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt15/translation-task.html"
_CITATION = """
@InProceedings{bojar-EtAl:2015:WMT,
  author    = {Bojar, Ond\v{r}ej  and  Chatterjee, Rajen  and  Federmann, Christian  and  Haddow, Barry  and  Huck, Matthias  and  Hokamp, Chris  and  Koehn, Philipp  and  Logacheva, Varvara  and  Monz, Christof  and  Negri, Matteo  and  Post, Matt  and  Scarton, Carolina  and  Specia, Lucia  and  Turchi, Marco},
  title     = {Findings of the 2015 Workshop on Statistical Machine Translation},
  booktitle = {Proceedings of the Tenth Workshop on Statistical Machine Translation},
  month     = {September},
  year      = {2015},
  address   = {Lisbon, Portugal},
  publisher = {Association for Computational Linguistics},
  pages     = {1--46},
  url       = {http://aclweb.org/anthology/W15-3001}
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "fi", "fr", "ru"]]


class Wmt15(Wmt):
    """WMT 15 translation datasets for all {xx, "en"} language pairs."""

    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2015 %s-%s translation task dataset." % (l1, l2),
            url=_URL,
            citation=_CITATION,
            language_pair=(l1, l2),
            version=nlp.Version("1.0.0"),
        )
        for l1, l2 in _LANGUAGE_PAIRS
    ]

    @property
    def _subsets(self):
        return {
            nlp.Split.TRAIN: [
                "europarl_v7",
                "europarl_v8_16",
                "commoncrawl",
                "multiun",
                "newscommentary_v10",
                "gigafren",
                "czeng_10",
                "yandexcorpus",
                "wikiheadlines_fi",
                "wikiheadlines_ru",
            ],
            nlp.Split.VALIDATION: ["newsdev2015", "newsdiscussdev2015", "newstest2014"],
            nlp.Split.TEST: ["newstest2015", "newsdiscusstest2015",],
        }
