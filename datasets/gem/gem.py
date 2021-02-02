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

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
authors={huggingface, Inc.
},
year={2020}
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
        "wiki_lingua": ["wiki_lingua_es_en", "wiki_lingua_ru_en", "wiki_lingua_tr_en", "wiki_lingua_vi_en"],
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
    },
    "cs_restaurants": {
        "train": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/train.json",
        "validation": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/devel.json",
        "test": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/test.json",
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
    },
    "mlsum_de": {
        "train": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_train.zip",
        "validation": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_val.zip",
        "test": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/de_test.zip",
        "bad_ids": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_mlsum_bad_ids.json",
    },
    "mlsum_es": {
        "train": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_train.zip",
        "validation": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_val.zip",
        "test": "https://gitlab.lip6.fr/scialom/mlsum_data/-/raw/master/MLSUM/es_test.zip",
        "bad_ids": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_mlsum_bad_ids.json",
    },
    "schema_guided_dialog": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_sgd.json.zip",
    },
    "totto": {
        "data": "https://storage.googleapis.com/totto/totto_data.zip",
    },
    "web_nlg_en": {
        "train": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_train.json",
        "validation": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_val.json",
        "test": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_en_test.json",
    },
    "web_nlg_ru": {
        "train": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_train.json",
        "validation": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_val.json",
        "test": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_web_nlg/webnlg_ru_test.json",
    },
    "wiki_auto_asset_turk": {
        "train": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-manual/train.tsv",
        "validation": "https://github.com/chaojiang06/wiki-auto/raw/master/wiki-manual/dev.tsv",
    },
    "wiki_lingua_es_en": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_ru_en": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_tr_en": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "wiki_lingua_vi_en": {
        "data": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_wikilingua.zip",
    },
    "xsum": {
        "data": "http://bollin.inf.ed.ac.uk/public/direct/XSUM-EMNLP18-Summary-Data-Original.tar.gz",
        "splits": "https://storage.googleapis.com/huggingface-nlp/datasets/gem/gem_xsum_confidence_0.8.json",
    },
}

# Add Turk and Asset files
for i in range(10):
    _URLs["wiki_auto_asset_turk"][
        f"test_asset_{i}"
    ] = f"https://github.com/facebookresearch/asset/raw/master/dataset/asset.test.simp.{i}"

for i in range(8):
    _URLs["wiki_auto_asset_turk"][
        f"test_turk_{i}"
    ] = f"https://raw.githubusercontent.com/cocoxu/simplification/master/data/turkcorpus/GEM/test.8turkers.tok.turk.{i}"

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
            version=datasets.Version("1.0.0"),
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
                    "meaning_representation": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name.startswith("mlsum"):
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
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
                    "dialog_acts": [
                        {
                            "act": datasets.ClassLabel(names=_SGD_ACTS),
                            "slot": datasets.Value("string"),
                            "values": [datasets.Value("string")],
                        }
                    ],
                    "dialog_id": datasets.Value("string"),
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
                    "source_id": datasets.Value("string"),
                    "target_id": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name.startswith("wiki_lingua"):
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
                    "source": datasets.Value("string"),
                    "target": datasets.Value("string"),
                    "references": [datasets.Value("string")],
                }
            )
        elif self.config.name == "xsum":
            features = datasets.Features(
                {
                    "gem_id": datasets.Value("string"),
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
            ]
        elif self.config.name == "cs_restaurants":
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name == "dart":
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name == "e2e_nlg":
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name.startswith("mlsum"):
            lang = self.config.name.split("_")[1]
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
            ]
        elif self.config.name == "schema_guided_dialog":
            return [
                datasets.SplitGenerator(
                    name=spl, gen_kwargs={"filepath": os.path.join(dl_dir["data"], "gem_sgd.json"), "split": spl}
                )
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name == "totto":
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
            ]
        elif self.config.name.startswith("web_nlg"):
            return [
                datasets.SplitGenerator(name=spl, gen_kwargs={"filepath": dl_dir[spl], "split": spl})
                for spl in ["train", "validation", "test"]
            ]
        elif self.config.name == "wiki_auto_asset_turk":
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
                        "split": "test",
                        "filepaths": [dl_dir[f"test_asset_{i}"] for i in range(10)],
                    },
                ),
                datasets.SplitGenerator(
                    name="test_turk",
                    gen_kwargs={
                        "filepath": "",
                        "split": "test",
                        "filepaths": [dl_dir[f"test_turk_{i}"] for i in range(8)],
                    },
                ),
            ]
        elif self.config.name.startswith("wiki_lingua"):
            lang = self.config.name.split("_")[-2]
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
        elif self.config.name == "xsum":
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
            ]

    def _generate_examples(self, filepath, split, filepaths=None, lang=None):
        """ Yields examples. """
        if self.config.name == "common_gen":
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
                                "concept_set_id": i,
                                "concepts": concepts,
                                "target": scene,
                                "references": [],
                            }
                    else:
                        id_ += 1
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "concept_set_id": id_,
                            "concepts": concepts,
                            "target": "" if split == "test" else data["scene"][0],
                            "references": [] if split == "test" else data["scene"],
                        }
        elif self.config.name == "cs_restaurants":
            with open(filepath, encoding="utf8") as f:
                data = json.load(f)
                for id_, instance in enumerate(data):
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
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
                            "dart_id": id_,
                            "tripleset": example["tripleset"],
                            "subtree_was_extended": example.get("subtree_was_extended", None),  # some are missing
                            "target_sources": [annotation["source"] for annotation in example["annotations"]],
                            "target": example["annotations"][0]["text"] if len(example["annotations"]) > 0 else "",
                            "references": [annotation["text"] for annotation in example["annotations"]],
                        }
        elif self.config.name == "e2e_nlg":
            with open(filepath, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for id_, example in enumerate(reader):
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
                        "meaning_representation": example["mr"],
                        "target": example["ref"],
                        "references": [] if split == "train" else [example["ref"]],
                    }
        elif self.config.name.startswith("mlsum"):
            bad_ids_dct = json.load(open(filepaths, encoding="utf-8"))
            bad_ids = dict((bad_url, True) for _, bad_url in bad_ids_dct[f"{lang}-{split}"])
            with open(filepath, encoding="utf-8") as f:
                id_ = -1
                for line in f:
                    data = json.loads(line)
                    if data["url"] in bad_ids:  # TODO : check | i or i-1?
                        continue
                    else:
                        id_ += 1
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "text": data["text"],
                            "target": data["summary"],
                            "references": [] if split == "train" else [data["summary"]],
                            "topic": data["topic"],
                            "url": data["url"],
                            "title": data["title"],
                            "date": data["date"],
                        }
        elif self.config.name == "schema_guided_dialog":
            examples = json.load(open(filepath, encoding="utf-8"))[split]
            for id_, example in enumerate(examples):
                yield id_, {
                    "gem_id": f"{self.config.name}-{split}-{id_}",
                    "dialog_acts": [
                        {
                            "act": act_id,
                            "slot": slot,
                            "values": values,
                        }
                        for act_id, slot, values in example["da"]
                    ],
                    "dialog_id": example["dialog_id"],
                    "turn_id": example["turn_ix"],
                    "prompt": example["prompt"],
                    "target": example["target"],
                    "references": [] if split == "train" else [example["target"]],
                }
        elif self.config.name == "totto":
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
            with open(filepath, encoding="utf-8") as f:
                examples = json.load(f)
                id_ = -1
                for example in examples["values"]:
                    if split == "train":
                        for target in example["target"]:
                            id_ += 1
                            yield id_, {
                                "gem_id": f"{self.config.name}-{split}-{id_}",
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
                            "input": example["input"],
                            "target": example["target"][0] if len(example["target"]) > 0 else "",
                            "references": example["target"],
                            "category": example["category"],
                            "webnlg_id": example["webnlg-id"],
                        }
        elif self.config.name == "wiki_auto_asset_turk":
            if split in ["train", "validation"]:
                keys = [
                    "target_id",
                    "source_id",
                    "target",
                    "source",
                ]
                with open(filepath, encoding="utf-8") as f:
                    for id_, line in enumerate(f):
                        values = line.strip().split("\t")
                        assert len(values) == 5, f"Not enough fields in ---- {line} --- {values}"
                        example = dict([(k, val) for k, val in zip(keys, values[1:])])
                        example["gem_id"] = f"{self.config.name}-{split}-{id_}"
                        example["references"] = [] if split == "train" else [example["target"]]
                        yield id_, example
            elif split.startswith("test"):
                files = [open(f_name, encoding="utf-8") for f_name in filepaths]
                for id_, lines in enumerate(zip(*files)):
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
                        "source_id": "",
                        "target_id": "",
                        "target": lines[1].strip(),
                        "source": lines[0].strip(),
                        "references": [line.strip() for line in lines[1:]],
                    }
        elif self.config.name.startswith("wiki_lingua"):
            with open(os.path.join(filepath, f"{split}.src"), encoding="utf-8") as f_in:
                with open(os.path.join(filepath, f"{split}.tgt"), encoding="utf-8") as f_out:
                    for id_, (src, tgt) in enumerate(zip(f_in, f_out)):
                        yield id_, {
                            "gem_id": f"{self.config.name}-{split}-{id_}",
                            "source": src.strip(),
                            "target": tgt.strip(),
                            "references": [] if split == "train" else [tgt.strip()],
                        }
        elif self.config.name == "xsum":
            with open(filepath, "r", encoding="utf-8") as f:
                split_ids = json.load(f)
            for id_, i in enumerate(split_ids[split]):
                with open(os.path.join(filepaths, i + ".summary"), "r", encoding="utf-8") as f:
                    text = "".join([line for line in f.readlines() if line not in _XSUM_REMOVE_LINES and line.strip()])
                    segs = text.split("[SN]")
                    yield id_, {
                        "gem_id": f"{self.config.name}-{split}-{id_}",
                        "xsum_id": i,
                        "document": segs[8].strip(),
                        "target": segs[6].strip(),
                        "references": [] if split == "train" else [segs[6].strip()],
                    }
