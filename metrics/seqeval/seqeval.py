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
""" seqeval metric. """

from collections import defaultdict

import nlp
from seqeval.metrics import accuracy_score, precision_score, recall_score, f1_score

_CITATION = """\
"""

_DESCRIPTION = """\
seqeval is a Python framework for sequence labeling evaluation.
seqeval can evaluate the performance of chunking tasks such as named-entity recognition, part-of-speech tagging, semantic role labeling and so on.

This is well-tested by using the Perl script conlleval, which can be used for
measuring the performance of a system that has processed the CoNLL-2000 shared task data.

seqeval supports following formats:
IOB1
IOB2
IOE1
IOE2
IOBES

See the [README.md] file at https://github.com/chakki-works/seqeval for more information.
"""

_KWARGS_DESCRIPTION = """
Produces labelling scores along with its sufficient statistics
from a source against one or more references.

Args:
    predictions: List of List of predicted labels (Estimated targets as returned by a tagger)
    references: List of List of reference labels (Ground truth (correct) target values)
    suffix: True if the types are not in IOBs format False otherwise. default: False
Returns:
    Overall:
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': F1 score, also known as balanced F-score or F-measure,
    Per type:
        'precision': precision,
        'recall': recall,
        'f1': F1 score, also known as balanced F-score or F-measure,
"""

def end_of_chunk(prev_tag, tag, prev_type, type_):
    """Checks if a chunk ended between the previous and current word.
    Args:
        prev_tag: previous chunk tag.
        tag: current chunk tag.
        prev_type: previous type.
        type_: current type.
    Returns:
        chunk_end: boolean.
    """
    chunk_end = False

    if (prev_tag in ["B", "I"] and tag in ["B", "S", "O"]) or prev_tag in ["E", "S"]:
        chunk_end = True

    if prev_tag not in ['O', '.'] and prev_type != type_:
        chunk_end = True

    return chunk_end


def start_of_chunk(prev_tag, tag, prev_type, type_):
    """Checks if a chunk started between the previous and current word.
    Args:
        prev_tag: previous chunk tag.
        tag: current chunk tag.
        prev_type: previous type.
        type_: current type.
    Returns:
        chunk_start: boolean.
    """
    chunk_start = False

    if (prev_tag in ["E", "S", "O"] and tag in ["E", "I"]) or tag in ["B", "S"]:
        chunk_start = True

    if tag not in ['O', '.'] and prev_type != type_:
        chunk_start = True

    return chunk_start

def get_entities(seq, suffix=False):
    """Gets entities from sequence.
    Args:
        seq (list): sequence of labels.
    Returns:
        list: list of (chunk_type, chunk_start, chunk_end).
    """
    if any(isinstance(s, list) for s in seq):
        seq = [item for sublist in seq for item in sublist + ['O']]

    prev_tag = 'O'
    prev_type = ''
    begin_offset = 0
    chunks = []
    for i, chunk in enumerate(seq + ['O']):
        if suffix:
            tag = chunk[-1]
            type_ = chunk.split('-')[0]
        else:
            tag = chunk[0]
            type_ = chunk.split('-')[-1]

        if end_of_chunk(prev_tag, tag, prev_type, type_):
            chunks.append((prev_type, begin_offset, i-1))
        if start_of_chunk(prev_tag, tag, prev_type, type_):
            begin_offset = i
        prev_tag = tag
        prev_type = type_

    return chunks

class Seqeval(nlp.Metric):
    def _info(self):
        return nlp.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            homepage="https://github.com/chakki-works/seqeval",
            inputs_description=_KWARGS_DESCRIPTION,
            features=nlp.Features({
                'predictions': nlp.Sequence(nlp.Value('string', id='label'), id='sequence'),
                'references': nlp.Sequence(nlp.Value('string', id='label'), id='sequence'),
            }),
            codebase_urls=["https://github.com/chakki-works/seqeval"],
            reference_urls=["https://github.com/chakki-works/seqeval"]
        )

    def _compute(self, predictions, references, suffix=False):
        true_entities = set(get_entities(references, suffix))
        pred_entities = set(get_entities(predictions, suffix))
        d1 = defaultdict(set)
        d2 = defaultdict(set)
        scores = {}

        for e in true_entities:
            d1[e[0]].add((e[1], e[2]))

        for e in pred_entities:
            d2[e[0]].add((e[1], e[2]))
        
        for type_name, true_entities in d1.items():
            scores[type_name] = {}
            pred_entities = d2[type_name]
            nb_correct = len(true_entities & pred_entities)
            nb_pred = len(pred_entities)
            nb_true = len(true_entities)

            p = nb_correct / nb_pred if nb_pred > 0 else 0
            r = nb_correct / nb_true if nb_true > 0 else 0
            f1 = 2 * p * r / (p + r) if p + r > 0 else 0

            scores[type_name]["precision"] = p
            scores[type_name]["recall"] = r
            scores[type_name]["f1"] = f1
            scores[type_name]["number"] = nb_true

        scores["overall_precision"] = precision_score(y_true=references, y_pred=predictions, suffix=suffix)
        scores["overall_recall"] = recall_score(y_true=references, y_pred=predictions, suffix=suffix)
        scores["overall_f1"] = f1_score(y_true=references, y_pred=predictions, suffix=suffix)
        scores["overall_accuracy"] = accuracy_score(y_true=references, y_pred=predictions)

        return scores
