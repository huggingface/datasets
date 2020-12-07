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
"""Arabic Poetry Metric dataset."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_DESCRIPTION = """\
Arabic Poetry Metric Classification.
The dataset contains the verses and their corresponding meter classes.\
Meter classes are represented as numbers from 0 to 13. \
The dataset can be highly useful for further research in order to improve the field of Arabic poems’ meter classification.\
The train dataset contains 47,124 records and the test dataset contains 8316 records.
"""

_CITATION = """\
@article{metrec2020,
  title={MetRec: A dataset for meter classification of arabic poetry},
  author={Al-shaibani, Maged S and Alyafeai, Zaid and Ahmad, Irfan},
  journal={Data in Brief},
  year={2020},
  publisher={Elsevier}
}
"""

_DOWNLOAD_URL = "https://raw.githubusercontent.com/zaidalyafeai/MetRec/master/baits.zip"


class MetRecConfig(datasets.BuilderConfig):
    """BuilderConfig for MetRec."""

    def __init__(self, **kwargs):
        """BuilderConfig for MetRec.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MetRecConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Metrec(datasets.GeneratorBasedBuilder):
    """Metrec dataset."""

    BUILDER_CONFIGS = [
        MetRecConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "saree",
                            "kamel",
                            "mutakareb",
                            "mutadarak",
                            "munsareh",
                            "madeed",
                            "mujtath",
                            "ramal",
                            "baseet",
                            "khafeef",
                            "taweel",
                            "wafer",
                            "hazaj",
                            "rajaz",
                        ]
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/zaidalyafeai/MetRec",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive, os.path.join("final_baits", "train.txt")):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "final_baits")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "train.txt")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"directory": os.path.join(data_dir, "test.txt")}
            ),
        ]

    def _generate_examples(self, directory, labeled=True):
        """Generate examples."""
        # For labeled examples, extract the label from the path.

        with open(directory, encoding="UTF-8") as f:
            for id_, record in enumerate(f.read().splitlines()):
                label, bait = record.split(" ", 1)
                yield str(id_), {"text": bait, "label": int(label)}
