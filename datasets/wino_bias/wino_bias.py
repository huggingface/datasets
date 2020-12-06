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
"""WinoBias: Winograd-schema dataset for detecting gender bias"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@article{DBLP:journals/corr/abs-1804-06876,
  author    = {Jieyu Zhao and
               Tianlu Wang and
               Mark Yatskar and
               Vicente Ordonez and
               Kai{-}Wei Chang},
  title     = {Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods},
  journal   = {CoRR},
  volume    = {abs/1804.06876},
  year      = {2018},
  url       = {http://arxiv.org/abs/1804.06876},
  archivePrefix = {arXiv},
  eprint    = {1804.06876},
  timestamp = {Mon, 13 Aug 2018 16:47:01 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1804-06876.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
WinoBias, a Winograd-schema dataset for coreference resolution focused on gender bias. 
The corpus contains Winograd-schema style sentences with entities corresponding to people
referred by their occupation (e.g. the nurse, the doctor, the carpenter).
"""

_HOMEPAGE = "https://uclanlp.github.io/corefBias/overview"

_LICENSE = "MIT License (https://github.com/uclanlp/corefBias/blob/master/LICENSE)"

_URL = {
    "https://drive.google.com/uc?export=download&confirm=yLNb&id=14Im3BnNl-d2fYETYmiH5yq6eFGLVC3g0"
}


class WinoBias(datasets.GeneratorBasedBuilder):
    """WinoBias: Winograd-schema dataset for detecting gender bias"""

    VERSION = datasets.Version("4.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="wino_bias", version=VERSION, description="WinoBias: Winograd-schema dataset for detecting gender bias"),
    ]


    def _info(self):
        
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            # Info about features for this: http://cemantix.org/data/ontonotes.html
            features= datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "part_number": datasets.Value("int64"),
                    "word_number": datasets.Sequence(datasets.Value("int64")),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                '"',
                                "''",
                                "#",
                                "$",
                                "(",
                                ")",
                                ",",
                                ".",
                                ":",
                                "``",
                                "CC",
                                "CD",
                                "DT",
                                "EX",
                                "FW",
                                "IN",
                                "JJ",
                                "JJR",
                                "JJS",
                                "LS",
                                "MD",
                                "NN",
                                "NNP",
                                "NNPS",
                                "NNS",
                                "NN|SYM",
                                "PDT",
                                "POS",
                                "PRP",
                                "PRP$",
                                "RB",
                                "RBR",
                                "RBS",
                                "RP",
                                "SYM",
                                "TO",
                                "UH",
                                "VB",
                                "VBD",
                                "VBG",
                                "VBN",
                                "VBP",
                                "VBZ",
                                "WDT",
                                "WP",
                                "WP$",
                                "WRB",
                            ]
                        )
                    ),
                    "parse_bit": datasets.Sequence(datasets.Value("string")),
                    "predicate_lemma": datasets.Sequence(datasets.Value("string")),
                    "predicate_framenet_id": datasets.Sequence(datasets.Value("int32")),
                    "word_sense": datasets.Sequence(datasets.Value("float32")),
                    "speaker": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "PERSON",
                                "NORP",
                                "FAC",
                                "ORG",
                                "GPE",
                                "LOC",
                                "PRODUCT",
                                "EVENT",
                                "WORK_OF_ART",
                                "LAW",
                                "LANGUAGE",
                                "DATE",
                                "TIME",
                                "PERCENT",
                                "MONEY",
                                "QUANTITY",
                                "ORDINAL",
                                "CARDINAL"
                            ]
                        )
                    ),
                    "verbal_predicates": datasets.Sequence(datasets.Value("string"))
                }
            )
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
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "anonymized.augmented.train.english.v4_auto_conll")
                },
            )
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open("../anonymized.augmented.train.english.v4_auto_conll", encoding="utf-8") as f:
            _id = 0
            document_id = 0
            part_number = 0
            word_num = []
            tokens = []
            pos_tags = []
            parse_bit = []
            predicate_lemma = []
            predicate_framenet_id = []
            word_sense = []
            speaker = []
            ner_tags = []
            verbal_predicates = []
            for line in f:
                if line.startswith("#begin") or line.startswith("#end"): 
                    continue;
                elif line == "" or line == "\n":  
                    id_ += 1
                    yield id_, {
                        "document_id": document_id,
                        "part_number": part_number,
                        "word_number": word_num,
                        "tokens": tokens,
                        "pos_tags": pos_tags,
                        "parse_bit": parse_bit,
                        "predicate_lemma": predicate_lemma,
                        "predicate_framenet_id": predicate_framenet_id,
                        "word_sense": word_sense,
                        "speaker": speaker,
                        "ner_tags": ner_tags,
                        "verbal_predicates": verbal_predicates
                    }
                    word_num = []
                    tokens = []
                    pos_tags = []
                    parse_bit = []
                    predicate_lemma = []
                    predicate_framenet_id = []
                    word_sense = []
                    speaker = []
                    ner_tags = []
                    verbal_predicates = []
                else:
                    splits = line.split(" ")
                    document_id = splits[0]
                    part_number = splits[1]
                    word_num.append(splits[2])
                    tokens.append(splits[3])
                    pos_tags.append(splits[4])
                    parse_bit.append(splits[5])
                    predicate_lemma.append(splits[6])
                    predicate_framenet_id.append(splits[7])
                    word_sense.append(splits[8])
                    speaker.append(splits[9])
                    ner_tags.append(splits[10])
                    verbal_predicates.append(splits[11:])
