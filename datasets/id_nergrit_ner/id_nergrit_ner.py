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
"""Nergrit Corpus"""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets


_CITATION = """\
@inproceedings{id_nergrit_ner,
  author    = {Gria Inovasi Teknologi},
  title     = {NERGRIT CORPUS},
  year      = {2019},
  url       = {https://github.com/grit-id/nergrit-corpus},
}
"""

_DESCRIPTION = """\
Nergrit Corpus is a dataset collection for Indonesian Named Entity Recognition, Statement Extraction, and Sentiment
Analysis. id_nergrit_ner is the Named Entity Recognition of this dataset collection which contains 18 entities as
follow:
    'CRD': Cardinal
    'DAT': Date
    'EVT': Event
    'FAC': Facility
    'GPE': Geopolitical Entity
    'LAW': Law Entity (such as Undang-Undang)
    'LOC': Location
    'MON': Money
    'NOR': Political Organization
    'ORD': Ordinal
    'ORG': Organization
    'PER': Person
    'PRC': Percent
    'PRD': Product
    'QTY': Quantity
    'REG': Religion
    'TIM': Time
    'WOA': Work of Art
    'LAN': Language
"""

_HOMEPAGE = "https://github.com/grit-id/nergrit-corpus"

_LICENSE = ""

_URLs = [
    "https://github.com/cahya-wirawan/indonesian-language-models/raw/master/data/nergrit-corpus_20190726_corrected.tgz",
    "https://cloud.uncool.ai/index.php/s/2QEcMrgwkjMAo4o/download",
]


class IdNergritNerConfig(datasets.BuilderConfig):
    """BuilderConfig for IdNergritNer"""

    def __init__(self, **kwargs):
        """BuilderConfig for IdNergritNer.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdNergritNerConfig, self).__init__(**kwargs)


class IdNergritNer(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdNergritNerConfig(
            name="id_nergrit_ner",
            version=VERSION,
            description="IdNergritNer dataset",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(
                    datasets.features.ClassLabel(
                        names=[
                            "B-CRD",
                            "B-DAT",
                            "B-EVT",
                            "B-FAC",
                            "B-GPE",
                            "B-LAN",
                            "B-LAW",
                            "B-LOC",
                            "B-MON",
                            "B-NOR",
                            "B-ORD",
                            "B-ORG",
                            "B-PER",
                            "B-PRC",
                            "B-PRD",
                            "B-QTY",
                            "B-REG",
                            "B-TIM",
                            "B-WOA",
                            "I-CRD",
                            "I-DAT",
                            "I-EVT",
                            "I-FAC",
                            "I-GPE",
                            "I-LAN",
                            "I-LAW",
                            "I-LOC",
                            "I-MON",
                            "I-NOR",
                            "I-ORD",
                            "I-ORG",
                            "I-PER",
                            "I-PRC",
                            "I-PRD",
                            "I-QTY",
                            "I-REG",
                            "I-TIM",
                            "I-WOA",
                            "O",
                        ]
                    )
                ),
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
                    "filepath": os.path.join(data_dir, "nergrit-corpus/ner/data/train_corrected.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "nergrit-corpus/ner/data/test_corrected.txt"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "nergrit-corpus/ner/data/valid_corrected.txt"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        logging.info("⏳ Generating %s examples from = %s", split, filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                splits = line.split()
                if len(splits) != 2:
                    if tokens:
                        assert len(tokens) == len(ner_tags), "word len doesn't match label length"
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
