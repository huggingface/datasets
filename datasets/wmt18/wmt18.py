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
"""WMT18: Translate dataset."""

import nlp

from .wmt_utils import CWMT_SUBSET_NAMES, Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt18/translation-task.html"
_CITATION = """\
@InProceedings{bojar-EtAl:2018:WMT1,
  author    = {Bojar, Ond\v{r}ej  and  Federmann, Christian  and  Fishel, Mark
    and Graham, Yvette  and  Haddow, Barry  and  Huck, Matthias  and
    Koehn, Philipp  and  Monz, Christof},
  title     = {Findings of the 2018 Conference on Machine Translation (WMT18)},
  booktitle = {Proceedings of the Third Conference on Machine Translation,
    Volume 2: Shared Task Papers},
  month     = {October},
  year      = {2018},
  address   = {Belgium, Brussels},
  publisher = {Association for Computational Linguistics},
  pages     = {272--307},
  url       = {http://www.aclweb.org/anthology/W18-6401}
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "et", "fi", "kk", "ru", "tr", "zh"]]


class Wmt18(Wmt):
    """WMT 18 translation datasets for all {xx, "en"} language pairs."""

    # Version history:
    # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2018 %s-%s translation task dataset." % (l1, l2),
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
                "europarl_v8_18",
                "paracrawl_v1",
                "commoncrawl",
                "newscommentary_v13",
                "czeng_17",
                "yandexcorpus",
                "wikiheadlines_fi",
                "wikiheadlines_ru",
                "setimes_2",
                "uncorpus_v1",
                "rapid_2016",
            ]
            + CWMT_SUBSET_NAMES,
            nlp.Split.VALIDATION: ["newsdev2018", "newstest2017", "newstestB2017"],
            nlp.Split.TEST: ["newstest2018"],
        }
