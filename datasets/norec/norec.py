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
import glob
import os

import conllu

import datasets


_CITATION = """\
@InProceedings{VelOvrBer18,
  author = {Erik Velldal and Lilja Ovrelid and
            Eivind Alexander Bergem and Cathrine Stadsnes and
            Samia Touileb and Fredrik Jorgensen},
  title = {{NoReC}: The {N}orwegian {R}eview {C}orpus},
  booktitle = {Proceedings of the 11th edition of the
               Language Resources and Evaluation Conference},
  year = {2018},
  address = {Miyazaki, Japan},
  pages = {4186--4191}
}
"""

_DESCRIPTION = """\
NoReC was created as part of the SANT project (Sentiment Analysis for Norwegian Text), a collaboration between the Language Technology Group (LTG) at the Department of Informatics at the University of Oslo, the Norwegian Broadcasting Corporation (NRK), Schibsted Media Group and Aller Media. This first release of the corpus comprises 35,194 reviews extracted from eight different news sources: Dagbladet, VG, Aftenposten, Bergens Tidende, Fædrelandsvennen, Stavanger Aftenblad, DinSide.no and P3.no. In terms of publishing date the reviews mainly cover the time span 2003–2017, although it also includes a handful of reviews dating back as far as 1998.
"""

_URL = "https://www.mn.uio.no/ifi/english/research/projects/sant/data/norec/norec-1.0.1.tar.gz"
_TRAIN = "conllu/train"
_DEV = "conllu/dev"
_TEST = "conllu/test"


class Norec(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "idx": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "ADJ",
                                "ADP",
                                "ADV",
                                "AUX",
                                "CCONJ",
                                "DET",
                                "INTJ",
                                "NOUN",
                                "NUM",
                                "PART",
                                "PRON",
                                "PROPN",
                                "PUNCT",
                                "SCONJ",
                                "SYM",
                                "VERB",
                                "X",
                            ]
                        )
                    ),
                    "xpos_tags": datasets.Sequence(datasets.Value("string")),
                    "feats": datasets.Sequence(datasets.Value("string")),
                    "head": datasets.Sequence(datasets.Value("string")),
                    "deprel": datasets.Sequence(datasets.Value("string")),
                    "deps": datasets.Sequence(datasets.Value("string")),
                    "misc": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/ljos/navnkjenner",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        sub_path = os.path.join(path, "norec", "conllu.tar.gz")
        conllu_path = dl_manager.extract(sub_path)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "datapath": os.path.join(conllu_path, "conllu", "train"),
                    "path": path,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "datapath": os.path.join(conllu_path, "conllu", "dev"),
                    "path": path,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "datapath": os.path.join(conllu_path, "conllu", "test"),
                    "path": path,
                },
            ),
        ]

    def _generate_examples(self, datapath, path):
        conllu_files = sorted(glob.glob(os.path.join(datapath, "*.conllu")))
        counter = 0
        for cf in conllu_files:
            with open(cf, "r", encoding="utf-8") as data_file:
                tokenlist = list(conllu.parse_incr(data_file))
                for sent in tokenlist:
                    res = {
                        "idx": sent.metadata["sent_id"],
                        "text": sent.metadata["text"],
                        "tokens": [str(token["form"]) for token in sent],
                        "lemmas": [str(token["lemma"]) for token in sent],
                        "pos_tags": [str(token["upostag"]) for token in sent],
                        "xpos_tags": [str(token["xpostag"]) for token in sent],
                        "feats": [str(token["feats"]) for token in sent],
                        "head": [str(token["head"]) for token in sent],
                        "deprel": [str(token["deprel"]) for token in sent],
                        "deps": [str(token["deps"]) for token in sent],
                        "misc": [str(token["misc"]) for token in sent],
                    }
                    yield counter, res
                    counter += 1
