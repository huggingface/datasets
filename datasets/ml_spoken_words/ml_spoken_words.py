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

"""
Multilingual Spoken Words Corpus is a large and growing audio dataset of spoken
words in 50 languages collectively spoken by over 5 billion people, for academic
research and commercial applications in keyword spotting and spoken term search,
licensed under CC-BY 4.0. The dataset contains more than 340,000 keywords,
totaling 23.4 million 1-second spoken examples (over 6,000 hours).
 """


import csv
from functools import partial

import datasets


_CITATION = """\
@inproceedings{mazumder2021multilingual,
  title={Multilingual Spoken Words Corpus},
  author={Mazumder, Mark and Chitlangia, Sharad and Banbury, Colby and Kang, Yiping and Ciro, Juan Manuel and Achorn, Keith and Galvez, Daniel and Sabini, Mark and Mattson, Peter and Kanter, David and others},
  booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
  year={2021}
}
"""

_DESCRIPTION = """\
Multilingual Spoken Words Corpus is a large and growing audio dataset of spoken
words in 50 languages collectively spoken by over 5 billion people, for academic
research and commercial applications in keyword spotting and spoken term search,
licensed under CC-BY 4.0. The dataset contains more than 340,000 keywords,
totaling 23.4 million 1-second spoken examples (over 6,000 hours). The dataset
has many use cases, ranging from voice-enabled consumer devices to call center
automation. This dataset is generated by applying forced alignment on crowd-sourced sentence-level
audio to produce per-word timing estimates for extraction.
All alignments are included in the dataset.
"""

_HOMEPAGE = "https://mlcommons.org/en/multilingual-spoken-words/"

_LICENSE = "CC-BY 4.0."

_VERSION = datasets.Version("1.0.0")

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
            languages (:obj:`Union[List[str], str]`): language or list of languages to load
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            *args,
            name="+".join(languages) if isinstance(languages, list) else languages,
            **kwargs,
        )
        self.languages = languages if isinstance(languages, list) else [languages]


class MlSpokenWords(datasets.GeneratorBasedBuilder):
    """
    Multilingual Spoken Words Corpus is a large and growing audio dataset of spoken
    words in 50 languages collectively spoken by over 5 billion people, for academic
    research and commercial applications in keyword spotting and spoken term search,
    licensed under CC-BY 4.0. The dataset contains more than 340,000 keywords,
    totaling 23.4 million 1-second spoken examples (over 6,000 hours).
    """

    VERSION = _VERSION
    BUILDER_CONFIGS = [MlSpokenWordsConfig(languages=[lang], version=_VERSION) for lang in _LANGUAGES]
    BUILDER_CONFIG_CLASS = MlSpokenWordsConfig

    def _info(self):
        features = datasets.Features(
            {
                "file": datasets.Value("string"),
                "is_valid": datasets.Value("bool"),
                "language": datasets.ClassLabel(names=self.config.languages),
                "speaker_id": datasets.Value("string"),
                "gender": datasets.ClassLabel(names=_GENDERS),
                "keyword": datasets.Value("string"),  # seems that there are too many of them (340k unique keywords)
                "audio": datasets.Audio(sampling_rate=48_000),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
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
                            "gender": gender if gender and gender != "NA" else "NAN",  # some values are "NA"
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
