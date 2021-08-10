# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
""" SARI metric."""

from collections import Counter

import sacrebleu
import sacremoses
from packaging import version

import datasets


_CITATION = """\
@inproceedings{xu-etal-2016-optimizing,
title = {Optimizing Statistical Machine Translation for Text Simplification},
authors={Xu, Wei and Napoles, Courtney and Pavlick, Ellie and Chen, Quanze and Callison-Burch, Chris},
journal = {Transactions of the Association for Computational Linguistics},
volume = {4},
year={2016},
url = {https://www.aclweb.org/anthology/Q16-1029},
pages = {401--415},
}
"""

_DESCRIPTION = """\
SARI is a metric used for evaluating automatic text simplification systems.
The metric compares the predicted simplified sentences against the reference
and the source sentences. It explicitly measures the goodness of words that are
added, deleted and kept by the system.
Sari = (F1_add + F1_keep + P_del) / 3
where
F1_add: n-gram F1 score for add operation
F1_keep: n-gram F1 score for keep operation
P_del: n-gram precision score for delete operation
n = 4, as in the original paper.

This implementation is adapted from Tensorflow's tensor2tensor implementation [3].
It has two differences with the original GitHub [1] implementation:
  (1) Defines 0/0=1 instead of 0 to give higher scores for predictions that match
      a target exactly.
  (2) Fixes an alleged bug [2] in the keep score computation.
[1] https://github.com/cocoxu/simplification/blob/master/SARI.py
    (commit 0210f15)
[2] https://github.com/cocoxu/simplification/issues/6
[3] https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/utils/sari_hook.py
"""


_KWARGS_DESCRIPTION = """
Calculates sari score (between 0 and 100) given a list of source and predicted
sentences, and a list of lists of reference sentences.
Args:
    sources: list of source sentences where each sentence should be a string.
    predictions: list of predicted sentences where each sentence should be a string.
    references: list of lists of reference sentences where each sentence should be a string.
Returns:
    sari: sari score
Examples:
    >>> sources=["About 95 species are currently accepted ."]
    >>> predictions=["About 95 you now get in ."]
    >>> references=[["About 95 species are currently known .","About 95 species are now accepted .","95 species are now accepted ."]]
    >>> sari = datasets.load_metric("sari")
    >>> results = sari.compute(sources=sources, predictions=predictions, references=references)
    >>> print(results)
    {'sari': 26.953601953601954}
"""


def SARIngram(sgrams, cgrams, rgramslist, numref):
    rgramsall = [rgram for rgrams in rgramslist for rgram in rgrams]
    rgramcounter = Counter(rgramsall)

    sgramcounter = Counter(sgrams)
    sgramcounter_rep = Counter()
    for sgram, scount in sgramcounter.items():
        sgramcounter_rep[sgram] = scount * numref

    cgramcounter = Counter(cgrams)
    cgramcounter_rep = Counter()
    for cgram, ccount in cgramcounter.items():
        cgramcounter_rep[cgram] = ccount * numref

    # KEEP
    keepgramcounter_rep = sgramcounter_rep & cgramcounter_rep
    keepgramcountergood_rep = keepgramcounter_rep & rgramcounter
    keepgramcounterall_rep = sgramcounter_rep & rgramcounter

    keeptmpscore1 = 0
    keeptmpscore2 = 0
    for keepgram in keepgramcountergood_rep:
        keeptmpscore1 += keepgramcountergood_rep[keepgram] / keepgramcounter_rep[keepgram]
        # Fix an alleged bug [2] in the keep score computation.
        # keeptmpscore2 += keepgramcountergood_rep[keepgram] / keepgramcounterall_rep[keepgram]
        keeptmpscore2 += keepgramcountergood_rep[keepgram]
    # Define 0/0=1 instead of 0 to give higher scores for predictions that match
    #      a target exactly.
    keepscore_precision = 1
    keepscore_recall = 1
    if len(keepgramcounter_rep) > 0:
        keepscore_precision = keeptmpscore1 / len(keepgramcounter_rep)
    if len(keepgramcounterall_rep) > 0:
        # Fix an alleged bug [2] in the keep score computation.
        # keepscore_recall = keeptmpscore2 / len(keepgramcounterall_rep)
        keepscore_recall = keeptmpscore2 / sum(keepgramcounterall_rep.values())
    keepscore = 0
    if keepscore_precision > 0 or keepscore_recall > 0:
        keepscore = 2 * keepscore_precision * keepscore_recall / (keepscore_precision + keepscore_recall)

    # DELETION
    delgramcounter_rep = sgramcounter_rep - cgramcounter_rep
    delgramcountergood_rep = delgramcounter_rep - rgramcounter
    delgramcounterall_rep = sgramcounter_rep - rgramcounter
    deltmpscore1 = 0
    deltmpscore2 = 0
    for delgram in delgramcountergood_rep:
        deltmpscore1 += delgramcountergood_rep[delgram] / delgramcounter_rep[delgram]
        deltmpscore2 += delgramcountergood_rep[delgram] / delgramcounterall_rep[delgram]
    # Define 0/0=1 instead of 0 to give higher scores for predictions that match
    # a target exactly.
    delscore_precision = 1
    if len(delgramcounter_rep) > 0:
        delscore_precision = deltmpscore1 / len(delgramcounter_rep)

    # ADDITION
    addgramcounter = set(cgramcounter) - set(sgramcounter)
    addgramcountergood = set(addgramcounter) & set(rgramcounter)
    addgramcounterall = set(rgramcounter) - set(sgramcounter)

    addtmpscore = 0
    for addgram in addgramcountergood:
        addtmpscore += 1

    # Define 0/0=1 instead of 0 to give higher scores for predictions that match
    # a target exactly.
    addscore_precision = 1
    addscore_recall = 1
    if len(addgramcounter) > 0:
        addscore_precision = addtmpscore / len(addgramcounter)
    if len(addgramcounterall) > 0:
        addscore_recall = addtmpscore / len(addgramcounterall)
    addscore = 0
    if addscore_precision > 0 or addscore_recall > 0:
        addscore = 2 * addscore_precision * addscore_recall / (addscore_precision + addscore_recall)

    return (keepscore, delscore_precision, addscore)


def SARIsent(ssent, csent, rsents):
    numref = len(rsents)

    s1grams = ssent.split(" ")
    c1grams = csent.split(" ")
    s2grams = []
    c2grams = []
    s3grams = []
    c3grams = []
    s4grams = []
    c4grams = []

    r1gramslist = []
    r2gramslist = []
    r3gramslist = []
    r4gramslist = []
    for rsent in rsents:
        r1grams = rsent.split(" ")
        r2grams = []
        r3grams = []
        r4grams = []
        r1gramslist.append(r1grams)
        for i in range(0, len(r1grams) - 1):
            if i < len(r1grams) - 1:
                r2gram = r1grams[i] + " " + r1grams[i + 1]
                r2grams.append(r2gram)
            if i < len(r1grams) - 2:
                r3gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2]
                r3grams.append(r3gram)
            if i < len(r1grams) - 3:
                r4gram = r1grams[i] + " " + r1grams[i + 1] + " " + r1grams[i + 2] + " " + r1grams[i + 3]
                r4grams.append(r4gram)
        r2gramslist.append(r2grams)
        r3gramslist.append(r3grams)
        r4gramslist.append(r4grams)

    for i in range(0, len(s1grams) - 1):
        if i < len(s1grams) - 1:
            s2gram = s1grams[i] + " " + s1grams[i + 1]
            s2grams.append(s2gram)
        if i < len(s1grams) - 2:
            s3gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2]
            s3grams.append(s3gram)
        if i < len(s1grams) - 3:
            s4gram = s1grams[i] + " " + s1grams[i + 1] + " " + s1grams[i + 2] + " " + s1grams[i + 3]
            s4grams.append(s4gram)

    for i in range(0, len(c1grams) - 1):
        if i < len(c1grams) - 1:
            c2gram = c1grams[i] + " " + c1grams[i + 1]
            c2grams.append(c2gram)
        if i < len(c1grams) - 2:
            c3gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2]
            c3grams.append(c3gram)
        if i < len(c1grams) - 3:
            c4gram = c1grams[i] + " " + c1grams[i + 1] + " " + c1grams[i + 2] + " " + c1grams[i + 3]
            c4grams.append(c4gram)

    (keep1score, del1score, add1score) = SARIngram(s1grams, c1grams, r1gramslist, numref)
    (keep2score, del2score, add2score) = SARIngram(s2grams, c2grams, r2gramslist, numref)
    (keep3score, del3score, add3score) = SARIngram(s3grams, c3grams, r3gramslist, numref)
    (keep4score, del4score, add4score) = SARIngram(s4grams, c4grams, r4gramslist, numref)
    avgkeepscore = sum([keep1score, keep2score, keep3score, keep4score]) / 4
    avgdelscore = sum([del1score, del2score, del3score, del4score]) / 4
    avgaddscore = sum([add1score, add2score, add3score, add4score]) / 4
    finalscore = (avgkeepscore + avgdelscore + avgaddscore) / 3
    return finalscore


def normalize(sentence, lowercase: bool = True, tokenizer: str = "13a", return_str: bool = True):

    # Normalization is requried for the ASSET dataset (one of the primary
    # datasets in sentence simplification) to allow using space
    # to split the sentence. Even though Wiki-Auto and TURK datasets,
    # do not require normalization, we do it for consistency.
    # Code adapted from the EASSE library [1] written by the authors of the ASSET dataset.
    # [1] https://github.com/feralvam/easse/blob/580bba7e1378fc8289c663f864e0487188fe8067/easse/utils/preprocessing.py#L7

    if lowercase:
        sentence = sentence.lower()

    if tokenizer in ["13a", "intl"]:
        if version.parse(sacrebleu.__version__).major >= 2:
            normalized_sent = sacrebleu.metrics.bleu._get_tokenizer(tokenizer)()(sentence)
        else:
            normalized_sent = sacrebleu.TOKENIZERS[tokenizer]()(sentence)
    elif tokenizer == "moses":
        normalized_sent = sacremoses.MosesTokenizer().tokenize(sentence, return_str=True, escape=False)
    elif tokenizer == "penn":
        normalized_sent = sacremoses.MosesTokenizer().penn_tokenize(sentence, return_str=True)
    else:
        normalized_sent = sentence

    if not return_str:
        normalized_sent = normalized_sent.split()

    return normalized_sent


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Sari(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Value("string", id="sequence"),
                    "references": datasets.Sequence(datasets.Value("string", id="sequence"), id="references"),
                }
            ),
            codebase_urls=[
                "https://github.com/cocoxu/simplification/blob/master/SARI.py",
                "https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/utils/sari_hook.py",
            ],
            reference_urls=["https://www.aclweb.org/anthology/Q16-1029.pdf"],
        )

    def _compute(self, sources, predictions, references):

        if not (len(sources) == len(predictions) == len(references)):
            raise ValueError("Sources length must match predictions and references lengths.")
        sari_score = 0
        for src, pred, refs in zip(sources, predictions, references):
            sari_score += SARIsent(normalize(src), normalize(pred), [normalize(sent) for sent in refs])
        sari_score = sari_score / len(predictions)
        return {"sari": 100 * sari_score}
