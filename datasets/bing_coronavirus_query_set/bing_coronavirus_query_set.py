# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

# Lint as: python3

import datasets


_DESCRIPTION = """\
This dataset was curated from the Bing search logs (desktop users only) over the period of Jan 1st, 2020 – (Current Month - 1). Only searches that were issued many times by multiple users were included. The dataset includes queries from all over the world that had an intent related to the Coronavirus or Covid-19. In some cases this intent is explicit in the query itself (e.g., “Coronavirus updates Seattle”), in other cases it is implicit , e.g. “Shelter in place”. The implicit intent of search queries (e.g., “Toilet paper”) was extracted using random walks on the click graph as outlined in this paper by Microsoft Research. All personal data were removed.
"""
_HOMEPAGE_URL = "https://github.com/microsoft/BingCoronavirusQuerySet"
_CITATION = None

_VERSION = "1.0.0"
_BASE_URL = "https://raw.githubusercontent.com/microsoft/BingCoronavirusQuerySet/master/data/2020/{}_{}_{}.tsv"


class BingCoronavirusQuerySetConfig(datasets.BuilderConfig):
    def __init__(self, *args, queries_by=None, start_date=None, end_date=None, **kwargs):
        super().__init__(
            *args,
            name=f"{queries_by}_{start_date}_{end_date}",
            **kwargs,
        )
        self.queries_by = queries_by
        self.start_date = start_date
        self.end_date = end_date


class BingCoronavirusQuerySet(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        BingCoronavirusQuerySetConfig(
            queries_by="country",
            start_date="2020-09-01",
            end_date="2020-09-30",
            description="Query by: country, start_date: 2020-09-01, end_date: 2020-09-30",
            version=datasets.Version(_VERSION),
        )
    ]
    BUILDER_CONFIG_CLASS = BingCoronavirusQuerySetConfig

    def _info(self):
        if self.config.queries_by == "country":
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "Date": datasets.Value("string"),
                    "Query": datasets.Value("string"),
                    "IsImplicitIntent": datasets.Value("string"),
                    "Country": datasets.Value("string"),
                    "PopularityScore": datasets.Value("int32"),
                },
            )
        elif self.config.queries_by == "state":
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "Date": datasets.Value("string"),
                    "Query": datasets.Value("string"),
                    "IsImplicitIntent": datasets.Value("string"),
                    "State": datasets.Value("string"),
                    "Country": datasets.Value("string"),
                    "PopularityScore": datasets.Value("int32"),
                },
            )
        else:
            raise Exception("Unknown queries_by. Choose one of: country or state")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        def _base_url(queries_by, start_date, end_date):
            if queries_by == "country":
                queries_by = "QueriesByCountry"
            else:
                queries_by = "QueriesByState"
            return _BASE_URL.format(queries_by, start_date, end_date)

        download_url = _base_url(self.config.queries_by, self.config.start_date, self.config.end_date)
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        with open(datapath, encoding="utf-8") as f:
            for sentence_counter, row in enumerate(f):
                if sentence_counter == 0:
                    continue
                row = row.strip().split("\t")
                if self.config.queries_by == "country":
                    resp = {
                        "id": sentence_counter,
                        "Date": row[0],
                        "Query": row[1],
                        "IsImplicitIntent": row[2],
                        "Country": row[3],
                        "PopularityScore": row[4],
                    }
                else:
                    resp = {
                        "id": sentence_counter,
                        "Date": row[0],
                        "Query": row[1],
                        "IsImplicitIntent": row[2],
                        "State": row[3],
                        "Country": row[4],
                        "PopularityScore": int(row[5]),
                    }
                yield sentence_counter, resp
