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
"""Mac-Morpho dataset"""

import re

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """
@article{fonseca2015evaluating,
  title={Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese},
  author={Fonseca, Erick R and Rosa, Joao Luis G and Aluisio, Sandra Maria},
  journal={Journal of the Brazilian Computer Society},
  volume={21},
  number={1},
  pages={2},
  year={2015},
  publisher={Springer}
}
"""

_DESCRIPTION = """
Mac-Morpho is a corpus of Brazilian Portuguese texts annotated with part-of-speech tags.
Its first version was released in 2003 [1], and since then, two revisions have been made in order
to improve the quality of the resource [2, 3].
The corpus is available for download split into train, development and test sections.
These are 76%, 4% and 20% of the corpus total, respectively (the reason for the unusual numbers
is that the corpus was first split into 80%/20% train/test, and then 5% of the train section was
set aside for development). This split was used in [3], and new POS tagging research with Mac-Morpho
is encouraged to follow it in order to make consistent comparisons possible.


[1] Aluísio, S., Pelizzoni, J., Marchi, A.R., de Oliveira, L., Manenti, R., Marquiafável, V. 2003.
An account of the challenge of tagging a reference corpus for brazilian portuguese.
In: Proceedings of the 6th International Conference on Computational Processing of the Portuguese Language. PROPOR 2003

[2] Fonseca, E.R., Rosa, J.L.G. 2013. Mac-morpho revisited: Towards robust part-of-speech.
In: Proceedings of the 9th Brazilian Symposium in Information and Human Language Technology – STIL

[3] Fonseca, E.R., Aluísio, Sandra Maria, Rosa, J.L.G. 2015.
Evaluating word embeddings and a revised corpus for part-of-speech tagging in Portuguese.
Journal of the Brazilian Computer Society.
"""

_HOMEPAGE = "http://www.nilc.icmc.usp.br/macmorpho/"

_LICENSE = "Creative Commons Attribution 4.0 International License"

_URL = "http://www.nilc.icmc.usp.br/macmorpho/macmorpho-v3.tgz"


class MacMorpho(datasets.GeneratorBasedBuilder):
    """Mac-Morpho dataset."""

    VERSION = datasets.Version("3.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "PREP+PROADJ",
                                "IN",
                                "PREP+PRO-KS",
                                "NPROP",
                                "PREP+PROSUB",
                                "KC",
                                "PROPESS",
                                "NUM",
                                "PROADJ",
                                "PREP+ART",
                                "KS",
                                "PRO-KS",
                                "ADJ",
                                "ADV-KS",
                                "N",
                                "PREP",
                                "PROSUB",
                                "PREP+PROPESS",
                                "PDEN",
                                "V",
                                "PREP+ADV",
                                "PCP",
                                "CUR",
                                "ADV",
                                "PU",
                                "ART",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": "macmorpho-train.txt",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": "macmorpho-test.txt",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": "macmorpho-dev.txt",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, filepath, files):
        """Yields examples."""
        for path, f in files:
            if path == filepath:
                id_ = 0

                for line in f:

                    line = line.decode("utf-8").rstrip()
                    chunks = re.split(r"\s+", line)

                    tokens = []
                    pos_tags = []
                    for chunk in chunks:
                        token, tag = chunk.rsplit("_", 1)
                        tokens.append(token)
                        pos_tags.append(tag)

                    yield id_, {
                        "id": str(id_),
                        "tokens": tokens,
                        "pos_tags": pos_tags,
                    }
                    id_ += 1
                break
