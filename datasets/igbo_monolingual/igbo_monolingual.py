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
"""Igbo Monolingual Dataset"""


import json
import os

import datasets


_CITATION = """\
@misc{ezeani2020igboenglish,
title={Igbo-English Machine Translation: An Evaluation Benchmark},
author={Ignatius Ezeani and Paul Rayson and Ikechukwu Onyenwe and Chinedu Uchechukwu and Mark Hepple},
year={2020},
eprint={2004.00648},
archivePrefix={arXiv},
primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
A dataset is a collection of Monolingual Igbo sentences.
"""

_HOMEPAGE = "https://github.com/IgnatiusEzeani/IGBONLP/tree/master/ig_monoling"

_URL = "https://github.com/IgnatiusEzeani/IGBONLP/raw/master/ig_monoling/json.zip"


class IgboMonolingual(datasets.GeneratorBasedBuilder):
    """collection of Monolingual Igbo sentences from different sources"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="eze_goes_to_school",
            version=VERSION,
            description="Igbo sentences from Master's Thesis; UZOALOR, JOY UCHE",
        ),
        datasets.BuilderConfig(
            name="bbc-igbo", version=VERSION, description="Igbo sentences from https://www.bbc.com/igbo/"
        ),
        datasets.BuilderConfig(
            name="igbo-radio", version=VERSION, description="Igbo sentences from https://www.igboradio.com"
        ),
        datasets.BuilderConfig(
            name="jw-ot-igbo", version=VERSION, description="Igbo sentences from 929 pages of 39 books"
        ),
        datasets.BuilderConfig(
            name="jw-nt-igbo", version=VERSION, description="Igbo sentences from 260 pages of 27 books"
        ),
        datasets.BuilderConfig(
            name="jw-books", version=VERSION, description="Igbo sentences from 2204 pages of 48 books "
        ),
        datasets.BuilderConfig(
            name="jw-teta", version=VERSION, description="Igbo sentences from 392 pages of 37 magazines"
        ),
        datasets.BuilderConfig(
            name="jw-ulo_nche", version=VERSION, description="Igbo sentences from 594 pages of 55 magazines"
        ),
        datasets.BuilderConfig(
            name="jw-ulo_nche_naamu", version=VERSION, description="Igbo sentences from 870 pages of 88 magazines"
        ),
    ]

    def _info(self):
        if self.config.name == "eze_goes_to_school":
            features = datasets.Features(
                {
                    "format": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "chapters": datasets.Sequence(
                        {"title": datasets.Value("string"), "content": datasets.Value("string")}
                    ),
                }
            )
        elif self.config.name == "bbc-igbo":
            features = datasets.Features(
                {
                    "source": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "headline": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "tags": datasets.Sequence(datasets.Value("string")),
                }
            )
        elif self.config.name == "igbo-radio":
            features = datasets.Features(
                {
                    "source": datasets.Value("string"),
                    "headline": datasets.Value("string"),
                    "author": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "content": datasets.Value("string"),
                }
            )
        elif self.config.name == "jw-ot-igbo":
            features = datasets.Features(
                {
                    "format": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "chapters": datasets.Sequence(
                        {"title": datasets.Value("string"), "content": datasets.Value("string")}
                    ),
                }
            )
        elif self.config.name == "jw-nt-igbo":
            features = datasets.Features(
                {
                    "format": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "chapters": datasets.Sequence(
                        {"title": datasets.Value("string"), "content": datasets.Value("string")}
                    ),
                }
            )
        elif self.config.name == "jw-books":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "format": datasets.Value("string"),
                    "date": datasets.Value("string"),
                }
            )
        elif self.config.name == "jw-teta":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "format": datasets.Value("string"),
                    "date": datasets.Value("string"),
                }
            )
        elif self.config.name == "jw-ulo_nche":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "format": datasets.Value("string"),
                    "date": datasets.Value("string"),
                }
            )
        elif self.config.name == "jw-ulo_nche_naamu":
            features = datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                    "format": datasets.Value("string"),
                    "date": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)
        if self.config.name == "eze_goes_to_school":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "eze_goes_to_school.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "bbc-igbo":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "bbc-igbo.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "igbo-radio":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "igbo-radio.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-ot-igbo":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-ot-igbo.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-nt-igbo":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-nt-igbo.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-books":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-books.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-teta":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-teta.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-ulo_nche":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-ulo_nche.json"),
                        "split": "train",
                    },
                ),
            ]
        elif self.config.name == "jw-ulo_nche_naamu":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "jw-ulo_nche_naamu.json"),
                        "split": "train",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        if self.config.name == "eze_goes_to_school":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "format": data["format"],
                        "title": data["title"],
                        "chapters": data["chapters"],
                    }
        elif self.config.name == "bbc-igbo":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "source": data["source"] if "source" in data.keys() else "",
                        "title": data["title"] if "title" in data.keys() else "",
                        "description": data["description"] if "description" in data.keys() else "",
                        "date": data["date"] if "date" in data.keys() else "",
                        "headline": data["headline"] if "headline" in data.keys() else "",
                        "content": data["content"] if "content" in data.keys() else "",
                        "tags": data["tags"] if "tags" in data.keys() else [],
                    }
        elif self.config.name == "igbo-radio":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "source": data["source"],
                        "headline": data["headline"],
                        "author": data["author"],
                        "date": data["date"],
                        "description": data["description"] if "description" in data.keys() else "",
                        "content": data["content"] if "content" in data.keys() else "",
                    }
        elif self.config.name == "jw-ot-igbo":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "format": data["format"],
                        "title": data["title"],
                        "chapters": data["chapters"],
                    }
        elif self.config.name == "jw-nt-igbo":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "format": data["format"],
                        "title": data["title"],
                        "chapters": data["chapters"],
                    }
        elif self.config.name == "jw-books":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "title": data["title"],
                        "content": data["content"],
                        "format": data["format"],
                        "date": data["date"] if "date" in data.keys() else "",
                    }
        elif self.config.name == "jw-teta":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "title": data["title"],
                        "content": data["content"],
                        "format": data["format"],
                        "date": data["date"] if "date" in data.keys() else "",
                    }
        elif self.config.name == "jw-ulo_nche":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "title": data["title"],
                        "content": data["content"],
                        "format": data["format"],
                        "date": data["date"] if "date" in data.keys() else "",
                    }
        elif self.config.name == "jw-ulo_nche_naamu":
            with open(filepath, "r", encoding="utf-8") as f:
                json_data = json.load(f)
                for id_, data in enumerate(json_data):
                    yield id_, {
                        "title": data["title"],
                        "content": data["content"],
                        "format": data["format"],
                        "date": data["date"] if "date" in data.keys() else "",
                    }
