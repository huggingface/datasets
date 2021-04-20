# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""The United Nations Parallel Corpus v1.0"""


import itertools
import os

import datasets


_CITATION = """\
@inproceedings{ziemski-etal-2016-united,
    title = "The {U}nited {N}ations Parallel Corpus v1.0",
    author = "Ziemski, Micha{\\l}  and
      Junczys-Dowmunt, Marcin  and
      Pouliquen, Bruno",
    booktitle = "Proceedings of the Tenth International Conference on Language Resources and Evaluation ({LREC}'16)",
    month = may,
    year = "2016",
    address = "Portoro{\v{z}}, Slovenia",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L16-1561",
    pages = "3530--3534",
    abstract = "This paper describes the creation process and statistics of the official United Nations Parallel Corpus, the first parallel corpus composed from United Nations documents published by the original data creator. The parallel corpus presented consists of manually translated UN documents from the last 25 years (1990 to 2014) for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish. The corpus is freely available for download under a liberal license. Apart from the pairwise aligned documents, a fully aligned subcorpus for the six official UN languages is distributed. We provide baseline BLEU scores of our Moses-based SMT systems trained with the full data of language pairs involving English and for all possible translation directions of the six-way subcorpus.",
}
"""


_DESCRIPTION = """\
This parallel corpus consists of manually translated UN documents from the last 25 years (1990 to 2014) \
for the six official UN languages, Arabic, Chinese, English, French, Russian, and Spanish.
"""


_HOMEPAGE = "http://opus.nlpl.eu/UNPC.php"

_LANGUAGES = ["ar", "en", "es", "fr", "ru", "zh"]
_LANGUAGE_PAIRS = list(itertools.combinations(_LANGUAGES, 2))

_BASE_URL = "http://opus.nlpl.eu/download.php?f=UNPC/v1.0/moses"
_URLS = {f"{l1}-{l2}": f"{_BASE_URL}/{l1}-{l2}.txt.zip" for l1, l2 in _LANGUAGE_PAIRS}


class UnPc(datasets.GeneratorBasedBuilder):
    """The United Nations Parallel Corpus v1.0"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=f"{l1}-{l2}", version=datasets.Version("1.0.0"), description=f"UNPC {l1}-{l2}")
        for l1, l2 in _LANGUAGE_PAIRS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=tuple(self.config.name.split("-")))}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang_pair = self.config.name.split("-")
        data_dir = dl_manager.download_and_extract(_URLS[self.config.name])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, f"UNPC.{self.config.name}.{lang_pair[0]}"),
                    "target_file": os.path.join(data_dir, f"UNPC.{self.config.name}.{lang_pair[1]}"),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file):
        source, target = tuple(self.config.name.split("-"))
        with open(source_file, encoding="utf-8") as src_f, open(target_file, encoding="utf-8") as tgt_f:
            for idx, (l1, l2) in enumerate(zip(src_f, tgt_f)):
                result = {"translation": {source: l1.strip(), target: l2.strip()}}
                yield idx, result
