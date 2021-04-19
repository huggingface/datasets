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
"""NLU Evaluation Data."""

from __future__ import absolute_import, division, print_function

import csv
import re

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@InProceedings{XLiu.etal:IWSDS2019,
  author    = {Xingkun Liu, Arash Eshghi, Pawel Swietojanski and Verena Rieser},
  title     = {Benchmarking Natural Language Understanding Services for building Conversational Agents},
  booktitle = {Proceedings of the Tenth International Workshop on Spoken Dialogue Systems Technology (IWSDS)},
  month     = {April},
  year      = {2019},
  address   = {Ortigia, Siracusa (SR), Italy},
  publisher = {Springer},
  pages     = {xxx--xxx},
  url       = {http://www.xx.xx/xx/}
}
"""

# You can copy an official description
_DESCRIPTION = """\
Raw part of NLU Evaluation Data. It contains 25 715 non-empty examples from 68 unique intents belonging to 18 scenarios.
"""

_HOMEPAGE = "https://github.com/xliuhw/NLU-Evaluation-Data"

_LICENSE = "Creative Commons Attribution 4.0 International License (CC BY 4.0)"

_URL = "https://raw.githubusercontent.com/xliuhw/NLU-Evaluation-Data/master/AnnotatedData/NLU-Data-Home-Domain-Annotated-All.csv"

ANNOTATION_PATTERN = re.compile(r"\[(.+?)\s+\:+\s(.+?)\]")


def remove_annotations(text):
    """
    Remove named entity annotations from text example.

    Examples are defined based on `answer_annotation` column since it has the least number
    of Nans. However, this column contains patterns of annotation of the form:

        [named_entity : part_of_text]

        e.g. [time : five am], [date : this week]

    We identity them with regex rule and replace all occurrences with just part_of_text.
    """
    return ANNOTATION_PATTERN.sub(r"\2", text)


def define_intent_name(scenario, intent):
    """
    Intent name is defined as concatenation of `scenario` and `intent` values.

    See Also:
        https://github.com/xliuhw/NLU-Evaluation-Data/issues/5
    """
    return f"{scenario}_{intent}"


class NLUEvaluationDataset(datasets.GeneratorBasedBuilder):
    """Raw part of NLU Evaluation Data."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "answer_annotation": datasets.Value("string"),
                "scenario": datasets.Value("string"),
                "intent": datasets.Value("string"),
            }
        )
        post_process_features = datasets.Features(
            {
                "text": datasets.Value("string"),
                "scenario": datasets.Value("string"),
                "label": datasets.features.ClassLabel(
                    names=[
                        "alarm_query",
                        "alarm_remove",
                        "alarm_set",
                        "audio_volume_down",
                        "audio_volume_mute",
                        "audio_volume_other",
                        "audio_volume_up",
                        "calendar_query",
                        "calendar_remove",
                        "calendar_set",
                        "cooking_query",
                        "cooking_recipe",
                        "datetime_convert",
                        "datetime_query",
                        "email_addcontact",
                        "email_query",
                        "email_querycontact",
                        "email_sendemail",
                        "general_affirm",
                        "general_commandstop",
                        "general_confirm",
                        "general_dontcare",
                        "general_explain",
                        "general_greet",
                        "general_joke",
                        "general_negate",
                        "general_praise",
                        "general_quirky",
                        "general_repeat",
                        "iot_cleaning",
                        "iot_coffee",
                        "iot_hue_lightchange",
                        "iot_hue_lightdim",
                        "iot_hue_lightoff",
                        "iot_hue_lighton",
                        "iot_hue_lightup",
                        "iot_wemo_off",
                        "iot_wemo_on",
                        "lists_createoradd",
                        "lists_query",
                        "lists_remove",
                        "music_dislikeness",
                        "music_likeness",
                        "music_query",
                        "music_settings",
                        "news_query",
                        "play_audiobook",
                        "play_game",
                        "play_music",
                        "play_podcasts",
                        "play_radio",
                        "qa_currency",
                        "qa_definition",
                        "qa_factoid",
                        "qa_maths",
                        "qa_stock",
                        "recommendation_events",
                        "recommendation_locations",
                        "recommendation_movies",
                        "social_post",
                        "social_query",
                        "takeaway_order",
                        "takeaway_query",
                        "transport_query",
                        "transport_taxi",
                        "transport_ticket",
                        "transport_traffic",
                        "weather_query",
                    ]
                ),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            post_processed=datasets.info.PostProcessedInfo(
                features=post_process_features,
            ),
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
        ]

    def _post_process(self, dataset, resources_paths):
        # remove empty examples
        dataset = dataset.filter(lambda ex: True if ex["answer_annotation"] != "null" else False, with_indices=False)
        # remove annotations from examples and define label
        dataset = dataset.map(
            lambda ex: dict(
                ex,
                text=remove_annotations(ex["answer_annotation"]),
                label=self.info.post_processed.features["label"].encode_example(
                    define_intent_name(ex["scenario"], ex["intent"])
                ),
            ),
            batched=False,
            with_indices=False,
            features=datasets.Features(self.info.features, **self.info.post_processed.features),
        )
        # drop unused columns
        dataset = dataset.remove_columns(["answer_annotation", "intent"])
        return dataset

    def _generate_examples(self, filepath):
        """ Yields examples as (key, example) tuples. """
        with open(filepath, encoding="utf-8") as f:
            csv_reader = csv.reader(f, quotechar='"', delimiter=";", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            # call next to skip header
            next(csv_reader)
            for id_, row in enumerate(csv_reader):
                (
                    userid,
                    answerid,
                    scenario,
                    intent,
                    status,
                    answer_annotation,
                    notes,
                    suggested_entities,
                    answer_normalised,
                    answer,
                    question,
                ) = row

                yield id_, {"answer_annotation": answer_annotation, "scenario": scenario, "intent": intent}
