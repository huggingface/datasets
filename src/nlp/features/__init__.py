# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
"""`nlp.features.FeatureConnector` API defining feature types."""

from .class_label_feature import ClassLabel
from .feature import FeatureConnector
from .feature import Tensor
from .feature import TensorInfo
from .features_dict import FeaturesDict, Sequence
from .text_feature import Text
from .translation_feature import Translation
from .translation_feature import TranslationVariableLanguages

__all__ = [
    "ClassLabel",
    "FeatureConnector",
    "FeaturesDict",
    "Tensor",
    "TensorInfo",
    "Sequence",
    "Text",
]
