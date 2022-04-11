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


import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{id_nergrit_corpus,
  author    = {Gria Inovasi Teknologi},
  title     = {NERGRIT CORPUS},
  year      = {2019},
  url       = {https://github.com/grit-id/nergrit-corpus},
}
"""

_DESCRIPTION = """\
Nergrit Corpus is a dataset collection for Indonesian Named Entity Recognition, Statement Extraction, and Sentiment
Analysis. id_nergrit_corpus is the Named Entity Recognition of this dataset collection which contains 18 entities as
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


class IdNergritCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for IdNergritCorpus"""

    def __init__(self, label_classes=None, **kwargs):
        """BuilderConfig for IdNergritCorpus.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdNergritCorpusConfig, self).__init__(**kwargs)
        self.label_classes = label_classes


class IdNergritCorpus(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        IdNergritCorpusConfig(
            name="ner",
            version=VERSION,
            description="Named Entity Recognition dataset of Nergrit Corpus",
            label_classes=[
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
            ],
        ),
        IdNergritCorpusConfig(
            name="sentiment",
            version=VERSION,
            description="Sentiment Analysis dataset of Nergrit Corpus",
            label_classes=[
                "B-NEG",
                "B-NET",
                "B-POS",
                "I-NEG",
                "I-NET",
                "I-POS",
                "O",
            ],
        ),
        IdNergritCorpusConfig(
            name="statement",
            version=VERSION,
            description="Statement Extraction dataset of Nergrit Corpus",
            label_classes=[
                "B-BREL",
                "B-FREL",
                "B-STAT",
                "B-WHO",
                "I-BREL",
                "I-FREL",
                "I-STAT",
                "I-WHO",
                "O",
            ],
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "ner_tags": datasets.Sequence(datasets.features.ClassLabel(names=self.config.label_classes)),
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
        archive = dl_manager.download(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": f"nergrit-corpus/{self.config.name}/data/train_corrected.txt",
                    "split": "train",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": f"nergrit-corpus/{self.config.name}/data/test_corrected.txt",
                    "split": "test",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": f"nergrit-corpus/{self.config.name}/data/valid_corrected.txt",
                    "split": "dev",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, split, files):
        for path, f in files:
            if path == filepath:
                guid = 0
                tokens = []
                ner_tags = []
                for line in f:
                    splits = line.decode("utf-8").strip().split()
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
                break
