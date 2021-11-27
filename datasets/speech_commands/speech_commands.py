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
"""TODO: Add a description here."""


import glob
import os

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_URL = "https://www.tensorflow.org/datasets/catalog/speech_commands"
_DL_URL = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
_DESCRIPTION = "dummy description"  # TODO
_CITATION = "dummy citation"  # TODO
_LICENSE = "dummy license"  # TODO


WORDS = [
    "yes",
    "no",
    "up",
    "down",
    "left",
    "right",
    "on",
    "off",
    "stop",
    "go",
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "backward",
    "forward",
    "follow",
    "learn"

]

LABELS = WORDS + ["_unrecognized_", "_background_noise_"]


# class SpeechCommandsConfig(datasets.BuilderConfig):
#     #  TODO: likely I don't need a custom config
#     """BuilderConfig for SpeechCommands. """
#
#     def __init__(self, *args, **kwargs):
#         super(SpeechCommandsConfig, self).__init__(version=datasets.Version("0.0.2"), **kwargs)


class SpeechCommands(datasets.GeneratorBasedBuilder):
    # DEFAULT_WRITER_BATCH_SIZE = 256  # TODO: do I need it?
    # BUILDER_CONFIGS = [SpeechCommandsConfig()]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=16_000),
                    "label": datasets.ClassLabel(names=LABELS),
                    "speaker_id": datasets.Value("string"),
                    "utterance_id": datasets.Value("int8"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "label"),  # TODO: understand what that means
            homepage=_URL,
            citation=_CITATION,
            license=_LICENSE,
            version=datasets.Version("0.0.2"),
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(_DL_URL)
        split_to_paths = _split_files(archive_path)

        # TODO: make `archive_path` a class attribute / self.config attr since it's the same for each split?
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"archive_path": archive_path, "filenames": split_to_paths["train"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"archive_path": archive_path, "filenames": split_to_paths["val"]}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"archive_path": archive_path, "filenames": split_to_paths["test"]}
            ),
        ]

    def _generate_examples(self, archive_path, filenames):
        for key, audio_file in enumerate(sorted(filenames)):
            base_dir, filename = os.path.split(audio_file)
            _, word = os.path.split(base_dir)
            if word == "_background_noise_":
                yield key, {
                    "file": audio_file,
                    "audio": audio_file,
                    "label": "_background_noise_",
                    "speaker_id": None,
                    "utterance_id": 0,
                    "id": filename.split(".wav")[0]
            }
                continue

            elif word in WORDS:
                label = word
            else:
                label = "_unrecognized_"
                # TODO: or maybe I should preserve words outside the WORDS list too and
                # TODO: for example add another feature indicating if a word is unrecognized

            id_ = filename.split(".wav")[0]
            speaker_id, _, utterance_id = id_.split("_")

            yield key, {
                "file": audio_file,
                "audio": audio_file,
                "label": label,
                "speaker_id": speaker_id,
                "utterance_id": utterance_id,
                "id": id_
            }


def _split_files(archive_path):
    val_list_file = os.path.join(archive_path, "validation_list.txt")
    test_list_file = os.path.join(archive_path, "testing_list.txt")

    with open(val_list_file, encoding="utf-8") as val_f, \
            open(test_list_file, encoding="utf-8") as test_f:
        val_paths = [os.path.join(archive_path, path.strip()) for path in val_f.readlines()]
        test_paths = [os.path.join(archive_path, path.strip()) for path in test_f.readlines()]

    all_paths = glob.glob(os.path.join(archive_path, "**", "*.wav"))
    train_paths = list(set(all_paths) - set(val_paths) - set(test_paths))

    return {
        "train": train_paths,
        "val": val_paths,
        "test": test_paths,
    }
