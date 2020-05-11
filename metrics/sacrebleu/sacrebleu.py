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
""" SACREBLEU metric. """

import nlp
import sacrebleu as scb

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
    predictions: The system stream (a sequence of segments)
    references: A list of one or more reference streams (each a sequence of segments)
    smooth: The smoothing method to use
    smooth_value: For 'floor' smoothing, the floor to use
    force: Ignore data that looks already tokenized
    lowercase: Lowercase the data
    tokenize: The tokenizer to use
Returns:
    'score': BLEU score,
    'counts': Counts,
    'totals': Totals,
    'precisions': Precisions,
    'bp': Brevity penalty,
    'sys_len': predictions length,
    'ref_len': reference length,
"""

class Sacrebleu(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/mjpost/sacreBLEU",
            inputs_description=_KWARGS_DESCRIPTION,
            predictions_features=nlp.Sequence(nlp.Value('string')),
            references_features=nlp.Sequence(nlp.Sequence(nlp.Value('string'))),
            codebase_urls=["https://github.com/mjpost/sacreBLEU"],
            reference_urls=["https://github.com/mjpost/sacreBLEU",
                            "https://en.wikipedia.org/wiki/BLEU",
                            "https://towardsdatascience.com/evaluating-text-output-in-nlp-bleu-at-your-own-risk-e8609665a213"]
        )

    def _compute(self, predictions, references, smooth_method='exp',
                smooth_value=None,
                force=False,
                lowercase=False,
                tokenize=scb.sacrebleu.DEFAULT_TOKENIZER,
                use_effective_order=False):
        output = scb.corpus_bleu(
            sys_stream=predictions,
            ref_streams=references,
            smooth_method=smooth_method,
            smooth_value=smooth_value,
            force=force,
            lowercase=lowercase,
            tokenize=tokenize,
            use_effective_order=use_effective_order)
        output_dict = {
            'score': output.score,
            'counts': output.counts,
            'totals': output.totals,
            'precisions': output.precisions,
            'bp': output.bp,
            'sys_len': output.sys_len,
            'ref_len': output.ref_len,
        }
        return output_dict
