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
from functools import partial

import datasets
from datasets.utils.streaming_download_manager import xopen

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

_BASE_URL = "https://huggingface.co/datasets/polinaeterna/ml_spoken_words/resolve/main/data/{lang}/"
_AUDIO_URL = _BASE_URL + "{split}/audio/{n}.tar.gz"
_SPLITS_URL = _BASE_URL + "splits.tar.gz"
_N_FILES_URL = _BASE_URL + "{split}/n_files.txt"

_GENDERS = ["MALE", "FEMALE", "OTHER", "NAN"]


_LANGUAGES = [
    "ar",
    "as",
    "br",
    "ca",
    "cnh",
    "cs",
    "cv",
    "cy",
    "de",
    "dv",
    "el",
    "en",
    "eo",
    "es",
    "et",
    "eu",
    "fa",
    "fr",
    "fy-NL",
    "ga-IE",
    "gn",
    "ha",
    "ia",
    "id",
    "it",
    "ka",
    "ky",
    "lt",
    "lv",
    "mn",
    "mt",
    "nl",
    "or",
    "pl",
    "pt",
    "rm-sursilv",
    "rm-vallader",
    "ro",
    "ru",
    "rw",
    "sah",
    "sk",
    "sl",
    "sv-SE",
    "ta",
    "tr",
    "tt",
    "uk",
    "vi",
    "zh-CN",
]


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
            name="+".join(languages) if isinstance(languages, list) else languages,
            **kwargs,
        )
        self.languages = languages if isinstance(languages, list) else [languages]


class MlSpokenWords(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        MlSpokenWordsConfig(languages=[lang]) for lang in _LANGUAGES
    ]
    BUILDER_CONFIG_CLASS = MlSpokenWordsConfig

    def _info(self):
        features = datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "is_valid": datasets.Value("string"),
                    "language": datasets.ClassLabel(names=self.config.languages),
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
        splits_archive_path = [dl_manager.download(_SPLITS_URL.format(lang=lang)) for lang in self.config.languages]
        download_audio = partial(_download_audio_archives, dl_manager=dl_manager)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "audio_archives": [download_audio(split="train", lang=lang) for lang in self.config.languages],
                    "splits_archive": [dl_manager.iter_archive(path) for path in splits_archive_path],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "audio_archives": [download_audio(split="dev", lang=lang) for lang in self.config.languages],
                    "splits_archive": [dl_manager.iter_archive(path) for path in splits_archive_path],
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "audio_archives": [download_audio(split="test", lang=lang) for lang in self.config.languages],
                    "splits_archive": [dl_manager.iter_archive(path) for path in splits_archive_path],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, audio_archives, splits_archive, split):
        metadata = dict()
        for lang_idx, lang in enumerate(self.config.languages):
            for split_filename, split_file in splits_archive[lang_idx]:
                if split_filename.split(".csv")[0] == split:
                    # TODO: how to correctly process csv files from tar?
                    csv_reader = csv.reader([line.decode("utf-8") for line in split_file.readlines()], delimiter=",")
                    for i, (link, word, is_valid, speaker, gender) in enumerate(csv_reader):
                        if i == 0:
                            continue
                        audio_filename = "_".join(link.split("/"))
                        metadata[audio_filename] = {
                            "keyword": word,
                            "is_valid": is_valid,
                            "speaker_id": speaker,
                            "gender": gender if gender else "NAN",  # some values are None
                        }

            for audio_archive in audio_archives[lang_idx]:
                for audio_filename, audio_file in audio_archive:
                    yield audio_filename, {
                        "file": audio_filename,
                        "language": lang,
                        "audio": {"path": audio_filename, "bytes": audio_file.read()},
                        **metadata[audio_filename],
                    }


def _download_audio_archives(dl_manager, lang, split):
    """
    All audio files are stored in several .tar.gz archives with names like 0.tar.gz, 1.tar.gz, ...
    Number of archives stored in a separate .txt file (n_files.txt)

    Prepare all the audio archives for iterating over them and their audio files.
    """

    n_files_url = _N_FILES_URL.format(lang=lang, split=split)
    n_files_path = dl_manager.download(n_files_url)

    with open(n_files_path, "r", encoding="utf-8") as file:
        n_files = int(file.read().strip())  # the file contains a number of archives

    archive_urls = [_AUDIO_URL.format(lang=lang, split=split, n=i) for i in range(n_files)]
    archive_paths = dl_manager.download(archive_urls)

    return [dl_manager.iter_archive(archive_path) for archive_path in archive_paths]
