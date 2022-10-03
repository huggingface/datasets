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
"""CoNLL2012 shared task data based on OntoNotes 5.0"""

import glob
import os
from collections import defaultdict
from typing import DefaultDict, Iterator, List, Optional, Tuple

import datasets


_CITATION = """\
@inproceedings{pradhan-etal-2013-towards,
    title = "Towards Robust Linguistic Analysis using {O}nto{N}otes",
    author = {Pradhan, Sameer  and
      Moschitti, Alessandro  and
      Xue, Nianwen  and
      Ng, Hwee Tou  and
      Bj{\"o}rkelund, Anders  and
      Uryupina, Olga  and
      Zhang, Yuchen  and
      Zhong, Zhi},
    booktitle = "Proceedings of the Seventeenth Conference on Computational Natural Language Learning",
    month = aug,
    year = "2013",
    address = "Sofia, Bulgaria",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/W13-3516",
    pages = "143--152",
}

Ralph Weischedel, Martha Palmer, Mitchell Marcus, Eduard Hovy, Sameer Pradhan, \
Lance Ramshaw, Nianwen Xue, Ann Taylor, Jeff Kaufman, Michelle Franchini, \
Mohammed El-Bachouti, Robert Belvin, Ann Houston. \
OntoNotes Release 5.0 LDC2013T19. \
Web Download. Philadelphia: Linguistic Data Consortium, 2013.
"""

_DESCRIPTION = """\
OntoNotes v5.0 is the final version of OntoNotes corpus, and is a large-scale, multi-genre,
multilingual corpus manually annotated with syntactic, semantic and discourse information.

This dataset is the version of OntoNotes v5.0 extended and is used in the CoNLL-2012 shared task.
It includes v4 train/dev and v9 test data for English/Chinese/Arabic and corrected version v12 train/dev/test data (English only).

The source of data is the Mendeley Data repo [ontonotes-conll2012](https://data.mendeley.com/datasets/zmycy7t9h9), which seems to be as the same as the official data, but users should use this dataset on their own responsibility.

See also summaries from paperwithcode, [OntoNotes 5.0](https://paperswithcode.com/dataset/ontonotes-5-0) and [CoNLL-2012](https://paperswithcode.com/dataset/conll-2012-1)

For more detailed info of the dataset like annotation, tag set, etc., you can refer to the documents in the Mendeley repo mentioned above.
"""

_URL = "https://data.mendeley.com/public-files/datasets/zmycy7t9h9/files/b078e1c4-f7a4-4427-be7f-9389967831ef/file_downloaded"


class Conll2012Ontonotesv5Config(datasets.BuilderConfig):
    """BuilderConfig for the CoNLL formatted OntoNotes dataset."""

    def __init__(self, language=None, conll_version=None, **kwargs):
        """BuilderConfig for the CoNLL formatted OntoNotes dataset.

        Args:
          language: string, one of the language {"english", "chinese", "arabic"} .
          conll_version: string, "v4" or "v12". Note there is only English v12.
          **kwargs: keyword arguments forwarded to super.
        """
        assert language in ["english", "chinese", "arabic"]
        assert conll_version in ["v4", "v12"]
        if conll_version == "v12":
            assert language == "english"
        super(Conll2012Ontonotesv5Config, self).__init__(
            name=f"{language}_{conll_version}",
            description=f"{conll_version} of CoNLL formatted OntoNotes dataset for {language}.",
            version=datasets.Version("1.0.0"),  # hf dataset script version
            **kwargs,
        )
        self.language = language
        self.conll_version = conll_version


class Conll2012Ontonotesv5(datasets.GeneratorBasedBuilder):
    """The CoNLL formatted OntoNotes dataset."""

    BUILDER_CONFIGS = [
        Conll2012Ontonotesv5Config(
            language=lang,
            conll_version="v4",
        )
        for lang in ["english", "chinese", "arabic"]
    ] + [
        Conll2012Ontonotesv5Config(
            language="english",
            conll_version="v12",
        )
    ]

    def _info(self):
        lang = self.config.language
        conll_version = self.config.conll_version
        if lang == "arabic":
            pos_tag_feature = datasets.Value("string")
        else:
            tag_set = _POS_TAGS[f"{lang}_{conll_version}"]
            pos_tag_feature = datasets.ClassLabel(num_classes=len(tag_set), names=tag_set)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "sentences": [
                        {
                            "part_id": datasets.Value("int32"),
                            "words": datasets.Sequence(datasets.Value("string")),
                            "pos_tags": datasets.Sequence(pos_tag_feature),
                            "parse_tree": datasets.Value("string"),
                            "predicate_lemmas": datasets.Sequence(datasets.Value("string")),
                            "predicate_framenet_ids": datasets.Sequence(datasets.Value("string")),
                            "word_senses": datasets.Sequence(datasets.Value("float32")),
                            "speaker": datasets.Value("string"),
                            "named_entities": datasets.Sequence(
                                datasets.ClassLabel(num_classes=37, names=_NAMED_ENTITY_TAGS)
                            ),
                            "srl_frames": [
                                {
                                    "verb": datasets.Value("string"),
                                    "frames": datasets.Sequence(datasets.Value("string")),
                                }
                            ],
                            "coref_spans": datasets.Sequence(datasets.Sequence(datasets.Value("int32"), length=3)),
                        }
                    ],
                }
            ),
            homepage="https://conll.cemantix.org/2012/introduction.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        lang = self.config.language
        conll_version = self.config.conll_version
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, f"conll-2012/{conll_version}/data")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"conll_files_directory": os.path.join(data_dir, f"train/data/{lang}")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"conll_files_directory": os.path.join(data_dir, f"development/data/{lang}")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"conll_files_directory": os.path.join(data_dir, f"test/data/{lang}")},
            ),
        ]

    def _generate_examples(self, conll_files_directory):
        conll_files = sorted(glob.glob(os.path.join(conll_files_directory, "**/*gold_conll"), recursive=True))
        for idx, conll_file in enumerate(conll_files):
            sentences = []
            for sent in Ontonotes().sentence_iterator(conll_file):
                document_id = sent.document_id
                sentences.append(
                    {
                        "part_id": sent.sentence_id,  # should be part id, according to https://conll.cemantix.org/2012/data.html
                        "words": sent.words,
                        "pos_tags": sent.pos_tags,
                        "parse_tree": sent.parse_tree,
                        "predicate_lemmas": sent.predicate_lemmas,
                        "predicate_framenet_ids": sent.predicate_framenet_ids,
                        "word_senses": sent.word_senses,
                        "speaker": sent.speakers[0],
                        "named_entities": sent.named_entities,
                        "srl_frames": [{"verb": f[0], "frames": f[1]} for f in sent.srl_frames],
                        "coref_spans": [(c[0], *c[1]) for c in sent.coref_spans],
                    }
                )
            yield idx, {"document_id": document_id, "sentences": sentences}


# --------------------------------------------------------------------------------------------------------
# Tag set
_NAMED_ENTITY_TAGS = [
    "O",  # out of named entity
    "B-PERSON",
    "I-PERSON",
    "B-NORP",
    "I-NORP",
    "B-FAC",  # FACILITY
    "I-FAC",
    "B-ORG",  # ORGANIZATION
    "I-ORG",
    "B-GPE",
    "I-GPE",
    "B-LOC",
    "I-LOC",
    "B-PRODUCT",
    "I-PRODUCT",
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
    "B-EVENT",
    "I-EVENT",
    "B-WORK_OF_ART",
    "I-WORK_OF_ART",
    "B-LAW",
    "I-LAW",
    "B-LANGUAGE",
    "I-LANGUAGE",
]

_POS_TAGS = {
    "english_v4": [
        "XX",  # missing
        "``",
        "$",
        "''",
        ",",
        "-LRB-",  # (
        "-RRB-",  # )
        ".",
        ":",
        "ADD",
        "AFX",
        "CC",
        "CD",
        "DT",
        "EX",
        "FW",
        "HYPH",
        "IN",
        "JJ",
        "JJR",
        "JJS",
        "LS",
        "MD",
        "NFP",
        "NN",
        "NNP",
        "NNPS",
        "NNS",
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
    ],  # 49
    "english_v12": [
        "XX",  # misssing
        "``",
        "$",
        "''",
        "*",
        ",",
        "-LRB-",  # (
        "-RRB-",  # )
        ".",
        ":",
        "ADD",
        "AFX",
        "CC",
        "CD",
        "DT",
        "EX",
        "FW",
        "HYPH",
        "IN",
        "JJ",
        "JJR",
        "JJS",
        "LS",
        "MD",
        "NFP",
        "NN",
        "NNP",
        "NNPS",
        "NNS",
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
        "VERB",
        "WDT",
        "WP",
        "WP$",
        "WRB",
    ],  # 51
    "chinese_v4": [
        "X",  # missing
        "AD",
        "AS",
        "BA",
        "CC",
        "CD",
        "CS",
        "DEC",
        "DEG",
        "DER",
        "DEV",
        "DT",
        "ETC",
        "FW",
        "IJ",
        "INF",
        "JJ",
        "LB",
        "LC",
        "M",
        "MSP",
        "NN",
        "NR",
        "NT",
        "OD",
        "ON",
        "P",
        "PN",
        "PU",
        "SB",
        "SP",
        "URL",
        "VA",
        "VC",
        "VE",
        "VV",
    ],  # 36
}

# --------------------------------------------------------------------------------------------------------
# The CoNLL(2012) file reader
# Modified the original code to get rid of extra package dependency.
# Original code: https://github.com/allenai/allennlp-models/blob/main/allennlp_models/common/ontonotes.py


class OntonotesSentence:
    """
    A class representing the annotations available for a single CONLL formatted sentence.
    # Parameters
    document_id : `str`
        This is a variation on the document filename
    sentence_id : `int`
        The integer ID of the sentence within a document.
    words : `List[str]`
        This is the tokens as segmented/tokenized in the bank.
    pos_tags : `List[str]`
        This is the Penn-Treebank-style part of speech. When parse information is missing,
        all parts of speech except the one for which there is some sense or proposition
        annotation are marked with a XX tag. The verb is marked with just a VERB tag.
    parse_tree : `nltk.Tree`
        An nltk Tree representing the parse. It includes POS tags as pre-terminal nodes.
        When the parse information is missing, the parse will be `None`.
    predicate_lemmas : `List[Optional[str]]`
        The predicate lemma of the words for which we have semantic role
        information or word sense information. All other indices are `None`.
    predicate_framenet_ids : `List[Optional[int]]`
        The PropBank frameset ID of the lemmas in `predicate_lemmas`, or `None`.
    word_senses : `List[Optional[float]]`
        The word senses for the words in the sentence, or `None`. These are floats
        because the word sense can have values after the decimal, like `1.1`.
    speakers : `List[Optional[str]]`
        The speaker information for the words in the sentence, if present, or `None`
        This is the speaker or author name where available. Mostly in Broadcast Conversation
        and Web Log data. When not available the rows are marked with an "-".
    named_entities : `List[str]`
        The BIO tags for named entities in the sentence.
    srl_frames : `List[Tuple[str, List[str]]]`
        A dictionary keyed by the verb in the sentence for the given
        Propbank frame labels, in a BIO format.
    coref_spans : `Set[TypedSpan]`
        The spans for entity mentions involved in coreference resolution within the sentence.
        Each element is a tuple composed of (cluster_id, (start_index, end_index)). Indices
        are `inclusive`.
    """

    def __init__(
        self,
        document_id: str,
        sentence_id: int,
        words: List[str],
        pos_tags: List[str],
        parse_tree: Optional[str],
        predicate_lemmas: List[Optional[str]],
        predicate_framenet_ids: List[Optional[str]],
        word_senses: List[Optional[float]],
        speakers: List[Optional[str]],
        named_entities: List[str],
        srl_frames: List[Tuple[str, List[str]]],
        coref_spans,
    ) -> None:

        self.document_id = document_id
        self.sentence_id = sentence_id
        self.words = words
        self.pos_tags = pos_tags
        self.parse_tree = parse_tree
        self.predicate_lemmas = predicate_lemmas
        self.predicate_framenet_ids = predicate_framenet_ids
        self.word_senses = word_senses
        self.speakers = speakers
        self.named_entities = named_entities
        self.srl_frames = srl_frames
        self.coref_spans = coref_spans


class Ontonotes:
    """
    This `DatasetReader` is designed to read in the English OntoNotes v5.0 data
    in the format used by the CoNLL 2011/2012 shared tasks. In order to use this
    Reader, you must follow the instructions provided [here (v12 release):]
    (https://cemantix.org/data/ontonotes.html), which will allow you to download
    the CoNLL style annotations for the  OntoNotes v5.0 release -- LDC2013T19.tgz
    obtained from LDC.
    Once you have run the scripts on the extracted data, you will have a folder
    structured as follows:
    ```
    conll-formatted-ontonotes-5.0/
     ── data
       ├── development
           └── data
               └── english
                   └── annotations
                       ├── bc
                       ├── bn
                       ├── mz
                       ├── nw
                       ├── pt
                       ├── tc
                       └── wb
       ├── test
           └── data
               └── english
                   └── annotations
                       ├── bc
                       ├── bn
                       ├── mz
                       ├── nw
                       ├── pt
                       ├── tc
                       └── wb
       └── train
           └── data
               └── english
                   └── annotations
                       ├── bc
                       ├── bn
                       ├── mz
                       ├── nw
                       ├── pt
                       ├── tc
                       └── wb
    ```
    The file path provided to this class can then be any of the train, test or development
    directories(or the top level data directory, if you are not utilizing the splits).
    The data has the following format, ordered by column.
    1.  Document ID : `str`
        This is a variation on the document filename
    2.  Part number : `int`
        Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
    3.  Word number : `int`
        This is the word index of the word in that sentence.
    4.  Word : `str`
        This is the token as segmented/tokenized in the Treebank. Initially the `*_skel` file
        contain the placeholder [WORD] which gets replaced by the actual token from the
        Treebank which is part of the OntoNotes release.
    5.  POS Tag : `str`
        This is the Penn Treebank style part of speech. When parse information is missing,
        all part of speeches except the one for which there is some sense or proposition
        annotation are marked with a XX tag. The verb is marked with just a VERB tag.
    6.  Parse bit : `str`
        This is the bracketed structure broken before the first open parenthesis in the parse,
        and the word/part-of-speech leaf replaced with a `*`. When the parse information is
        missing, the first word of a sentence is tagged as `(TOP*` and the last word is tagged
        as `*)` and all intermediate words are tagged with a `*`.
    7.  Predicate lemma : `str`
        The predicate lemma is mentioned for the rows for which we have semantic role
        information or word sense information. All other rows are marked with a "-".
    8.  Predicate Frameset ID : `int`
        The PropBank frameset ID of the predicate in Column 7.
    9.  Word sense : `float`
        This is the word sense of the word in Column 3.
    10. Speaker/Author : `str`
        This is the speaker or author name where available. Mostly in Broadcast Conversation
        and Web Log data. When not available the rows are marked with an "-".
    11. Named Entities : `str`
        These columns identifies the spans representing various named entities. For documents
        which do not have named entity annotation, each line is represented with an `*`.
    12. Predicate Arguments : `str`
        There is one column each of predicate argument structure information for the predicate
        mentioned in Column 7. If there are no predicates tagged in a sentence this is a
        single column with all rows marked with an `*`.
    -1. Co-reference : `str`
        Co-reference chain information encoded in a parenthesis structure. For documents that do
         not have co-reference annotations, each line is represented with a "-".
    """

    def dataset_iterator(self, file_path: str) -> Iterator[OntonotesSentence]:
        """
        An iterator over the entire dataset, yielding all sentences processed.
        """
        for conll_file in self.dataset_path_iterator(file_path):
            yield from self.sentence_iterator(conll_file)

    @staticmethod
    def dataset_path_iterator(file_path: str) -> Iterator[str]:
        """
        An iterator returning file_paths in a directory
        containing CONLL-formatted files.
        """
        for root, _, files in list(os.walk(file_path)):
            for data_file in sorted(files):
                # These are a relic of the dataset pre-processing. Every
                # file will be duplicated - one file called filename.gold_skel
                # and one generated from the preprocessing called filename.gold_conll.
                if not data_file.endswith("gold_conll"):
                    continue

                yield os.path.join(root, data_file)

    def dataset_document_iterator(self, file_path: str) -> Iterator[List[OntonotesSentence]]:
        """
        An iterator over CONLL formatted files which yields documents, regardless
        of the number of document annotations in a particular file. This is useful
        for conll data which has been preprocessed, such as the preprocessing which
        takes place for the 2012 CONLL Coreference Resolution task.
        """
        with open(file_path, "r", encoding="utf8") as open_file:
            conll_rows = []
            document: List[OntonotesSentence] = []
            for line in open_file:
                line = line.strip()
                if line != "" and not line.startswith("#"):
                    # Non-empty line. Collect the annotation.
                    conll_rows.append(line)
                else:
                    if conll_rows:
                        document.append(self._conll_rows_to_sentence(conll_rows))
                        conll_rows = []
                if line.startswith("#end document"):
                    yield document
                    document = []
            if document:
                # Collect any stragglers or files which might not
                # have the '#end document' format for the end of the file.
                yield document

    def sentence_iterator(self, file_path: str) -> Iterator[OntonotesSentence]:
        """
        An iterator over the sentences in an individual CONLL formatted file.
        """
        for document in self.dataset_document_iterator(file_path):
            for sentence in document:
                yield sentence

    def _conll_rows_to_sentence(self, conll_rows: List[str]) -> OntonotesSentence:
        document_id: str = None
        sentence_id: int = None
        # The words in the sentence.
        sentence: List[str] = []
        # The pos tags of the words in the sentence.
        pos_tags: List[str] = []
        # the pieces of the parse tree.
        parse_pieces: List[str] = []
        # The lemmatised form of the words in the sentence which
        # have SRL or word sense information.
        predicate_lemmas: List[str] = []
        # The FrameNet ID of the predicate.
        predicate_framenet_ids: List[str] = []
        # The sense of the word, if available.
        word_senses: List[float] = []
        # The current speaker, if available.
        speakers: List[str] = []

        verbal_predicates: List[str] = []
        span_labels: List[List[str]] = []
        current_span_labels: List[str] = []

        # Cluster id -> List of (start_index, end_index) spans.
        clusters: DefaultDict[int, List[Tuple[int, int]]] = defaultdict(list)
        # Cluster id -> List of start_indices which are open for this id.
        coref_stacks: DefaultDict[int, List[int]] = defaultdict(list)

        for index, row in enumerate(conll_rows):
            conll_components = row.split()

            document_id = conll_components[0]
            sentence_id = int(conll_components[1])
            word = conll_components[3]
            pos_tag = conll_components[4]
            parse_piece = conll_components[5]

            # Replace brackets in text and pos tags
            # with a different token for parse trees.
            if pos_tag != "XX" and word != "XX":
                if word == "(":
                    parse_word = "-LRB-"
                elif word == ")":
                    parse_word = "-RRB-"
                else:
                    parse_word = word
                if pos_tag == "(":
                    pos_tag = "-LRB-"
                if pos_tag == ")":
                    pos_tag = "-RRB-"
                (left_brackets, right_hand_side) = parse_piece.split("*")
                # only keep ')' if there are nested brackets with nothing in them.
                right_brackets = right_hand_side.count(")") * ")"
                parse_piece = f"{left_brackets} ({pos_tag} {parse_word}) {right_brackets}"
            else:
                # There are some bad annotations in the CONLL data.
                # They contain no information, so to make this explicit,
                # we just set the parse piece to be None which will result
                # in the overall parse tree being None.
                parse_piece = None

            lemmatised_word = conll_components[6]
            framenet_id = conll_components[7]
            word_sense = conll_components[8]
            speaker = conll_components[9]

            if not span_labels:
                # If this is the first word in the sentence, create
                # empty lists to collect the NER and SRL BIO labels.
                # We can't do this upfront, because we don't know how many
                # components we are collecting, as a sentence can have
                # variable numbers of SRL frames.
                span_labels = [[] for _ in conll_components[10:-1]]
                # Create variables representing the current label for each label
                # sequence we are collecting.
                current_span_labels = [None for _ in conll_components[10:-1]]

            self._process_span_annotations_for_word(conll_components[10:-1], span_labels, current_span_labels)

            # If any annotation marks this word as a verb predicate,
            # we need to record its index. This also has the side effect
            # of ordering the verbal predicates by their location in the
            # sentence, automatically aligning them with the annotations.
            word_is_verbal_predicate = any("(V" in x for x in conll_components[11:-1])
            if word_is_verbal_predicate:
                verbal_predicates.append(word)

            self._process_coref_span_annotations_for_word(conll_components[-1], index, clusters, coref_stacks)

            sentence.append(word)
            pos_tags.append(pos_tag)
            parse_pieces.append(parse_piece)
            predicate_lemmas.append(lemmatised_word if lemmatised_word != "-" else None)
            predicate_framenet_ids.append(framenet_id if framenet_id != "-" else None)
            word_senses.append(float(word_sense) if word_sense != "-" else None)
            speakers.append(speaker if speaker != "-" else None)

        named_entities = span_labels[0]
        srl_frames = [(predicate, labels) for predicate, labels in zip(verbal_predicates, span_labels[1:])]

        if all(parse_pieces):
            parse_tree = "".join(parse_pieces)
        else:
            parse_tree = None
        coref_span_tuples = {(cluster_id, span) for cluster_id, span_list in clusters.items() for span in span_list}
        return OntonotesSentence(
            document_id,
            sentence_id,
            sentence,
            pos_tags,
            parse_tree,
            predicate_lemmas,
            predicate_framenet_ids,
            word_senses,
            speakers,
            named_entities,
            srl_frames,
            coref_span_tuples,
        )

    @staticmethod
    def _process_coref_span_annotations_for_word(
        label: str,
        word_index: int,
        clusters: DefaultDict[int, List[Tuple[int, int]]],
        coref_stacks: DefaultDict[int, List[int]],
    ) -> None:
        """
        For a given coref label, add it to a currently open span(s), complete a span(s) or
        ignore it, if it is outside of all spans. This method mutates the clusters and coref_stacks
        dictionaries.
        # Parameters
        label : `str`
            The coref label for this word.
        word_index : `int`
            The word index into the sentence.
        clusters : `DefaultDict[int, List[Tuple[int, int]]]`
            A dictionary mapping cluster ids to lists of inclusive spans into the
            sentence.
        coref_stacks : `DefaultDict[int, List[int]]`
            Stacks for each cluster id to hold the start indices of active spans (spans
            which we are inside of when processing a given word). Spans with the same id
            can be nested, which is why we collect these opening spans on a stack, e.g:
            [Greg, the baker who referred to [himself]_ID1 as 'the bread man']_ID1
        """
        if label != "-":
            for segment in label.split("|"):
                # The conll representation of coref spans allows spans to
                # overlap. If spans end or begin at the same word, they are
                # separated by a "|".
                if segment[0] == "(":
                    # The span begins at this word.
                    if segment[-1] == ")":
                        # The span begins and ends at this word (single word span).
                        cluster_id = int(segment[1:-1])
                        clusters[cluster_id].append((word_index, word_index))
                    else:
                        # The span is starting, so we record the index of the word.
                        cluster_id = int(segment[1:])
                        coref_stacks[cluster_id].append(word_index)
                else:
                    # The span for this id is ending, but didn't start at this word.
                    # Retrieve the start index from the document state and
                    # add the span to the clusters for this id.
                    cluster_id = int(segment[:-1])
                    start = coref_stacks[cluster_id].pop()
                    clusters[cluster_id].append((start, word_index))

    @staticmethod
    def _process_span_annotations_for_word(
        annotations: List[str],
        span_labels: List[List[str]],
        current_span_labels: List[Optional[str]],
    ) -> None:
        """
        Given a sequence of different label types for a single word and the current
        span label we are inside, compute the BIO tag for each label and append to a list.
        # Parameters
        annotations : `List[str]`
            A list of labels to compute BIO tags for.
        span_labels : `List[List[str]]`
            A list of lists, one for each annotation, to incrementally collect
            the BIO tags for a sequence.
        current_span_labels : `List[Optional[str]]`
            The currently open span per annotation type, or `None` if there is no open span.
        """
        for annotation_index, annotation in enumerate(annotations):
            # strip all bracketing information to
            # get the actual propbank label.
            label = annotation.strip("()*")

            if "(" in annotation:
                # Entering into a span for a particular semantic role label.
                # We append the label and set the current span for this annotation.
                bio_label = "B-" + label
                span_labels[annotation_index].append(bio_label)
                current_span_labels[annotation_index] = label
            elif current_span_labels[annotation_index] is not None:
                # If there's no '(' token, but the current_span_label is not None,
                # then we are inside a span.
                bio_label = "I-" + current_span_labels[annotation_index]
                span_labels[annotation_index].append(bio_label)
            else:
                # We're outside a span.
                span_labels[annotation_index].append("O")
            # Exiting a span, so we reset the current span label for this annotation.
            if ")" in annotation:
                current_span_labels[annotation_index] = None
