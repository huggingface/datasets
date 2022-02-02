# coding=utf-8
# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
# TODO: Address all TODOs and remove all explanatory comments
"""TODO: Add a description here."""


import csv
import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
author={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = ""

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)

_AUDIO_URL = "https://huggingface.co/datasets/polinaeterna/ml_spoken_words/resolve/main/data/{lang}/{split}/audio/{n}.tar.gz"
_SPLITS_URL = "https://huggingface.co/datasets/polinaeterna/ml_spoken_words/resolve/main/data/{lang}/splits.tar.gz"

_GENDERS = ["MALE", "FEMALE", "OTHER", "NAN", None]  # TODO: I guess I need to replace Nones with NANs

_LANGUAGES = [
    "en",
    "es",
    "ru",
    "tt"
]  # TODO


class MlSpokenWordsConfig(datasets.BuilderConfig):
    """BuilderConfig for MlSpokenWords."""

    def __init__(self, *args, languages, **kwargs):
        """BuilderConfig for MlSpokenWords.
        Args:
            languages (:obj:`List[str]`): list of languages to load
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            *args,
            name="+".join(languages),
            **kwargs,
        )
        self.languages = languages


class MlSpokenWords(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        MlSpokenWordsConfig(languages=[lang]) for lang in _LANGUAGES
    ]
    BUILDER_CONFIG_CLASS = MlSpokenWordsConfig
    # DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
                {
                    "is_valid": datasets.Value("string"),
                    "language": datasets.ClassLabel(names=_LANGUAGES),
                    "speaker_id": datasets.Value("string"),
                    "gender": datasets.ClassLabel(names=_GENDERS),
                    "keyword": datasets.Value("string"),  # seems that there are too many of them (340k unique keywords)
                    "audio": datasets.Audio(sampling_rate=48_000)
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        lang=self.config.name
        splits_archive_path = dl_manager.download(_SPLITS_URL.format(lang=lang))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "audio_archive": dl_manager.iter_archive(
                        dl_manager.download(_AUDIO_URL.format(lang=lang, split="train", n=0))
                    ),
                    "splits_archive": dl_manager.iter_archive(splits_archive_path),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "audio_archive": dl_manager.iter_archive(
                        dl_manager.download(_AUDIO_URL.format(lang=lang, split="dev", n=0))
                    ),
                    "splits_archive": dl_manager.iter_archive(splits_archive_path),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "audio_archive": dl_manager.iter_archive(
                        dl_manager.download(_AUDIO_URL.format(lang=lang, split="test", n=0))
                    ),
                    "splits_archive": dl_manager.iter_archive(splits_archive_path),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, audio_archive, splits_archive, split):
        metadata = dict()
        from io import StringIO

        for split_filename, split_file in splits_archive:
            if split_filename.split(".csv")[0] == split:
                csv_reader = csv.reader(StringIO(split_file.read().decode()), delimiter=",")  # TODO ?? 
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        continue
                    link, word, is_valid, speaker, gender = row
                    audio_filename = "_".join(link.split("/"))
                    metadata[audio_filename] = {
                        "keyword": word,
                        "is_valid": is_valid,
                        "speaker_id": speaker,
                        "gender": gender,
                    }

        for audio_filename, audio_file in audio_archive:
            yield audio_filename, {
                "language": self.config.name,
                "audio": {"path": audio_filename, "bytes": audio_file.read()},
                **metadata[audio_filename],
            }