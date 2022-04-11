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

""" Dataset with clickbait and fake news in Bulgarian. """


import openpyxl  # noqa: requires this pandas optional dependency for reading xlsx files
import pandas as pd

import datasets


_CITATION = """\
@InProceedings{clickbait_news_bg,
title = {Dataset with clickbait and fake news in Bulgarian. Introduced for the Hack the Fake News 2017.},
authors={Data Science Society},
year={2017},
url={https://gitlab.com/datasciencesociety/case_fake_news/}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Dataset with clickbait and fake news in Bulgarian. Introduced for the Hack the Fake News 2017.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://gitlab.com/datasciencesociety/case_fake_news/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    "default_train": "https://gitlab.com/datasciencesociety/case_fake_news/-/raw/master/data/FN_Training_Set.xlsx",
    "default_validation": "https://gitlab.com/datasciencesociety/case_fake_news/-/raw/master/data/FN_Validation_Set.xlsx",
}


class ClickbaitNewsBG(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.0")
    DEFAULT_CONFIG_NAME = "default"

    def _info(self):
        if self.config.name == "default":
            features = datasets.Features(
                {
                    "fake_news_score": datasets.features.ClassLabel(names=["legitimate", "fake"]),
                    "click_bait_score": datasets.features.ClassLabel(names=["normal", "clickbait"]),
                    "content_title": datasets.Value("string"),
                    "content_url": datasets.Value("string"),
                    "content_published_time": datasets.Value("string"),
                    "content": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download(_URLs)

        return [
            datasets.SplitGenerator(
                name=spl_enum,
                gen_kwargs={
                    "filepath": data_dir[f"{self.config.name}_{spl}"],
                    "split": spl,
                },
            )
            for spl, spl_enum in [
                ("train", datasets.Split.TRAIN),
                ("validation", datasets.Split.VALIDATION),
            ]
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        keys = [
            "fake_news_score",
            "click_bait_score",
            "content_title",
            "content_url",
            "content_published_time",
            "content",
        ]
        with open(filepath, "rb") as f:
            data = pd.read_excel(f, engine="openpyxl")
            for id_, row in enumerate(data.itertuples()):
                row_dict = dict()
                for key, value in zip(keys, row[1:]):
                    if key == "fake_news_score":
                        row_dict[key] = "legitimate" if value == 1 else "fake"
                    elif key == "click_bait_score":
                        row_dict[key] = "normal" if value == 1 else "clickbait"
                    else:
                        row_dict[key] = str(value)
                yield id_, row_dict
