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
""" TER metric as available in sacrebleu. """
import sacrebleu as scb

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
    abstract = "We examine a new, intuitive measure for evaluating machine-translation output that avoids the knowledge intensiveness of more meaning-based approaches, and the labor-intensiveness of human judgments. Translation Edit Rate (TER) measures the amount of editing that a human would have to perform to change a system output so it exactly matches a reference translation. We show that the single-reference variant of TER correlates as well with human judgments of MT quality as the four-reference variant of BLEU. We also define a human-targeted TER (or HTER) and show that it yields higher correlations with human judgments than BLEU{---}even when BLEU is given human-targeted references. Our results indicate that HTER correlates with human judgments better than HMETEOR and that the four-reference variants of TER and HTER correlate with human judgments as well as{---}or better than{---}a second human judgment does.",
}
"""

_DESCRIPTION = """\
Besides calculating BLEU scores, SacreBLEU is also capable in calculating TER scores, among other things.
Specifically, it is inspired by the TERCOM implementation which can be found here: https://github.com/jhclark/tercom

See the [README.md] file at https://github.com/mjpost/sacreBLEU#ter for more information.
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
    'score': TER score
    'num_edits': number of edits required
    'ref_length': reference length

Examples:

    >>> predictions = ["hello there general kenobi", "foo bar foobar"]
    >>> references = [["hello there general kenobi", "hello there !"], ["foo bar foobar", "foo bar foobar"]]
    >>> ter = datasets.load_metric("ter")
    >>> results = ter.compute(predictions=predictions, references=references)
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Ter(datasets.Metric):
    """Largely borrowed from the sacrebleu implementation in `datasets`"""
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/mjpost/sacreBLEU#ter",
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=["https://github.com/mjpost/sacreBLEU#ter"],
            reference_urls=[
                "https://github.com/mjpost/sacreBLEU#ter",
                "http://www.cs.umd.edu/~snover/tercom/",
                "https://github.com/jhclark/tercom",
            ],
        )

    def _compute(self,
                 predictions,
                 references,
                 normalized: bool = False,
                 no_punct: bool = False,
                 asian_support: bool = False,
                 case_sensitive: bool = False
                 ):
        references_per_prediction = len(references[0])
        if any(len(refs) != references_per_prediction for refs in references):
            raise ValueError("Sacrebleu requires the same number of references for each prediction")
        transformed_references = [[refs[i] for refs in references] for i in range(references_per_prediction)]
        output = scb.corpus_ter(
            predictions,
            transformed_references,
            normalized=normalized,
            no_punct=no_punct,
            asian_support=asian_support,
            case_sensitive=case_sensitive
        )
        output_dict = {
            "score": output.score,
            "num_edits": output.num_edits,
            "ref_length": output.ref_length
        }
        return output_dict
