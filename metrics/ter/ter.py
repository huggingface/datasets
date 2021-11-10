# coding=utf-8
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
""" TER metric as available in sacrebleu. """
import sacrebleu as scb
from packaging import version
from sacrebleu import TER

import datasets


_CITATION = """\
@inproceedings{snover-etal-2006-study,
    title = "A Study of Translation Edit Rate with Targeted Human Annotation",
    author = "Snover, Matthew  and
      Dorr, Bonnie  and
      Schwartz, Rich  and
      Micciulla, Linnea  and
      Makhoul, John",
    booktitle = "Proceedings of the 7th Conference of the Association for Machine Translation in the Americas: Technical Papers",
    month = aug # " 8-12",
    year = "2006",
    address = "Cambridge, Massachusetts, USA",
    publisher = "Association for Machine Translation in the Americas",
    url = "https://aclanthology.org/2006.amta-papers.25",
    pages = "223--231",
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
TER (Translation Edit Rate, also called Translation Error Rate) is a metric to quantify the edit operations that a
hypothesis requires to match a reference translation. We use the implementation that is already present in sacrebleu
(https://github.com/mjpost/sacreBLEU#ter), which in turn is inspired by the TERCOM implementation, which can be found
here: https://github.com/jhclark/tercom.

The implementation here is slightly different from sacrebleu in terms of the required input format. The length of
the references and hypotheses lists need to be the same, so you may need to transpose your references compared to
sacrebleu's required input format. See https://github.com/huggingface/datasets/issues/3154#issuecomment-950746534

See the README.md file at https://github.com/mjpost/sacreBLEU#ter for more information.
"""

_KWARGS_DESCRIPTION = """
Produces TER scores alongside the number of edits and reference length.

Args:
    predictions: The system stream (a sequence of segments).
    references: A list of one or more reference streams (each a sequence of segments).
    normalized: Whether to apply basic tokenization to sentences.
    no_punct: Whether to remove punctuations from sentences.
    asian_support: Whether to support Asian character processing.
    case_sensitive: Whether to disable lowercasing.

Returns:
    'score': TER score (num_edits / sum_ref_lengths * 100),
    'num_edits': The cumulative number of edits,
    'ref_length': The cumulative average reference length.

Examples:

    >>> predictions = ["hello there general kenobi", "foo bar foobar"]
    >>> references = [["hello there general kenobi", "hello there !"], ["foo bar foobar", "foo bar foobar"]]
    >>> ter = datasets.load_metric("ter")
    >>> results = ter.compute(predictions=predictions, references=references)
    >>> print(results)
    {'score': 0.0, 'num_edits': 0, 'ref_length': 6.5}
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Ter(datasets.Metric):
    def _info(self):
        if version.parse(scb.__version__) < version.parse("1.4.12"):
            raise ImportWarning(
                "To use `sacrebleu`, the module `sacrebleu>=1.4.12` is required, and the current version of `sacrebleu` doesn't match this condition.\n"
                'You can install it with `pip install "sacrebleu>=1.4.12"`.'
            )
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="http://www.cs.umd.edu/~snover/tercom/",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=["https://github.com/mjpost/sacreBLEU#ter"],
            reference_urls=[
                "https://github.com/jhclark/tercom",
            ],
        )

    def _compute(
        self,
        predictions,
        references,
        normalized: bool = False,
        no_punct: bool = False,
        asian_support: bool = False,
        case_sensitive: bool = False,
    ):
        references_per_prediction = len(references[0])
        if any(len(refs) != references_per_prediction for refs in references):
            raise ValueError("Sacrebleu requires the same number of references for each prediction")
        transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]

        sb_ter = TER(normalized, no_punct, asian_support, case_sensitive)
        output = sb_ter.corpus_score(predictions, transformed_references)

        return {"score": output.score, "num_edits": output.num_edits, "ref_length": output.ref_length}
