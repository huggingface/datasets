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
"""The WMT EnDe Translate dataset used by the Tensor2Tensor library."""

import nlp

from .wmt_utils import Wmt, WmtConfig


_URL = "https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/translate_ende.py"
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


class WmtT2t(Wmt):
    """The WMT EnDe Translate dataset used by the Tensor2Tensor library."""

    BUILDER_CONFIGS = [
        WmtConfig(  # pylint:disable=g-complex-comprehension
            description="WMT T2T EnDe translation task dataset.",
            url=_URL,
            citation=_CITATION,
            language_pair=("de", "en"),
            version=nlp.Version("1.0.0"),
        )
    ]

    @property
    def manual_download_instructions(self):
        if self.config.language_pair[1] in ["cs", "hi", "ru"]:
            return "Please download the data manually as explained. TODO(PVP)"

    @property
    def _subsets(self):
        return {
            nlp.Split.TRAIN: ["europarl_v7", "commoncrawl", "newscommentary_v13"],
            nlp.Split.VALIDATION: ["newstest2013"],
            nlp.Split.TEST: ["newstest2014"],
        }
