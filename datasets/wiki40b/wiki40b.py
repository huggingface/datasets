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

"""Wiki40B: A clean Wikipedia dataset for 40+ languages."""

from __future__ import absolute_import, division, print_function

import logging

import datasets


_CITATION = """
"""

_DESCRIPTION = """
Clean-up text for 40+ Wikipedia languages editions of pages
correspond to entities. The datasets have train/dev/test splits per language.
The dataset is cleaned up by page filtering to remove disambiguation pages,
redirect pages, deleted pages, and non-entity pages. Each example contains the
wikidata id of the entity, and the full Wikipedia article after page processing
that removes non-content sections and structured objects.
"""

_LICENSE = """
This work is licensed under the Creative Commons Attribution-ShareAlike
3.0 Unported License. To view a copy of this license, visit
http://creativecommons.org/licenses/by-sa/3.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
"""

_URL = "https://research.google/pubs/pub49029/"

_DATA_DIRECTORY = "gs://tfds-data/downloads/wiki40b/tfrecord_prod"

WIKIPEDIA_LANGUAGES = [
    "en",
    "ar",
    "zh-cn",
    "zh-tw",
    "nl",
    "fr",
    "de",
    "it",
    "ja",
    "ko",
    "pl",
    "pt",
    "ru",
    "es",
    "th",
    "tr",
    "bg",
    "ca",
    "cs",
    "da",
    "el",
    "et",
    "fa",
    "fi",
    "he",
    "hi",
    "hr",
    "hu",
    "id",
    "lt",
    "lv",
    "ms",
    "no",
    "ro",
    "sk",
    "sl",
    "sr",
    "sv",
    "tl",
    "uk",
    "vi",
]


class Wiki40bConfig(datasets.BuilderConfig):
    """BuilderConfig for Wiki40B."""

    def __init__(self, language=None, **kwargs):
        """BuilderConfig for Wiki40B.

        Args:
          language: string, the language code for the Wiki40B dataset to use.
          **kwargs: keyword arguments forwarded to super.
        """
        super(Wiki40bConfig, self).__init__(
            name=str(language), description="Wiki40B dataset for {0}.".format(language), **kwargs
        )
        self.language = language


_VERSION = datasets.Version("1.1.0")


class Wiki40b(datasets.BeamBasedBuilder):
    """Wiki40B: A Clean Wikipedia Dataset for Mutlilingual Language Modeling."""

    BUILDER_CONFIGS = [
        Wiki40bConfig(
            version=_VERSION,
            language=lang,
        )  # pylint:disable=g-complex-comprehension
        for lang in WIKIPEDIA_LANGUAGES
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "wikidata_id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "version_id": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        lang = self.config.language

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepaths": f"{_DATA_DIRECTORY}/train/{lang}_examples-*"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepaths": f"{_DATA_DIRECTORY}/dev/{lang}_examples-*"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepaths": f"{_DATA_DIRECTORY}/test/{lang}_examples-*"},
            ),
        ]

    def _build_pcollection(self, pipeline, filepaths):
        """Build PCollection of examples."""
        import apache_beam as beam
        import tensorflow as tf

        logging.info("generating examples from = %s", filepaths)

        def _extract_content(example):
            """Extracts content from a TFExample."""
            wikidata_id = example.features.feature["wikidata_id"].bytes_list.value[0].decode("utf-8")
            text = example.features.feature["text"].bytes_list.value[0].decode("utf-8")
            version_id = example.features.feature["version_id"].bytes_list.value[0].decode("utf-8")

            # wikidata_id could be duplicated with different texts.
            yield wikidata_id + text, {
                "wikidata_id": wikidata_id,
                "text": text,
                "version_id": version_id,
            }

        return (
            pipeline
            | beam.io.ReadFromTFRecord(filepaths, coder=beam.coders.ProtoCoder(tf.train.Example))
            | beam.FlatMap(_extract_content)
        )
