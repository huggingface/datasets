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
""" SACREBLEU metric. """

import sacrebleu as scb
from packaging import version

import datasets


_CITATION = """\
@inproceedings{post-2018-call,
    title = "A Call for Clarity in Reporting {BLEU} Scores",
    author = "Post, Matt",
    booktitle = "Proceedings of the Third Conference on Machine Translation: Research Papers",
    month = oct,
    year = "2018",
    address = "Belgium, Brussels",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W18-6319",
    pages = "186--191",
}
"""

_DESCRIPTION = """\
SacreBLEU provides hassle-free computation of shareable, comparable, and reproducible BLEU scores.
Inspired by Rico Sennrich's `multi-bleu-detok.perl`, it produces the official WMT scores but works with plain text.
It also knows all the standard test sets and handles downloading, processing, and tokenization for you.

See the [README.md] file at https://github.com/mjpost/sacreBLEU for more information.
"""

_KWARGS_DESCRIPTION = """
Produces BLEU scores along with its sufficient statistics
from a source against one or more references.

Args:
    predictions: The system stream (a sequence of segments).
    references: A list of one or more reference streams (each a sequence of segments).
    smooth_method: The smoothing method to use. (Default: 'exp').
    smooth_value: The smoothing value. Only valid for 'floor' and 'add-k'. (Defaults: floor: 0.1, add-k: 1).
    tokenize: Tokenization method to use for BLEU. If not provided, defaults to 'zh' for Chinese, 'ja-mecab' for
        Japanese and '13a' (mteval) otherwise.
    lowercase: Lowercase the data. If True, enables case-insensitivity. (Default: False).
    force: Insist that your tokenized input is actually detokenized.

Returns:
    'score': BLEU score,
    'counts': Counts,
    'totals': Totals,
    'precisions': Precisions,
    'bp': Brevity penalty,
    'sys_len': predictions length,
    'ref_len': reference length,

Examples:

    >>> predictions = ["hello there general kenobi", "foo bar foobar"]
    >>> references = [["hello there general kenobi", "hello there !"], ["foo bar foobar", "foo bar foobar"]]
    >>> sacrebleu = datasets.load_metric("sacrebleu")
    >>> results = sacrebleu.compute(predictions=predictions, references=references)
    >>> print(list(results.keys()))
    ['score', 'counts', 'totals', 'precisions', 'bp', 'sys_len', 'ref_len']
    >>> print(round(results["score"], 1))
    100.0
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Sacrebleu(datasets.Metric):
    def _info(self):
        if version.parse(scb.__version__) < version.parse("1.4.12"):
            raise ImportWarning(
                "To use `sacrebleu`, the module `sacrebleu>=1.4.12` is required, and the current version of `sacrebleu` doesn't match this condition.\n"
                'You can install it with `pip install "sacrebleu>=1.4.12"`.'
            )
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/mjpost/sacreBLEU",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=["https://github.com/mjpost/sacreBLEU"],
            reference_urls=[
                "https://github.com/mjpost/sacreBLEU",
                "https://en.wikipedia.org/wiki/BLEU",
                "https://towardsdatascience.com/evaluating-text-output-in-nlp-bleu-at-your-own-risk-e8609665a213",
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        smooth_method="exp",
        smooth_value=None,
        force=False,
        lowercase=False,
        tokenize=None,
        use_effective_order=False,
    ):
        references_per_prediction = len(references[0])
        if any(len(refs) != references_per_prediction for refs in references):
            raise ValueError("Sacrebleu requires the same number of references for each prediction")
        transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]
        output = scb.corpus_bleu(
            predictions,
            transformed_references,
            smooth_method=smooth_method,
            smooth_value=smooth_value,
            force=force,
            lowercase=lowercase,
            use_effective_order=use_effective_order,
            **(dict(tokenize=tokenize) if tokenize else {}),
        )
        output_dict = {
            "score": output.score,
            "counts": output.counts,
            "totals": output.totals,
            "precisions": output.precisions,
            "bp": output.bp,
            "sys_len": output.sys_len,
            "ref_len": output.ref_len,
        }
        return output_dict
