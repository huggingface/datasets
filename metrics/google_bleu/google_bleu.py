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
""" Google BLEU (aka GLEU) metric. """

from typing import Dict, List

from nltk.translate import gleu_score

import datasets
from datasets import MetricInfo


_CITATION = """\
@misc{wu2016googles,
      title={Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation},
      author={Yonghui Wu and Mike Schuster and Zhifeng Chen and Quoc V. Le and Mohammad Norouzi and Wolfgang Macherey
              and Maxim Krikun and Yuan Cao and Qin Gao and Klaus Macherey and Jeff Klingner and Apurva Shah and Melvin
              Johnson and Xiaobing Liu and Łukasz Kaiser and Stephan Gouws and Yoshikiyo Kato and Taku Kudo and Hideto
              Kazawa and Keith Stevens and George Kurian and Nishant Patil and Wei Wang and Cliff Young and
              Jason Smith and Jason Riesa and Alex Rudnick and Oriol Vinyals and Greg Corrado and Macduff Hughes
              and Jeffrey Dean},
      year={2016},
      eprint={1609.08144},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The BLEU score has some undesirable properties when used for single
sentences, as it was designed to be a corpus measure. We therefore
use a slightly different score for our RL experiments which we call
the 'GLEU score'. For the GLEU score, we record all sub-sequences of
1, 2, 3 or 4 tokens in output and target sequence (n-grams). We then
compute a recall, which is the ratio of the number of matching n-grams
to the number of total n-grams in the target (ground truth) sequence,
and a precision, which is the ratio of the number of matching n-grams
to the number of total n-grams in the generated output sequence. Then
GLEU score is simply the minimum of recall and precision. This GLEU
score's range is always between 0 (no matches) and 1 (all match) and
it is symmetrical when switching output and target. According to
our experiments, GLEU score correlates quite well with the BLEU
metric on a corpus level but does not have its drawbacks for our per
sentence reward objective.
"""

_KWARGS_DESCRIPTION = """\
Computes corpus-level Google BLEU (GLEU) score of translated segments against one or more references.
Instead of averaging the sentence level GLEU scores (i.e. macro-average precision), Wu et al. (2016) sum up the matching
tokens and the max of hypothesis and reference tokens for each sentence, then compute using the aggregate values.

Args:
    predictions: list of translations to score.
        Each translation should be tokenized into a list of tokens.
    references: list of lists of references for each translation.
        Each reference should be tokenized into a list of tokens.
    min_len: The minimum order of n-gram this function should extract.
    max_len: The maximum order of n-gram this function should extract.

Returns:
    'google_bleu': bleu score

Examples:
    >>> hyp1 = ['It', 'is', 'a', 'guide', 'to', 'action', 'which',
    ...         'ensures', 'that', 'the', 'military', 'always',
    ...         'obeys', 'the', 'commands', 'of', 'the', 'party']
    >>> ref1a = ['It', 'is', 'a', 'guide', 'to', 'action', 'that',
    ...          'ensures', 'that', 'the', 'military', 'will', 'forever',
    ...          'heed', 'Party', 'commands']
    >>> ref1b = ['It', 'is', 'the', 'guiding', 'principle', 'which',
    ...          'guarantees', 'the', 'military', 'forces', 'always',
    ...          'being', 'under', 'the', 'command', 'of', 'the', 'Party']
    >>> ref1c = ['It', 'is', 'the', 'practical', 'guide', 'for', 'the',
    ...          'army', 'always', 'to', 'heed', 'the', 'directions',
    ...          'of', 'the', 'party']

    >>> hyp2 = ['he', 'read', 'the', 'book', 'because', 'he', 'was',
    ...         'interested', 'in', 'world', 'history']
    >>> ref2a = ['he', 'was', 'interested', 'in', 'world', 'history',
    ...          'because', 'he', 'read', 'the', 'book']

    >>> list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
    >>> hypotheses = [hyp1, hyp2]
    >>> google_bleu = datasets.load_metric("google_bleu")
    >>> results = google_bleu.compute(predictions=hypotheses, references=list_of_references)
    >>> print(results["google_bleu"])
    0.5673076923076923
"""


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class GoogleBleu(datasets.Metric):
    def _info(self) -> MetricInfo:
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Sequence(datasets.Value("string", id="token"), id="sequence"),
                    "references": datasets.Sequence(
                        datasets.Sequence(datasets.Value("string", id="token"), id="sequence"), id="references"
                    ),
                }
            ),
        )

    def _compute(
        self,
        predictions: List[List[List[str]]],
        references: List[List[str]],
        min_len: int = 1,
        max_len: int = 4,
    ) -> Dict[str, float]:
        return {
            "google_bleu": gleu_score.corpus_gleu(
                list_of_references=references, hypotheses=predictions, min_len=min_len, max_len=max_len
            )
        }
