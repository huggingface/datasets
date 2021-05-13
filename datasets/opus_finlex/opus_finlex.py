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


import os

import datasets


_CITATION = """\
J. Tiedemann, 2012, Parallel Data, Tools and Interfaces in OPUS. In Proceedings of the \
8th International Conference on Language Resources and Evaluation (LREC 2012)"""


_DESCRIPTION = """\
The Finlex Data Base is a comprehensive collection of legislative and other judicial information of Finland, \
which is available in Finnish, Swedish and partially in English. This corpus is taken from the Semantic Finlex serice \
that provides the Finnish and Swedish data as linked open data and also raw XML files."""


_HOMEPAGE = "http://opus.nlpl.eu/Finlex.php"


_LICENSE = ""


_URLs = {"train": "https://object.pouta.csc.fi/OPUS-Finlex/v2018/moses/fi-sv.txt.zip"}


class OpusFinlex(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [datasets.BuilderConfig(name="fi-sv", version=VERSION)]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=tuple(self.config.name.split("-")))}
            ),
            supervised_keys=None,
            homepage="http://opus.nlpl.eu/Finlex.php",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "source_file": os.path.join(data_dir["train"], "Finlex.fi-sv.fi"),
                    "target_file": os.path.join(data_dir["train"], "Finlex.fi-sv.sv"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file, split):
        """This function returns the examples in the raw (text) form."""
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
