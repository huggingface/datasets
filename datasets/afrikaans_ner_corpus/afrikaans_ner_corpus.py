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
""" Named entity annotated data from the NCHLT Text Resource Development: Phase II Project for Afrikaans"""

from __future__ import absolute_import, division, print_function

import logging
import os

import datasets


_CITATION = """\
@inproceedings{afrikaans_ner_corpus,
  author    = {	Gerhard van Huyssteen and
                Martin Puttkammer and
                E.B. Trollip and
                J.C. Liversage and
              Roald Eiselen},
  title     = {NCHLT Afrikaans Named Entity Annotated Corpus},
  booktitle = {Eiselen, R. 2016. Government domain named entity recognition for South African languages. Proceedings of the 10th      Language Resource and Evaluation Conference, Portorož, Slovenia.},
  year      = {2016},
  url       = {https://repo.sadilar.org/handle/20.500.12185/299},
}
"""

_DESCRIPTION = """\
Named entity annotated data from the NCHLT Text Resource Development: Phase II Project, annotated with PERSON, LOCATION, ORGANISATION and MISCELLANEOUS tags.
"""

_URL = "https://repo.sadilar.org/bitstream/handle/20.500.12185/299/nchlt_afrikaans_named_entity_annotated_corpus.zip?sequence=3&isAllowed=y"


_EXTRACTED_FILE = "NCHLT Afrikaans Named Entity Annotated Corpus/Dataset.NCHLT-II.AF.NER.Full.txt"


class AfrikaansNerCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for AfrikaansNerCorpus"""

    def __init__(self, **kwargs):
        """BuilderConfig for AfrikaansNerCorpus.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AfrikaansNerCorpusConfig, self).__init__(**kwargs)


class AfrikaansNerCorpus(datasets.GeneratorBasedBuilder):
    """ Afrikaans Ner dataset"""

    BUILDER_CONFIGS = [
        AfrikaansNerCorpusConfig(
            name="afrikaans_ner_corpus",
            version=datasets.Version("1.0.0"),
            description="AfrikaansNerCorpus dataset",
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
            homepage="https://repo.sadilar.org/handle/20.500.12185/299",
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
        logging.info("⏳ Generating examples from = %s", filepath)
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
