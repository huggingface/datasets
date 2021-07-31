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

# _TRAIN_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/train.en"
# _TEST_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/test.en"
# _VAL_EN = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/val.en"

# _TRAIN_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/train.lg"
# _TEST_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/test.lg"
# _VAL_LG = "https://raw.githubusercontent.com/SunbirdAI/toy-hf-datasets/main/val.lg"

_TRAIN_ACH = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.ach"
_TEST_ACH = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.ach"
_VAL_ACH = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.ach"

_TRAIN_LGG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.lgg"
_TEST_LGG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.lgg"
_VAL_LGG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/val.lgg"

_TRAIN_TEO = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.teo"
_TEST_TEO = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.teo"
_VAL_TEO = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/val.teo"

_TRAIN_RUN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.run"
_TEST_RUN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.run"
_VAL_RUN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/val.run"

_TRAIN_EN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.en"
_TEST_EN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.en"
_VAL_EN = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/val.en"

_TRAIN_LUG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/train.lug"
_TEST_LUG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/test.lug"
_VAL_LUG = "https://sunbird-translate.s3.us-east-2.amazonaws.com/sunbird-ug-lang-v1.0/val.lug"

_LANGUAGE_PAIRS = [
    ("lug", "en", "run","teo","ach","lgg"),
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
        test_en = dl_manager.download_and_extract(_TEST_EN)
        valid_en = dl_manager.download_and_extract(_VAL_EN)

        train_run = dl_manager.download_and_extract(_TRAIN_RUN)
        test_run = dl_manager.download_and_extract(_TEST_RUN)
        valid_run = dl_manager.download_and_extract(_VAL_RUN)

        train_teo = dl_manager.download_and_extract(_TRAIN_TEO)
        test_teo = dl_manager.download_and_extract(_TEST_TEO)
        valid_teo = dl_manager.download_and_extract(_VAL_TEO)

        train_lug = dl_manager.download_and_extract(_TRAIN_LUG)
        test_lug = dl_manager.download_and_extract(_TEST_LUG)
        valid_lug = dl_manager.download_and_extract(_VAL_LUG)

        train_lgg = dl_manager.download_and_extract(_TRAIN_LGG)
        test_lgg = dl_manager.download_and_extract(_TEST_LGG)
        valid_lgg = dl_manager.download_and_extract(_VAL_LGG)

        train_ach = dl_manager.download_and_extract(_TRAIN_ACH)
        test_ach = dl_manager.download_and_extract(_TEST_ACH)
        valid_ach = dl_manager.download_and_extract(_VAL_ACH) 
## testing commits
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"en_datapath":  train_en,
                            "run_datapath": train_run,
                            "teo_datapath": train_teo,
                            "lug_datapath": train_lug,
                            "lgg_datapath": train_lgg,
                            "ach_datapath": train_ach
                            },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"en_datapath": valid_en,
                            "run_datapath": valid_run,
                            "teo_datapath": valid_teo,
                            "lug_datapath": valid_lug,
                            "lgg_datapath": valid_lgg,
                            "ach_datapath": valid_ach},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"en_datapath": test_en,
                            "run_datapath": test_run,
                            "teo_datapath": test_teo,
                            "lug_datapath": test_lug,
                            "lgg_datapath": test_lgg,
                            "ach_datapath": test_ach
                            },
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
