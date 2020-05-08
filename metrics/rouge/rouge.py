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
""" ROUGE metric. """

import nlp
from .nmt_rouge import rouge  # From: https://github.com/tensorflow/nmt/blob/master/nmt/scripts/rouge.py

_CITATION = """\
@inproceedings{lin-2004-rouge,
    title = "{ROUGE}: A Package for Automatic Evaluation of Summaries",
    author = "Lin, Chin-Yew",
    booktitle = "Text Summarization Branches Out",
    month = jul,
    year = "2004",
    address = "Barcelona, Spain",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W04-1013",
    pages = "74--81",
}
"""

_DESCRIPTION = """\
ROUGE, or Recall-Oriented Understudy for Gisting Evaluation, is a set of metrics and a software package used for
evaluating automatic summarization and machine translation software in natural language processing.
The metrics compare an automatically produced summary or translation against a reference or a set of references (human-produced) summary or translation.

The following five evaluation metrics are available:
ROUGE-N: Overlap of N-grams[2] between the system and reference summaries.
ROUGE-1 refers to the overlap of unigram (each word) between the system and reference summaries.
ROUGE-2 refers to the overlap of bigrams between the system and reference summaries.
ROUGE-L: Longest Common Subsequence (LCS)[3] based statistics. Longest common subsequence problem takes into account sentence level structure similarity naturally and identifies longest co-occurring in sequence n-grams automatically.
ROUGE-W: Weighted LCS-based statistics that favors consecutive LCSes .
ROUGE-S: Skip-bigram[4] based co-occurrence statistics. Skip-bigram is any pair of words in their sentence order.
ROUGE-SU: Skip-bigram plus unigram-based co-occurrence statistics.
"""

_KWARGS_DESCRIPTION = """
Calculates average rouge scores for a list of hypotheses and references
Args:
    predictions: list of predictions to score. Each predictions
        should be a string with tokens separated by spaces.
    references: list of reference for each prediction. Each
        reference should be a string with tokens separated by spaces.
Returns:
    rouge_1/f_score: rouge_1 f1,
    rouge_1/r_score: rouge_1 recall,
    rouge_1/p_score: rouge_1 precision,
    rouge_2/f_score: rouge_2 f1,
    rouge_2/r_score: rouge_2 recall,
    rouge_2/p_score: rouge_2 precision,
    rouge_l/f_score: rouge_l f1,
    rouge_l/r_score: rouge_l recall,
    rouge_l/p_score: rouge_l precision
"""

class Rouge(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            predictions_features=nlp.Sequence(nlp.Value('string')),
            references_features=nlp.Sequence(nlp.Value('string')),
            codebase_urls=["https://github.com/tensorflow/nmt/blob/master/nmt/scripts/rouge.py"],
            reference_urls=["https://en.wikipedia.org/wiki/ROUGE_(metric)",
                            "http://research.microsoft.com/en-us/um/people/cyl/download/papers/rouge-working-note-v1.3.1.pdf"]
        )

    def _compute(self, predictions, references):
        score = rouge(hypotheses=predictions, references=references)
        return score
