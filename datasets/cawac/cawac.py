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
"""caWaC: Catalan web corpus dataset."""

import datasets


_CITATION = """\
@inproceedings{DBLP:conf/lrec/LjubesicT14,
  author    = {Nikola Ljubesic and
               Antonio Toral},
  editor    = {Nicoletta Calzolari and
               Khalid Choukri and
               Thierry Declerck and
               Hrafn Loftsson and
               Bente Maegaard and
               Joseph Mariani and
               Asunci{\'{o}}n Moreno and
               Jan Odijk and
               Stelios Piperidis},
  title     = {caWaC - {A} web corpus of Catalan and its application to language
               modeling and machine translation},
  booktitle = {Proceedings of the Ninth International Conference on Language Resources
               and Evaluation, {LREC} 2014, Reykjavik, Iceland, May 26-31, 2014},
  pages     = {1728--1732},
  publisher = {European Language Resources Association {(ELRA)}},
  year      = {2014},
  url       = {http://www.lrec-conf.org/proceedings/lrec2014/summaries/841.html},
  timestamp = {Mon, 19 Aug 2019 15:23:35 +0200},
  biburl    = {https://dblp.org/rec/conf/lrec/LjubesicT14.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
caWaC is a 780-million-token web corpus of Catalan built from the .cat top-level-domain in late 2013.
"""

_LICENSE = "CC BY-SA 3.0"

_URL = "http://nlp.ffzg.hr/resources/corpora/cawac/"
_URLS = "http://nlp.ffzg.hr/data/corpora/cawac.uniq.sortr.gz"


class Cawac(datasets.GeneratorBasedBuilder):
    """caWaC: Catalan web corpus dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf8") as f:
            for id_, row in enumerate(f):
                yield id_, {
                    "sentence": row,
                }
