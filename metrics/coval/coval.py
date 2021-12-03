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
""" CoVal metric. """
import coval  # From: git+https://github.com/ns-moosavi/coval.git noqa: F401
from coval.conll import reader, util
from coval.eval import evaluator

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@InProceedings{moosavi2019minimum,
    author = { Nafise Sadat Moosavi, Leo Born, Massimo Poesio and Michael Strube},
    title = {Using Automatically Extracted Minimum Spans to Disentangle Coreference Evaluation from Boundary Detection},
    year = {2019},
    booktitle = {Proceedings of the 57th Annual Meeting of
        the Association for Computational Linguistics (Volume 1: Long Papers)},
    publisher = {Association for Computational Linguistics},
    address = {Florence, Italy},
}

@inproceedings{10.3115/1072399.1072405,
author = {Vilain, Marc and Burger, John and Aberdeen, John and Connolly, Dennis and Hirschman, Lynette},
title = {A Model-Theoretic Coreference Scoring Scheme},
year = {1995},
isbn = {1558604022},
publisher = {Association for Computational Linguistics},
address = {USA},
url = {https://doi.org/10.3115/1072399.1072405},
doi = {10.3115/1072399.1072405},
booktitle = {Proceedings of the 6th Conference on Message Understanding},
pages = {45–52},
numpages = {8},
location = {Columbia, Maryland},
series = {MUC6 ’95}
}

@INPROCEEDINGS{Bagga98algorithmsfor,
    author = {Amit Bagga and Breck Baldwin},
    title = {Algorithms for Scoring Coreference Chains},
    booktitle = {In The First International Conference on Language Resources and Evaluation Workshop on Linguistics Coreference},
    year = {1998},
    pages = {563--566}
}

@INPROCEEDINGS{Luo05oncoreference,
    author = {Xiaoqiang Luo},
    title = {On coreference resolution performance metrics},
    booktitle = {In Proc. of HLT/EMNLP},
    year = {2005},
    pages = {25--32},
    publisher = {URL}
}

@inproceedings{moosavi-strube-2016-coreference,
    title = "Which Coreference Evaluation Metric Do You Trust? A Proposal for a Link-based Entity Aware Metric",
    author = "Moosavi, Nafise Sadat  and
      Strube, Michael",
    booktitle = "Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2016",
    address = "Berlin, Germany",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P16-1060",
    doi = "10.18653/v1/P16-1060",
    pages = "632--642",
}

"""

_DESCRIPTION = """\
CoVal is a coreference evaluation tool for the CoNLL and ARRAU datasets which
implements of the common evaluation metrics including MUC [Vilain et al, 1995],
B-cubed [Bagga and Baldwin, 1998], CEAFe [Luo et al., 2005],
LEA [Moosavi and Strube, 2016] and the averaged CoNLL score
(the average of the F1 values of MUC, B-cubed and CEAFe)
[Denis and Baldridge, 2009a; Pradhan et al., 2011].

This wrapper of CoVal currently only work with CoNLL line format:
The CoNLL format has one word per line with all the annotation for this word in column separated by spaces:
Column	Type	Description
1	Document ID	This is a variation on the document filename
2	Part number	Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
3	Word number
4	Word itself	This is the token as segmented/tokenized in the Treebank. Initially the *_skel file contain the placeholder [WORD] which gets replaced by the actual token from the Treebank which is part of the OntoNotes release.
5	Part-of-Speech
6	Parse bit	This is the bracketed structure broken before the first open parenthesis in the parse, and the word/part-of-speech leaf replaced with a *. The full parse can be created by substituting the asterix with the "([pos] [word])" string (or leaf) and concatenating the items in the rows of that column.
7	Predicate lemma	The predicate lemma is mentioned for the rows for which we have semantic role information. All other rows are marked with a "-"
8	Predicate Frameset ID	This is the PropBank frameset ID of the predicate in Column 7.
9	Word sense	This is the word sense of the word in Column 3.
10	Speaker/Author	This is the speaker or author name where available. Mostly in Broadcast Conversation and Web Log data.
11	Named Entities	These columns identifies the spans representing various named entities.
12:N	Predicate Arguments	There is one column each of predicate argument structure information for the predicate mentioned in Column 7.
N	Coreference	Coreference chain information encoded in a parenthesis structure.
More informations on the format can be found here (section "*_conll File Format"): http://www.conll.cemantix.org/2012/data.html

Details on the evaluation on CoNLL can be found here: https://github.com/ns-moosavi/coval/blob/master/conll/README.md

CoVal code was written by @ns-moosavi.
Some parts are borrowed from https://github.com/clarkkev/deep-coref/blob/master/evaluation.py
The test suite is taken from https://github.com/conll/reference-coreference-scorers/
Mention evaluation and the test suite are added by @andreasvc.
Parsing CoNLL files is developed by Leo Born.
"""

_KWARGS_DESCRIPTION = """
Calculates coreference evaluation metrics.
Args:
    predictions: list of sentences. Each sentence is a list of word predictions to score in the CoNLL format.
        Each prediction is a word with its annotations as a string made of columns joined with spaces.
        Only columns 4, 5, 6 and the last column are used (word, POS, Pars and coreference annotation)
        See the details on the format in the description of the metric.
    references: list of sentences. Each sentence is a list of word reference to score in the CoNLL format.
        Each reference is a word with its annotations as a string made of columns joined with spaces.
        Only columns 4, 5, 6 and the last column are used (word, POS, Pars and coreference annotation)
        See the details on the format in the description of the metric.
    keep_singletons: After extracting all mentions of key or system files,
        mentions whose corresponding coreference chain is of size one,
        are considered as singletons. The default evaluation mode will include
        singletons in evaluations if they are included in the key or the system files.
        By setting 'keep_singletons=False', all singletons in the key and system files
        will be excluded from the evaluation.
    NP_only: Most of the recent coreference resolvers only resolve NP mentions and
        leave out the resolution of VPs. By setting the 'NP_only' option, the scorer will only evaluate the resolution of NPs.
    min_span: By setting 'min_span', the scorer reports the results based on automatically detected minimum spans.
        Minimum spans are determined using the MINA algorithm.

Returns:
    'mentions': mentions
    'muc': MUC metric [Vilain et al, 1995]
    'bcub': B-cubed [Bagga and Baldwin, 1998]
    'ceafe': CEAFe [Luo et al., 2005]
    'lea': LEA [Moosavi and Strube, 2016]
    'conll_score': averaged CoNLL score (the average of the F1 values of MUC, B-cubed and CEAFe)

Examples:

    >>> coval = datasets.load_metric('coval')
    >>> words = ['bc/cctv/00/cctv_0005   0   0       Thank   VBP  (TOP(S(VP*    thank  01   1    Xu_li  *           (V*)        *       -',
    ... 'bc/cctv/00/cctv_0005   0   1         you   PRP        (NP*)      -    -   -    Xu_li  *        (ARG1*)   (ARG0*)   (116)',
    ... 'bc/cctv/00/cctv_0005   0   2    everyone    NN        (NP*)      -    -   -    Xu_li  *    (ARGM-DIS*)        *    (116)',
    ... 'bc/cctv/00/cctv_0005   0   3         for    IN        (PP*       -    -   -    Xu_li  *        (ARG2*         *       -',
    ... 'bc/cctv/00/cctv_0005   0   4    watching   VBG   (S(VP*))))   watch  01   1    Xu_li  *             *)      (V*)      -',
    ... 'bc/cctv/00/cctv_0005   0   5           .     .          *))      -    -   -    Xu_li  *             *         *       -']
    >>> references = [words]
    >>> predictions = [words]
    >>> results = coval.compute(predictions=predictions, references=references)
    >>> print(results) # doctest:+ELLIPSIS
    {'mentions/recall': 1.0,[...] 'conll_score': 100.0}
"""


def get_coref_infos(
    key_lines, sys_lines, NP_only=False, remove_nested=False, keep_singletons=True, min_span=False, doc="dummy_doc"
):

    key_doc_lines = {doc: key_lines}
    sys_doc_lines = {doc: sys_lines}

    doc_coref_infos = {}

    key_nested_coref_num = 0
    sys_nested_coref_num = 0
    key_removed_nested_clusters = 0
    sys_removed_nested_clusters = 0
    key_singletons_num = 0
    sys_singletons_num = 0

    key_clusters, singletons_num = reader.get_doc_mentions(doc, key_doc_lines[doc], keep_singletons)
    key_singletons_num += singletons_num

    if NP_only or min_span:
        key_clusters = reader.set_annotated_parse_trees(key_clusters, key_doc_lines[doc], NP_only, min_span)

    sys_clusters, singletons_num = reader.get_doc_mentions(doc, sys_doc_lines[doc], keep_singletons)
    sys_singletons_num += singletons_num

    if NP_only or min_span:
        sys_clusters = reader.set_annotated_parse_trees(sys_clusters, key_doc_lines[doc], NP_only, min_span)

    if remove_nested:
        nested_mentions, removed_clusters = reader.remove_nested_coref_mentions(key_clusters, keep_singletons)
        key_nested_coref_num += nested_mentions
        key_removed_nested_clusters += removed_clusters

        nested_mentions, removed_clusters = reader.remove_nested_coref_mentions(sys_clusters, keep_singletons)
        sys_nested_coref_num += nested_mentions
        sys_removed_nested_clusters += removed_clusters

    sys_mention_key_cluster = reader.get_mention_assignments(sys_clusters, key_clusters)
    key_mention_sys_cluster = reader.get_mention_assignments(key_clusters, sys_clusters)

    doc_coref_infos[doc] = (key_clusters, sys_clusters, key_mention_sys_cluster, sys_mention_key_cluster)

    if remove_nested:
        logger.info(
            "Number of removed nested coreferring mentions in the key "
            f"annotation: {key_nested_coref_num}; and system annotation: {sys_nested_coref_num}"
        )
        logger.info(
            "Number of resulting singleton clusters in the key "
            f"annotation: {key_removed_nested_clusters}; and system annotation: {sys_removed_nested_clusters}"
        )

    if not keep_singletons:
        logger.info(
            f"{key_singletons_num:d} and {sys_singletons_num:d} singletons are removed from the key and system "
            "files, respectively"
        )

    return doc_coref_infos


def evaluate(key_lines, sys_lines, metrics, NP_only, remove_nested, keep_singletons, min_span):
    doc_coref_infos = get_coref_infos(key_lines, sys_lines, NP_only, remove_nested, keep_singletons, min_span)

    output_scores = {}
    conll = 0
    conll_subparts_num = 0

    for name, metric in metrics:
        recall, precision, f1 = evaluator.evaluate_documents(doc_coref_infos, metric, beta=1)
        if name in ["muc", "bcub", "ceafe"]:
            conll += f1
            conll_subparts_num += 1
        output_scores.update({f"{name}/recall": recall, f"{name}/precision": precision, f"{name}/f1": f1})

        logger.info(
            name.ljust(10),
            f"Recall: {recall * 100:.2f}",
            f" Precision: {precision * 100:.2f}",
            f" F1: {f1 * 100:.2f}",
        )

    if conll_subparts_num == 3:
        conll = (conll / 3) * 100
        logger.info(f"CoNLL score: {conll:.2f}")
        output_scores.update({"conll_score": conll})

    return output_scores


def check_gold_parse_annotation(key_lines):
    has_gold_parse = False
    for line in key_lines:
        if not line.startswith("#"):
            if len(line.split()) > 6:
                parse_col = line.split()[5]
                if not parse_col == "-":
                    has_gold_parse = True
                    break
                else:
                    break
    return has_gold_parse


@datasets.utils.file_utils.add_start_docstrings(_DESCRIPTION, _KWARGS_DESCRIPTION)
class Coval(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": datasets.Sequence(datasets.Value("string")),
                    "references": datasets.Sequence(datasets.Value("string")),
                }
            ),
            codebase_urls=["https://github.com/ns-moosavi/coval"],
            reference_urls=[
                "https://github.com/ns-moosavi/coval",
                "https://www.aclweb.org/anthology/P16-1060",
                "http://www.conll.cemantix.org/2012/data.html",
            ],
        )

    def _compute(
        self, predictions, references, keep_singletons=True, NP_only=False, min_span=False, remove_nested=False
    ):
        allmetrics = [
            ("mentions", evaluator.mentions),
            ("muc", evaluator.muc),
            ("bcub", evaluator.b_cubed),
            ("ceafe", evaluator.ceafe),
            ("lea", evaluator.lea),
        ]

        if min_span:
            has_gold_parse = util.check_gold_parse_annotation(references)
            if not has_gold_parse:
                raise NotImplementedError("References should have gold parse annotation to use 'min_span'.")
                # util.parse_key_file(key_file)
                # key_file = key_file + ".parsed"

        score = evaluate(
            key_lines=references,
            sys_lines=predictions,
            metrics=allmetrics,
            NP_only=NP_only,
            remove_nested=remove_nested,
            keep_singletons=keep_singletons,
            min_span=min_span,
        )

        return score
