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
"""Fake News vs Satire: A Dataset and Analysis."""


import os

import openpyxl  # noqa: requires this pandas optional dependency for reading xlsx files
import pandas as pd

import datasets


_CITATION = """
@inproceedings{inproceedings,
author = {Golbeck, Jennifer and Everett, Jennine and Falak, Waleed and Gieringer, Carl and Graney, Jack and Hoffman, Kelly and Huth, Lindsay and Ma, Zhenya and Jha, Mayanka and Khan, Misbah and Kori, Varsha and Mauriello, Matthew and Lewis, Elo and Mirano, George and IV, William and Mussenden, Sean and Nelson, Tammie and Mcwillie, Sean and Pant, Akshat and Cheakalos, Paul},
year = {2018},
month = {05},
pages = {17-21},
title = {Fake News vs Satire: A Dataset and Analysis},
doi = {10.1145/3201064.3201100}
}
"""

_DESCRIPTION = """
Fake news has become a major societal issue and a technical challenge for social media companies to identify. This content is difficult to identify because the term "fake news" covers intentionally false, deceptive stories as well as factual errors, satire, and sometimes, stories that a person just does not like. Addressing the problem requires clear definitions and examples. In this work, we present a dataset of fake news and satire stories that are hand coded, verified, and, in the case of fake news, include rebutting stories. We also include a thematic content analysis of the articles, identifying major themes that include hyperbolic support or condemnation of a gure, conspiracy theories, racist themes, and discrediting of reliable sources. In addition to releasing this dataset for research use, we analyze it and show results based on language that are promising for classification purposes. Overall, our contribution of a dataset and initial analysis are designed to support future work by fake news researchers.
"""

_HOMEPAGE = "https://dl.acm.org/doi/10.1145/3201064.3201100"

# _LICENSE = ""

_URLs = "https://github.com/jgolbeck/fakenews/raw/master/FakeNewsData.zip"


class FakeNewsEnglish(datasets.GeneratorBasedBuilder):
    """Fake News vs Satire: A Dataset and Analysis"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "article_number": datasets.Value("int32"),
                "url_of_article": datasets.Value("string"),
                "fake_or_satire": datasets.ClassLabel(names=["Satire", "Fake"]),
                "url_of_rebutting_article": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "FakeNewsData", "Fake News Stories.xlsx")},
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, "rb") as f:
            f = pd.read_excel(f, engine="openpyxl")
            for id_, row in f.iterrows():
                yield id_, {
                    "article_number": row["Article Number"],
                    "url_of_article": str(row["URL of article"]),
                    "fake_or_satire": str(row["Fake or Satire?"]),
                    "url_of_rebutting_article": str(row["URL of rebutting article"]),
                }
