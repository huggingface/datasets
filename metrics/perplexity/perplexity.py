# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors.
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
""" Perplexity metric. """

import nlp
import numpy as np

_CITATION = """\
"""

_DESCRIPTION = """
In natural language processing, perplexity is a way of evaluating language models.
A language model is a probability distribution over entire sentences or texts.
The perplexity is a measurement of how well the probability distribution predicts a sample.
It may be used to compare probability models.

A low perplexity indicates the probability distribution is good at predicting the sample.

The perplexity of a discrete probability distribution p is defined as:
2^{H(p)}=2^{-\sum _{x}p(x)\log _{2}p(x)}}2^{{H(p)}}=2^{{-\sum _{x}p(x)\log _{2}p(x)}

The exponent may also be regarded as a cross-entropy, the perplexity can thus be computed as
the exponential of the loss when the loss of the mopdel is a cross-entropy loss.
"""

_KWARGS_DESCRIPTION = """
Computes perplexity.
Args:
    predictions: List of model probability over the distribution.
    references: List of samples (correct classes)
Returns:
    'perplexity': The perplexity
"""

class Perplexity(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            prediction_features=nlp.Sequence(nlp.Value('float')),
            reference_features=nlp.Value('int64'),
            codebase_urls=[],
            reference_urls=["https://en.wikipedia.org/wiki/Perplexity"],
            use_numpy=True,
        )

    def _compute(self, predictions: np.ndarray, references: np.ndarray):
        log_probs = np.log(predictions)
        log_probs = log_probs[references]
        score = np.exp(np.mean(log_probs))
        return {'perplexity': score.float()}
