# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import datasets


_DESCRIPTION = """\
Parallel Igbo-English Dataset
"""
_HOMEPAGE_URL = "https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_en_mt"
_CITATION = """\
@misc{ezeani2020igboenglish,
    title={Igbo-English Machine Translation: An Evaluation Benchmark},
    author={Ignatius Ezeani and Paul Rayson and Ikechukwu Onyenwe and Chinedu Uchechukwu and Mark Hepple},
    year={2020},
    eprint={2004.00648},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2004.00648}
}
"""

_VERSION = "1.0.0"
_TRAIN_EN = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/train.en"
_VALID_EN = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/val.en"
_TEST_EN = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/test.en"
_TRAIN_IG = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/train.ig"
_VALID_IG = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/val.ig"
_TEST_IG = "https://raw.githubusercontent.com/IgnatiusEzeani/IGBONLP/master/ig_en_mt/benchmark_dataset/test.ig"

_LANGUAGE_PAIRS = [
    ("ig", "en"),
]


class IgboEnglishMachineTranslationConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class IgboEnglishMachineTranslation(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        IgboEnglishMachineTranslationConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = IgboEnglishMachineTranslationConfig

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
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_en = dl_manager.download_and_extract(_TRAIN_EN)
        train_ig = dl_manager.download_and_extract(_TRAIN_IG)

        valid_en = dl_manager.download_and_extract(_VALID_EN)
        valid_ig = dl_manager.download_and_extract(_VALID_IG)

        test_en = dl_manager.download_and_extract(_TEST_EN)
        test_ig = dl_manager.download_and_extract(_TEST_IG)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"ig_datapath": train_ig, "en_datapath": train_en},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"ig_datapath": valid_ig, "en_datapath": valid_en},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"ig_datapath": test_ig, "en_datapath": test_en},
            ),
        ]

    def _generate_examples(self, ig_datapath, en_datapath):
        with open(ig_datapath, encoding="utf-8") as f1, open(en_datapath, encoding="utf-8") as f2:
            for sentence_counter, (x, y) in enumerate(zip(f1, f2)):
                x = x.strip()
                y = y.strip()
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "translation": {"ig": x, "en": y},
                    },
                )
                yield result
