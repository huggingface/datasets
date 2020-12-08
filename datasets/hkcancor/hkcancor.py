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

from __future__ import absolute_import, division, print_function

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
POS scheme - Peita-Fujitsu-Renmin Ribao (PRF) corpus (Duan et al., 2000)
"""

_HOMEPAGE = "http://compling.hss.ntu.edu.sg/hkcancor/"

_LICENSE = "CC BY 4.0"

_URL = "http://compling.hss.ntu.edu.sg/hkcancor/data/hkcancor-utf8.zip"


class Hkcancor(datasets.GeneratorBasedBuilder):
    """Hong Kong Cantonese Corpus (HKCanCor)."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "conversation_id": datasets.Value("string"),
                "speaker": datasets.Value("string"),
                "turn_number": datasets.Value("int16"),
                "words": datasets.Sequence(datasets.Value("string")),
                "transcriptions": datasets.Sequence(datasets.Value("string")),
                "pos_tags": datasets.Sequence(datasets.Value("string")),
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
        data_dir = dl_manager.download_and_extract(_URL) + "/utf8/"

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
        """ Yields examples. """

        downloaded_files = [data_dir + fn for fn in os.listdir(data_dir)]
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
                        words = []
                        pos_tags = []
                        transcriptions = []
                        current_sentence = [w.strip() for w in child.text.split("\n") if w and not w.isspace()]
                        for w in current_sentence:
                            word_data = w.split("/")
                            words.append(word_data[0])
                            pos_tags.append(word_data[1])
                            transcriptions.append(word_data[2])

                        num_words = len(words)
                        num_pos_tags = len(pos_tags)
                        num_transcriptions = len(transcriptions)

                        assert len(words) == len(
                            pos_tags
                        ), "Sizes do not match: {nw} vs {np} for words vs pos-tags in {fp}".format(
                            nw=num_words, np=num_pos_tags, fp=filepath
                        )
                        assert len(pos_tags) == len(
                            transcriptions
                        ), "Sizes do not match: {np} vs {nt} for words vs pos-tags in {fp}".format(
                            np=num_pos_tags, nt=num_transcriptions, fp=filepath
                        )

                        # Corpus doesn't come with conversation-level ids, and
                        # multiple texts can correspond to the same tape number,
                        # date, and speakers.
                        # The following workaround prepends metadata with the
                        # first few transcriptions in the conversation
                        # to create an identifier.
                        id_from_transcriptions = "".join(transcriptions[:5])[:5].upper()
                        id_ = "{tn}-{rd}-{it}".format(tn=tape_number, rd=date_recorded, it=id_from_transcriptions)
                        yield id_, {
                            "conversation_id": id_,
                            "speaker": current_speaker,
                            "turn_number": turn_number,
                            "words": words,
                            "transcriptions": transcriptions,
                            "pos_tags": pos_tags,
                        }
