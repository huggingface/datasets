# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""BigPatent Dataset."""
import glob
import gzip
import json
import os

import datasets


_HOMEPAGE = "https://evasharma.github.io/bigpatent/"

_CITATION = """
@misc{sharma2019bigpatent,
    title={BIGPATENT: A Large-Scale Dataset for Abstractive and Coherent Summarization},
    author={Eva Sharma and Chen Li and Lu Wang},
    year={2019},
    eprint={1906.03741},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
BIGPATENT, consisting of 1.3 million records of U.S. patent documents
along with human written abstractive summaries.
Each US patent application is filed under a Cooperative Patent Classification
(CPC) code. There are nine such classification categories:
A (Human Necessities), B (Performing Operations; Transporting),
C (Chemistry; Metallurgy), D (Textiles; Paper), E (Fixed Constructions),
F (Mechanical Engineering; Lightning; Heating; Weapons; Blasting),
G (Physics), H (Electricity), and
Y (General tagging of new or cross-sectional technology)
There are two features:
  - description: detailed description of patent.
  - abstract: Patent abastract.
"""

_LICENSE = "Creative Commons Attribution 4.0 International"

_REPO = "https://huggingface.co/datasets/big_patent/resolve/main/data"
_URLS = {
    "train": f"{_REPO}/train.zip",
    "validation": f"{_REPO}/val.zip",
    "test": f"{_REPO}/test.zip",
}

_DOCUMENT = "description"
_SUMMARY = "abstract"

_CPC_DESCRIPTION = {
    "a": "Human Necessities",
    "b": "Performing Operations; Transporting",
    "c": "Chemistry; Metallurgy",
    "d": "Textiles; Paper",
    "e": "Fixed Constructions",
    "f": "Mechanical Engineering; Lightning; Heating; Weapons; Blasting",
    "g": "Physics",
    "h": "Electricity",
    "y": "General tagging of new or cross-sectional technology",
}

# Available versions:
# 1.0.0 lower cased tokenized words.
# 2.0.0 cased raw strings.
# 2.1.0 cased raw strings (fixed).
# TODO Add raw string versions

_VERSION = "1.0.0"


class BigPatentConfig(datasets.BuilderConfig):
    """BuilderConfig for BigPatent."""

    def __init__(self, *args, cpc_codes=None, **kwargs):
        """BuilderConfig for BigPatent.
        Args:
            cpc_codes: str, cpc_codes
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(*args, version=_VERSION, **kwargs)
        self.cpc_codes = cpc_codes


class BigPatent(datasets.GeneratorBasedBuilder):
    """BigPatent datasets."""

    BUILDER_CONFIGS = [
        BigPatentConfig(
            cpc_codes=list(_CPC_DESCRIPTION),
            name="all",
            description="Patents under all categories.",
        ),
    ] + [
        BigPatentConfig(  # pylint:disable=g-complex-comprehension
            cpc_codes=[k],
            name=k,
            description=f"Patents under Cooperative Patent Classification (CPC) {k}: {v}",
        )
        for k, v in sorted(_CPC_DESCRIPTION.items())
    ]
    DEFAULT_CONFIG_NAME = "all"
    VERSION = _VERSION

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({_DOCUMENT: datasets.Value("string"), _SUMMARY: datasets.Value("string")}),
            supervised_keys=(_DOCUMENT, _SUMMARY),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_paths = dl_manager.download_and_extract(_URLS)
        split_dirs = {datasets.Split.TRAIN: "train", datasets.Split.VALIDATION: "val", datasets.Split.TEST: "test"}
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={"path": dl_paths[split], "split_dir": split_dirs[split]},
            )
            for split in split_dirs
        ]

    def _generate_examples(self, path=None, split_dir=None):
        """Yields examples."""
        for cpc_code in self.config.cpc_codes:
            filenames = glob.glob(os.path.join(path, split_dir, cpc_code, "*"))
            for filename in sorted(filenames):
                with open(filename, "rb") as fin:
                    fin = gzip.GzipFile(fileobj=fin)
                    for row in fin:
                        json_obj = json.loads(row)
                        yield json_obj["publication_number"], {
                            _DOCUMENT: json_obj[_DOCUMENT],
                            _SUMMARY: json_obj[_SUMMARY],
                        }
