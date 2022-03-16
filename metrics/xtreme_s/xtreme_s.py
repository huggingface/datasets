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

from typing import List

from packaging import version
from sklearn.metrics import f1_score

import datasets
from datasets.config import PY_VERSION


if PY_VERSION < version.parse("3.8"):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata


# TODO(Patrick/Anton)
_CITATION = """\
"""

_DESCRIPTION = """\
    XTREME-S is a benchmark to evaluate universal cross-lingual speech representations in many languages.
    XTREME-S covers four task families: speech recognition, classification, speech-to-text translation and retrieval.
"""

_KWARGS_DESCRIPTION = """
Compute XTREME-S evaluation metric associated to each XTREME-S dataset.
Args:
    predictions: list of predictions to score.
        Each translation should be tokenized into a list of tokens.
    references: list of lists of references for each translation.
        Each reference should be tokenized into a list of tokens.
    bleu_kwargs: optional dict of keywords to be passed when computing 'bleu'.
        Keywords include Dict can be one of 'smooth_method', 'smooth_value', 'force', 'lowercase',
        'tokenize', 'use_effective_order'.
    wer_kwargs: optional dict of keywords to be passed when computing 'wer' and 'cer'.
        Keywords include 'concatenate_texts'.
Returns: depending on the XTREME-S task, one or several of:
    "accuracy": Accuracy - for 'fleurs-lang_id', 'minds14'
    "f1": F1 score - for 'minds14'
    "wer": Word error rate - for 'mls', 'fleurs-asr', 'voxpopuli'
    "cer": Character error rate - for 'mls', 'fleurs-asr', 'voxpopuli'
    "bleu": BLEU score according to the `sacrebleu` metric - for 'covost2'
Examples:

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'mls')  # 'mls', 'voxpopuli', 'fleurs-asr'
    >>> references = ["it is sunny here", "paper and pen are essentials"]
    >>> predictions = ["it's sunny", "paper pen are essential"]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'wer': 0.56, 'cer': 0.27}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'covost2')
    >>> references = ["bonjour paris", "il est necessaire de faire du sport de temps en temp"]
    >>> predictions = ["bonjour paris", "il est important de faire du sport souvent"]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'bleu': 31.65}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'fleurs-lang_id')
    >>> references = [0, 1, 0, 0, 1]
    >>> predictions = [0, 1, 1, 0, 0]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'accuracy': 0.6}

    >>> xtreme_s_metric = datasets.load_metric('xtreme_s', 'minds14')
    >>> references = [0, 1, 0, 0, 1]
    >>> predictions = [0, 1, 1, 0, 0]
    >>> results = xtreme_s_metric.compute(predictions=predictions, references=references)
    >>> print({k: round(v, 2) for k, v in results.items()})
    {'f1': 0.58, 'accuracy': 0.6}
"""

_CONFIG_NAMES = ["fleurs-asr", "mls", "voxpopuli", "covost2", "fleurs-lang_id", "minds14"]
SENTENCE_DELIMITER = ""

try:
    from jiwer import transforms as tr

    _jiwer_available = True
except ImportError:
    _jiwer_available = False

if _jiwer_available and version.parse(importlib_metadata.version("jiwer")) < version.parse("2.3.0"):

    class SentencesToListOfCharacters(tr.AbstractTransform):
        def __init__(self, sentence_delimiter: str = " "):
            self.sentence_delimiter = sentence_delimiter

        def process_string(self, s: str):
            return list(s)

        def process_list(self, inp: List[str]):
            chars = []
            for sent_idx, sentence in enumerate(inp):
                chars.extend(self.process_string(sentence))
                if self.sentence_delimiter is not None and self.sentence_delimiter != "" and sent_idx < len(inp) - 1:
                    chars.append(self.sentence_delimiter)
            return chars

    cer_transform = tr.Compose(
        [tr.RemoveMultipleSpaces(), tr.Strip(), SentencesToListOfCharacters(SENTENCE_DELIMITER)]
    )
elif _jiwer_available:
    cer_transform = tr.Compose(
        [
            tr.RemoveMultipleSpaces(),
            tr.Strip(),
            tr.ReduceToSingleSentence(SENTENCE_DELIMITER),
            tr.ReduceToListOfListOfChars(),
        ]
    )
else:
    cer_transform = None


def simple_accuracy(preds, labels):
    return float((preds == labels).mean())


def f1_and_simple_accuracy(preds, labels):
    return {
        "f1": float(f1_score(y_true=labels, y_pred=preds, average="macro")),
        "accuracy": simple_accuracy(preds, labels),
    }


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
    labels = [[label] for label in labels]
    preds = list(preds)
    try:
        import sacrebleu as scb
    except ImportError:
        raise ValueError(
            "sacrebleu has to be installed in order to apply the bleu metric for covost2."
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


def wer_and_cer(preds, labels, concatenate_texts, config_name):
    try:
        from jiwer import compute_measures
    except ImportError:
        raise ValueError(
            f"jiwer has to be installed in order to apply the wer metric for {config_name}."
            "You can install it via `pip install jiwer`."
        )

    if concatenate_texts:
        wer = compute_measures(labels, preds)["wer"]

        cer = compute_measures(labels, preds, truth_transform=cer_transform, hypothesis_transform=cer_transform)["wer"]
        return {"wer": wer, "cer": cer}
    else:

        def compute_score(preds, labels, score_type="wer"):
            incorrect = 0
            total = 0
            for prediction, reference in zip(preds, labels):
                if score_type == "wer":
                    measures = compute_measures(reference, prediction)
                elif score_type == "cer":
                    measures = compute_measures(
                        reference, prediction, truth_transform=cer_transform, hypothesis_transform=cer_transform
                    )
                incorrect += measures["substitutions"] + measures["deletions"] + measures["insertions"]
                total += measures["substitutions"] + measures["deletions"] + measures["hits"]
            return incorrect / total

        return {"wer": compute_score(preds, labels, "wer"), "cer": compute_score(preds, labels, "cer")}


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class XtremeS(datasets.Metric):
    def _info(self):
        if self.config_name not in _CONFIG_NAMES:
            raise KeyError(f"You should supply a configuration name selected in {_CONFIG_NAMES}")

        pred_type = "int64" if self.config_name in ["fleurs-lang_id", "minds14"] else "string"

        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {"predictions": datasets.Value(pred_type), "references": datasets.Value(pred_type)}
            ),
            codebase_urls=[],
            reference_urls=[],
            format="numpy",
        )

    def _compute(self, predictions, references, bleu_kwargs=None, wer_kwargs=None):

        bleu_kwargs = bleu_kwargs if bleu_kwargs is not None else {}
        wer_kwargs = wer_kwargs if wer_kwargs is not None else {}

        if self.config_name == "fleurs-lang_id":
            return {"accuracy": simple_accuracy(predictions, references)}
        elif self.config_name == "minds14":
            return f1_and_simple_accuracy(predictions, references)
        elif self.config_name == "covost2":
            smooth_method = bleu_kwargs.pop("smooth_method", "exp")
            smooth_value = bleu_kwargs.pop("smooth_value", None)
            force = bleu_kwargs.pop("force", False)
            lowercase = bleu_kwargs.pop("lowercase", False)
            tokenize = bleu_kwargs.pop("tokenize", None)
            use_effective_order = bleu_kwargs.pop("use_effective_order", False)
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
        elif self.config_name in ["fleurs-asr", "mls", "voxpopuli"]:
            concatenate_texts = wer_kwargs.pop("concatenate_texts", False)
            return wer_and_cer(predictions, references, concatenate_texts, self.config_name)
        else:
            raise KeyError(f"You should supply a configuration name selected in {_CONFIG_NAMES}")
