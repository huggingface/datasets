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
"""WMT17: Translate dataset."""

import datasets

from .wmt_utils import CWMT_SUBSET_NAMES, Wmt, WmtConfig


_URL = "http://www.statmt.org/wmt17/translation-task.html"
_CITATION = """
@InProceedings{bojar-EtAl:2017:WMT1,
  author    = {Bojar, Ond\v{r}ej  and  Chatterjee, Rajen  and  Federmann, Christian  and  Graham, Yvette  and  Haddow, Barry  and  Huang, Shujian  and  Huck, Matthias  and  Koehn, Philipp  and  Liu, Qun  and  Logacheva, Varvara  and  Monz, Christof  and  Negri, Matteo  and  Post, Matt  and  Rubino, Raphael  and  Specia, Lucia  and  Turchi, Marco},
  title     = {Findings of the 2017 Conference on Machine Translation (WMT17)},
  booktitle = {Proceedings of the Second Conference on Machine Translation, Volume 2: Shared Task Papers},
  month     = {September},
  year      = {2017},
  address   = {Copenhagen, Denmark},
  publisher = {Association for Computational Linguistics},
  pages     = {169--214},
  url       = {http://www.aclweb.org/anthology/W17-4717}
}
"""

_LANGUAGE_PAIRS = [(lang, "en") for lang in ["cs", "de", "fi", "lv", "ru", "tr", "zh"]]


class Wmt17(Wmt):
    """WMT 17 translation datasets for all {xx, "en"} language pairs."""

    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT 2017 %s-%s translation task dataset." % (l1, l2),
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

    @property
    def _subsets(self):
        return {
            datasets.Split.TRAIN: [
                "europarl_v7",
                "europarl_v8_16",
                "commoncrawl",
                "newscommentary_v12",
                "czeng_16",
                "yandexcorpus",
                "wikiheadlines_fi",
                "wikiheadlines_ru",
                "setimes_2",
                "uncorpus_v1",
                "rapid_2016",
                "leta_v1",
                "dcep_v1",
                "onlinebooks_v1",
            ]
            + CWMT_SUBSET_NAMES,
            datasets.Split.VALIDATION: ["newsdev2017", "newstest2016", "newstestB2016"],
            datasets.Split.TEST: ["newstest2017", "newstestB2017"],
        }
