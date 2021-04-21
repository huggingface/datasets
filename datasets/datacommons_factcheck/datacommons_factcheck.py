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
"""DataCommons Fact Checked claims"""


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {Data Commons 2019 Fact Checks},
authors={datacommons.org},
year={2019}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
A dataset of fact checked claims by news media maintained by datacommons.org
"""

_HOMEPAGE = "https://datacommons.org/factcheck/faq"

_LICENSE = "CC-BY-NC-4.0"

_URL = "https://datacommons.org/data/factcheck/fact_checks_20190605.txt.gz"


class DatacommonsFactcheck(datasets.GeneratorBasedBuilder):
    """DataCommons Fact Checked claims"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="fctchk_politifact_wapo", version=VERSION, description="The 06/05/2019 version of the dataset"
        ),
        datasets.BuilderConfig(
            name="weekly_standard",
            version=VERSION,
            description="Includes Weekly Standard fact checked claims. See the README for concerns about these data items.",
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "fctchk_politifact_wapo"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        features = datasets.Features(
            {
                "reviewer_name": datasets.Value("string"),
                "claim_text": datasets.Value("string"),
                "review_date": datasets.Value("string"),
                "review_url": datasets.Value("string"),
                "review_rating": datasets.Value("string"),
                "claim_author_name": datasets.Value("string"),
                "claim_date": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        file_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": file_path,
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            id_ = -1
            for row in f:
                data = json.loads(row.strip()[35:-9])
                res = {
                    "reviewer_name": data["author"]["name"],
                    "claim_text": data["claimReviewed"],
                    "review_date": data.get("datePublished", ""),
                    "review_url": data["url"],
                    "review_rating": data["reviewRating"]["alternateName"],
                    "claim_author_name": data["itemReviewed"]["author"].get("name", ""),
                    "claim_date": data["itemReviewed"].get("datePublished", ""),
                }
                if self.config.name == "weekly_standard":
                    if data["author"]["name"] == "The Weekly Standard":
                        id_ += 1
                        yield id_, res
                else:
                    if data["author"]["name"] != "The Weekly Standard":
                        id_ += 1
                        yield id_, res
