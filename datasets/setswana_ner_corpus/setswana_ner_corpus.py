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
""" Named entity annotated data from the NCHLT Text Resource Development: Phase II Project for Setswana"""


import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@inproceedings{sepedi_ner_corpus,
  author    = {S.S.B.M. Phakedi and
              Roald Eiselen},
  title     = {NCHLT Setswana Named Entity Annotated Corpus},
  booktitle = {Eiselen, R. 2016. Government domain named entity recognition for South African languages. Proceedings of the 10th      Language Resource and Evaluation Conference, Portorož, Slovenia.},
  year      = {2016},
  url       = {https://repo.sadilar.org/handle/20.500.12185/341},
}
"""

_DESCRIPTION = """\
Named entity annotated data from the NCHLT Text Resource Development: Phase II Project, annotated with PERSON, LOCATION, ORGANISATION and MISCELLANEOUS tags.
"""

_URL = "https://repo.sadilar.org/bitstream/handle/20.500.12185/341/nchlt_setswana_named_entity_annotated_corpus.zip?sequence=3&isAllowed=y"


_EXTRACTED_FILE = "NCHLT Setswana Named Entity Annotated Corpus/Dataset.NCHLT-II.tn.NER.Full.txt"


class SetswanaNerCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for SetswanaNerCorpus"""

    def __init__(self, **kwargs):
        """BuilderConfig for SetswanaNerCorpus.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SetswanaNerCorpusConfig, self).__init__(**kwargs)


class SetswanaNerCorpus(datasets.GeneratorBasedBuilder):
    """Setswana Ner dataset"""

    BUILDER_CONFIGS = [
        SetswanaNerCorpusConfig(
            name="setswana_ner_corpus",
            version=datasets.Version("1.0.0"),
            description="SetswanaNerCorpus dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "OUT",
                                "B-PERS",
                                "I-PERS",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-MISC",
                                "I-MISC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://repo.sadilar.org/handle/20.500.12185/341",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, _EXTRACTED_FILE)},
            ),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    splits = line.split("\t")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
