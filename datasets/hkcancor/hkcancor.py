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
"""Hong Kong Cantonese Corpus (HKCanCor)."""


import os
import xml.etree.ElementTree as ET

import datasets


_CITATION = """\
@article{luke2015hong,
  author={Luke, Kang-Kwong and Wong, May LY},
  title={The Hong Kong Cantonese corpus: design and uses},
  journal={Journal of Chinese Linguistics},
  year={2015},
  pages={309-330},
  month={12}
}
@misc{lee2020,
  author = {Lee, Jackson},
  title = {PyCantonese: Cantonese Linguistics and NLP in Python},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {https://github.com/jacksonllee/pycantonese},
  commit = {1d58f44e1cb097faa69de6b617e1d28903b84b98}
}
"""

_DESCRIPTION = """\
The Hong Kong Cantonese Corpus (HKCanCor) comprise transcribed conversations
recorded between March 1997 and August 1998. It contains recordings of
spontaneous speech (51 texts) and radio programmes (42 texts),
which involve 2 to 4 speakers, with 1 text of monologue.

In total, the corpus contains around 230,000 Chinese words.
The text is word-segmented, annotated with part-of-speech (POS) tags and
romanised Cantonese pronunciation.

Romanisation scheme - Linguistic Society of Hong Kong (LSHK)
POS scheme - Peita-Fujitsu-Renmin Ribao (PRF) corpus (Duan et al., 2000),
             with extended tags for Cantonese-specific phenomena added by
             Luke and Wang (see original paper for details).
"""

_HOMEPAGE = "http://compling.hss.ntu.edu.sg/hkcancor/"

_LICENSE = "CC BY 4.0"

_URL = "http://compling.hss.ntu.edu.sg/hkcancor/data/hkcancor-utf8.zip"


class Hkcancor(datasets.GeneratorBasedBuilder):
    """Hong Kong Cantonese Corpus (HKCanCor)."""

    VERSION = datasets.Version("1.0.0")

    # Original tagset has 110 + tags and includes fine-grained annotations,
    # e.g., distinguish morphemes vs non-moprhemes. For practical purposes
    # (usability, comparing across datasets), Lee 2020 mapped HKCanCor tags
    # to the Universal Dependencies 2.0 scheme. The following is adapted from:
    # https://github.com/jacksonllee/pycantonese/blob/master/pycantonese/pos_tagging/hkcancor_to_ud.py

    pos_map = {
        "!": "PUNCT",
        '"': "PUNCT",
        "#": "X",
        "'": "PUNCT",
        ",": "PUNCT",
        "-": "PUNCT",
        ".": "PUNCT",
        "...": "PUNCT",
        "?": "PUNCT",
        "A": "ADJ",  # HKCanCor: Adjective
        "AD": "ADV",  # HKCanCor: Adjective as Adverbial
        "AG": "ADJ",  # HKCanCor: Adjective Morpheme
        "AIRWAYS0": "PROPN",
        "AN": "NOUN",  # HKCanCor: Adjective with Nominal Function
        "AND": "PROPN",  # In one instance of "Chilli and Pepper"
        "B": "ADJ",  # HKCanCor: Non-predicate Adjective
        "BG": "ADJ",  # HKCanCor: Non-predicate Adjective Morpheme
        "BEAN0": "PROPN",  # In one instance of "Mr Bean"
        "C": "CCONJ",  # HKCanCor: Conjunction
        "CENTRE0": "NOUN",  # In one instance of "career centre"
        "CG": "CCONJ",
        "D": "ADV",  # HKCanCor: Adverb
        "D1": "ADV",  # Most instances are gwai2 "ghost".
        "DG": "ADV",  # HKCanCor: Adverb Morpheme
        "E": "INTJ",  # HKCanCor: Interjection
        "ECHO0": "PROPN",  # In one instance of "Big Echo"
        "F": "ADV",  # HKCanCor: Directional Locality
        "G": "X",  # HKCanCor: Morpheme
        "G1": "V",  # The first A in the "A-not-AB" pattern, where AB is a verb.
        "G2": "ADJ",  # The first A in "A-not-AB", where AB is an adjective.
        "H": "PROPN",  # HKCanCor: Prefix (aa3 阿 followed by a person name)
        "HILL0": "PROPN",  # In "Benny Hill"
        "I": "X",  # HKCanCor: Idiom
        "IG": "X",
        "J": "NOUN",  # HKCanCor: Abbreviation
        "JB": "ADJ",
        "JM": "NOUN",
        "JN": "NOUN",
        "JNS": "PROPN",
        "JNT": "PROPN",
        "JNZ": "PROPN",
        "K": "X",  # HKCanCor: Suffix (sing3 性 for nouns; dei6 地 for adverbs)
        "KONG": "PROPN",  # In "Hong Kong"
        "L": "X",  # Fixed Expression
        "L1": "X",
        "LG": "X",
        "M": "NUM",  # HKCanCor: Numeral
        "MG": "X",
        "MONTY0": "PROPN",  # In "Full Monty"
        "MOUNTAIN0": "PROPN",  # In "Blue Mountain"
        "N": "NOUN",  # Common Noun
        "N1": "DET",  # HKCanCor: only used for ne1 呢; determiner
        "NG": "NOUN",
        "NR": "PROPN",  # HKCanCor: Personal Name
        "NS": "PROPN",  # HKCanCor: Place Name
        "NSG": "PROPN",
        "NT": "PROPN",  # HKCanCor: Organization Name
        "NX": "NOUN",  # HKCanCor: Nominal Character String
        "NZ": "PROPN",  # HKCanCor: Other Proper Noun
        "O": "X",  # HKCanCor: Onomatopoeia
        "P": "ADP",  # HKCanCor: Preposition
        "PEPPER0": "PROPN",  # In "Chilli and Pepper"
        "Q": "NOUN",  # HKCanCor: Classifier
        "QG": "NOUN",  # HKCanCor: Classifier Morpheme
        "R": "PRON",  # HKCanCor: Pronoun
        "RG": "PRON",  # HKCanCor: Pronoun Morpheme
        "S": "NOUN",  # HKCanCor: Space Word
        "SOUND0": "PROPN",  # In "Manchester's Sound"
        "T": "ADV",  # HKCanCor: Time Word
        "TELECOM0": "PROPN",  # In "Hong Kong Telecom"
        "TG": "ADV",  # HKCanCor: Time Word Morpheme
        "TOUCH0": "PROPN",  # In "Don't Touch" (a magazine)
        "U": "PART",  # HKCanCor: Auxiliary (e.g., ge3 嘅 after an attributive adj)
        "UG": "PART",  # HKCanCor: Auxiliary Morpheme
        "U0": "PROPN",  # U as in "Hong Kong U" (= The University of Hong Kong)
        "V": "VERB",  # HKCanCor: Verb
        "V1": "VERB",
        "VD": "ADV",  # HKCanCor: Verb as Adverbial
        "VG": "VERB",
        "VK": "VERB",
        "VN": "NOUN",  # HKCanCor: Verb with Nominal Function
        "VU": "AUX",
        "VUG": "AUX",
        "W": "PUNCT",  # HKCanCor: Punctuation
        "X": "X",  # HKCanCor: Unclassified Item
        "XA": "ADJ",
        "XB": "ADJ",
        "XC": "CCONJ",
        "XD": "ADV",
        "XE": "INTJ",
        "XJ": "X",
        "XJB": "PROPN",
        "XJN": "NOUN",
        "XJNT": "PROPN",
        "XJNZ": "PROPN",
        "XJV": "VERB",
        "XJA": "X",
        "XL1": "INTJ",
        "XM": "NUM",
        "XN": "NOUN",
        "XNG": "NOUN",
        "XNR": "PROPN",
        "XNS": "PROPN",
        "XNT": "PROPN",
        "XNX": "NOUN",
        "XNZ": "PROPN",
        "XO": "X",
        "XP": "ADP",
        "XQ": "NOUN",
        "XR": "PRON",
        "XS": "PROPN",
        "XT": "NOUN",
        "XV": "VERB",
        "XVG": "VERB",
        "XVN": "NOUN",
        "XX": "X",
        "Y": "PART",  # HKCanCor: Modal Particle
        "YG": "PART",  # HKCanCor: Modal Particle Morpheme
        "Y1": "PART",
        "Z": "ADJ",  # HKCanCor: Descriptive
    }

    def _info(self):

        pos_tags_prf = datasets.Sequence(datasets.features.ClassLabel(names=[tag for tag in self.pos_map.keys()]))

        pos_tags_ud = datasets.Sequence(
            datasets.features.ClassLabel(names=[tag for tag in set(self.pos_map.values())])
        )

        features = datasets.Features(
            {
                "conversation_id": datasets.Value("string"),
                "speaker": datasets.Value("string"),
                "turn_number": datasets.Value("int16"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "transcriptions": datasets.Sequence(datasets.Value("string")),
                "pos_tags_prf": pos_tags_prf,
                "pos_tags_ud": pos_tags_ud,
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.join(dl_manager.download_and_extract(_URL), "utf8")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": data_dir,
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, data_dir, split):
        """Yields examples."""

        downloaded_files = [os.path.join(data_dir, fn) for fn in sorted(os.listdir(data_dir))]
        for filepath in downloaded_files:
            # Each file in the corpus contains one conversation
            with open(filepath, encoding="utf-8") as f:
                xml = f.read()
                # Add dummy root node to form valid tree
                xml = "<root>" + xml + "</root>"
                tree = ET.fromstring(xml)

            # Extract dialogue metadata
            info = [line.strip() for line in tree.find("info").text.split("\n") if line and not line.endswith("END")]
            tape_number = "".join(info[0].split("-")[1:])
            date_recorded = "".join(info[1].split("-")[1:])

            turn_number = -1
            for sent in tree.findall("sent"):
                for child in sent.iter():
                    if child.tag == "sent_head":
                        current_speaker = child.text.strip()[:-1]
                        turn_number += 1
                    elif child.tag == "sent_tag":
                        tokens = []
                        pos_prf = []
                        pos_ud = []
                        transcriptions = []
                        current_sentence = [w.strip() for w in child.text.split("\n") if w and not w.isspace()]
                        for w in current_sentence:
                            token_data = w.split("/")
                            tokens.append(token_data[0])
                            transcriptions.append(token_data[2])

                            prf_tag = token_data[1].upper()
                            ud_tag = self.pos_map.get(prf_tag, "X")
                            pos_prf.append(prf_tag)
                            pos_ud.append(ud_tag)

                        num_tokens = len(tokens)
                        num_pos_tags = len(pos_prf)
                        num_transcriptions = len(transcriptions)

                        assert len(tokens) == len(
                            pos_prf
                        ), f"Sizes do not match: {num_tokens} vs {num_pos_tags} for tokens vs pos-tags in {filepath}"
                        assert len(pos_prf) == len(
                            transcriptions
                        ), f"Sizes do not match: {num_pos_tags} vs {num_transcriptions} for tokens vs pos-tags in {filepath}"

                        # Corpus doesn't come with conversation-level ids, and
                        # multiple texts can correspond to the same tape number,
                        # date, and speakers.
                        # The following workaround prepends metadata with the
                        # first few transcriptions in the conversation
                        # to create an identifier.
                        id_from_transcriptions = "".join(transcriptions[:5])[:5].upper()
                        id_ = f"{tape_number}-{date_recorded}-{id_from_transcriptions}"
                        yield id_, {
                            "conversation_id": id_,
                            "speaker": current_speaker,
                            "turn_number": turn_number,
                            "tokens": tokens,
                            "transcriptions": transcriptions,
                            "pos_tags_prf": pos_prf,
                            "pos_tags_ud": pos_ud,
                        }
