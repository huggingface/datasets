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
import os

import numpy as np

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
complete analysis of the compositional effects of sentiment in language.
"""

_HOMEPAGE = "https://nlp.stanford.edu/sentiment/"

_LICENSE = ""

_URL = 'https://www.dropbox.com/s/9j9dc55hs28wrye/stanfordSentimentTreebank.zip?dl=1'


class Sst(datasets.GeneratorBasedBuilder):
    """The Stanford Sentiment Treebank"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="sentences", version=VERSION, description="Sentiment labels for complete sentences."
        ),
        datasets.BuilderConfig(
            name="phrases",
            version=VERSION,
            description="Sentiment labels for sentences and their sub-sentences (phrases).",
        ),
        datasets.BuilderConfig(
            name="ptb", version=VERSION, description="Penn-treebank-style labelled trees. Labels are binned in 5 bins."
        ),
    ]

    DEFAULT_CONFIG_NAME = "sentences"

    def _info(self):

        if self.config.name == "sentences":
            features = datasets.Features(
                {
                    "sentence_id": datasets.Value("int64"),
                    "sentence": datasets.Value("string"),
                    "label": datasets.Value("float"),
                    "tokens": datasets.Value("string"),
                    "tree": datasets.Value("string"),
                }
            )
        elif self.config.name == "phrases":
            features = datasets.Features(
                {
                    "sentence_id": datasets.Value("int64"),
                    "phrase": datasets.Value("string"),
                    "label": datasets.Value("float"),
                }
            )
        else:
            features = datasets.Features(
                {
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
        data_dir = dl_manager.download_and_extract(_URL)

        file_paths = {}
        for split_index in range(1, 4):
            file_paths[split_index] = {
                "phrases_path": os.path.join(data_dir, "dictionary.txt"),
                "labels_path": os.path.join(data_dir, "sentiment_labels.txt"),
                "tokens_path": os.path.join(data_dir, "SOStr.txt"),
                "trees_path": os.path.join(data_dir, "STree.txt"),
                "splits_path": os.path.join(data_dir, "datasetSplit.txt"),
                "sentences_path": os.path.join(data_dir, "datasetSentences.txt"),
                "ptb_filepath": None,
                "split_id": str(split_index),
            }

        ptb_file_paths = {}
        for ptb_split in ['train', 'dev', 'test']:
            ptb_file_paths[ptb_split] = {
                "phrases_path": None,
                "labels_path": None,
                "tokens_path": None,
                "trees_path": None,
                "splits_path": None,
                "sentences_path": None,
                "ptb_filepath": os.path.join(data_dir, "ptb_" + ptb_split + ".txt"),
                "split_id": None,  
            }

        if self.config.name == "ptb":
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=ptb_file_paths['train']),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=ptb_file_paths['dev']),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=ptb_file_paths['test']),
            ]
        else:
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=file_paths[1]),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=file_paths[3]),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=file_paths[2]),
            ]

    def _generate_examples(self, phrases_path, labels_path, tokens_path, trees_path, splits_path, sentences_path, split_id, ptb_filepath):

        if self.config.name == "ptb":
            with open(ptb_filepath) as fp:
                ptb_reader = csv.reader(fp, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(ptb_reader):
                    yield id_, {"tree": row[0]}
        else:

            # Store the labels of all possible phrases in a dictionary
            sst = {}
            with open(phrases_path) as f, open(labels_path) as g:
                phrase_reader = csv.reader(f, delimiter="|", quoting=csv.QUOTE_NONE)
                for row in phrase_reader:
                    sst[row[1]] = {}
                    sst[row[1]]["phrase"] = row[0]

                label_reader = csv.DictReader(g, delimiter="|", quoting=csv.QUOTE_NONE)
                for row in label_reader:
                    sst[row["phrase ids"]]["label"] = float(row["sentiment values"])
            sst = {v["phrase"]: v["label"] for (k, v) in sst.items()}

            # Read parse trees for each complete sentence
            trees = {}
            with open(tokens_path) as tok, open(trees_path) as tr:
                tok_reader = csv.reader(tok, delimiter="\t", quoting=csv.QUOTE_NONE)
                tree_reader = csv.reader(tr, delimiter="\t", quoting=csv.QUOTE_NONE)
                for i, row in enumerate(tok_reader, start=1):
                    trees[i] = {}
                    trees[i]["tokens"] = row[0]
                for i, row in enumerate(tree_reader, start=1):
                    trees[i]["tree"] = row[0]

            with open(splits_path) as spl, open(sentences_path) as snt:

                splits_reader = csv.DictReader(spl, delimiter=",", quoting=csv.QUOTE_NONE)
                splits = {row["sentence_index"]: row["splitset_label"] for row in splits_reader}

                sentence_reader = csv.DictReader(snt, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(sentence_reader):
                    if splits[row["sentence_index"]] == split_id:
                        tokens = trees[int(row["sentence_index"])]["tokens"]
                        parse_tree = trees[int(row["sentence_index"])]["tree"]

                        if self.config.name == "sentences":
                            yield id_, {
                                "sentence_id": row["sentence_index"],
                                "sentence": row["sentence"],
                                "label": sst[row["sentence"]],
                                "tokens": tokens,
                                "tree": parse_tree,
                            }

                        else:
                            # Traverse a parse tree to extract every possible phrase in a sentence
                            token_list = np.array(tokens.split("|"))
                            tree_nodes = np.array([int(t) - 1 for t in parse_tree.split("|")])

                            tree = {}
                            root = len(tree_nodes) - 1
                            backstop = 0

                            # Initialize the tree
                            for i, token in enumerate(tree_nodes):
                                tree[i] = {}
                                if i < len(token_list):
                                    tree[i]["text"] = token_list[i]
                                    tree[i]["is_literal"] = True
                                    tree[i]["leftmost"] = i
                                else:
                                    tree[i]["text"] = None
                                    tree[i]["is_literal"] = False
                                    tree[i]["leftmost"] = None

                            # Traverse
                            while tree[root]["is_literal"] is False:
                                backstop += 1
                                for top_node in range(len(tree_nodes) - 1, len(token_list) - 1, -1):
                                    siblings = np.where(tree_nodes == top_node)
                                    left = siblings[0][0]
                                    right = siblings[0][1]
                                    if (tree[left]["is_literal"]) & (tree[right]["is_literal"]):
                                        common_parent = tree[tree_nodes[left]]
                                        if tree[left]["leftmost"] < tree[right]["leftmost"]:
                                            common_parent["text"] = tree[left]["text"] + " " + tree[right]["text"]
                                        else:
                                            common_parent["text"] = tree[right]["text"] + " " + tree[left]["text"]
                                        common_parent["is_literal"] = True
                                        common_parent["leftmost"] = min(
                                            tree[left]["leftmost"], tree[right]["leftmost"]
                                        )
                                        tree[left]["is_literal"] = False
                                        tree[right]["is_literal"] = False
                                if backstop > 1000:
                                    raise (RuntimeError("Couldn't parse the tree."))

                            phrases = [tree[n]["text"] for n in range(len(token_list), len(tree_nodes))]

                            for phrase in phrases:
                                yield id_, {
                                    "sentence_id": row["sentence_index"],
                                    "phrase": phrase,
                                    "label": sst[phrase],
                                }
