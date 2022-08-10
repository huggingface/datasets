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


import collections

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

_URL = "https://raw.githubusercontent.com/uclanlp/corefBias/master/WinoBias/wino/data/conll_format"


class WinoBiasConfig(datasets.BuilderConfig):
    def __init__(self, **kwargs):
        super(WinoBiasConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class WinoBias(datasets.GeneratorBasedBuilder):
    """WinoBias: Winograd-schema dataset for detecting gender bias"""

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    def __init__(self, *args, writer_batch_size=None, **kwargs):
        super(WinoBias, self).__init__(*args, **kwargs)
        # Batch size used by the ArrowWriter
        # It defines the number of samples that are kept in memory before writing them
        # and also the length of the arrow chunks
        # None means that the ArrowWriter will use its default value
        self._writer_batch_size = writer_batch_size or 100

    BUILDER_CONFIGS = [
        WinoBiasConfig(
            name="type1_pro",
            description="winoBias type1_pro_stereotype data in cornll format",
        ),
        WinoBiasConfig(
            name="type1_anti",
            description="winoBias type1_anti_stereotype data in cornll format",
        ),
        WinoBiasConfig(
            name="type2_pro",
            description="winoBias type2_pro_stereotype data in cornll format",
        ),
        WinoBiasConfig(
            name="type2_anti",
            description="winoBias type2_anti_stereotype data in cornll format",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            # Info about features for this: http://cemantix.org/data/ontonotes.html
            features=datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "part_number": datasets.Value("string"),
                    "word_number": datasets.Sequence(datasets.Value("int32")),
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
                                "HYPH",
                                "XX",
                                "NFP",
                                "AFX",
                                "ADD",
                                "-LRB-",
                                "-RRB-",
                                "-",
                            ]
                        )
                    ),
                    "parse_bit": datasets.Sequence(datasets.Value("string")),
                    "predicate_lemma": datasets.Sequence(datasets.Value("string")),
                    "predicate_framenet_id": datasets.Sequence(datasets.Value("string")),
                    "word_sense": datasets.Sequence(datasets.Value("string")),
                    "speaker": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-PERSON",
                                "I-PERSON",
                                "B-NORP",
                                "I-NORP",
                                "B-FAC",
                                "I-FAC",
                                "B-ORG",
                                "I-ORG",
                                "B-GPE",
                                "I-GPE",
                                "B-LOC",
                                "I-LOC",
                                "B-PRODUCT",
                                "I-PRODUCT",
                                "B-EVENT",
                                "I-EVENT",
                                "B-WORK_OF_ART",
                                "I-WORK_OF_ART",
                                "B-LAW",
                                "I-LAW",
                                "B-LANGUAGE",
                                "I-LANGUAGE",
                                "B-DATE",
                                "I-DATE",
                                "B-TIME",
                                "I-TIME",
                                "B-PERCENT",
                                "I-PERCENT",
                                "B-MONEY",
                                "I-MONEY",
                                "B-QUANTITY",
                                "I-QUANTITY",
                                "B-ORDINAL",
                                "I-ORDINAL",
                                "B-CARDINAL",
                                "I-CARDINAL",
                                "*",
                                "0",
                                "-",
                            ]
                        )
                    ),
                    "verbal_predicates": datasets.Sequence(datasets.Value("string")),
                    "coreference_clusters": datasets.Sequence(datasets.Value("string")),
                }
            ),
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

        dev_data_dir = dl_manager.download(_URL + "/dev_" + self.config.name + "_stereotype.v4_auto_conll")
        test_data_dir = dl_manager.download(_URL + "/test_" + self.config.name + "_stereotype.v4_auto_conll")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dev_data_dir},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": test_data_dir},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            id_ = 0
            document_id = None
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
            ner_start = False
            verbal_predicates = []
            coreference = []
            clusters = collections.defaultdict(list)
            coref_stacks = collections.defaultdict(list)
            for line in f:
                if line.startswith("#begin") or line.startswith("#end"):
                    continue
                elif not line.strip():
                    id_ += 1
                    yield str(id_), {
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
                        "verbal_predicates": verbal_predicates,
                        "coreference_clusters": sum(
                            clusters[1], []
                        ),  # flatten the list as writing the exmaples needs an array.
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
                    coreference = []
                    clusters = collections.defaultdict(list)
                    coref_stacks = collections.defaultdict(list)
                else:
                    splits = [s for s in line.split() if s]
                    if len(splits) > 7:
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
                        ner_word = splits[10]
                        coreference = splits[-1]
                        if ")" in ner_word and ner_start:
                            ner_start = False
                            ner_word = "0"
                        if "(" in ner_word:
                            ner_start = True
                            ner_word = ner_word.strip(" ").replace("(", "B-").replace("*", "").replace(")", "")
                            start_word = ner_word.strip(" ").replace("B-", "")
                        if ner_start:
                            if ner_word.strip(" ") == "*":
                                ner_word = "I-" + start_word
                        ner_tags.append(ner_word)
                        word_is_verbal_predicate = any(["(V" in x for x in splits[11:-1]])
                        if word_is_verbal_predicate:
                            verbal_predicates.append(splits[3])
                        if coreference != "-":
                            for segment in coreference.split("|"):
                                if segment[0] == "(":
                                    if segment[-1] == ")":
                                        cluster_id = int(segment[1:-1])
                                        clusters[cluster_id].append([splits[2], splits[2]])
                                    else:
                                        cluster_id = int(segment[1:])
                                        coref_stacks[cluster_id].append(splits[2])
                                else:
                                    cluster_id = int(segment[:-1])
                                    start = coref_stacks[cluster_id].pop()
                                    clusters[cluster_id].append([start, splits[2]])

            if tokens:
                # add the last one
                id_ += 1
                yield str(id_), {
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
                    "verbal_predicates": verbal_predicates,
                    "coreference_clusters": sum(clusters[1], []),
                }
