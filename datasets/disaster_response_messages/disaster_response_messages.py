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

from __future__ import absolute_import, division, print_function

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

_TRAIN_DOWNLOAD_URL = (
    "https://datasets.appen.com/appen_datasets/disaster_response_data/disaster_response_messages_training.csv"
)
_TEST_DOWNLOAD_URL = (
    "https://datasets.appen.com/appen_datasets/disaster_response_data/disaster_response_messages_test.csv"
)


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
                    "related": datasets.Value("int8"),
                    "PII": datasets.Value("int8"),
                    "request": datasets.Value("int8"),
                    "offer": datasets.Value("int8"),
                    "aid_related": datasets.Value("int8"),
                    "medical_help": datasets.Value("int8"),
                    "medical_products": datasets.Value("int8"),
                    "search_and_rescue": datasets.Value("int8"),
                    "security": datasets.Value("int8"),
                    "military": datasets.Value("int8"),
                    "child_alone": datasets.Value("int8"),
                    "water": datasets.Value("int8"),
                    "food": datasets.Value("int8"),
                    "shelter": datasets.Value("int8"),
                    "clothing": datasets.Value("int8"),
                    "money": datasets.Value("int8"),
                    "missing_people": datasets.Value("int8"),
                    "refugees": datasets.Value("int8"),
                    "death": datasets.Value("int8"),
                    "other_aid": datasets.Value("int8"),
                    "infrastructure_related": datasets.Value("int8"),
                    "transport": datasets.Value("int8"),
                    "buildings": datasets.Value("int8"),
                    "electricity": datasets.Value("int8"),
                    "tools": datasets.Value("int8"),
                    "hospitals": datasets.Value("int8"),
                    "shops": datasets.Value("int8"),
                    "aid_centers": datasets.Value("int8"),
                    "other_infrastructure": datasets.Value("int8"),
                    "weather_related": datasets.Value("int8"),
                    "floods": datasets.Value("int8"),
                    "storm": datasets.Value("int8"),
                    "fire": datasets.Value("int8"),
                    "earthquake": datasets.Value("int8"),
                    "cold": datasets.Value("int8"),
                    "other_weather": datasets.Value("int8"),
                    "direct_report": datasets.Value("int8"),
                }
            ),
            homepage="https://appen.com/datasets/combined-disaster-response-data/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
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
                # message=row[:2]
                # print(row)
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
                # print(type(related))
                # print(related)
                # print(message)
                # related=int(related)
                # PII=int(PII)
                # request=int(request)
                # offer=int(offer)
                # aid_related=int(aid_related)
                # medical_help=int(medical_help)
                # medical_products=int(medical_products)
                # search_and_rescue=int(search_and_rescue)
                # security=int(security)
                # military=int(military)
                # child_alone=int(child_alone)
                # water=int(water)
                # food=int(food)
                # shelter=int(shelter)
                # clothing=int(clothing)
                # money=int(money)
                # missing_people=int(missing_people)
                # refugees=int(refugees)
                # death=int(death)
                # other_aid=int(other_aid)
                # infrastructure_related=int(infrastructure_related)
                # transport=int(transport)
                # buildings=int(buildings)
                # electricity=int(electricity)
                # tools=int(tools)
                # hospitals=int(hospitals)
                # shops=int(shops)
                # aid_centers=int(aid_centers)
                # other_infrastructure=int(other_infrastructure)
                # weather_related=int(weather_related)
                # floods=int(floods)
                # storm=int(storm)
                # fire=int(fire)
                # earthquake=int(earthquake)
                # cold=int(cold)
                # other_weather=int(other_weather)
                # direct_report=int(direct_report)

                yield id_, {
                    "split": split,
                    "message": message,
                    "original": original,
                    "genre": genre,
                    "related": related,
                    "PII": PII,
                    "request": request,
                    "offer": offer,
                    "aid_related": aid_related,
                    "medical_help": medical_help,
                    "medical_products": medical_products,
                    "search_and_rescue": search_and_rescue,
                    "security": security,
                    "military": military,
                    "child_alone": child_alone,
                    "water": water,
                    "food": food,
                    "shelter": shelter,
                    "clothing": clothing,
                    "money": money,
                    "missing_people": missing_people,
                    "refugees": refugees,
                    "death": death,
                    "other_aid": other_aid,
                    "infrastructure_related": infrastructure_related,
                    "transport": transport,
                    "buildings": buildings,
                    "electricity": electricity,
                    "tools": tools,
                    "hospitals": hospitals,
                    "shops": shops,
                    "aid_centers": aid_centers,
                    "other_infrastructure": other_infrastructure,
                    "weather_related": weather_related,
                    "floods": floods,
                    "storm": storm,
                    "fire": fire,
                    "earthquake": earthquake,
                    "cold": cold,
                    "other_weather": other_weather,
                    "direct_report": direct_report,
                }
