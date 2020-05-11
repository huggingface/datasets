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
""" seqeval metric. """

import nlp
from seqeval.metrics import accuracy_score, precision_score, recall_score, f1_score

_CITATION = """\
"""

_DESCRIPTION = """\
seqeval is a Python framework for sequence labeling evaluation.
seqeval can evaluate the performance of chunking tasks such as named-entity recognition, part-of-speech tagging, semantic role labeling and so on.

This is well-tested by using the Perl script conlleval, which can be used for
measuring the performance of a system that has processed the CoNLL-2000 shared task data.

seqeval supports following formats:
IOB1
IOB2
IOE1
IOE2
IOBES

See the [README.md] file at https://github.com/chakki-works/seqeval for more information.
"""

_KWARGS_DESCRIPTION = """
Produces BLEU scores along with its sufficient statistics
from a source against one or more references.

Args:
    predictions: List of List of predicted labels (Estimated targets as returned by a tagger)
    references: List of List of reference labels (Ground truth (correct) target values)
Returns:
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': F1 score, also known as balanced F-score or F-measure,
"""

class Seqeval(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/chakki-works/seqeval",
            inputs_description=_KWARGS_DESCRIPTION,
            predictions_features=nlp.Sequence(nlp.Sequence(nlp.Value('string'))),
            references_features=nlp.Sequence(nlp.Sequence(nlp.Value('string'))),
            codebase_urls=["https://github.com/chakki-works/seqeval"],
            reference_urls=["https://github.com/chakki-works/seqeval"]
        )

    def _compute(self, predictions, references):
        scores = {
            'accuracy': accuracy_score(y_true=references, y_pred=predictions),
            'precision': precision_score(y_true=references, y_pred=predictions),
            'recall': recall_score(y_true=references, y_pred=predictions),
            'f1': f1_score(y_true=references, y_pred=predictions),
        }

        return scores
