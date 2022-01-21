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
"""HEAD-QA: A Healthcare Dataset for Complex Reasoning"""


import json
import os

import datasets


_CITATION = """\
@inproceedings{vilares-gomez-rodriguez-2019-head,
    title = "{HEAD}-{QA}: A Healthcare Dataset for Complex Reasoning",
    author = "Vilares, David  and
      G{\'o}mez-Rodr{\'i}guez, Carlos",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1092",
    doi = "10.18653/v1/P19-1092",
    pages = "960--966",
    abstract = "We present HEAD-QA, a multi-choice question answering testbed to encourage research on complex reasoning. The questions come from exams to access a specialized position in the Spanish healthcare system, and are challenging even for highly specialized humans. We then consider monolingual (Spanish) and cross-lingual (to English) experiments with information retrieval and neural techniques. We show that: (i) HEAD-QA challenges current methods, and (ii) the results lag well behind human performance, demonstrating its usefulness as a benchmark for future work.",
}
"""

_DESCRIPTION = """\
HEAD-QA is a multi-choice HEAlthcare Dataset. The questions come from exams to access a specialized position in the
Spanish healthcare system, and are challenging even for highly specialized humans. They are designed by the Ministerio
de Sanidad, Consumo y Bienestar Social.

The dataset contains questions about the following topics: medicine, nursing, psychology, chemistry, pharmacology and biology.
"""

_HOMEPAGE = "https://aghie.github.io/head-qa/"

_LICENSE = "MIT License"

_URL = "https://drive.google.com/u/0/uc?export=download&id=1a_95N5zQQoUCq8IBNVZgziHbeM-QxG2t"

_DIRS = {"es": "HEAD", "en": "HEAD_EN"}


class HeadQA(datasets.GeneratorBasedBuilder):
    """HEAD-QA: A Healthcare Dataset for Complex Reasoning"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="es", version=VERSION, description="Spanish HEAD dataset"),
        datasets.BuilderConfig(name="en", version=VERSION, description="English HEAD dataset"),
    ]

    DEFAULT_CONFIG_NAME = "es"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "name": datasets.Value("string"),
                    "year": datasets.Value("string"),
                    "category": datasets.Value("string"),
                    "qid": datasets.Value("int32"),
                    "qtext": datasets.Value("string"),
                    "ra": datasets.Value("int32"),
                    "image": datasets.Image(),
                    "answers": [
                        {
                            "aid": datasets.Value("int32"),
                            "atext": datasets.Value("string"),
                        }
                    ],
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)

        dir = _DIRS[self.config.name]
        data_lang_dir = os.path.join(data_dir, dir)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": data_dir, "filepath": os.path.join(data_lang_dir, f"train_{dir}.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_dir": data_dir, "filepath": os.path.join(data_lang_dir, f"test_{dir}.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"data_dir": data_dir, "filepath": os.path.join(data_lang_dir, f"dev_{dir}.json")},
            ),
        ]

    def _generate_examples(self, data_dir, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            head_qa = json.load(f)
            for exam_id, exam in enumerate(head_qa["exams"]):
                content = head_qa["exams"][exam]
                name = content["name"].strip()
                year = content["year"].strip()
                category = content["category"].strip()
                for question in content["data"]:
                    qid = int(question["qid"].strip())
                    qtext = question["qtext"].strip()
                    ra = int(question["ra"].strip())
                    image_path = question["image"].strip()

                    aids = [answer["aid"] for answer in question["answers"]]
                    atexts = [answer["atext"].strip() for answer in question["answers"]]
                    answers = [{"aid": aid, "atext": atext} for aid, atext in zip(aids, atexts)]

                    id_ = f"{exam_id}_{qid}"
                    yield id_, {
                        "name": name,
                        "year": year,
                        "category": category,
                        "qid": qid,
                        "qtext": qtext,
                        "ra": ra,
                        "image": os.path.join(data_dir, image_path) if image_path else None,
                        "answers": answers,
                    }
