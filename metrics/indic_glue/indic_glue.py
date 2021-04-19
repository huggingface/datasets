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
""" IndicGLUE benchmark metric. """

import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import f1_score

import datasets


_CITATION = """\
    @inproceedings{kakwani2020indicnlpsuite,
    title={{IndicNLPSuite: Monolingual Corpora, Evaluation Benchmarks and Pre-trained Multilingual Language Models for Indian Languages}},
    author={Divyanshu Kakwani and Anoop Kunchukuttan and Satish Golla and Gokul N.C. and Avik Bhattacharyya and Mitesh M. Khapra and Pratyush Kumar},
    year={2020},
    booktitle={Findings of EMNLP},
}
"""

_DESCRIPTION = """\
    IndicGLUE is a natural language understanding benchmark for Indian languages. It contains a wide
    variety of tasks and covers 11 major Indian languages - as, bn, gu, hi, kn, ml, mr, or, pa, ta, te.
"""

_KWARGS_DESCRIPTION = """
Compute IndicGLUE evaluation metric associated to each IndicGLUE dataset.
Args:
    predictions: list of predictions to score (as int64),
        except for 'cvit-mkb-clsr' where each prediction is a vector (of float32).
    references: list of ground truth labels corresponding to the predictions (as int64),
        except for 'cvit-mkb-clsr' where each reference is a vector (of float32).
Returns: depending on the IndicGLUE subset, one or several of:
    "accuracy": Accuracy
    "f1": F1 score
    "precision": Precision@10
Examples:

    >>> indic_glue_metric = datasets.load_metric('indic_glue', 'wnli')  # 'wnli' or any of ["copa", "sna", "csqa", "wstp", "inltkh", "bbca", "iitp-mr", "iitp-pr", "actsa-sc", "md"]
    >>> references = [0, 1]
    >>> predictions = [0, 1]
    >>> results = indic_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0}

    >>> indic_glue_metric = datasets.load_metric('indic_glue', 'wiki-ner')
    >>> references = [0, 1]
    >>> predictions = [0, 1]
    >>> results = indic_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0, 'f1': 1.0}

    >>> indic_glue_metric = datasets.load_metric('indic_glue', 'cvit-mkb-clsr')
    >>> references = [[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]]
    >>> predictions = [[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]]
    >>> results = indic_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'precision@10': 1.0}

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


def precision_at_10(en_sentvecs, in_sentvecs):
    en_sentvecs = np.array(en_sentvecs)
    in_sentvecs = np.array(in_sentvecs)
    n = en_sentvecs.shape[0]

    # mean centering
    en_sentvecs = en_sentvecs - np.mean(en_sentvecs, axis=0)
    in_sentvecs = in_sentvecs - np.mean(in_sentvecs, axis=0)

    sim = cdist(en_sentvecs, in_sentvecs, "cosine")
    actual = np.array(range(n))
    preds = sim.argsort(axis=1)[:, :10]
    matches = np.any(preds == actual[:, None], axis=1)
    return matches.mean()


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class IndicGlue(datasets.Metric):
    def _info(self):
        if self.config_name not in [
            "wnli",
            "copa",
            "sna",
            "csqa",
            "wstp",
            "inltkh",
            "bbca",
            "cvit-mkb-clsr",
            "iitp-mr",
            "iitp-pr",
            "actsa-sc",
            "md",
            "wiki-ner",
        ]:
            raise KeyError(
                "You should supply a configuration name selected in "
                '["wnli", "copa", "sna", "csqa", "wstp", "inltkh", "bbca", '
                '"cvit-mkb-clsr", "iitp-mr", "iitp-pr", "actsa-sc", "md", '
                '"wiki-ner"]'
            )
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("int64")
                    if self.config_name != "cvit-mkb-clsr"
                    else datasets.Sequence(datasets.Value("float32")),
                    "references": datasets.Value("int64")
                    if self.config_name != "cvit-mkb-clsr"
                    else datasets.Sequence(datasets.Value("float32")),
                }
            ),
            codebase_urls=[],
            reference_urls=[],
            format="numpy" if self.config_name != "cvit-mkb-clsr" else None,
        )

    def _compute(self, predictions, references):
        if self.config_name == "cvit-mkb-clsr":
            return {"precision@10": precision_at_10(predictions, references)}
        elif self.config_name in ["wiki-ner"]:
            return acc_and_f1(predictions, references)
        elif self.config_name in [
            "wnli",
            "copa",
            "sna",
            "csqa",
            "wstp",
            "inltkh",
            "bbca",
            "iitp-mr",
            "iitp-pr",
            "actsa-sc",
            "md",
        ]:
            return {"accuracy": simple_accuracy(predictions, references)}
        else:
            raise KeyError(
                "You should supply a configuration name selected in "
                '["wnli", "copa", "sna", "csqa", "wstp", "inltkh", "bbca", '
                '"cvit-mkb-clsr", "iitp-mr", "iitp-pr", "actsa-sc", "md", '
                '"wiki-ner"]'
            )
