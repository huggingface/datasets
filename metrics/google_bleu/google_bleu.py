# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
""" Google BLEU (aka GLEU) metric. """

from typing import Dict, Any

from nltk.translate import gleu_score

import datasets
from datasets import MetricInfo

_CITATION = ...

_DESCRIPTION = ...

_KWARGS_DESCRIPTION = ...


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class GoogleBleu(datasets.Metric):

    def _info(self) -> MetricInfo:
        pass

    def _compute(self, *, predictions=None, references=None, **kwargs) -> Dict[str, Any]:
        return {
            "google_bleu": gleu_score.corpus_gleu([references], predictions)
        }
