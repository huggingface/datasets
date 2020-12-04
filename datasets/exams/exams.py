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
"""EXAMS: a benchmark dataset for multilingual and cross-lingual question answering"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@article{hardalov2020exams,
  title={EXAMS: A Multi-subject High School Examinations Dataset for Cross-lingual and Multilingual Question Answering},
  author={Hardalov, Momchil and Mihaylov, Todor and Dimitrina Zlatkova and Yoan Dinkov and Ivan Koychev and Preslav Nvakov},
  journal={arXiv preprint arXiv:2011.03080},
  year={2020}
}
"""

_DESCRIPTION = """\
EXAMS is a benchmark dataset for multilingual and cross-lingual question answering from high school examinations.
It consists of more than 24,000 high-quality high school exam questions in 16 languages,
covering 8 language families and 24 school subjects from Natural Sciences and Social Sciences, among others.
"""

_HOMEPAGE = "https://github.com/mhardalov/exams-qa"

_LICENSE = "CC-BY-SA-4.0"

_URLS_LIST = [
    ("alignments", "https://github.com/mhardalov/exams-qa/raw/main/data/exams/parallel_questions.jsonl"),
]
_URLS_LIST += [
    (
        "multilingual_train",
        "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/train.jsonl.tar.gz",
    ),
    ("multilingual_dev", "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/dev.jsonl.tar.gz"),
    ("multilingual_test", "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/test.jsonl.tar.gz"),
    (
        "multilingual_with_para_train",
        "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/with_paragraphs/train_with_para.jsonl.tar.gz",
    ),
    (
        "multilingual_with_para_dev",
        "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/with_paragraphs/dev_with_para.jsonl.tar.gz",
    ),
    (
        "multilingual_with_para_test",
        "https://github.com/mhardalov/exams-qa/raw/main/data/exams/multilingual/with_paragraphs/test_with_para.jsonl.tar.gz",
    ),
]

_CROSS_LANGUAGES = ["bg", "hr", "hu", "it", "mk", "pl", "pt", "sq", "sr", "tr", "vi"]
_URLS_LIST += [
    ("crosslingual_test", "https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/test.jsonl.tar.gz"),
    (
        "crosslingual_with_para_test",
        "https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/with_paragraphs/test_with_para.jsonl.tar.gz",
    ),
]
for ln in _CROSS_LANGUAGES:
    _URLS_LIST += [
        (
            f"crosslingual_{ln}_train",
            f"https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/train_{ln}.jsonl.tar.gz",
        ),
        (
            f"crosslingual_with_para_{ln}_train",
            f"https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/with_paragraphs/train_{ln}_with_para.jsonl.tar.gz",
        ),
        (
            f"crosslingual_{ln}_dev",
            f"https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/dev_{ln}.jsonl.tar.gz",
        ),
        (
            f"crosslingual_with_para_{ln}_dev",
            f"https://github.com/mhardalov/exams-qa/raw/main/data/exams/cross-lingual/with_paragraphs/dev_{ln}_with_para.jsonl.tar.gz",
        ),
    ]
_URLs = dict(_URLS_LIST)


class ExamsConfig(datasets.BuilderConfig):
    def __init__(self, lang, with_para, **kwargs):
        super(ExamsConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.lang = lang
        self.with_para = "_with_para" if with_para else ""


class Exams(datasets.GeneratorBasedBuilder):
    """Exams dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIG_CLASS = ExamsConfig
    BUILDER_CONFIGS = [
        ExamsConfig(
            lang="",
            with_para=False,
            name="alignments",
            description="loads the alignment between question IDs across languages",
        ),
        ExamsConfig(
            lang="all",
            with_para=False,
            name="multilingual",
            description="Loads the unified multilingual train/dev/test split",
        ),
        ExamsConfig(
            lang="all",
            with_para=True,
            name="multilingual_with_para",
            description="Loads the unified multilingual train/dev/test split with Wikipedia support paragraphs",
        ),
        ExamsConfig(
            lang="all", with_para=False, name="crosslingual_test", description="Loads crosslingual test set only"
        ),
        ExamsConfig(
            lang="all",
            with_para=True,
            name="crosslingual_with_para_test",
            description="Loads crosslingual test set only with Wikipedia support paragraphs",
        ),
    ]
    for ln in _CROSS_LANGUAGES:
        BUILDER_CONFIGS += [
            ExamsConfig(
                lang=ln,
                with_para=False,
                name=f"crosslingual_{ln}",
                description=f"Loads crosslingual train and dev set for {ln}",
            ),
            ExamsConfig(
                lang=ln,
                with_para=True,
                name=f"crosslingual_with_para_{ln}",
                description=f"Loads crosslingual train and dev set for {ln} with Wikipedia support paragraphs",
            ),
        ]

    DEFAULT_CONFIG_NAME = (
        "multilingual_with_para"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        if self.config.name == "alignments":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "source_id": datasets.Value("string"),
                    "target_id_list": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question": {
                        "stem": datasets.Value("string"),
                        "choices": datasets.Sequence(
                            {
                                "text": datasets.Value("string"),
                                "label": datasets.Value("string"),
                                "para": datasets.Value("string"),
                            }
                        ),
                    },
                    "answerKey": datasets.Value("string"),
                    "info": {
                        "grade": datasets.Value("int32"),
                        "subject": datasets.Value("string"),
                        "language": datasets.Value("string"),
                    },
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        if self.config.name == "alignments":
            return [
                datasets.SplitGenerator(
                    name="full",
                    gen_kwargs={
                        "filepath": data_dir["alignments"],
                    },
                ),
            ]
        elif self.config.name in ["multilingual", "multilingual_with_para"]:
            return [
                datasets.SplitGenerator(
                    name=spl_enum,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir[f"{self.config.name}_{spl}"], f"{spl}{self.config.with_para}.jsonl"
                        ),
                    },
                )
                for spl, spl_enum in [
                    ("train", datasets.Split.TRAIN),
                    ("dev", datasets.Split.VALIDATION),
                    ("test", datasets.Split.TEST),
                ]
            ]
        elif self.config.name in ["crosslingual_test", "crosslingual_with_para_test"]:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir[f"{self.config.name}"], f"test{self.config.with_para}.jsonl"
                        ),
                    },
                ),
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=spl_enum,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir[f"{self.config.name}_{spl}"],
                            f"{spl}_{self.config.lang}{self.config.with_para}.jsonl",
                        )
                    },
                )
                for spl, spl_enum in [
                    ("train", datasets.Split.TRAIN),
                    ("dev", datasets.Split.VALIDATION),
                ]
            ]

    def _generate_examples(self, filepath):
        f = open(filepath, encoding="utf-8")
        if self.config.name == "alignments":
            for id_, line in enumerate(f):
                line_dict = json.loads(line.strip())
                in_id, out_list = list(line_dict.items())[0]
                yield id_, {"source_id": in_id, "target_id_list": out_list}
        else:
            for id_, line in enumerate(f):
                line_dict = json.loads(line.strip())
                for choice in line_dict["question"]["choices"]:
                    choice["para"] = choice.get("para", "")
                yield id_, line_dict
