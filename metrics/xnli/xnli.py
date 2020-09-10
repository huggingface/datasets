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
""" XNLI benchmark metric. """

import nlp


_CITATION = """\
@InProceedings{conneau2018xnli,
  author = "Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin",
  title = "XNLI: Evaluating Cross-lingual Sentence Representations",
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  location = "Brussels, Belgium",
}
"""

_DESCRIPTION = """\
XNLI is a subset of a few thousand examples from MNLI which has been translated
into a 14 different languages (some low-ish resource). As with MNLI, the goal is
to predict textual entailment (does sentence A imply/contradict/neither sentence
B) and is a classification task (given two sentences, predict one of three
labels).
"""

_KWARGS_DESCRIPTION = """
Computes XNLI score which is just simple accuracy.
Args:
    predictions: Predicted labels.
    references: Ground truth labels.
Returns:
    'accuracy': accuracy
"""


def simple_accuracy(preds, labels):
    return (preds == labels).mean()


class Xnli(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features(
                {
                    "predictions": nlp.Value("int64" if self.config_name != "sts-b" else "float32"),
                    "references": nlp.Value("int64" if self.config_name != "sts-b" else "float32"),
                }
            ),
            codebase_urls=[],
            reference_urls=[],
            format="numpy",
        )

    def _compute(self, predictions, references):
        return {"accuracy": simple_accuracy(predictions, references)}
