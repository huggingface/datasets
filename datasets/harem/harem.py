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
"""HAREM dataset"""


import json
import unicodedata
from typing import List, Tuple

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """
@inproceedings{santos2006harem,
  title={Harem: An advanced ner evaluation contest for portuguese},
  author={Santos, Diana and Seco, Nuno and Cardoso, Nuno and Vilela, Rui},
  booktitle={quot; In Nicoletta Calzolari; Khalid Choukri; Aldo Gangemi; Bente Maegaard; Joseph Mariani; Jan Odjik; Daniel Tapias (ed) Proceedings of the 5 th International Conference on Language Resources and Evaluation (LREC'2006)(Genoa Italy 22-28 May 2006)},
  year={2006}
}
"""

_DESCRIPTION = """
The HAREM is a Portuguese language corpus commonly used for Named Entity Recognition tasks. It includes about 93k words, from 129 different texts,
from several genres, and language varieties. The split of this dataset version follows the division made by [1], where 7% HAREM
documents are the validation set and the miniHAREM corpus (with about 65k words) is the test set. There are two versions of the dataset set,
a version that has a total of 10 different named entity classes (Person, Organization, Location, Value, Date, Title, Thing, Event,
Abstraction, and Other) and a "selective" version with only 5 classes (Person, Organization, Location, Value, and Date).

It's important to note that the original version of the HAREM dataset has 2 levels of NER details, namely "Category" and "Sub-type".
The dataset version processed here ONLY USE the "Category" level of the original dataset.

[1] Souza, Fábio, Rodrigo Nogueira, and Roberto Lotufo. "BERTimbau: Pretrained BERT Models for Brazilian Portuguese." Brazilian Conference on Intelligent Systems. Springer, Cham, 2020.
"""

_HOMEPAGE = "https://www.linguateca.pt/primeiroHAREM/harem_coleccaodourada_en.html"

_LICENSE = ""

_URLs = {
    "default": {
        "train": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/FirstHAREM-total-train.json",
        "dev": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/FirstHAREM-total-dev.json",
        "test": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/MiniHAREM-total.json",
    },
    "selective": {
        "train": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/FirstHAREM-selective-train.json",
        "dev": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/FirstHAREM-selective-dev.json",
        "test": "https://raw.githubusercontent.com/neuralmind-ai/portuguese-bert/master/ner_evaluation/data/MiniHAREM-selective.json",
    },
}


# method extracted from https://github.com/huggingface/transformers/blob/master/src/transformers/tokenization_utils.py#L77-L89
def _is_punctuation(char):
    """Checks whether `char` is a punctuation character."""
    cp = ord(char)
    # We treat all non-letter/number ASCII as punctuation.
    # Characters such as "^", "$", and "`" are not in the Unicode
    # Punctuation class but we treat them as punctuation anyways, for
    # consistency.
    if (cp >= 33 and cp <= 47) or (cp >= 58 and cp <= 64) or (cp >= 91 and cp <= 96) or (cp >= 123 and cp <= 126):
        return True
    cat = unicodedata.category(char)
    if cat.startswith("P"):
        return True
    return False


# method extracted from https://github.com/huggingface/transformers/blob/master/src/transformers/tokenization_utils.py#L53-L62
def _is_whitespace(char):
    """Checks whether `char` is a whitespace character."""
    # \t, \n, and \r are technically control characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


class Token:
    """Info about a single token."""

    def __init__(self, text: str, tail: str = ""):

        if not isinstance(text, str) or not text:
            raise TypeError("text should be a non-empty string.")
        self.text = text
        self.tail = tail

    def __len__(self):
        return len(self.text) + len(self.tail)

    def __add__(self, char):
        self.text += char
        return self


def reconstruct_text_from_tokens(tokens: List[Token], include_last_tail: bool = False) -> str:
    """Concatenates the text of a sequence of tokens."""

    def text_generator(tokens):
        for i, token in enumerate(tokens):
            yield token.text
            if i < len(tokens) - 1 or include_last_tail:
                yield token.tail

    return "".join(piece for piece in text_generator(tokens))


def tokenize(text: str) -> Tuple[List[Token], List[int]]:
    """Perform whitespace and punctuation tokenization keeping track of char alignment"""
    doc_tokens = []
    char_to_word_offset = []

    new_word = True
    curr_token = None

    def begin_new_token(doc_tokens, text):
        token = Token(text=text)
        doc_tokens.append(token)
        return token

    for offset, c in enumerate(text):
        if _is_whitespace(c):
            new_word = True
            if curr_token:
                curr_token.tail += c
        else:
            if _is_punctuation(c):
                curr_token = begin_new_token(doc_tokens, c)
                new_word = True
            else:
                if new_word:
                    curr_token = begin_new_token(doc_tokens, c)
                else:
                    curr_token += c
                new_word = False

        # OBS: Whitespaces that appear before any tokens will have offset -1
        # char_to_word_offset.append(len(doc_tokens) - 1)
        char_to_word_offset.append(max(0, len(doc_tokens) - 1))

    return doc_tokens, char_to_word_offset


class HAREM(datasets.GeneratorBasedBuilder):
    """HAREM dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="default",
            version=VERSION,
            description="All the tags (PESSOA, ORGANIZACAO, LOCAL, TEMPO, VALOR, ABSTRACCAO, ACONTECIMENTO, COISA, OBRA, OUTRO) will be used",
        ),
        datasets.BuilderConfig(
            name="selective",
            version=VERSION,
            description="Only a subset of the tags (PESSOA, ORGANIZACAO, LOCAL, TEMPO, VALOR) will be used",
        ),
    ]

    DEFAULT_CONFIG_NAME = "default"

    def _info(self):

        tags = [
            "O",
            "B-PESSOA",
            "I-PESSOA",
            "B-ORGANIZACAO",
            "I-ORGANIZACAO",
            "B-LOCAL",
            "I-LOCAL",
            "B-TEMPO",
            "I-TEMPO",
            "B-VALOR",
            "I-VALOR",
        ]

        if self.config.name == "default":
            tags += [
                "B-ABSTRACCAO",
                "I-ABSTRACCAO",
                "B-ACONTECIMENTO",
                "I-ACONTECIMENTO",
                "B-COISA",
                "I-COISA",
                "B-OBRA",
                "I-OBRA",
                "B-OUTRO",
                "I-OUTRO",
            ]

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(datasets.features.ClassLabel(names=tags)),
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

        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": data_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": data_dir["dev"], "split": "dev"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        logger.info("⏳ Generating examples from = %s", filepath)

        with open(filepath, "r", encoding="utf-8") as f:

            input_data = json.load(f)
            id_ = 0

            for document in input_data:
                doc_text = document["doc_text"]
                doc_id = document["doc_id"]

                doc_tokens, char_to_word_offset = tokenize(doc_text)
                tags = ["O"] * len(doc_tokens)

                def set_label(index, tag):
                    if tags[index] != "O":
                        logger.warning(
                            "Overwriting tag %s at position %s to %s",
                            tags[index],
                            index,
                            tag,
                        )
                    tags[index] = tag

                for entity in document["entities"]:
                    entity_text = entity["text"]
                    entity_type = entity["label"]
                    start_token = None
                    end_token = None

                    entity_start_offset = entity["start_offset"]
                    entity_end_offset = entity["end_offset"]
                    start_token = char_to_word_offset[entity_start_offset]

                    # end_offset is NOT inclusive to the text, e.g.,
                    # entity_text == doc_text[start_offset:end_offset]
                    end_token = char_to_word_offset[entity_end_offset - 1]

                    assert start_token <= end_token, "End token cannot come before start token."
                    reconstructed_text = reconstruct_text_from_tokens(doc_tokens[start_token : (end_token + 1)])
                    assert (
                        entity_text.strip() == reconstructed_text
                    ), "Entity text and reconstructed text are not equal: %s != %s" % (
                        entity_text,
                        reconstructed_text,
                    )

                    for token_index in range(start_token, end_token + 1):
                        if token_index == start_token:
                            tag = "B-" + entity_type
                        else:
                            tag = "I-" + entity_type
                        set_label(token_index, tag)

                yield id_, {
                    "id": doc_id,
                    "tokens": [x.text for x in doc_tokens],
                    "ner_tags": tags,
                }
                id_ += 1
