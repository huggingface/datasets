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
"""The SuperGLUE benchmark metric."""

from sklearn.metrics import f1_score, matthews_corrcoef

import datasets

from .record_evaluation import evaluate as evaluate_record


_CITATION = """\
@article{wang2019superglue,
  title={SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems},
  author={Wang, Alex and Pruksachatkun, Yada and Nangia, Nikita and Singh, Amanpreet and Michael, Julian and Hill, Felix and Levy, Omer and Bowman, Samuel R},
  journal={arXiv preprint arXiv:1905.00537},
  year={2019}
}
"""

_DESCRIPTION = """\
SuperGLUE (https://super.gluebenchmark.com/) is a new benchmark styled after
GLUE with a new set of more difficult language understanding tasks, improved
resources, and a new public leaderboard.
"""

_KWARGS_DESCRIPTION = """
Compute SuperGLUE evaluation metric associated to each SuperGLUE dataset.
Args:
    predictions: list of predictions to score. Depending on the SuperGlUE subset:
        - for 'record': list of question-answer dictionaries with the following keys:
            - 'idx': index of the question as specified by the dataset
            - 'prediction_text': the predicted answer text
        - for 'multirc': list of question-answer dictionaries with the following keys:
            - 'idx': index of the question-answer pair as specified by the dataset
            - 'prediction': the predicted answer label
        - otherwise: list of predicted labels
    references: list of reference labels. Depending on the SuperGLUE subset:
        - for 'record': list of question-answers dictionaries with the following keys:
            - 'idx': index of the question as specified by the dataset
            - 'answers': list of possible answers
        - otherwise: list of reference labels
Returns: depending on the SuperGLUE subset:
    - for 'record':
        - 'exact_match': Exact match between answer and gold answer
        - 'f1': F1 score
    - for 'multirc':
        - 'exact_match': Exact match between answer and gold answer
        - 'f1_m': Per-question macro-F1 score
        - 'f1_a': Average F1 score over all answers
    - for 'axb':
        'matthews_correlation': Matthew Correlation
    - for 'cb':
        - 'accuracy': Accuracy
        - 'f1': F1 score
    - for all others:
        - 'accuracy': Accuracy
Examples:

    >>> super_glue_metric = datasets.load_metric('super_glue', 'copa')  # any of ["copa", "rte", "wic", "wsc", "wsc.fixed", "boolq", "axg"]
    >>> predictions = [0, 1]
    >>> references = [0, 1]
    >>> results = super_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0}

    >>> super_glue_metric = datasets.load_metric('super_glue', 'cb')
    >>> predictions = [0, 1]
    >>> references = [0, 1]
    >>> results = super_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'accuracy': 1.0, 'f1': 1.0}

    >>> super_glue_metric = datasets.load_metric('super_glue', 'record')
    >>> predictions = [{'idx': {'passage': 0, 'query': 0}, 'prediction_text': 'answer'}]
    >>> references = [{'idx': {'passage': 0, 'query': 0}, 'answers': ['answer', 'another_answer']}]
    >>> results = super_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'exact_match': 1.0, 'f1': 1.0}

    >>> super_glue_metric = datasets.load_metric('super_glue', 'multirc')
    >>> predictions = [{'idx': {'answer': 0, 'paragraph': 0, 'question': 0}, 'prediction': 0}, {'idx': {'answer': 1, 'paragraph': 2, 'question': 3}, 'prediction': 1}]
    >>> references = [0, 1]
    >>> results = super_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'exact_match': 1.0, 'f1_m': 1.0, 'f1_a': 1.0}

    >>> super_glue_metric = datasets.load_metric('super_glue', 'axb')
    >>> references = [0, 1]
    >>> predictions = [0, 1]
    >>> results = super_glue_metric.compute(predictions=predictions, references=references)
    >>> print(results)
    {'matthews_correlation': 1.0}
"""


def simple_accuracy(preds, labels):
    return (preds == labels).mean()


def acc_and_f1(preds, labels, f1_avg="binary"):
    acc = simple_accuracy(preds, labels)
    f1 = f1_score(y_true=labels, y_pred=preds, average=f1_avg)
    return {
        "accuracy": acc,
        "f1": f1,
    }


def evaluate_multirc(ids_preds, labels):
    """
    Computes F1 score and Exact Match for MultiRC predictions.
    """
    question_map = {}
    for id_pred, label in zip(ids_preds, labels):
        question_id = "{}-{}".format(id_pred["idx"]["paragraph"], id_pred["idx"]["question"])
        pred = id_pred["prediction"]
        if question_id in question_map:
            question_map[question_id].append((pred, label))
        else:
            question_map[question_id] = [(pred, label)]
    f1s, ems = [], []
    for question, preds_labels in question_map.items():
        question_preds, question_labels = zip(*preds_labels)
        f1 = f1_score(y_true=question_labels, y_pred=question_preds, average="macro")
        f1s.append(f1)
        em = int(sum([p == l for p, l in preds_labels]) == len(preds_labels))
        ems.append(em)
    f1_m = sum(f1s) / len(f1s)
    em = sum(ems) / len(ems)
    f1_a = f1_score(y_true=labels, y_pred=[id_pred["prediction"] for id_pred in ids_preds])
    return {"exact_match": em, "f1_m": f1_m, "f1_a": f1_a}


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class SuperGlue(datasets.Metric):
    def _info(self):
        if self.config_name not in [
            "boolq",
            "cb",
            "copa",
            "multirc",
            "record",
            "rte",
            "wic",
            "wsc",
            "wsc.fixed",
            "axb",
            "axg",
        ]:
            raise KeyError(
                "You should supply a configuration name selected in "
                '["boolq", "cb", "copa", "multirc", "record", "rte", "wic", "wsc", "wsc.fixed", "axb", "axg",]'
            )
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(self._get_feature_types()),
            codebase_urls=[],
            reference_urls=[],
            format="numpy" if not self.config_name == "record" and not self.config_name == "multirc" else None,
        )

    def _get_feature_types(self):
        if self.config_name == "record":
            return {
                "predictions": {
                    "idx": {
                        "passage": datasets.Value("int64"),
                        "query": datasets.Value("int64"),
                    },
                    "prediction_text": datasets.Value("string"),
                },
                "references": {
                    "idx": {
                        "passage": datasets.Value("int64"),
                        "query": datasets.Value("int64"),
                    },
                    "answers": datasets.Sequence(datasets.Value("string")),
                },
            }
        elif self.config_name == "multirc":
            return {
                "predictions": {
                    "idx": {
                        "answer": datasets.Value("int64"),
                        "paragraph": datasets.Value("int64"),
                        "question": datasets.Value("int64"),
                    },
                    "prediction": datasets.Value("int64"),
                },
                "references": datasets.Value("int64"),
            }
        else:
            return {
                "predictions": datasets.Value("int64"),
                "references": datasets.Value("int64"),
            }

    def _compute(self, predictions, references):
        if self.config_name == "axb":
            return {"matthews_correlation": matthews_corrcoef(references, predictions)}
        elif self.config_name == "cb":
            return acc_and_f1(predictions, references, f1_avg="macro")
        elif self.config_name == "record":
            dataset = [
                {
                    "qas": [
                        {"id": ref["idx"]["query"], "answers": [{"text": ans} for ans in ref["answers"]]}
                        for ref in references
                    ]
                }
            ]
            predictions = {pred["idx"]["query"]: pred["prediction_text"] for pred in predictions}
            return evaluate_record(dataset, predictions)[0]
        elif self.config_name == "multirc":
            return evaluate_multirc(predictions, references)
        elif self.config_name in ["copa", "rte", "wic", "wsc", "wsc.fixed", "boolq", "axg"]:
            return {"accuracy": simple_accuracy(predictions, references)}
        else:
            raise KeyError(
                "You should supply a configuration name selected in "
                '["boolq", "cb", "copa", "multirc", "record", "rte", "wic", "wsc", "wsc.fixed", "axb", "axg",]'
            )
