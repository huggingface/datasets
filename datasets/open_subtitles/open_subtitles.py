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
import os

import datasets


_DESCRIPTION = """\
This is a new collection of translated movie subtitles from http://www.opensubtitles.org/.

IMPORTANT: If you use the OpenSubtitle corpus: Please, add a link to http://www.opensubtitles.org/ to your website and to your reports and publications produced with the data!

This is a slightly cleaner version of the subtitle collection using improved sentence alignment and better language checking.

62 languages, 1,782 bitexts
total number of files: 3,735,070
total number of tokens: 22.10G
total number of sentence fragments: 3.35G
"""
_HOMEPAGE_URL = "http://opus.nlpl.eu/OpenSubtitles.php"
_CITATION = """\
P. Lison and J. Tiedemann, 2016, OpenSubtitles2016: Extracting Large Parallel Corpora from Movie and TV Subtitles. In Proceedings of the 10th International Conference on Language Resources and Evaluation (LREC 2016)
"""

_VERSION = "2018.0.0"
_BASE_NAME = "OpenSubtitles.{}.{}"
_BASE_URL = "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/moses/{}-{}.txt.zip"

# Please note that only few pairs are shown here. You can use config to generate data for all language pairs
_LANGUAGE_PAIRS = [
    ("bs", "eo"),
    ("fr", "hy"),
    ("da", "ru"),
    ("en", "hi"),
    ("bn", "is"),
]


class OpenSubtitlesConfig(datasets.BuilderConfig):
    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2


class OpenSubtitles(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        OpenSubtitlesConfig(
            lang1=lang1,
            lang2=lang2,
            description=f"Translating {lang1} to {lang2} or vice versa",
            version=datasets.Version(_VERSION),
        )
        for lang1, lang2 in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = OpenSubtitlesConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "meta": {
                        "year": datasets.Value("uint32"),
                        "imdbId": datasets.Value("uint32"),
                        "subtitleId": {
                            self.config.lang1: datasets.Value("uint32"),
                            self.config.lang2: datasets.Value("uint32"),
                        },
                        "sentenceIds": {
                            self.config.lang1: datasets.Sequence(datasets.Value("uint32")),
                            self.config.lang2: datasets.Sequence(datasets.Value("uint32")),
                        },
                    },
                    "translation": datasets.Translation(languages=(self.config.lang1, self.config.lang2)),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        def _base_url(lang1, lang2):
            return _BASE_URL.format(lang1, lang2)

        download_url = _base_url(self.config.lang1, self.config.lang2)
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    @classmethod
    def _extract_info(cls, sentence_id):
        # see https://github.com/huggingface/datasets/issues/1844
        # sentence ids have the following format: en/2017/7006210/7050201.xml.gz
        # lang/year/imdb_id/opensubtitles_id.xml.gz
        parts = sentence_id[: -len(".xml.gz")].split("/")
        parts.pop(0)  # remove lang, we do not need it

        # returns year, imdb_id, opensubtitles_id
        return tuple(map(int, parts))

    def _generate_examples(self, datapath):
        l1, l2 = self.config.lang1, self.config.lang2
        folder = l1 + "-" + l2
        l1_file = _BASE_NAME.format(folder, l1)
        l2_file = _BASE_NAME.format(folder, l2)
        ids_file = _BASE_NAME.format(folder, "ids")
        l1_path = os.path.join(datapath, l1_file)
        l2_path = os.path.join(datapath, l2_file)
        ids_path = os.path.join(datapath, ids_file)
        with open(l1_path, encoding="utf-8") as f1, open(l2_path, encoding="utf-8") as f2, open(
            ids_path, encoding="utf-8"
        ) as f3:
            for sentence_counter, (x, y, _id) in enumerate(zip(f1, f2, f3)):
                x = x.strip()
                y = y.strip()
                l1_id, l2_id, l1_sid, l2_sid = _id.split("\t")
                year, imdb_id, l1_subtitle_id = self._extract_info(l1_id)
                _, _, l2_subtitle_id = self._extract_info(l2_id)
                l1_sentence_ids = list(map(int, l1_sid.split(" ")))
                l2_sentence_ids = list(map(int, l2_sid.split(" ")))

                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "meta": {
                            "year": year,
                            "imdbId": imdb_id,
                            "subtitleId": {l1: l1_subtitle_id, l2: l2_subtitle_id},
                            "sentenceIds": {l1: l1_sentence_ids, l2: l2_sentence_ids},
                        },
                        "translation": {l1: x, l2: y},
                    },
                )
                sentence_counter += 1
                yield result
