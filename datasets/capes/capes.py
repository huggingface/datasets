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
"""Capes: Parallel corpus of theses and dissertation abstracts in Portuguese and English from CAPES"""


import datasets


_CITATION = """\
@inproceedings{soares2018parallel,
  title={A Parallel Corpus of Theses and Dissertations Abstracts},
  author={Soares, Felipe and Yamashita, Gabrielli Harumi and Anzanello, Michel Jose},
  booktitle={International Conference on Computational Processing of the Portuguese Language},
  pages={345--352},
  year={2018},
  organization={Springer}
}
"""


_DESCRIPTION = """\
A parallel corpus of theses and dissertations abstracts in English and Portuguese were collected from the \
CAPES website (Coordenação de Aperfeiçoamento de Pessoal de Nível Superior) - Brazil. \
The corpus is sentence aligned for all language pairs. Approximately 240,000 documents were \
collected and aligned using the Hunalign algorithm.
"""


_HOMEPAGE = "https://sites.google.com/view/felipe-soares/datasets#h.p_kxOR6EhHm2a6"

_URL = "https://ndownloader.figstatic.com/files/14015837"


class Capes(datasets.GeneratorBasedBuilder):
    """Capes: Parallel corpus of theses and dissertation abstracts in Portuguese and English from CAPES"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="en-pt",
            version=datasets.Version("1.0.0"),
            description="Parallel corpus of theses and dissertation abstracts in Portuguese and English from CAPES",
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
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": "en_pt.en",
                    "target_file": "en_pt.pt",
                    "src_files": dl_manager.iter_archive(archive),
                    "tgt_files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file, src_files, tgt_files):
        source, target = tuple(self.config.name.split("-"))
        for src_path, src_f in src_files:
            if src_path == source_file:
                for tgt_path, tgt_f in tgt_files:
                    if tgt_path == target_file:
                        for idx, (l1, l2) in enumerate(zip(src_f, tgt_f)):
                            l1 = l1.decode("utf-8").strip()
                            l2 = l2.decode("utf-8").strip()
                            if l1 and l2:
                                result = {"translation": {source: l1, target: l2}}
                                yield idx, result
                        break
                break
