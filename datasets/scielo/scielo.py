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
"""Parallel corpus of full-text articles in Portuguese, English and Spanish from SciELO"""


import datasets


_CITATION = """\
@inproceedings{soares2018large,
  title={A Large Parallel Corpus of Full-Text Scientific Articles},
  author={Soares, Felipe and Moreira, Viviane and Becker, Karin},
  booktitle={Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC-2018)},
  year={2018}
}
"""


_DESCRIPTION = """\
A parallel corpus of full-text scientific articles collected from Scielo database in the following languages: \
English, Portuguese and Spanish. The corpus is sentence aligned for all language pairs, \
as well as trilingual aligned for a small subset of sentences. Alignment was carried out using the Hunalign algorithm.
"""


_HOMEPAGE = "https://sites.google.com/view/felipe-soares/datasets#h.p_92uSCyAjWSRB"

_LANGUAGES = ["en-es", "en-pt", "en-pt-es"]

_URLS = {
    "en-es": "https://ndownloader.figstatic.com/files/14019287",
    "en-pt": "https://ndownloader.figstatic.com/files/14019308",
    "en-pt-es": "https://ndownloader.figstatic.com/files/14019293",
}


class Scielo(datasets.GeneratorBasedBuilder):
    """Parallel corpus of full-text articles in Portuguese, English and Spanish from SciELO"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="en-es", version=datasets.Version("1.0.0"), description="English-Spanish"),
        datasets.BuilderConfig(name="en-pt", version=datasets.Version("1.0.0"), description="English-Portuguese"),
        datasets.BuilderConfig(
            name="en-pt-es", version=datasets.Version("1.0.0"), description="English-Portuguese-Spanish"
        ),
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
        archive = dl_manager.download(_URLS[self.config.name])
        lang_pair = self.config.name.split("-")
        fname = self.config.name.replace("-", "_")

        if self.config.name == "en-pt-es":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "source_file": f"{fname}.en",
                        "target_file": f"{fname}.pt",
                        "target_file_2": f"{fname}.es",
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": f"{fname}.{lang_pair[0]}",
                    "target_file": f"{fname}.{lang_pair[1]}",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file, files, target_file_2=None):
        for path, f in files:
            if path == source_file:
                source_sentences = f.read().decode("utf-8").split("\n")
            elif path == target_file:
                target_sentences = f.read().decode("utf-8").split("\n")
            elif self.config.name == "en-pt-es" and path == target_file_2:
                target_sentences_2 = f.read().decode("utf-8").split("\n")

        if self.config.name == "en-pt-es":
            source, target, target_2 = tuple(self.config.name.split("-"))
            for idx, (l1, l2, l3) in enumerate(zip(source_sentences, target_sentences, target_sentences_2)):
                result = {"translation": {source: l1, target: l2, target_2: l3}}
                yield idx, result
        else:
            source, target = tuple(self.config.name.split("-"))
            for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
                result = {"translation": {source: l1, target: l2}}
                yield idx, result
