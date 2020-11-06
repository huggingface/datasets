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
"""Public DGS Corpus: parallel corpus for German Sign Language (DGS) with German and English annotations"""

from __future__ import absolute_import, division, print_function

import json

import pympi
from tqdm import tqdm

import datasets


_DESCRIPTION = """
parallel corpus for German Sign Language (DGS) with German and English annotations
"""

_CITATION = """\
@misc{dgscorpus_3,
  title = {MEINE DGS -- annotiert. {\"O}ffentliches Korpus der Deutschen Geb{\"a}rdensprache, 3. Release / MY DGS -- annotated. Public Corpus of German Sign Language, 3rd release},
  author = {Konrad, Reiner and Hanke, Thomas and Langer, Gabriele and Blanck, Dolly and Bleicken, Julian and Hofmann, Ilona and Jeziorski, Olga and K{\"o}nig, Lutz and K{\"o}nig, Susanne and Nishio, Rie and Regen, Anja and Salden, Uta and Wagner, Sven and Worseck, Satu and B{\"o}se, Oliver and Jahn, Elena and Schulder, Marc},
  year = {2020},
  type = {languageresource},
  version = {3.0},
  publisher = {Universit{\"a}t Hamburg},
  url = {https://doi.org/10.25592/dgs.corpus-3.0},
  doi = {10.25592/dgs.corpus-3.0}
}
"""

_URL = "https://nlp.biu.ac.il/~amit/datasets/dgs.json"

_HOMEPAGE = "https://www.sign-lang.uni-hamburg.de/meinedgs//"


class DGS(datasets.GeneratorBasedBuilder):
    """Public DGS Corpus: parallel corpus for German Sign Language (DGS) with German and English annotations"""

    VERSION = datasets.Version("3.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "transcript": datasets.Value("string"),
                    "format": datasets.Value("string"),
                    "ilex": datasets.Value("string"),
                    "eaf": datasets.Value("string"),
                    "video_a": datasets.Value("string"),
                    "video_b": datasets.Value("string"),
                    "video_c": datasets.Value("string"),
                    "srt": datasets.Value("string"),
                    "cmdi": datasets.Value("string"),
                    "openpose": datasets.Value("string"),
                    "sentences": datasets.features.Sequence(
                        {
                            "participant": datasets.features.ClassLabel(names=["A", "B"]),
                            "start": datasets.Value("int32"),
                            "end": datasets.Value("int32"),
                            "german": datasets.Value("string"),
                            "english": datasets.Value("string"),
                            "glosses": datasets.features.Sequence(
                                {
                                    "start": datasets.Value("int32"),
                                    "end": datasets.Value("int32"),
                                    "hand": datasets.features.ClassLabel(names=["l", "r"]),
                                    "gloss": datasets.Value("string"),
                                    "Lexeme_Sign": datasets.Value("string"),
                                    "Gebärde": datasets.Value("string"),
                                    "Sign": datasets.Value("string"),
                                }
                            ),
                        }
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        index_path = dl_manager.download(_URL)

        with open(index_path, "r", encoding="utf-8") as f:
            index_data = json.load(f)

        urls = {url: url for datum in index_data.values() for url in datum.values() if url is not None}
        local_paths = dl_manager.download(urls)

        processed_data = {
            _id: {k: local_paths[v] if v is not None else None for k, v in datum.items()}
            for _id, datum in index_data.items()
        }

        final_data_path = index_path + ".final.json"
        with open(final_data_path, "w", encoding="utf-8") as f:
            json.dump(processed_data, f)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_path": final_data_path, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_path": final_data_path, "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_path": final_data_path, "split": "test"},
            ),
        ]

    def _get_elan_sentences(self, elan_path: str):
        print("elan_path", elan_path)
        eaf = pympi.Elan.Eaf(elan_path)

        timeslots = eaf.timeslots

        for participant in ["A", "B"]:
            german_tier_name = "Deutsche_Übersetzung_" + participant
            if german_tier_name not in eaf.tiers:
                continue

            german_text = list(eaf.tiers[german_tier_name][0].values())

            english_tier_name = "Translation_into_English_" + participant
            english_text = list(eaf.tiers[english_tier_name][0].values()) if english_tier_name in eaf.tiers else []

            all_glosses = []
            for hand in ["r", "l"]:
                hand_tier = "Lexem_Gebärde_" + hand + "_" + participant
                if hand_tier not in eaf.tiers:
                    continue

                gloss = {
                    _id: {"start": timeslots[s], "end": timeslots[e], "gloss": val, "hand": hand}
                    for _id, (s, e, val, _) in eaf.tiers[hand_tier][0].items()
                }
                for tier in ["Lexeme_Sign", "Gebärde", "Sign"]:
                    items = eaf.tiers[tier + "_" + hand + "_" + participant][1]
                    for ref, val, _1, _2 in items.values():
                        if ref in gloss:  # 2 files have a missing reference
                            gloss[ref][tier] = val

                all_glosses += list(gloss.values())

            for (s, e, val, _) in german_text:
                sentence = {"participant": participant, "start": timeslots[s], "end": timeslots[e], "german": val}

                # Add English sentence
                english_sentence = [val for (s2, e2, val2, _) in english_text if s == s2 and e == e2]
                sentence["english"] = english_sentence[0] if len(english_sentence) > 0 else None

                # Add glosses
                sentence["glosses"] = list(
                    sorted(
                        [
                            item
                            for item in all_glosses
                            if item["start"] >= sentence["start"] and item["end"] <= sentence["end"]
                        ],
                        key=lambda d: d["start"],
                    )
                )

                yield sentence

    def _generate_examples(self, data_path, split):
        """ Yields examples. """

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for i, (_id, datum) in tqdm(list(enumerate(data.items()))):
                # Test and Dev splits get 1/7th of the data (~14%) each
                if (
                    (i % 7 == 0 and split == "test")
                    or (i % 7 == 1 and split == "dev")
                    or (i % 7 > 1 and split == "train")
                ):
                    datum["sentences"] = list(self._get_elan_sentences(datum["eaf"]))
                    yield i, datum
