# Copyright 2022 The HuggingFace Datasets Authors.
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
""" XTREME-S benchmark metric. """

from sklearn.metrics import f1_score
from packaging import version

import datasets


# TODO(Patrick/Anton)
_CITATION = """\
"""

# TODO(Patrick/Anton)
_DESCRIPTION = """\
"""

# TODO(Patrick/Anton)
# Also add tests
_KWARGS_DESCRIPTION = """
    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'mls')  # 'mls' or 'voxpopuli' or 'babel'
    >>> references = ["it is sunny here", "paper and pen are essentials"]
    >>> predictions = ["it's sunny", "paper pen are essential"]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'wer': 0.56}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'covost2')
    >>> references = ["bonjour paris", "il est necessaire de faire du sport de temps en temp"]
    >>> predictions = ["bonjour paris", "il est important de faire du sport souvent"]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'bleu': 19.38}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'fleurs')
    >>> references = [0, 1, 0, 0, 1]
    >>> predictions = [0, 1, 1, 0, 0]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'accuracy': 0.6'}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'minds14')
    >>> references = [0, 1, 0, 0, 1]
    >>> predictions = [0, 1, 1, 0, 0]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'f1': 0.5}
"""

#    >>> print({"pearson": round(results["pearson"], 2), "spearmanr": round(results["spearmanr"], 2)})

_CONFIG_NAMES = ["babel", "mls", "voxpopuli", "covost2", "fleurs", "minds14"]


def simple_accuracy(preds, labels):
    return float((preds == labels).mean())


def f1(preds, labels):
    return float(f1_score(y_true=labels, y_pred=preds))


def bleu(
    preds,
    labels,
    smooth_method="exp",
    smooth_value=None,
    force=False,
    lowercase=False,
    tokenize=None,
    use_effective_order=False,
):
    # xtreme-s can only have one label
    labels = [[l] for l in labels]
    preds = list(preds)
    try:
        import sacrebleu as scb
    except ImportError:
        raise ValueError(
            f"sacrebleu has to be installed in order to apply the bleu metric for covost2."
            "You can install it via `pip install sacrebleu`."
        )

    if version.parse(scb.__version__) < version.parse("1.4.12"):
        raise ImportWarning(
            "To use `sacrebleu`, the module `sacrebleu>=1.4.12` is required, and the current version of `sacrebleu` doesn't match this condition.\n"
            'You can install it with `pip install "sacrebleu>=1.4.12"`.'
        )

    references_per_prediction = len(labels[0])
    if any(len(refs) != references_per_prediction for refs in labels):
        raise ValueError("Sacrebleu requires the same number of references for each prediction")
    transformed_references = [[refs[i] for refs in labels] for i in range(references_per_prediction)]
    output = scb.corpus_bleu(
        preds,
        transformed_references,
        smooth_method=smooth_method,
        smooth_value=smooth_value,
        force=force,
        lowercase=lowercase,
        use_effective_order=use_effective_order,
        **(dict(tokenize=tokenize) if tokenize else {}),
    )
    return {"bleu": output.score}


def wer(preds, labels, concatenate_texts, config_name):
    try:
        from jiwer import compute_measures
    except ImportError:
        raise ValueError(
            f"jiwer has to be installed in order to apply the wer metric for {config_name}."
            "You can install it via `pip install jiwer`."
        )
    if concatenate_texts:
        return {"wer": compute_measures(labels, preds)["wer"]}
    else:
        incorrect = 0
        total = 0
        for prediction, reference in zip(preds, labels):
            measures = compute_measures(reference, prediction)
            incorrect += measures["substitutions"] + measures["deletions"] + measures["insertions"]
            total += measures["substitutions"] + measures["deletions"] + measures["hits"]
        return {"wer": incorrect / total}


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class XtremeS(datasets.Metric):
    def _info(self):
        if self.config_name not in _CONFIG_NAMES:
            raise KeyError(
                f"You should supply a configuration name selected in {_CONFIG_NAMES}"
            )

        pred_type = "int64" if self.config_name in ["fleurs", "minds14"] else "string"

        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value(pred_type),
                    "references": datasets.Value(pred_type)
                }
            ),
            codebase_urls=[],
            reference_urls=[],
            format="numpy",
        )

    def _compute(self, predictions, references, **kwargs):
        if self.config_name == "fleurs":
            return {"accuracy": simple_accuracy(predictions, references)}
        elif self.config_name == "minds14":
            return {"f1": f1(predictions, references)}
        elif self.config_name == "covost2":
            smooth_method = kwargs.pop("smooth_method", "exp")
            smooth_value = kwargs.pop("smooth_value", None)
            force = kwargs.pop("force", False)
            lowercase = kwargs.pop("lowercase", False)
            tokenize = kwargs.pop("tokenize", None)
            use_effective_order = kwargs.pop("use_effective_order", False)
            return bleu(
                preds=predictions,
                labels=references,
                smooth_method=smooth_method,
                smooth_value=smooth_value,
                force=force,
                lowercase=lowercase,
                tokenize=tokenize,
                use_effective_order=use_effective_order,
            )
        elif self.config_name in ["babel", "mls", "voxpopuli"]:
            concatenate_texts = kwargs.pop("concatenate_texts", False)
            return wer(predictions, references, concatenate_texts, self.config_name)
        else:
            raise KeyError(
                f"You should supply a configuration name selected in {_CONFIG_NAMES}"
            )
