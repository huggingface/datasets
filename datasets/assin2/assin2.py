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
"""ASSIN 2 dataset."""


import xml.etree.ElementTree as ET

import datasets


_CITATION = """
@inproceedings{real2020assin,
  title={The assin 2 shared task: a quick overview},
  author={Real, Livy and Fonseca, Erick and Oliveira, Hugo Goncalo},
  booktitle={International Conference on Computational Processing of the Portuguese Language},
  pages={406--412},
  year={2020},
  organization={Springer}
}
"""

_DESCRIPTION = """
The ASSIN 2 corpus is composed of rather simple sentences. Following the procedures of SemEval 2014 Task 1.
The training and validation data are composed, respectively, of 6,500 and 500 sentence pairs in Brazilian Portuguese,
annotated for entailment and semantic similarity. Semantic similarity values range from 1 to 5, and text entailment
classes are either entailment or none. The test data are composed of approximately 3,000 sentence pairs with the same
annotation. All data were manually annotated.
"""

_HOMEPAGE = "https://sites.google.com/view/assin2"

_LICENSE = ""

_URLS = {
    "train": "https://drive.google.com/u/0/uc?id=1Q9j1a83CuKzsHCGaNulSkNxBm7Dkn7Ln&export=download",
    "dev": "https://drive.google.com/u/0/uc?id=1kb7xq6Mb3eaqe9cOAo70BaG9ypwkIqEU&export=download",
    "test": "https://drive.google.com/u/0/uc?id=1J3FpQaHxpM-FDfBUyooh-sZF-B-bM_lU&export=download",
}


class Assin2(datasets.GeneratorBasedBuilder):
    """ASSIN 2 dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "sentence_pair_id": datasets.Value("int64"),
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "relatedness_score": datasets.Value("float32"),
                "entailment_judgment": datasets.features.ClassLabel(names=["NONE", "ENTAILMENT"]),
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
        data_dir = dl_manager.download(_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_dir["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        id_ = 0

        with open(filepath, "rb") as f:

            tree = ET.parse(f)
            root = tree.getroot()

            for pair in root:

                yield id_, {
                    "sentence_pair_id": int(pair.attrib.get("id")),
                    "premise": pair.find(".//t").text,
                    "hypothesis": pair.find(".//h").text,
                    "relatedness_score": float(pair.attrib.get("similarity")),
                    "entailment_judgment": pair.attrib.get("entailment").upper(),
                }

                id_ += 1
