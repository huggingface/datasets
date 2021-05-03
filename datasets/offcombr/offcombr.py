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
"""OffComBR: an annotated dataset containing for hate speech detection in Portuguese composed of news comments on the Brazilian Web."""


import datasets


_CITATION = """\
@article{Pelle2017,
title={Offensive Comments in the Brazilian Web: a dataset and baseline results},
author={Rogers P. de Pelle and Viviane P. Moreira},
booktitle={6th Brazilian Workshop on Social Network Analysis and Mining (BraSNAM)},
year={2017},
}
"""

_DESCRIPTION = """\
OffComBR: an annotated dataset containing for hate speech detection in Portuguese composed of news comments on the Brazilian Web.
"""

_HOMEPAGE = "http://www.inf.ufrgs.br/~rppelle/hatedetector/"

_LICENSE = "Unknown"

_URLs = {
    "offcombr-2": "https://github.com/rogersdepelle/OffComBR/raw/master/OffComBR2.arff",
    "offcombr-3": "https://github.com/rogersdepelle/OffComBR/raw/master/OffComBR3.arff",
}


class Offcombr(datasets.GeneratorBasedBuilder):
    """OffComBR: an annotated dataset containing for hate speech detection in Portuguese composed of news comments on the Brazilian Web."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="offcombr-2",
            version=VERSION,
            description="OffComBR-2 contains samples with Fleiss Kappa measure between annotators of 0.71",
        ),
        datasets.BuilderConfig(
            name="offcombr-3",
            version=VERSION,
            description="OffComBR-3 only contains instances for which the class has been agreed by all three judges",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "label": datasets.ClassLabel(names=["no", "yes"]),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=("label", "text"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        urls = _URLs[self.config.name]
        data_file = dl_manager.download_and_extract(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                if id_ < 8:
                    continue

                label, *text = row.split(",")
                text = "".join(text)
                yield id_, {
                    "label": label,
                    "text": text.strip().strip("'"),
                }
