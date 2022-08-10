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
"""DART: Open-Domain Structured Data Record to Text Generation"""

import json

import datasets


_CITATION = """\
@article{radev2020dart,
  title={DART: Open-Domain Structured Data Record to Text Generation},
  author={Dragomir Radev and Rui Zhang and Amrit Rau and Abhinand Sivaprasad and Chiachun Hsieh and Nazneen Fatema Rajani and Xiangru Tang and Aadit Vyas and Neha Verma and Pranav Krishna and Yangxiaokang Liu and Nadia Irwanto and Jessica Pan and Faiaz Rahman and Ahmad Zaidi and Murori Mutuma and Yasin Tarabar and Ankit Gupta and Tao Yu and Yi Chern Tan and Xi Victoria Lin and Caiming Xiong and Richard Socher},
  journal={arXiv preprint arXiv:2007.02871},
  year={2020}
"""

_DESCRIPTION = """\
DART is a large and open-domain structured DAta Record to Text generation corpus with high-quality
sentence annotations with each input being a set of entity-relation triples following a tree-structured ontology.
It consists of 82191 examples across different domains with each input being a semantic RDF triple set derived
from data records in tables and the tree ontology of table schema, annotated with sentence description that
covers all facts in the triple set.

DART is released in the following paper where you can find more details and baseline results:
https://arxiv.org/abs/2007.02871
"""

_URL = "https://raw.githubusercontent.com/Yale-LILY/dart/master/data/v1.1.1/"
_TRAINING_FILE = "dart-v1.1.1-full-train.json"
_DEV_FILE = "dart-v1.1.1-full-dev.json"
_TEST_FILE = "dart-v1.1.1-full-test.json"


class Dart(datasets.GeneratorBasedBuilder):
    """Dart dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tripleset": datasets.Sequence(datasets.Sequence(datasets.Value("string"))),
                    "subtree_was_extended": datasets.Value("bool"),
                    "annotations": datasets.Sequence(
                        {
                            "source": datasets.Value("string"),
                            "text": datasets.Value("string"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/Yale-LILY/dart",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            data = json.loads(f.read())
            for example_idx, example in enumerate(data):
                yield example_idx, {
                    "tripleset": example["tripleset"],
                    "subtree_was_extended": example.get("subtree_was_extended", None),  # some are missing
                    "annotations": {
                        "source": [annotation["source"] for annotation in example["annotations"]],
                        "text": [annotation["text"] for annotation in example["annotations"]],
                    },
                }
