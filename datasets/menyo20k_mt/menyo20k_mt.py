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
"""MENYO-20k: A Multi-domain English - Yorùbá Corpus for Machine Translations"""


import csv

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@dataset{david_ifeoluwa_adelani_2020_4297448,
  author       = {David Ifeoluwa Adelani and
                  Jesujoba O. Alabi and
                  Damilola Adebonojo and
                  Adesina Ayeni and
                  Mofe Adeyemi and
                  Ayodele Awokoya},
  title        = {MENYO-20k: A Multi-domain English - Yorùbá Corpus
                  for Machine Translation},
  month        = nov,
  year         = 2020,
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.4297448},
  url          = {https://doi.org/10.5281/zenodo.4297448}
}
"""


# You can copy an official description
_DESCRIPTION = """\
MENYO-20k is a multi-domain parallel dataset with texts obtained from news articles, ted talks, movie transcripts, radio transcripts, science and technology texts, and other short articles curated from the web and professional translators. The dataset has 20,100 parallel sentences split into 10,070 training sentences, 3,397 development sentences, and 6,633 test sentences (3,419 multi-domain, 1,714 news domain, and 1,500 ted talks speech transcript domain). The development and test sets are available upon request.
"""


_HOMEPAGE = "https://zenodo.org/record/4297448#.X81G7s0zZPY"


_LICENSE = "For non-commercial use because some of the data sources like Ted talks and JW news requires permission for commercial use."


# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://raw.githubusercontent.com/uds-lsv/menyo-20k_MT/master/data/train.tsv"


class Menyo20kMt(datasets.GeneratorBasedBuilder):
    """MENYO-20k: A Multi-domain English - Yorùbá Corpus for Machine Translations"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="menyo20k_mt",
            version=VERSION,
            description="MENYO-20k: A Multi-domain English - Yorùbá Corpus for Machine Translations",
        )
    ]

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features({"translation": datasets.features.Translation(languages=("en", "yo"))}),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                result = {"translation": {"en": row["English"], "yo": row["Yoruba"]}}
                yield idx, result
