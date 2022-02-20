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
"""PANL BPPT"""


import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{id_panl_bppt,
  author    = {PAN Localization - BPPT},
  title     = {Parallel Text Corpora, English Indonesian},
  year      = {2009},
  url       = {http://digilib.bppt.go.id/sampul/p92-budiono.pdf},
}
"""

_DESCRIPTION = """\
Parallel Text Corpora for Multi-Domain Translation System created by BPPT (Indonesian Agency for the Assessment and
Application of Technology) for PAN Localization Project (A Regional Initiative to Develop Local Language Computing
Capacity in Asia). The dataset contains around 24K sentences divided in 4 difference topics (Economic, international,
Science and Technology and Sport).
"""

_HOMEPAGE = "http://digilib.bppt.go.id/sampul/p92-budiono.pdf"

_LICENSE = ""

_URLs = ["https://github.com/cahya-wirawan/indonesian-language-models/raw/master/data/BPPTIndToEngCorpusHalfM.zip"]


class IdPanlBpptConfig(datasets.BuilderConfig):
    """BuilderConfig for IdPanlBppt"""

    def __init__(self, src_tag=None, tgt_tag=None, topics=None, **kwargs):
        """BuilderConfig for IdPanlBppt.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdPanlBpptConfig, self).__init__(**kwargs)
        self.src_tag = src_tag
        self.tgt_tag = tgt_tag
        self.topics = topics


class IdPanlBppt(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdPanlBpptConfig(
            name="id_panl_bppt",
            version=VERSION,
            description="IdPanlBppt dataset",
            src_tag="en",
            tgt_tag="id",
            topics=[
                {"name": "Economy", "words": "150K"},
                {"name": "International", "words": "150K"},
                {"name": "Science", "words": "100K"},
                {"name": "Sport", "words": "100K"},
            ],
        ),
    ]
    BUILDER_CONFIG_CLASS = IdPanlBpptConfig

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "translation": datasets.features.Translation(languages=[self.config.src_tag, self.config.tgt_tag]),
                "topic": datasets.features.ClassLabel(names=[topic["name"] for topic in self.config.topics]),
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
        my_urls = _URLs[0]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": os.path.join(data_dir, "plain"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, data_dir, split):
        logger.info("⏳ Generating %s examples from = %s", split, data_dir)
        id = 0
        for topic in self.config.topics:
            src_path = f"PANL-BPPT-{topic['name'][:3].upper()}-{self.config.src_tag.upper()}-{topic['words']}w.txt"
            tgt_path = f"PANL-BPPT-{topic['name'][:3].upper()}-{self.config.tgt_tag.upper()}-{topic['words']}w.txt"
            with open(os.path.join(data_dir, src_path), encoding="utf-8") as f1, open(
                os.path.join(data_dir, tgt_path), encoding="utf-8"
            ) as f2:
                src = f1.read().split("\n")[:-1]
                tgt = f2.read().split("\n")[:-1]
                for idx, (s, t) in enumerate(zip(src, tgt)):
                    yield id, {
                        "id": str(id),
                        "translation": {self.config.src_tag: s, self.config.tgt_tag: t},
                        "topic": topic["name"],
                    }
                    id += 1
