# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3

import csv
import os

import pandas as pd

import datasets


_CITATION = ""

_DESCRIPTION = ""

XX_EN_LANGUAGES = [
    "fr",
    "de",
    "es",
    "ca",
    "it",
    "ru",
    "zh-CN",
    "pt",
    "fa",
    "et",
    "mn",
    "nl",
    "tr",
    "ar",
    "sv-SE",
    "lv",
    "sl",
    "ta",
    "ja",
    "id",
    "cy",
]


EN_XX_LANGUAGES = [
    "de",
    "tr",
    "fa",
    "sv-SE",
    "mn",
    "zh-CN",
    "cy",
    "ca",
    "sl",
    "et",
    "id",
    "ar",
    "ta",
    "lv",
    "ja",
]

COVOST_URL_TEMPLATE = "https://dl.fbaipublicfiles.com/covost/" "covost_v2.{src_lang}_{tgt_lang}.tsv.tar.gz"


def _get_builder_configs():
    builder_configs = [
        datasets.BuilderConfig(name=f"en-{lang}", version=datasets.Version()) for lang in EN_XX_LANGUAGES
    ]

    builder_configs += [
        datasets.BuilderConfig(name=f"{lang}-en", version=datasets.Version()) for lang in XX_EN_LANGUAGES
    ]
    return builder_configs


class Covost2(datasets.GeneratorBasedBuilder):
    """CoVOST2 Dataset."""

    VERSION = datasets.Version("")

    BUILDER_CONFIGS = _get_builder_configs()

    @property
    def manual_download_instructions(self):
        return "Manual download"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                client_id=datasets.Value("string"),
                path=datasets.Value("string"),
                sentence=datasets.Value("string"),
                translation=datasets.Value("string"),
                id=datasets.Value("string"),
            ),
            supervised_keys=("path", "sentence", "translation"),
            homepage="",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_root = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        source_lang, target_lang = self.config.name.split("-")
        source_path = os.path.join(data_root, source_lang)

        if not os.path.exists(source_path):
            raise FileNotFoundError("source path not found")

        covost_url = COVOST_URL_TEMPLATE.format(src_lang=source_lang, tgt_lang=target_lang)
        extracted_path = dl_manager.download_and_extract(covost_url)

        covost_tsv_path = os.path.join(extracted_path, f"covost_v2.{source_lang}_{target_lang}")
        cv_tsv_path = os.path.join(source_path, "validated.tsv")

        covost_tsv = self._load_df_from_tsv(covost_tsv_path)
        cv_tsv = self._load_df_from_tsv(cv_tsv_path)

        df = pd.merge(
            left=cv_tsv[["path", "sentence", "client_id"]],
            right=covost_tsv[["path", "translation", "split"]],
            how="inner",
            on="path",
        )

        train_df = df[(df["split"] == "train") | (df["split"] == f"train_covost")]
        valid_df = df[df["split"] == "dev"]
        test_df = df[df["split"] == "test"]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"df": train_df, "source_path": source_path}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"df": valid_df, "source_path": source_path}
            ),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"df": test_df, "source_path": source_path}),
        ]

    def _get_builder_conifgs(self, df, source_path):
        for i, row in df.iterrows():
            yield i, {
                "id": row["path"].replace(".mp3", ""),
                "client_id": row["client_id"],
                "sentence": row["sentence"],
                "translation": row["translation"],
                "path": os.path.join(source_path, "clips", row["path"]),
            }

    def _load_df_from_tsv(self, path):
        return pd.read_csv(
            path,
            sep="\t",
            header=0,
            encoding="utf-8",
            escapechar="\\",
            quoting=csv.QUOTE_NONE,
            na_filter=False,
        )
