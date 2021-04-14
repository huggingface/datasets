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
"""EiTB-ParCC: Parallel Corpus of Comparable News"""


import os

import datasets


_CITATION = """\
@InProceedings{TIEDEMANN12.463,
  author = {J{\"o}rg Tiedemann},
  title = {Parallel Data, Tools and Interfaces in OPUS},
  booktitle = {Proceedings of the Eight International Conference on Language Resources and Evaluation (LREC'12)},
  year = {2012},
  month = {may},
  date = {23-25},
  address = {Istanbul, Turkey},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Mehmet Ugur Dogan and Bente Maegaard and Joseph Mariani and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  isbn = {978-2-9517408-7-7},
  language = {english}
 }
"""


_DESCRIPTION = """\
EiTB-ParCC: Parallel Corpus of Comparable News. A Basque-Spanish parallel corpus provided by \
Vicomtech (https://www.vicomtech.org), extracted from comparable news produced by the \
Basque public broadcasting group Euskal Irrati Telebista.
"""


_HOMEPAGE = "http://opus.nlpl.eu/EiTB-ParCC.php"

_URL = "http://opus.nlpl.eu/download.php?f=EiTB-ParCC/v1/moses/es-eu.txt.zip"


class EitbParcc(datasets.GeneratorBasedBuilder):
    """EiTB-ParCC: Parallel Corpus of Comparable News"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="es-eu", version=datasets.Version("1.0.0"), description="A Basque-Spanish parallel"
        )
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
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, f"EiTB-ParCC.{self.config.name}.{lang_pair[0]}"),
                    "target_file": os.path.join(data_dir, f"EiTB-ParCC.{self.config.name}.{lang_pair[1]}"),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file):
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
        with open(target_file, encoding="utf-8") as f:
            target_sentences = f.read().split("\n")

        assert len(target_sentences) == len(source_sentences), "Sizes do not match: %d vs %d for %s vs %s." % (
            len(source_sentences),
            len(target_sentences),
            source_file,
            target_file,
        )

        source, target = tuple(self.config.name.split("-"))
        for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
            result = {"translation": {source: l1, target: l2}}
            yield idx, result
