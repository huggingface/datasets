# Copyright 2021 The HuggingFace Datasets Authors.
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
""" Chrf(++) metric as available in sacrebleu. """
import sacrebleu as scb
from packaging import version
from sacrebleu import CHRF

import datasets


_CITATION = """\
@inproceedings{popovic-2015-chrf,
    title = "chr{F}: character n-gram {F}-score for automatic {MT} evaluation",
    author = "Popovi{\'c}, Maja",
    booktitle = "Proceedings of the Tenth Workshop on Statistical Machine Translation",
    month = sep,
    year = "2015",
    address = "Lisbon, Portugal",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W15-3049",
    doi = "10.18653/v1/W15-3049",
    pages = "392--395",
}
@inproceedings{popovic-2017-chrf,
    title = "chr{F}++: words helping character n-grams",
    author = "Popovi{\'c}, Maja",
    booktitle = "Proceedings of the Second Conference on Machine Translation",
    month = sep,
    year = "2017",
    address = "Copenhagen, Denmark",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W17-4770",
    doi = "10.18653/v1/W17-4770",
    pages = "612--618",
}
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
ChrF and ChrF++ are two MT evaluation metrics. They both use the F-score statistic for character n-gram matches,
and ChrF++ adds word n-grams as well which correlates more strongly with direct assessment. We use the implementation
that is already present in sacrebleu.

The implementation here is slightly different from sacrebleu in terms of the required input format. The length of
the references and hypotheses lists need to be the same, so you may need to transpose your references compared to
sacrebleu's required input format. See https://github.com/huggingface/datasets/issues/3154#issuecomment-950746534

See the README.md file at https://github.com/mjpost/sacreBLEU#chrf--chrf for more information.
"""

_KWARGS_DESCRIPTION = """
Produces ChrF(++) scores for hypotheses given reference translations.

Args:
    predictions (list of str): The predicted sentences.
    references (list of list of str): The references. There should be one reference sub-list for each prediction sentence.
    char_order (int): Character n-gram order. Defaults to `6`.
    word_order (int): Word n-gram order. If equals to `2`, the metric is referred to as chrF++. Defaults to `0`.
    beta (int): Determine the importance of recall w.r.t precision. Defaults to `2`.
    lowercase (bool): if `True`, enables case-insensitivity. Defaults to `False`.
    whitespace (bool): If `True`, include whitespaces when extracting character n-grams.
    eps_smoothing (bool): If `True`, applies epsilon smoothing similar
    to reference chrF++.py, NLTK and Moses implementations. If `False`,
    it takes into account effective match order similar to sacreBLEU < 2.0.0. Defaults to `False`.

Returns:
    'score' (float): The chrF (chrF++) score,
    'char_order' (int): The character n-gram order,
    'word_order' (int): The word n-gram order. If equals to 2, the metric is referred to as chrF++,
    'beta' (int): Determine the importance of recall w.r.t precision

Examples:
    Example 1--a simple example of calculating chrF:
        >>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
        >>> reference = [["The relationship between dogs and cats is not exactly friendly."], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
        >>> chrf = datasets.load_metric("chrf")
        >>> results = chrf.compute(predictions=prediction, references=reference)
        >>> print(results)
        {'score': 84.64214891738334, 'char_order': 6, 'word_order': 0, 'beta': 2}

    Example 2--the same example, but with the argument word_order=2, to calculate chrF++ instead of chrF:
        >>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
        >>> reference = [["The relationship between dogs and cats is not exactly friendly."], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
        >>> chrf = datasets.load_metric("chrf")
        >>> results = chrf.compute(predictions=prediction,
        ...                         references=reference,
        ...                         word_order=2)
        >>> print(results)
        {'score': 82.87263732906315, 'char_order': 6, 'word_order': 2, 'beta': 2}

    Example 3--the same chrF++ example as above, but with `lowercase=True` to normalize all case:
        >>> prediction = ["The relationship between cats and dogs is not exactly friendly.", "a good bookshop is just a genteel black hole that knows how to read."]
        >>> reference = [["The relationship between dogs and cats is not exactly friendly."], ["A good bookshop is just a genteel Black Hole that knows how to read."]]
        >>> chrf = datasets.load_metric("chrf")
        >>> results = chrf.compute(predictions=prediction,
        ...                         references=reference,
        ...                         word_order=2,
        ...                         lowercase=True)
        >>> print(results)
        {'score': 92.12853119829202, 'char_order': 6, 'word_order': 2, 'beta': 2}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class ChrF(datasets.Metric):
    def _info(self):
        if version.parse(scb.__version__) < version.parse("1.4.12"):
            raise ImportWarning(
                "To use `sacrebleu`, the module `sacrebleu>=1.4.12` is required, and the current version of `sacrebleu` doesn't match this condition.\n"
                'You can install it with `pip install "sacrebleu>=1.4.12"`.'
            )
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/mjpost/sacreBLEU#chrf--chrf",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=["https://github.com/mjpost/sacreBLEU#chrf--chrf"],
            reference_urls=[
                "https://github.com/m-popovic/chrF",
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        char_order: int = CHRF.CHAR_ORDER,
        word_order: int = CHRF.WORD_ORDER,
        beta: int = CHRF.BETA,
        lowercase: bool = False,
        whitespace: bool = False,
        eps_smoothing: bool = False,
    ):
        references_per_prediction = len(references[0])
        if any(len(refs) != references_per_prediction for refs in references):
            raise ValueError("Sacrebleu requires the same number of references for each prediction")
        transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]

        sb_chrf = CHRF(char_order, word_order, beta, lowercase, whitespace, eps_smoothing)
        output = sb_chrf.corpus_score(predictions, transformed_references)

        return {
            "score": output.score,
            "char_order": output.char_order,
            "word_order": output.word_order,
            "beta": output.beta,
        }
