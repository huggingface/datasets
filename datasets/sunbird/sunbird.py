# coding=utf-8
# Copyright 2021 Sunbird AI.
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
"""Sunbird AI machine translation benchmark dataset."""


import collections

import datasets


_DESCRIPTION = """\
Evaluation datasets for low-resource machine translation: Luganda-English.
"""

_CITATION = """\
        TO ADD: Sunbird citation
"""

_VERSION = "1.0.0"
_TRAIN_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/train.en"
_TEST_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/test.en"
_VAL_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/val.en"
_TRAIN_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/train.lg"
_TEST_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/test.lg"
_VAL_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-datasets/main/val.lg"

_LANGUAGE_PAIRS = [
    ("lg", "en"),
]


# https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/train.en
# Tuple that describes a single pair of files with matching translations.
# language_to_file is the map from language (2 letter string: example 'en')
# to the file path in the extracted directory.
# TranslateData = collections.namedtuple("TranslateData", ["url", "language_to_file"])


class SunbirdConfig(datasets.BuilderConfig):
    """BuilderConfig for Sunbird."""
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class Sunbird(datasets.GeneratorBasedBuilder):
    """Sunbird machine translation dataset."""

    BUILDER_CONFIGS = [
        SunbirdConfig(
            lang1=lang1,
            lang2= lang2,
            description = f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = SunbirdConfig


    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "translation": datasets.Translation(languages=(self.config.lang1, self.config.lang2)),
                 },
            ),
            supervised_keys=None,
            homepage="https://sunbird.ai/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_en = dl_manager.download_and_extract(_TRAIN_EN)
        train_lg = dl_manager.download_and_extract(_TRAIN_LG)

        valid_en = dl_manager.download_and_extract(_VAL_EN)
        valid_lg = dl_manager.download_and_extract(_VAL_LG)

        test_en = dl_manager.download_and_extract(_TEST_EN)
        test_lg = dl_manager.download_and_extract(_TEST_LG)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"lg_datapath": train_lg, "en_datapath": train_en},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"lg_datapath": valid_lg, "en_datapath": valid_en},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"lg_datapath": test_lg, "en_datapath": test_en},
            ),
        ]

    def _generate_examples(self, lg_datapath, en_datapath):
        with open(lg_datapath, encoding="utf-8") as f1, open(en_datapath, encoding="utf-8") as f2:
            for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                x = x.strip()
                y = y.strip()
                print(x)
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "translation": {"lg": x, "en": y},
                    },
                )
                yield result
