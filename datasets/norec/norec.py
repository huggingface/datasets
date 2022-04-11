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

import tarfile

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
        archive = dl_manager.download(_URL)
        subarchive_path = "norec/conllu.tar.gz"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": "conllu/train",
                    "subarchive_path": subarchive_path,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_dir": "conllu/dev",
                    "subarchive_path": subarchive_path,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data_dir": "conllu/test",
                    "subarchive_path": subarchive_path,
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, data_dir, subarchive_path, files):
        counter = 0
        for path, f in files:
            if path == subarchive_path:
                stream = tarfile.open(fileobj=f, mode="r|*")
                for tarinfo in stream:
                    file_path = tarinfo.name
                    if file_path.startswith(data_dir) and file_path.endswith(".conllu"):
                        data = stream.extractfile(tarinfo).read().decode("utf-8")
                        for sent in conllu.parse(data):
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
                    stream.members = []
                del stream
                break
