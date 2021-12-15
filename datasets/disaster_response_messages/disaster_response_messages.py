# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Multilingual Disaster Response Messages dataset."""


import csv

import datasets


_DESCRIPTION = """\
This dataset contains 30,000 messages drawn from events including an earthquake in Haiti in 2010, an earthquake in Chile in 2010, floods in Pakistan in 2010, super-storm Sandy in the U.S.A. in 2012, and news articles spanning a large number of years and 100s of different disasters.
The data has been encoded with 36 different categories related to disaster response and has been stripped of messages with sensitive information in their entirety.
Upon release, this is the featured dataset of a new Udacity course on Data Science and the AI4ALL summer school and is especially utile for text analytics and natural language processing (NLP) tasks and models.
The input data in this job contains thousands of untranslated disaster-related messages and their English translations.
"""

_CITATION = """\
@inproceedings{title={Multilingual Disaster Response Messages}
}
"""

_TRAIN_DOWNLOAD_URL = "https://s3.amazonaws.com/datasets.huggingface.co/disaster_response_messages_training.csv"

_TEST_DOWNLOAD_URL = "https://s3.amazonaws.com/datasets.huggingface.co/disaster_response_messages_test.csv"

_VALID_DOWNLOAD_URL = "https://s3.amazonaws.com/datasets.huggingface.co/disaster_response_messages_validation.csv"


class DisasterResponseMessages(datasets.GeneratorBasedBuilder):
    """Multilingual Disaster Response Messages dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "split": datasets.Value("string"),
                    "message": datasets.Value("string"),
                    "original": datasets.Value("string"),
                    "genre": datasets.Value("string"),
                    "related": datasets.ClassLabel(names=["false", "true", "maybe"]),
                    "PII": datasets.Value("int8"),
                    "request": datasets.ClassLabel(names=["false", "true"]),
                    "offer": datasets.Value("int8"),
                    "aid_related": datasets.ClassLabel(names=["false", "true"]),
                    "medical_help": datasets.ClassLabel(names=["false", "true"]),
                    "medical_products": datasets.ClassLabel(names=["false", "true"]),
                    "search_and_rescue": datasets.ClassLabel(names=["false", "true"]),
                    "security": datasets.ClassLabel(names=["false", "true"]),
                    "military": datasets.ClassLabel(names=["false", "true"]),
                    "child_alone": datasets.Value("int8"),
                    "water": datasets.ClassLabel(names=["false", "true"]),
                    "food": datasets.ClassLabel(names=["false", "true"]),
                    "shelter": datasets.ClassLabel(names=["false", "true"]),
                    "clothing": datasets.ClassLabel(names=["false", "true"]),
                    "money": datasets.ClassLabel(names=["false", "true"]),
                    "missing_people": datasets.ClassLabel(names=["false", "true"]),
                    "refugees": datasets.ClassLabel(names=["false", "true"]),
                    "death": datasets.ClassLabel(names=["false", "true"]),
                    "other_aid": datasets.ClassLabel(names=["false", "true"]),
                    "infrastructure_related": datasets.ClassLabel(names=["false", "true"]),
                    "transport": datasets.ClassLabel(names=["false", "true"]),
                    "buildings": datasets.ClassLabel(names=["false", "true"]),
                    "electricity": datasets.ClassLabel(names=["false", "true"]),
                    "tools": datasets.ClassLabel(names=["false", "true"]),
                    "hospitals": datasets.ClassLabel(names=["false", "true"]),
                    "shops": datasets.ClassLabel(names=["false", "true"]),
                    "aid_centers": datasets.ClassLabel(names=["false", "true"]),
                    "other_infrastructure": datasets.ClassLabel(names=["false", "true"]),
                    "weather_related": datasets.ClassLabel(names=["false", "true"]),
                    "floods": datasets.ClassLabel(names=["false", "true"]),
                    "storm": datasets.ClassLabel(names=["false", "true"]),
                    "fire": datasets.ClassLabel(names=["false", "true"]),
                    "earthquake": datasets.ClassLabel(names=["false", "true"]),
                    "cold": datasets.ClassLabel(names=["false", "true"]),
                    "other_weather": datasets.ClassLabel(names=["false", "true"]),
                    "direct_report": datasets.ClassLabel(names=["false", "true"]),
                }
            ),
            homepage="https://appen.com/datasets/combined-disaster-response-data/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path, test_path, valid_path = dl_manager.download_and_extract(
            [_TRAIN_DOWNLOAD_URL, _TEST_DOWNLOAD_URL, _VALID_DOWNLOAD_URL]
        )
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
        ]

    def _generate_examples(self, filepath):
        """Generate Distaster Response Messages examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader, None)
            for id_, row in enumerate(csv_reader):
                row = row[1:]
                (
                    split,
                    message,
                    original,
                    genre,
                    related,
                    PII,
                    request,
                    offer,
                    aid_related,
                    medical_help,
                    medical_products,
                    search_and_rescue,
                    security,
                    military,
                    child_alone,
                    water,
                    food,
                    shelter,
                    clothing,
                    money,
                    missing_people,
                    refugees,
                    death,
                    other_aid,
                    infrastructure_related,
                    transport,
                    buildings,
                    electricity,
                    tools,
                    hospitals,
                    shops,
                    aid_centers,
                    other_infrastructure,
                    weather_related,
                    floods,
                    storm,
                    fire,
                    earthquake,
                    cold,
                    other_weather,
                    direct_report,
                ) = row

                yield id_, {
                    "split": (split),
                    "message": (message),
                    "original": (original),
                    "genre": (genre),
                    "related": int(related),
                    "PII": int(PII),
                    "request": int(request),
                    "offer": int(offer),
                    "aid_related": int(aid_related),
                    "medical_help": int(medical_help),
                    "medical_products": int(medical_products),
                    "search_and_rescue": int(search_and_rescue),
                    "security": int(security),
                    "military": int(military),
                    "child_alone": int(child_alone),
                    "water": int(water),
                    "food": int(food),
                    "shelter": int(shelter),
                    "clothing": int(clothing),
                    "money": int(money),
                    "missing_people": int(missing_people),
                    "refugees": int(refugees),
                    "death": int(death),
                    "other_aid": int(other_aid),
                    "infrastructure_related": int(infrastructure_related),
                    "transport": int(transport),
                    "buildings": int(buildings),
                    "electricity": int(electricity),
                    "tools": int(tools),
                    "hospitals": int(hospitals),
                    "shops": int(shops),
                    "aid_centers": int(aid_centers),
                    "other_infrastructure": int(other_infrastructure),
                    "weather_related": int(weather_related),
                    "floods": int(floods),
                    "storm": int(storm),
                    "fire": int(fire),
                    "earthquake": int(earthquake),
                    "cold": int(cold),
                    "other_weather": int(other_weather),
                    "direct_report": int(direct_report),
                }
