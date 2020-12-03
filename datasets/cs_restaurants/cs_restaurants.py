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
"""Czech restaurant information dataset for NLG"""

from __future__ import absolute_import, division, print_function

import json

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{DBLP:journals/corr/abs-1910-05298,
  author    = {Ondrej Dusek and
               Filip Jurcicek},
  title     = {Neural Generation for Czech: Data and Baselines},
  journal   = {CoRR},
  volume    = {abs/1910.05298},
  year      = {2019},
  url       = {http://arxiv.org/abs/1910.05298},
  archivePrefix = {arXiv},
  eprint    = {1910.05298},
  timestamp = {Wed, 16 Oct 2019 16:25:53 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1910-05298.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
This is a dataset for NLG in task-oriented spoken dialogue systems with Czech as the target language. It originated as
a translation of the English San Francisco Restaurants dataset by Wen et al. (2015).
"""

_LICENSE = "Creative Commons 4.0 BY-SA"

_URLs = {
    "CSRestaurants": "https://raw.githubusercontent.com/UFAL-DSG/cs_restaurant_dataset/master/",
}


class CSRestaurants(datasets.GeneratorBasedBuilder):
    """Czech restaurant information dataset for NLG"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [datasets.BuilderConfig(name="CSRestaurants", description="NLG data for Czech")]
    DEFAULT_CONFIG_NAME = "CSRestaurants"

    def _info(self):
        features = datasets.Features(
            {
                "da": datasets.Value("string"),
                "delex_da": datasets.Value("string"),
                "text": datasets.Value("string"),
                "delex_text": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/UFAL-DSG/cs_restaurant_dataset",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        master_url = _URLs[self.config.name]
        train_path = dl_manager.download_and_extract(master_url + "train.json")
        valid_path = dl_manager.download_and_extract(master_url + "devel.json")
        test_path = dl_manager.download_and_extract(master_url + "test.json")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """

        with open(filepath, encoding="utf8") as f:
            data = json.load(f)
            for id_, instance in enumerate(data):
                yield id_, {
                    "da": instance["da"],
                    "delex_da": instance["delex_da"],
                    "text": instance["text"],
                    "delex_text": instance["delex_text"],
                }
