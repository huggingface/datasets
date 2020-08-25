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
""" GLUE benchmark metric. """

import nlp
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import matthews_corrcoef, f1_score

_CITATION = """\
@inproceedings{wang2019glue,
  title={{GLUE}: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding},
  author={Wang, Alex and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R.},
  note={In the Proceedings of ICLR.},
  year={2019}
}
"""

_DESCRIPTION = """\
GLUE, the General Language Understanding Evaluation benchmark
(https://gluebenchmark.com/) is a collection of resources for training,
evaluating, and analyzing natural language understanding systems.
"""

_KWARGS_DESCRIPTION = """
Compute GLUE evaluation metric associated to each GLUE dataset.
Args:
    predictions: list of translations to score.
        Each translation should be tokenized into a list of tokens.
    references: list of lists of references for each translation.
        Each reference should be tokenized into a list of tokens.
Returns: depending on the GLUE subset, one or several of:
    "accuracy": Accuracy
    "f1": F1
    "pearson": Pearson Correlation
    "spearmanr": Spearman Correlation
    "matthews_correlation": Matthew Correlation
"""

def simple_accuracy(preds, labels):
    return (preds == labels).mean()

def acc_and_f1(preds, labels):
    acc = simple_accuracy(preds, labels)
    f1 = f1_score(y_true=labels, y_pred=preds)
    return {
        "accuracy": acc,
        "f1": f1,
    }

def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    spearman_corr = spearmanr(preds, labels)[0]
    return {
        "pearson": pearson_corr,
        "spearmanr": spearman_corr,
    }


class Glue(nlp.Metric):
    def _info(self):
        if self.config_name not in ["sst2", "mnli", "mnli_mismatched", "mnli_matched",
                "cola", "stsb", "mrpc", "qqp", "qnli", "rte", "wnli", "hans"]:
            raise KeyError('You should supply a configuration name selected in '
                           '["sst2", "mnli", "mnli_mismatched", "mnli_matched", '
                           '"cola", "stsb", "mrpc", "qqp", "qnli", "rte", "wnli", "hans"]')
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features({
                'predictions': nlp.Value('int64' if self.config_name != 'stsb' else 'float32'),
                'references': nlp.Value('int64' if self.config_name != 'stsb' else 'float32'),
            }),
            codebase_urls=[],
            reference_urls=[],
            format='numpy'
        )

    def _compute(self, predictions, references):
        if self.config_name == "cola":
            return {"matthews_correlation": matthews_corrcoef(references, predictions)}
        elif self.config_name == "stsb":
            return pearson_and_spearman(predictions, references)
        elif self.config_name in ["mrpc", "qqp"]:
            return acc_and_f1(predictions, references)
        elif self.config_name in ["sst2", "mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]:
            return {"accuracy": simple_accuracy(predictions, references)}
        else:
            raise KeyError('You should supply a configuration name selected in '
                           '["sst2", "mnli", "mnli_mismatched", "mnli_matched", '
                           '"cola", "stsb", "mrpc", "qqp", "qnli", "rte", "wnli", "hans"]')
