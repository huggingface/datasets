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
"""GEM: Generation Evaluation Metrics supporting datasets"""


import csv
import json
import os

import datasets


_CITATION = """\
@article{gem_benchmark,
  author    = {Sebastian Gehrmann and
               Tosin P. Adewumi and
               Karmanya Aggarwal and
               Pawan Sasanka Ammanamanchi and
               Aremu Anuoluwapo and
               Antoine Bosselut and
               Khyathi Raghavi Chandu and
               Miruna{-}Adriana Clinciu and
               Dipanjan Das and
               Kaustubh D. Dhole and
               Wanyu Du and
               Esin Durmus and
               Ondrej Dusek and
               Chris Emezue and
               Varun Gangal and
               Cristina Garbacea and
               Tatsunori Hashimoto and
               Yufang Hou and
               Yacine Jernite and
               Harsh Jhamtani and
               Yangfeng Ji and
               Shailza Jolly and
               Dhruv Kumar and
               Faisal Ladhak and
               Aman Madaan and
               Mounica Maddela and
               Khyati Mahajan and
               Saad Mahamood and
               Bodhisattwa Prasad Majumder and
               Pedro Henrique Martins and
               Angelina McMillan{-}Major and
               Simon Mille and
               Emiel van Miltenburg and
               Moin Nadeem and
               Shashi Narayan and
               Vitaly Nikolaev and
               Rubungo Andre Niyongabo and
               Salomey Osei and
               Ankur P. Parikh and
               Laura Perez{-}Beltrachini and
               Niranjan Ramesh Rao and
               Vikas Raunak and
               Juan Diego Rodriguez and
               Sashank Santhanam and
               Joao Sedoc and
               Thibault Sellam and
               Samira Shaikh and
               Anastasia Shimorina and
               Marco Antonio Sobrevilla Cabezudo and
               Hendrik Strobelt and
               Nishant Subramani and
               Wei Xu and
               Diyi Yang and
               Akhila Yerukola and
               Jiawei Zhou},
  title     = {The {GEM} Benchmark: Natural Language Generation, its Evaluation and
               Metrics},
  journal   = {CoRR},
  volume    = {abs/2102.01672},
  year      = {2021},
  url       = {https://arxiv.org/abs/2102.01672},
  archivePrefix = {arXiv},
  eprint    = {2102.01672}
}
"""

_DESCRIPTION = """\
GEM is a benchmark environment for Natural Language Generation with a focus on its Evaluation,
both through human annotations and automated Metrics.

GEM aims to:
- measure NLG progress across 13 datasets spanning many NLG tasks and languages.
- provide an in-depth analysis of data and models presented via data statements and challenge sets.
- develop standards for evaluation of generated text using both automated and human metrics.

It is our goal to regularly update GEM and to encourage toward more inclusive practices in dataset development
by extending existing data or developing datasets for additional languages.
"""

_HOMEPAGE = "https://gem-benchmark.github.io/"

_LICENSE = "CC-BY-SA-4.0"

_TASKS = {
    "summarization": {
        "mlsum": ["mlsum_de", "mlsum_es"],
        "wiki_lingua": [
            "wiki_lingua_es_en_v0",
            "wiki_lingua_ru_en_v0",
            "wiki_lingua_tr_en_v0",
            "wiki_lingua_vi_en_v0",
            "wiki_lingua_arabic_ar",
            "wiki_lingua_chinese_zh",
            "wiki_lingua_czech_cs",
            "wiki_lingua_dutch_nl",
            "wiki_lingua_english_en",
            "wiki_lingua_french_fr",
            "wiki_lingua_german_de",
            "wiki_lingua_hindi_hi",
            "wiki_lingua_indonesian_id",
            "wiki_lingua_italian_it",
            "wiki_lingua_japanese_ja",
            "wiki_lingua_korean_ko",
            "wiki_lingua_portuguese_pt",
            "wiki_lingua_russian_ru",
            "wiki_lingua_spanish_es",
            "wiki_lingua_thai_th",
            "wiki_lingua_turkish_tr",
            "wiki_lingua_vietnamese_vi",
        ],
        "xsum": ["xsum"],
    },
    "struct2text": {
        "common_gen": ["common_gen"],
        "cs_restaurants": ["cs_restaurants"],
        "dart": ["dart"],
        "e2e": ["e2e_nlg"],
        "totto": ["totto"],
        "web_nlg": ["web_nlg_en", "web_nlg_ru"],
    },
    "simplification": {
        "wiki_auto_asset_turk": ["wiki_auto_asset_turk"],
    },
    "dialog": {
        "schema_guided_dialog": ["schema_guided_dialog"],
    },
}

_URLs = {
    "common_gen": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/common_gen/commongen_data.zip",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/common_gen.zip",
    },
    "cs_restaurants": {
        "train": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/train.json",
        "validation": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/devel.json",
        "test": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/test.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/cs_restaurants.zip",
    },
    "dart": {
        "train": "https://raw.githubusercontent.com/Yale-LILY/dart/master/data/v1.1.1/dart-v1.1.1-full-train.json",
        "validation": "https://raw.githubusercontent.com/Yale-LILY/dart/master/data/v1.1.1/dart-v1.1.1-full-dev.json",
        "test": "https://raw.githubusercontent.com/Yale-LILY/dart/master/data/v1.1.1/dart-v1.1.1-full-test.json",
    },
    "e2e_nlg": {
        "train": "https://github.com/tuetschek/e2e-cleaning/raw/master/cleaned-data/train-fixed.no-ol.csv",
        "validation": "https://github.com/tuetschek/e2e-cleaning/raw/master/cleaned-data/devel-fixed.no-ol.csv",
        "test": "https://github.com/tuetschek/e2e-cleaning/raw/master/cleaned-data/test-fixed.csv",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/e2e_nlg.zip",
    },
    "mlsum_de": {
        "train": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_train.zip",
        "validation": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_val.zip",
        "test": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_test.zip",
        "bad_ids": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_mlsum_bad_ids_fixed.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/mlsum_de.zip",
    },
    "mlsum_es": {
        "train": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_train.zip",
        "validation": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_val.zip",
        "test": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_test.zip",
        "bad_ids": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_mlsum_bad_ids_fixed.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/mlsum_es.zip",
    },
    "schema_guided_dialog": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_sgd_context.zip",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/schema_guided_dialog.zip",
    },
    "totto": {
        "data": "https://storage.googleapis.com/totto/totto_data.zip",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/totto.zip",
    },
    "web_nlg_en": {
        "train": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_train.json",
        "validation": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_val.json",
        "test": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_test.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/web_nlg_en.zip",
    },
    "web_nlg_ru": {
        "train": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_train.json",
        "validation": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_val.json",
        "test": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_test.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/web_nlg_ru.zip",
    },
    "wiki_auto_asset_turk": {
        "train": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_with_split/train.tsv",
        "validation": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-auto/GEM2021/full_with_split/valid.tsv",
        "test_turk": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_turk_detokenized.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/wiki_auto_asset_turk_train_valid.zip",
    },
    "wiki_lingua_es_en_v0": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_ru_en_v0": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_tr_en_v0": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_vi_en_v0": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_arabic_ar": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/arabic.zip",
    },
    "wiki_lingua_chinese_zh": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/chinese.zip",
    },
    "wiki_lingua_czech_cs": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/czech.zip",
    },
    "wiki_lingua_dutch_nl": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/dutch.zip",
    },
    "wiki_lingua_english_en": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/english.zip",
    },
    "wiki_lingua_french_fr": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/french.zip",
    },
    "wiki_lingua_german_de": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/german.zip",
    },
    "wiki_lingua_hindi_hi": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/hindi.zip",
    },
    "wiki_lingua_indonesian_id": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/indonesian.zip",
    },
    "wiki_lingua_italian_it": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/italian.zip",
    },
    "wiki_lingua_japanese_ja": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/japanese.zip",
    },
    "wiki_lingua_korean_ko": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/korean.zip",
    },
    "wiki_lingua_portuguese_pt": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/portuguese.zip",
    },
    "wiki_lingua_russian_ru": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/russian.zip",
    },
    "wiki_lingua_spanish_es": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/spanish.zip",
    },
    "wiki_lingua_thai_th": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/thai.zip",
    },
    "wiki_lingua_turkish_tr": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/turkish.zip",
    },
    "wiki_lingua_vietnamese_vi": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua_full/vietnamese.zip",
    },
    "xsum": {
        "data": "http://bollin.inf.ed.ac.uk/public/direct/XSUM-EMNLP18-Summary-Data-Original.tar.gz",
        "splits": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_xsum_confidence_0.8.json",
        "challenge_set": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_challenge_sets/xsum.zip",
    },
}

# Add Asset files
_URLs["wiki_auto_asset_turk"][
    "test_asset_orig"
] = "https://github.com/facebookresearch/asset/raw/master/dataset/asset.test.orig"
for i in range(10):
    _URLs["wiki_auto_asset_turk"][
        f"test_asset_{i}"
    ] = f"https://github.com/facebookresearch/asset/raw/master/dataset/asset.test.simp.{i}"

_SGD_ACTS = [
    "AFFIRM",
    "AFFIRM_INTENT",
    "CONFIRM",
    "GOODBYE",
    "INFORM",
    "INFORM_COUNT",
    "INFORM_INTENT",
    "NEGATE",
    "NEGATE_INTENT",
    "NOTIFY_FAILURE",
    "NOTIFY_SUCCESS",
    "OFFER",
    "OFFER_INTENT",
    "REQUEST",
    "REQUEST_ALTS",
    "REQ_MORE",
    "SELECT",
    "THANK_YOU",
]

_XSUM_REMOVE_LINES = set(
    [
        "Share this with\n",
        "Email\n",
        "Facebook\n",
        "Messenger\n",
        "Twitter\n",
        "Pinterest\n",
        "WhatsApp\n",
        "Linkedin\n",
        "LinkedIn\n",
        "Copy this link\n",
        "These are external links and will open in a new window\n",
    ]
)


class Gem(datasets.GeneratorBasedBuilder):
    """GEM: datasets supporting the Generation Evaluation Metrics 2021 shared task."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name=conf,
            version=datasets.Version("1.1.0"),
            description=f"GEM benchmark: {task} task, {conf} subset",
        )
        for task, dset_confs in _TASKS.items()
        for conf_list in dset_confs.values()
        for conf in conf_list
    ]

    DEFAULT_CONFIG_NAME = "common_gen"  # First alphabetical

    def _info(self):
        if self.config.name == "common_gen":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "concept_set_id": datasets.Value("int32"),
                    "concepts": [datasets.Value("string")],
                    "target": datasets.Value("string"),  # single target for train
                    "references": [datasets.Value("string")],  # multiple references for validation
                }
            )
        elif self.config.name == "cs_restaurants":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "dialog_act": datasets.Value("string"),
                    "dialog_act_delexicalized": datasets.Value("string"),
                    "target_delexicalized": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name == "dart":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "dart_id": datasets.Value("int32"),
                    "tripleset": [[datasets.Value("string")]],  # list of triples
                    "subtree_was_extended": datasets.Value("bool"),
                    "target_sources": [datasets.Value("string")],
                    "target": datasets.Value("string"),  # single target for train
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name == "e2e_nlg":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "meaning_representation": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name.startswith("mlsum"):
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "topic": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name == "schema_guided_dialog":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "dialog_acts": [
                        {
                            "act": datasets.ClassLabel(names=_SGD_ACTS),
                            "slot": datasets.Value("string"),
                            "values": [datasets.Value("string")],
                        }
                    ],
                    "context": [datasets.Value("string")],
                    "dialog_id": datasets.Value("string"),
                    "service": datasets.Value("string"),
                    "turn_id": datasets.Value("int32"),
                    "prompt": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name == "totto":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "totto_id": datasets.Value("int32"),
                    "table_page_title": datasets.Value("string"),
                    "table_webpage_url": datasets.Value("string"),
                    "table_section_title": datasets.Value("string"),
                    "table_section_text": datasets.Value("string"),
                    "table": [
                        [
                            {
                                "column_span": datasets.Value("int32"),
                                "is_header": datasets.Value("bool"),
                                "row_span": datasets.Value("int32"),
                                "value": datasets.Value("string"),
                            }
                        ]
                    ],
                    "highlighted_cells": [[datasets.Value("int32")]],
                    "example_id": datasets.Value("string"),
                    "sentence_annotations": [
                        {
                            "original_sentence": datasets.Value("string"),
                            "sentence_after_deletion": datasets.Value("string"),
                            "sentence_after_ambiguity": datasets.Value("string"),
                            "final_sentence": datasets.Value("string"),
                        }
                    ],
                    "overlap_subset": datasets.Value("string"),
                    "target": datasets.Value("string"),  # single target for train
                    "references": [datasets.Value("string")],
                },
            )
        elif self.config.name.startswith("web_nlg"):
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "input": [datasets.Value("string")],
                    "target": datasets.Value("string"),  # single target for train
                    "references": [datasets.Value("string")],
                    "category": datasets.Value("string"),
                    "webnlg_id": datasets.Value("string"),
                }
            )
        elif self.config.name == "wiki_auto_asset_turk":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name.startswith("wiki_lingua"):
            if "v0" in self.config.name:
                features = datasets.Features(
                    {
                        "gem_id": datasets.Value("string"),
                        "gem_parent_id": datasets.Value("string"),
                        "source": datasets.Value("string"),
                        "target": datasets.Value("string"),
                        "references": [datasets.Value("string")],
                    }
                )
            else:
                ln = self.config.name.split("_")[-1]
                features = datasets.Features(
                    {
                        "gem_id": datasets.Value("string"),
                        "gem_parent_id": datasets.Value("string"),
                        "source_aligned": datasets.Translation(languages=[ln, "en"]),
                        "target_aligned": datasets.Translation(languages=[ln, "en"]),
                        "source": datasets.Value("string"),
                        "target": datasets.Value("string"),
                        "references": [datasets.Value("string")],
                    }
                )
        elif self.config.name == "xsum":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "gem_parent_id": datasets.Value("string"),
                    "xsum_id": datasets.Value("string"),
                    "document": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
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
        dl_dir = dl_manager.download_and_extract(_URLs[self.config.name])
        if self.config.name == "common_gen":
            challenge_sets = [
                ("challenge_train_sample", "train_common_gen_RandomSample500.json"),
                ("challenge_validation_sample", "validation_common_gen_RandomSample500.json"),
                ("challenge_test_scramble", "test_common_gen_ScrambleInputStructure500.json"),
            ]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "commongen.train.jsonl"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "commongen.dev.jsonl"),
                        "split": "validation",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "commongen.test_noref.jsonl"),
                        "split": "test",
                    },
                ),
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name == "cs_restaurants":
            challenge_sets = [
                ("challenge_train_sample", "train_cs_restaurants_RandomSample500.json"),
                ("challenge_validation_sample", "validation_cs_restaurants_RandomSample500.json"),
                ("challenge_test_scramble", "test_cs_restaurants_ScrambleInputStructure500.json"),
            ]
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name == "dart":
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name == "e2e_nlg":
            challenge_sets = [
                ("challenge_train_sample", "train_e2e_nlg_RandomSample500.json"),
                ("challenge_validation_sample", "validation_e2e_nlg_RandomSample500.json"),
                ("challenge_test_scramble", "test_e2e_nlg_ScrambleInputStructure500.json"),
            ]
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name.startswith("mlsum"):
            lang = self.config.name.split("_")[1]
            challenge_sets = [
                ("challenge_train_sample", f"train_mlsum_{lang}_RandomSample500.json"),
                ("challenge_validation_sample", f"validation_mlsum_{lang}_RandomSample500.json"),
                ("challenge_test_covid", f"{lang}_test_covid19_cleaned.jsonl"),
            ]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["train"], lang + "_train.jsonl"),
                        "split": "train",
                        "lang": lang,
                        "filepaths": dl_dir["bad_ids"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["validation"], lang + "_val.jsonl"),
                        "split": "validation",
                        "lang": lang,
                        "filepaths": dl_dir["bad_ids"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["test"], lang + "_test.jsonl"),
                        "split": "test",
                        "lang": lang,
                        "filepaths": dl_dir["bad_ids"],
                    },
                ),
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name == "schema_guided_dialog":
            challenge_sets = [
                ("challenge_train_sample", "train_schema_guided_dialog_RandomSample500_reformatted.json"),
                ("challenge_validation_sample", "validation_schema_guided_dialog_RandomSample500_reformatted.json"),
                ("challenge_test_backtranslation", "test_schema_guided_dialog_BackTranslation500_reformatted.json"),
                (
                    "challenge_test_bfp02",
                    "test_schema_guided_dialog_ButterFingersPerturbation_p=0.02_500_reformatted.json",
                ),
                (
                    "challenge_test_bfp05",
                    "test_schema_guided_dialog_ButterFingersPerturbation_p=0.05_500_reformatted.json",
                ),
                ("challenge_test_nopunc", "test_schema_guided_dialog_WithoutPunctuation500_reformatted.json"),
                ("challenge_test_scramble", "test_schema_guided_dialog_ScrambleInputStructure500_reformatted.json"),
            ]
            return [
                datasets.SplitGenerator(
                    name=spl, gen_kwargs={"filepath": os.path.join(dl_dir["data"], "gem_sgd.json"), "split": spl}
                )
                for spl in ["train", "validation", "test"]
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name == "totto":
            challenge_sets = [
                ("challenge_train_sample", "train_totto_RandomSample500.json"),
                ("challenge_validation_sample", "validation_totto_RandomSample500.json"),
                ("challenge_test_scramble", "test_totto_ScrambleInputStructure500.json"),
            ]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "totto_data/totto_train_data.jsonl"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "totto_data/totto_dev_data.jsonl"),
                        "split": "validation",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["data"], "totto_data/unlabeled_totto_test_data.jsonl"),
                        "split": "test",
                    },
                ),
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name.startswith("web_nlg"):
            ln = self.config.name.split("_")[-1]
            challenge_sets = [
                ("challenge_train_sample", f"train_web_nlg_{ln}_RandomSample500.json"),
                ("challenge_validation_sample", f"validation_web_nlg_{ln}_RandomSample500.json"),
                ("challenge_test_scramble", f"test_web_nlg_{ln}_ScrambleInputStructure500.json"),
            ]
            if ln == "en":
                challenge_sets += [("challenge_test_numbers", f"test_web_nlg_{ln}_replace_numbers_500.json")]
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], self.config.name, filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name == "wiki_auto_asset_turk":
            challenge_sets = [
                ("challenge_train_sample", "train_wiki_auto_asset_turk_RandomSample500.json"),
                ("challenge_validation_sample", "validation_wiki_auto_asset_turk_RandomSample500.json"),
                ("challenge_test_asset_backtranslation", "test_asset_wiki_auto_asset_turk_BackTranslation.json"),
                (
                    "challenge_test_asset_bfp02",
                    "test_asset_wiki_auto_asset_turk_ButterFingersPerturbation_p=0.02.json",
                ),
                (
                    "challenge_test_asset_bfp05",
                    "test_asset_wiki_auto_asset_turk_ButterFingersPerturbation_p=0.05.json",
                ),
                ("challenge_test_asset_nopunc", "test_asset_wiki_auto_asset_turk_WithoutPunctuation.json"),
                ("challenge_test_turk_backtranslation", "detok_test_turk_wiki_auto_asset_turk_BackTranslation.json"),
                (
                    "challenge_test_turk_bfp02",
                    "detok_test_turk_wiki_auto_asset_turk_ButterFingersPerturbation_p=0.02.json",
                ),
                (
                    "challenge_test_turk_bfp05",
                    "detok_test_turk_wiki_auto_asset_turk_ButterFingersPerturbation_p=0.05.json",
                ),
                ("challenge_test_turk_nopunc", "detok_test_turk_wiki_auto_asset_turk_WithoutPunctuation.json"),
            ]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": dl_dir["train"],
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": dl_dir["validation"],
                        "split": "validation",
                    },
                ),
                datasets.SplitGenerator(
                    name="test_asset",
                    gen_kwargs={
                        "filepath": "",
                        "split": "test_asset",
                        "filepaths": [dl_dir["test_asset_orig"]] + [dl_dir[f"test_asset_{i}"] for i in range(10)],
                    },
                ),
                datasets.SplitGenerator(
                    name="test_turk",
                    gen_kwargs={
                        "filepath": dl_dir["test_turk"],
                        "split": "test_turk",
                    },
                ),
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], "wiki_auto_asset_turk", filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]
        elif self.config.name.startswith("wiki_lingua"):
            if "v0" in self.config.name:
                lang = self.config.name.split("_")[-3]
                base_dir = os.path.join(dl_dir["data"], "GEM_data_crosslingual", f"{lang}_en")
                return [
                    datasets.SplitGenerator(
                        name=datasets.Split.TRAIN,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "train",
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.VALIDATION,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "val",
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.TEST,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "test",
                        },
                    ),
                ]
            else:
                lang_name = self.config.name.split("_")[-2]
                lang = self.config.name.split("_")[-1]
                base_dir = os.path.join(dl_dir["data"], lang_name)
                return [
                    datasets.SplitGenerator(
                        name=datasets.Split.TRAIN,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "train",
                            "lang": lang,
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.VALIDATION,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "val",
                            "lang": lang,
                        },
                    ),
                    datasets.SplitGenerator(
                        name=datasets.Split.TEST,
                        gen_kwargs={
                            "filepath": base_dir,
                            "split": "test",
                            "lang": lang,
                        },
                    ),
                ]
        elif self.config.name == "xsum":
            challenge_sets = [
                ("challenge_train_sample", "train_xsum_RandomSample500.json"),
                ("challenge_validation_sample", "validation_xsum_RandomSample500.json"),
                ("challenge_test_backtranslation", "test_xsum_BackTranslation500.json"),
                ("challenge_test_bfp_02", "test_xsum_ButterFingersPerturbation_p=0.02_500.json"),
                ("challenge_test_bfp_05", "test_xsum_ButterFingersPerturbation_p=0.05_500.json"),
                ("challenge_test_nopunc", "test_xsum_WithoutPunctuation500.json"),
                ("challenge_test_covid", "en_test_covid19.jsonl"),
            ]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": dl_dir["splits"],
                        "split": "train",
                        "filepaths": os.path.join(dl_dir["data"], "bbc-summary-data"),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": dl_dir["splits"],
                        "split": "validation",
                        "filepaths": os.path.join(dl_dir["data"], "bbc-summary-data"),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": dl_dir["splits"],
                        "split": "test",
                        "filepaths": os.path.join(dl_dir["data"], "bbc-summary-data"),
                    },
                ),
            ] + [
                datasets.SplitGenerator(
                    name=challenge_split,
                    gen_kwargs={
                        "filepath": os.path.join(dl_dir["challenge_set"], "xsum", filename),
                        "split": challenge_split,
                    },
                )
                for challenge_split, filename in challenge_sets
            ]

    def _generate_examples(self, filepath, split, filepaths=None, lang=None):
        """Yields examples."""
        if self.config.name == "common_gen":
            if split.startswith("challenge"):
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                with open(filepath, encoding="utf-8") as f:
                    id_ = -1
                    i = -1
                    for row in f:
                        row = row.replace(", }", "}")  # Fix possible JSON format error
                        data = json.loads(row)
                        concepts = [word for word in data["concept_set"].split("#")]
                        if split == "train":
                            i += 1
                            for scene in data["scene"]:
                                id_ += 1
                                yield id_, {
                                    "gem_id": f"{self.config.name}-{split}-{id_}",
                                    "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                    "concept_set_id": i,
                                    "concepts": concepts,
                                    "target": scene,
                                    "references": [],
                                }
                        else:
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "concept_set_id": id_,
                                "concepts": concepts,
                                "target": "" if split == "test" else data["scene"][0],
                                "references": [] if split == "test" else data["scene"],
                            }
        elif self.config.name == "cs_restaurants":
            if split.startswith("challenge"):
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                with open(filepath, encoding="utf8") as f:
                    data = json.load(f)
                    for id_, instance in enumerate(data):
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                            "dialog_act": instance["da"],
                            "dialog_act_delexicalized": instance["delex_da"],
                            "target": instance["text"],
                            "target_delexicalized": instance["delex_text"],
                            "references": [] if split == "train" else [instance["text"]],
                        }
        elif self.config.name == "dart":
            with open(filepath, encoding="utf-8") as f:
                data = json.loads(f.read())
                id_ = -1
                i = -1
                for example in data:
                    if split == "train":
                        i += 1
                        for annotation in example["annotations"]:
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "dart_id": i,
                                "tripleset": example["tripleset"],
                                "subtree_was_extended": example.get("subtree_was_extended", None),  # some are missing
                                "target_sources": [annotation["source"] for annotation in example["annotations"]],
                                "target": annotation["text"],
                                "references": [],
                            }
                    else:
                        id_ += 1
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                            "dart_id": id_,
                            "tripleset": example["tripleset"],
                            "subtree_was_extended": example.get("subtree_was_extended", None),  # some are missing
                            "target_sources": [annotation["source"] for annotation in example["annotations"]],
                            "target": example["annotations"][0]["text"] if len(example["annotations"]) > 0 else "",
                            "references": [annotation["text"] for annotation in example["annotations"]],
                        }
        elif self.config.name == "e2e_nlg":
            if split.startswith("challenge"):
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                with open(filepath, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for id_, example in enumerate(reader):
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                            "meaning_representation": example["mr"],
                            "target": example["ref"],
                            "references": [] if split == "train" else [example["ref"]],
                        }
        elif self.config.name.startswith("mlsum"):
            if split in ["train", "validation", "test", "challenge_test_covid"]:
                if split == "challenge_test_covid":
                    bad_ids = {}
                else:
                    bad_ids_dct = json.load(open(filepaths, encoding="utf-8"))
                    bad_ids = dict((bad_url, True) for _, bad_url in bad_ids_dct[f"{lang}-{split}"])
                with open(filepath, encoding="utf-8") as f:
                    id_ = -1
                    for line in f:
                        data = json.loads(line)
                        if data["url"] in bad_ids:
                            continue
                        else:
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "text": data["text"],
                                "target": data["summary"],
                                "references": [] if split == "train" else [data["summary"]],
                                "topic": data["topic"],
                                "url": data["url"],
                                "title": data["title"],
                                "date": data["date"],
                            }
            else:
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
        elif self.config.name == "schema_guided_dialog":
            if "challenge" in split:
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                examples = json.load(open(filepath, encoding="utf-8"))[split]
                for id_, example in enumerate(examples):
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
                        "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                        "dialog_acts": [
                            {
                                "act": act_id,
                                "slot": slot,
                                "values": values,
                            }
                            for act_id, slot, values in example["da"]
                        ],
                        "context": example["context"],
                        "dialog_id": example["dialog_id"],
                        "service": example["service"],
                        "turn_id": example["turn_ix"],
                        "prompt": example["prompt"],
                        "target": example["target"],
                        "references": [] if split == "train" else [example["target"]],
                    }
        elif self.config.name == "totto":
            if "challenge" in split:
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                with open(filepath, "r", encoding="utf-8") as json_file:
                    json_list = list(json_file)
                id_ = -1
                i = -1
                for json_str in json_list:
                    result = json.loads(json_str)
                    if split == "train":
                        i += 1
                        for sentence in result["sentence_annotations"]:
                            id_ += 1
                            response = {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "totto_id": i,
                                "table_page_title": result["table_page_title"],
                                "table_webpage_url": result["table_webpage_url"],
                                "table_section_title": result["table_section_title"],
                                "table_section_text": result["table_section_text"],
                                "table": result["table"],
                                "highlighted_cells": result["highlighted_cells"],
                                "example_id": str(result["example_id"]),
                                "overlap_subset": "none",
                                "sentence_annotations": [sentence],
                                "references": [],
                                "target": sentence["final_sentence"],
                            }
                            yield id_, response
                    else:
                        id_ += 1
                        response = {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                            "totto_id": id_,
                            "table_page_title": result["table_page_title"],
                            "table_webpage_url": result["table_webpage_url"],
                            "table_section_title": result["table_section_title"],
                            "table_section_text": result["table_section_text"],
                            "table": result["table"],
                            "highlighted_cells": result["highlighted_cells"],
                            "example_id": str(result["example_id"]),
                            "overlap_subset": str(result["overlap_subset"]),
                        }
                        response["sentence_annotations"] = [] if split == "test" else result["sentence_annotations"]
                        response["references"] = [
                            sentence["final_sentence"] for sentence in response["sentence_annotations"]
                        ]
                        response["target"] = response["references"][0] if len(response["references"]) > 0 else ""
                        yield id_, response
        elif self.config.name.startswith("web_nlg"):
            if "challenge" in split:
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    if len(exple) == 0:
                        continue
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    yield id_, exple
            else:
                with open(filepath, encoding="utf-8") as f:
                    examples = json.load(f)
                    id_ = -1
                    for example in examples["values"]:
                        if split == "train":
                            for target in example["target"]:
                                id_ += 1
                                yield id_, {
                                    "gem_id": f"{self.config.name}-{split}-{id_}",
                                    "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                    "input": example["input"],
                                    "target": target,
                                    "references": [] if split == "train" else example["target"],
                                    "category": example["category"],
                                    "webnlg_id": example["webnlg-id"],
                                }
                        else:
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "input": example["input"],
                                "target": example["target"][0] if len(example["target"]) > 0 else "",
                                "references": example["target"],
                                "category": example["category"],
                                "webnlg_id": example["webnlg-id"],
                            }
        elif self.config.name == "wiki_auto_asset_turk":
            if split in ["train", "validation"]:
                keys = [
                    "source",
                    "target",
                ]
                with open(filepath, encoding="utf-8") as f:
                    for id_, line in enumerate(f):
                        values = line.strip().split("\t")
                        assert len(values) == 2, f"Not enough fields in ---- {line} --- {values}"
                        example = dict([(k, val) for k, val in zip(keys, values)])
                        example["gem_id"] = f"{self.config.name}-{split}-{id_}"
                        example["gem_parent_id"] = example["gem_id"]
                        example["references"] = [] if split == "train" else [example["target"]]
                        yield id_, example
            elif split == "test_turk":
                examples = json.load(open(filepath, encoding="utf-8"))
                for id_, example in enumerate(examples):
                    example["gem_parent_id"] = example["gem_id"]
                    for k in ["source_id", "target_id"]:
                        if k in example:
                            del example[k]
                    yield id_, example
            elif split == "test_asset":
                files = [open(f_name, encoding="utf-8") for f_name in filepaths]
                for id_, lines in enumerate(zip(*files)):
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
                        "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                        "target": lines[1].strip(),
                        "source": lines[0].strip(),
                        "references": [line.strip() for line in lines[1:]],
                    }
            else:
                exples = json.load(open(filepath, encoding="utf-8"))
                if isinstance(exples, dict):
                    assert len(exples) == 1, "multiple entries found"
                    exples = list(exples.values())[0]
                for id_, exple in enumerate(exples):
                    exple["gem_parent_id"] = exple["gem_id"]
                    exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                    for k in ["source_id", "target_id"]:
                        if k in exple:
                            del exple[k]
                    yield id_, exple
        elif self.config.name.startswith("wiki_lingua"):
            if "v0" in self.config.name:
                with open(os.path.join(filepath, f"{split}.src"), encoding="utf-8") as f_in:
                    with open(os.path.join(filepath, f"{split}.tgt"), encoding="utf-8") as f_out:
                        for id_, (src, tgt) in enumerate(zip(f_in, f_out)):
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "source": src.strip(),
                                "target": tgt.strip(),
                                "references": [] if split == "train" else [tgt.strip()],
                            }
            else:
                with open(os.path.join(filepath, f"{split}.src.{lang}"), encoding="utf-8") as f_in_ln:
                    with open(os.path.join(filepath, f"{split}.src.en"), encoding="utf-8") as f_in_en:
                        with open(os.path.join(filepath, f"{split}.tgt.{lang}"), encoding="utf-8") as f_out_ln:
                            with open(os.path.join(filepath, f"{split}.tgt.en"), encoding="utf-8") as f_out_en:
                                for id_, (src_ln, src_en, tgt_ln, tgt_en) in enumerate(
                                    zip(f_in_ln, f_in_en, f_out_ln, f_out_en)
                                ):
                                    yield id_, {
                                        "gem_id": f"{self.config.name}-{split}-{id_}",
                                        "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                        "source_aligned": {lang: src_ln.strip(), "en": src_en.strip()},
                                        "target_aligned": {lang: tgt_ln.strip(), "en": tgt_en.strip()},
                                        "source": src_ln.strip(),
                                        "target": tgt_en.strip(),
                                        "references": [] if split == "train" else [tgt_en.strip()],
                                    }
        elif self.config.name == "xsum":
            if "challenge" in split:
                if "covid" in split:
                    with open(filepath, encoding="utf-8") as f:
                        id_ = -1
                        for line in f:
                            data = json.loads(line)
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
                                "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                                "xsum_id": data["url"],
                                "document": data["text"],
                                "target": data["summary"],
                                "references": [] if split == "train" else [data["summary"]],
                            }
                else:
                    exples = json.load(open(filepath, encoding="utf-8"))
                    if isinstance(exples, dict):
                        assert len(exples) == 1, "multiple entries found"
                        exples = list(exples.values())[0]
                    for id_, exple in enumerate(exples):
                        exple["gem_parent_id"] = exple["gem_id"]
                        exple["gem_id"] = f"{self.config.name}-{split}-{id_}"
                        yield id_, exple
            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    split_ids = json.load(f)
                for id_, i in enumerate(split_ids[split]):
                    with open(os.path.join(filepaths, i + ".summary"), "r", encoding="utf-8") as f:
                        text = "".join(
                            [line for line in f.readlines() if line not in _XSUM_REMOVE_LINES and line.strip()]
                        )
                        segs = text.split("[SN]")
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "gem_parent_id": f"{self.config.name}-{split}-{id_}",
                            "xsum_id": i,
                            "document": segs[8].strip(),
                            "target": segs[6].strip(),
                            "references": [] if split == "train" else [segs[6].strip()],
                        }
