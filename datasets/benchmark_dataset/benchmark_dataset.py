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
# TODO: Address all TODOs and remove all explanatory comments
"""TODO: Add a description here."""

import csv
import os

import datasets
from transliterate import translit

_ROOT_URL = "https://huggingface.co/datasets/polinaeterna/benchmark_dataset/resolve/main/"
_BASE_URL = _ROOT_URL + "{config}/"

_GENDERS = ["MALE", "FEMALE", "OTHER", "NAN"]


class BenchmarkDataset(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="single-tar", version=VERSION, description="All data in one .tar.gz"),
        datasets.BuilderConfig(name="splits-tar", version=VERSION, description="Separate .tar.gz for each splits"),
        datasets.BuilderConfig(name="zip", version=VERSION, description="All data in one .zip"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "file": datasets.Value("string"),
                "is_valid": datasets.Value("bool"),
                "speaker_id": datasets.Value("string"),
                "gender": datasets.ClassLabel(names=_GENDERS),
                "keyword": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=16_000),
            }
        )
        return datasets.DatasetInfo(
            features=features,
        )

    def _split_generators(self, dl_manager):
        splits_urls = {
            "train": _ROOT_URL + "train.csv",
            "dev": _ROOT_URL + "dev.csv",
            "test": _ROOT_URL + "test.csv",
        }
        splits_paths = dl_manager.download(splits_urls)

        if self.config.name == "single-tar":
            url = _BASE_URL.format(config=self.config.name) + "audio.tar.gz"
            archive_path = dl_manager.download(url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_path),
                        "split_path": splits_paths["train"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_path),
                        "split_path": splits_paths["dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_path),
                        "split_path": splits_paths["test"],
                    },
                ),
            ]

        elif self.config.name == "zip":
            url = _BASE_URL.format(config=self.config.name) + "audio-translit.zip"
            archive_path = dl_manager.download_and_extract(url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "audio_archive": archive_path,
                        "split_path": splits_paths["train"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "audio_archive": archive_path,
                        "split_path": splits_paths["dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "audio_archive": archive_path,
                        "split_path": splits_paths["test"],
                    },
                ),
            ]

        elif self.config.name == "splits-tar":
            urls = {
                "train": _BASE_URL.format(config=self.config.name) + "train.tar.gz",
                "dev": _BASE_URL.format(config=self.config.name) + "dev.tar.gz",
                "test": _BASE_URL.format(config=self.config.name) + "test.tar.gz"
            }
            archive_paths = dl_manager.download(urls)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_paths["train"]),
                        "split_path": splits_paths["train"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_paths["dev"]),
                        "split_path": splits_paths["dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "audio_archive": dl_manager.iter_archive(archive_paths["test"]),
                        "split_path": splits_paths["test"],
                    },
                ),
            ]

    def _generate_examples_single_tar(self, audio_archive, split_path):
        metadata = dict()
        with open(split_path, "r", encoding="utf-8") as split_file:
            csv_reader = csv.reader(split_file, delimiter=",")
            for i, (link, word, is_valid, speaker, gender) in enumerate(csv_reader):
                if i == 0:
                    continue
                audio_filename = "_".join(link.split("/")).split(".opus")[0] + ".wav"
                metadata[audio_filename] = {
                    "keyword": word,
                    "is_valid": is_valid,
                    "speaker_id": speaker,
                    "gender": gender if gender and gender != "NA" else "NAN",  # some values are "NA"
                }
        split_audio_filenames = set(metadata.keys())

        for audio_filename, audio_file in audio_archive:
            if audio_filename in split_audio_filenames:
                yield audio_filename, {
                    "file": audio_filename,
                    "audio": {"path": audio_filename, "bytes": audio_file.read()},
                    **metadata[audio_filename],
                }

    def _generate_examples_splits_tar(self, audio_archive, split_path):
        metadata = dict()
        with open(split_path, "r", encoding="utf-8") as split_file:
            csv_reader = csv.reader(split_file, delimiter=",")
            for i, (link, word, is_valid, speaker, gender) in enumerate(csv_reader):
                if i == 0:
                    continue
                audio_filename = "_".join(link.split("/")).split(".opus")[0] + ".wav"
                metadata[audio_filename] = {
                    "keyword": word,
                    "is_valid": is_valid,
                    "speaker_id": speaker,
                    "gender": gender if gender and gender != "NA" else "NAN",  # some values are "NA"
                }

        for audio_filename, audio_file in audio_archive:
            yield audio_filename, {
                "file": audio_filename,
                "audio": {"path": audio_filename, "bytes": audio_file.read()},
                **metadata[audio_filename],
            }

    def _generate_examples_zip(self, audio_archive, split_path):
        with open(split_path, "r", encoding="utf-8") as split_file:
            csv_reader = csv.reader(split_file, delimiter=",")
            for i, (link, word, is_valid, speaker, gender) in enumerate(csv_reader):
                if i == 0:
                    continue
                audio_filename = "_".join(link.split("/")).split(".opus")[0] + ".wav"
                meta = {
                    "keyword": word,
                    "is_valid": is_valid,
                    "speaker_id": speaker,
                    "gender": gender if gender and gender != "NA" else "NAN",  # some values are "NA"
                }
                audio_path = os.path.join(audio_archive, "audio-translit", translit(audio_filename, reversed=True))
                yield audio_path, {
                    "file": audio_filename,
                    "audio": {
                        "path": audio_filename,
                        "bytes": open(audio_path, "rb").read()
                    },
                    **meta,
            }

    def _generate_examples(self, audio_archive, split_path):
        if self.config.name == "single-tar":
            yield from self._generate_examples_single_tar(audio_archive, split_path)
        elif self.config.name == "splits-tar":
            yield from self._generate_examples_splits_tar(audio_archive, split_path)
        elif self.config.name == "zip":
            yield from self._generate_examples_zip(audio_archive, split_path)
