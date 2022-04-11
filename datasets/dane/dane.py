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
"""DaNE: named entity annotation for the Danish Universal Dependencies
treebank using the CoNLL-2003 annotation scheme."""


import os

import datasets


_CITATION = """\
@inproceedings{hvingelby-etal-2020-dane,
    title = "{D}a{NE}: A Named Entity Resource for {D}anish",
    author = "Hvingelby, Rasmus  and
      Pauli, Amalie Brogaard  and
      Barrett, Maria  and
      Rosted, Christina  and
      Lidegaard, Lasse Malm  and
      Søgaard, Anders",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.565",
    pages = "4597--4604",
    abstract = "We present a named entity annotation for the Danish Universal Dependencies treebank using the CoNLL-2003 annotation scheme: DaNE. It is the largest publicly available, Danish named entity gold annotation. We evaluate the quality of our annotations intrinsically by double annotating the entire treebank and extrinsically by comparing our annotations to a recently released named entity annotation of the validation and test sections of the Danish Universal Dependencies treebank. We benchmark the new resource by training and evaluating competitive architectures for supervised named entity recognition (NER), including FLAIR, monolingual (Danish) BERT and multilingual BERT. We explore cross-lingual transfer in multilingual BERT from five related languages in zero-shot and direct transfer setups, and we show that even with our modestly-sized training set, we improve Danish NER over a recent cross-lingual approach, as well as over zero-shot transfer from five related languages. Using multilingual BERT, we achieve higher performance by fine-tuning on both DaNE and a larger Bokm{\aa}l (Norwegian) training set compared to only using DaNE. However, the highest performance isachieved by using a Danish BERT fine-tuned on DaNE. Our dataset enables improvements and applicability for Danish NER beyond cross-lingual methods. We employ a thorough error analysis of the predictions of the best models for seen and unseen entities, as well as their robustness on un-capitalized text. The annotated dataset and all the trained models are made publicly available.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

_DESCRIPTION = """\
The DaNE dataset has been annotated with Named Entities for PER, ORG and LOC
by the Alexandra Institute.
It is a reannotation of the UD-DDT (Universal Dependency - Danish Dependency Treebank)
which has annotations for dependency parsing and part-of-speech (POS) tagging.
The Danish UD treebank (Johannsen et al., 2015, UD-DDT) is a conversion of
the Danish Dependency Treebank (Buch-Kromann et al. 2003) based on texts
from Parole (Britt, 1998).
"""

_HOMEPAGE = "https://github.com/alexandrainst/danlp/blob/master/docs/docs/datasets.md#dane"

_LICENSE = "CC BY-SA 4.0"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "http://danlp-downloads.alexandra.dk/datasets/ddt.zip"


class Dane(datasets.GeneratorBasedBuilder):
    """DaNE dataset"""

    def _info(self):
        features = datasets.Features(
            {
                "sent_id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "tok_ids": datasets.Sequence(datasets.Value("int64")),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "lemmas": datasets.Sequence(datasets.Value("string")),
                "pos_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "NUM",
                            "CCONJ",
                            "PRON",
                            "VERB",
                            "INTJ",
                            "AUX",
                            "ADJ",
                            "PROPN",
                            "PART",
                            "ADV",
                            "PUNCT",
                            "ADP",
                            "NOUN",
                            "X",
                            "DET",
                            "SYM",
                            "SCONJ",
                        ]
                    )
                ),
                "morph_tags": datasets.Sequence(datasets.Value("string")),
                "dep_ids": datasets.Sequence(datasets.Value("int64")),
                "dep_labels": datasets.Sequence(
                    datasets.ClassLabel(
                        names=[
                            "parataxis",
                            "mark",
                            "nummod",
                            "discourse",
                            "compound:prt",
                            "reparandum",
                            "vocative",
                            "list",
                            "obj",
                            "dep",
                            "det",
                            "obl:loc",
                            "flat",
                            "iobj",
                            "cop",
                            "expl",
                            "obl",
                            "conj",
                            "nmod",
                            "root",
                            "acl:relcl",
                            "goeswith",
                            "appos",
                            "fixed",
                            "obl:tmod",
                            "xcomp",
                            "advmod",
                            "nmod:poss",
                            "aux",
                            "ccomp",
                            "amod",
                            "cc",
                            "advcl",
                            "nsubj",
                            "punct",
                            "case",
                        ]
                    )
                ),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "O",
                            "B-PER",
                            "I-PER",
                            "B-ORG",
                            "I-ORG",
                            "B-LOC",
                            "I-LOC",
                            "B-MISC",
                            "I-MISC",
                        ]
                    )
                ),
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "ddt.train.conllu"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "ddt.test.conllu"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "ddt.dev.conllu"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            guid = 0
            sent_id = ""
            text = ""
            tok_ids = []
            tokens = []
            lemmas = []
            pos_tags = []
            morph_tags = []
            dephead_ids = []
            dep_labels = []
            ner_tags = []
            for line in f:
                if line.startswith("#"):
                    var, val = line.split(" = ", maxsplit=1)
                    var = var.replace("# ", "")
                    if var == "sent_id":
                        sent_id = val
                    elif var == "text":
                        text = val
                elif line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "sent_id": sent_id,
                            "text": text,
                            "tok_ids": tok_ids,
                            "tokens": tokens,
                            "lemmas": lemmas,
                            "pos_tags": pos_tags,
                            "morph_tags": morph_tags,
                            "dep_ids": dephead_ids,
                            "dep_labels": dep_labels,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        sent_id = ""
                        text = ""
                        tok_ids = []
                        tokens = []
                        lemmas = []
                        pos_tags = []
                        morph_tags = []
                        dephead_ids = []
                        dep_labels = []
                        ner_tags = []
                else:
                    # conllu tokens tab space separated
                    splits = line.split("\t")
                    tok_ids.append(int(splits[0]))
                    tokens.append(splits[1])
                    lemmas.append(splits[2])
                    pos_tags.append(splits[3])
                    morph_tags.append(splits[5])
                    dephead_ids.append(splits[6])
                    dep_labels.append(splits[7])
                    ner_tags.append(splits[9].rstrip().replace("name=", "").split("|")[0])
            # last example
            if tok_ids:
                yield guid, {
                    "sent_id": sent_id,
                    "text": text,
                    "tok_ids": tok_ids,
                    "tokens": tokens,
                    "lemmas": lemmas,
                    "pos_tags": pos_tags,
                    "morph_tags": morph_tags,
                    "dep_ids": dephead_ids,
                    "dep_labels": dep_labels,
                    "ner_tags": ner_tags,
                }
