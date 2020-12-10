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
"""Coached Conversational Preference Elicitation Dataset to Understanding Movie Preferences"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{48414,
title	= {Coached Conversational Preference Elicitation: A Case Study in Understanding Movie Preferences},
author	= {Filip Radlinski and Krisztian Balog and Bill Byrne and Karthik Krishnamoorthi},
year	= {2019},
booktitle	= {Proceedings of the Annual SIGdial Meeting on Discourse and Dialogue}
}
"""

_DESCRIPTION = """\
A dataset consisting of 502 English dialogs with 12,000 annotated utterances between a user and an assistant discussing
movie preferences in natural language. It was collected using a Wizard-of-Oz methodology between two paid crowd-workers,
where one worker plays the role of an 'assistant', while the other plays the role of a 'user'. The 'assistant' elicits
the 'user’s' preferences about movies following a Coached Conversational Preference Elicitation (CCPE) method. The
assistant asks questions designed to minimize the bias in the terminology the 'user' employs to convey his or her
preferences as much as possible, and to obtain these preferences in natural language. Each dialog is annotated with
entity mentions, preferences expressed about entities, descriptions of entities provided, and other statements of
entities."""

_HOMEPAGE = "https://research.google/tools/datasets/coached-conversational-preference-elicitation/"

_LICENSE = "https://creativecommons.org/licenses/by-sa/4.0/"

_URLs = {"dataset": "https://storage.googleapis.com/dialog-data-corpus/CCPE-M-2019/data.json"}


class CoachedConvPrefConfig(datasets.BuilderConfig):
    """BuilderConfig for DialogRE"""

    def __init__(self, **kwargs):
        """BuilderConfig for DialogRE.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(CoachedConvPrefConfig, self).__init__(**kwargs)


class CoachedConvPref(datasets.GeneratorBasedBuilder):
    """Coached Conversational Preference Elicitation Dataset to Understanding Movie Preferences"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        CoachedConvPrefConfig(
            name="coached_conv_pref",
            version=datasets.Version("1.1.0"),
            description="Coached Conversational Preference Elicitation Dataset to Understanding Movie Preferences",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "conversationId": datasets.Value("string"),
                    "utterances": datasets.Sequence(
                        {
                            "index": datasets.Value("int32"),
                            "speaker": datasets.features.ClassLabel(names=["USER", "ASSISTANT"]),
                            "text": datasets.Value("string"),
                            "segments": datasets.Sequence(
                                {
                                    "startIndex": datasets.Value("int32"),
                                    "endIndex": datasets.Value("int32"),
                                    "text": datasets.Value("string"),
                                    "annotations": datasets.Sequence(
                                        {
                                            "annotationType": datasets.features.ClassLabel(
                                                names=[
                                                    "ENTITY_NAME",
                                                    "ENTITY_PREFERENCE",
                                                    "ENTITY_DESCRIPTION",
                                                    "ENTITY_OTHER",
                                                ]
                                            ),
                                            "entityType": datasets.features.ClassLabel(
                                                names=[
                                                    "MOVIE_GENRE_OR_CATEGORY",
                                                    "MOVIE_OR_SERIES",
                                                    "PERSON",
                                                    "SOMETHING_ELSE",
                                                ]
                                            ),
                                        }
                                    ),
                                }
                            ),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URLs)

        # Dataset is a single corpus (does not contain any split)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["dataset"]),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        # Empty Segment list with annotations dictionary
        # First prompt of a conversation does not contain the segment dictionary
        # We are setting it to None values
        segments_empty = [
            {
                "startIndex": 0,
                "endIndex": 0,
                "text": "",
                "annotations": [],
            }
        ]

        with open(filepath, encoding="utf-8") as f:
            dataset = json.load(f)

            for id_, data in enumerate(dataset):
                conversationId = data["conversationId"]

                utterances = data["utterances"]
                for utterance in utterances:
                    if "segments" not in utterance:
                        utterance["segments"] = segments_empty.copy()

                yield id_, {
                    "conversationId": conversationId,
                    "utterances": utterances,
                }
