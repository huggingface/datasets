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
"""WMT16: Translate dataset."""

import nlp

from .wmt_utils import Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt16/translation-task.html"
_CITATION = """
@InProceedings{bojar-EtAl:2016:WMT1,
  author    = {Bojar, Ond\v{r}ej  and  Chatterjee, Rajen  and  Federmann, Christian  and  Graham, Yvette  and  Haddow, Barry  and  Huck, Matthias  and  Jimeno Yepes, Antonio  and  Koehn, Philipp  and  Logacheva, Varvara  and  Monz, Christof  and  Negri, Matteo  and  Neveol, Aurelie  and  Neves, Mariana  and  Popel, Martin  and  Post, Matt  and  Rubino, Raphael  and  Scarton, Carolina  and  Specia, Lucia  and  Turchi, Marco  and  Verspoor, Karin  and  Zampieri, Marcos},
  title     = {Findings of the 2016 Conference on Machine Translation},
  booktitle = {Proceedings of the First Conference on Machine Translation},
  month     = {August},
  year      = {2016},
  address   = {Berlin, Germany},
  publisher = {Association for Computational Linguistics},
  pages     = {131--198},
  url       = {http://www.aclweb.org/anthology/W/W16/W16-2301}
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "fi", "ro", "ru", "tr"]]


class Wmt16(Wmt):
    """WMT 16 translation datasets for all {xx, "en"} language pairs."""

    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2016 %s-%s translation task dataset." % (l1, l2),
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
                "newscommentary_v11",
                "czeng_16pre",
                "yandexcorpus",
                "wikiheadlines_fi",
                "wikiheadlines_ru",
                "setimes_2",
            ],
            nlp.Split.VALIDATION: ["newsdev2016", "newstest2015"],
            nlp.Split.TEST: ["newstest2016", "newstestB2016"],
        }
