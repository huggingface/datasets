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
"""TODO: Add a description here."""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@inproceedings{socher-etal-2013-recursive,
    title = "Recursive Deep Models for Semantic Compositionality Over a Sentiment Treebank",
    author = "Socher, Richard and Perelygin, Alex and Wu, Jean and
      Chuang, Jason and Manning, Christopher D. and Ng, Andrew and Potts, Christopher",
    booktitle = "Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing",
    month = oct,
    year = "2013",
    address = "Seattle, Washington, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D13-1170",
    pages = "1631--1642",
}
"""

_DESCRIPTION = """\
The Stanford Sentiment Treebank, the first corpus with fully labeled parse trees that allows for a
complete analysis of the compositional effects of sentiment in language. In this version we include
only sentences and sub-sentences with their sentiment labels. Parse trees are not included.
"""

_HOMEPAGE = "https://nlp.stanford.edu/sentiment/"

_LICENSE = ""

_URL = 'https://www.dropbox.com/s/4xlyud4l5mllom0/stanfordSentimentTreebank.zip?dl=1'


class SstPhrases(datasets.GeneratorBasedBuilder):
    """The Stanford Sentiment Treebank"""

    def _info(self):

        features = datasets.Features(
            {
                "phrase": datasets.Value("string"),
                "label": datasets.Value("float"),
                "tokens": datasets.Value("string"),
                "tree": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "phrases_path" : os.path.join(data_dir, "dictionary.txt"),
                    "labels_path" : os.path.join(data_dir, "sentiment_labels.txt"),
                    "splits_path" : os.path.join(data_dir, "datasetSplit.txt"),
                    "sentences_path" : os.path.join(data_dir, "datasetSentences.txt"),
                    "tokens_path": os.path.join(data_dir, "SOStr.txt"),
                    "trees_path": os.path.join(data_dir, "STree.txt"),
                    "split_id" : '1',
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "phrases_path": os.path.join(data_dir, "dictionary.txt"),
                    "labels_path" : os.path.join(data_dir, "sentiment_labels.txt"),
                    "splits_path" : os.path.join(data_dir, "datasetSplit.txt"),
                    "sentences_path" : os.path.join(data_dir, "datasetSentences.txt"),
                    "tokens_path": os.path.join(data_dir, "SOStr.txt"),
                    "trees_path": os.path.join(data_dir, "STree.txt"),
                    "split_id" : '3',
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "phrases_path": os.path.join(data_dir, "dictionary.txt"),
                    "labels_path" : os.path.join(data_dir, "sentiment_labels.txt"),
                    "splits_path" : os.path.join(data_dir, "datasetSplit.txt"),
                    "sentences_path" : os.path.join(data_dir, "datasetSentences.txt"),
                    "tokens_path": os.path.join(data_dir, "SOStr.txt"),
                    "trees_path": os.path.join(data_dir, "STree.txt"),
                    "split_id" : '2',
                },
            ),
            datasets.SplitGenerator(
                name='dictionary',
                gen_kwargs={
                    "phrases_path": os.path.join(data_dir, "dictionary.txt"),
                    "labels_path" : os.path.join(data_dir, "sentiment_labels.txt"),
                    "splits_path" : os.path.join(data_dir, "datasetSplit.txt"),
                    "sentences_path" : os.path.join(data_dir, "datasetSentences.txt"),
                    "tokens_path": os.path.join(data_dir, "SOStr.txt"),
                    "trees_path": os.path.join(data_dir, "STree.txt"),
                    "split_id" : '0',
                },
            ),
        ]

    def _generate_examples(self, phrases_path, labels_path, splits_path, sentences_path, tokens_path, trees_path, split_id):
        """ Yields examples. """
        # Create a dictionary with all sentences, sub-sentences and their labels
        sst = {}
        with open(phrases_path) as f, open(labels_path) as g:
            phrase_reader = csv.reader(f, delimiter='|', quoting=csv.QUOTE_NONE)
            for row in phrase_reader:
                sst[row[1]] = {}
                sst[row[1]]['phrase'] = row[0]
                
            label_reader = csv.DictReader(g, delimiter="|", quoting=csv.QUOTE_NONE)
            for row in label_reader:
                sst[row['phrase ids']]['label'] = float(row['sentiment values'])

        sst = {v['phrase']:v['label'] for (k, v) in sst.items()}

        # Return it if split='dictionary' in load_dataset()
        if split_id == '0':
            for id_, (phrase, label) in enumerate(sst.items()):
                yield id_, {
                    'phrase': phrase,
                    'label': label,
                    'tokens': None,
                    'tree' : None
                }
        # Else return only the whole sentences with their parse trees and labels.
        else:
            # Parse trees for each whole sentence
            trees = {}
            with open(tokens_path) as tok, open(trees_path) as tr:
                tok_reader = csv. reader(tok, delimiter='\t', quoting=csv.QUOTE_NONE)
                tree_reader = csv.reader(tr, delimiter='\t', quoting=csv.QUOTE_NONE)
                for i, row in enumerate(tok_reader, start=1):
                    trees[i] = {}
                    trees[i]['tokens'] = row[0]
                for i, row in enumerate(tree_reader, start=1):
                    trees[i]['tree'] = row[0]

            # The mapping from sentence_index to split_id is given in the 'splits_path' file
            with open(splits_path) as spl, open(sentences_path) as snt:

                splits_reader = csv.DictReader(spl, delimiter=",", quoting=csv.QUOTE_NONE)
                splits = {row['sentence_index']: row['splitset_label'] for row in splits_reader}

                sentence_reader = csv.DictReader(snt, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(sentence_reader):
                    if splits[row['sentence_index']] == split_id:
                        yield id_, {
                            'phrase': row['sentence'],
                            'label' : sst[row['sentence']],
                            'tokens': trees[int(row['sentence_index'])]['tokens'],
                            'tree': trees[int(row['sentence_index'])]['tree'],
                        }
