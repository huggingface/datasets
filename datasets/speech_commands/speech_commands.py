# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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

"""Speech Commands, an audio dataset of spoken words designed to help train and evaluate keyword spotting systems. """


import os
import textwrap

import datasets


_CITATION = """
@article{speechcommandsv2,
   author = { {Warden}, P.},
    title = "{Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition}",
  journal = {ArXiv e-prints},
  archivePrefix = "arXiv",
  eprint = {1804.03209},
  primaryClass = "cs.CL",
  keywords = {Computer Science - Computation and Language, Computer Science - Human-Computer Interaction},
    year = 2018,
    month = apr,
    url = {https://arxiv.org/abs/1804.03209},
}
"""

_DESCRIPTION = """
This is a set of one-second .wav audio files, each containing a single spoken
English word or background noise. These words are from a small set of commands, and are spoken by a
variety of different speakers. This data set is designed to help train simple
machine learning models. This dataset is covered in more detail at
[https://arxiv.org/abs/1804.03209](https://arxiv.org/abs/1804.03209).

Version 0.01 of the data set (configuration `"v0.01"`) was released on August 3rd 2017 and contains
64,727 audio files.

In version 0.01 thirty different words were recoded: "Yes", "No", "Up", "Down", "Left",
"Right", "On", "Off", "Stop", "Go", "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
"Bed", "Bird", "Cat", "Dog", "Happy", "House", "Marvin", "Sheila", "Tree", "Wow".


In version 0.02 more words were added: "Backward", "Forward", "Follow", "Learn", "Visual".

In both versions, ten of them are used as commands by convention: "Yes", "No", "Up", "Down", "Left",
"Right", "On", "Off", "Stop", "Go". Other words are considered to be auxiliary (in current implementation
it is marked by `True` value of `"is_unknown"` feature). Their function is to teach a model to distinguish core words
from unrecognized ones.

The `_silence_` class contains a set of longer audio clips that are either recordings or
a mathematical simulation of noise.

"""

_LICENSE = "Creative Commons BY 4.0 License"

_URL = "https://www.tensorflow.org/datasets/catalog/speech_commands"

_DL_URL = "http://download.tensorflow.org/data/speech_commands_{name}.tar.gz"

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
]

UNKNOWN_WORDS_V1 = [
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
    "bed",
    "bird",
    "cat",
    "dog",
    "happy",
    "house",
    "marvin",
    "sheila",
    "tree",
    "wow",
]

UNKNOWN_WORDS_V2 = UNKNOWN_WORDS_V1 + [
    "backward",
    "forward",
    "follow",
    "learn",
    "visual",
]

UNKNOWN = "_unknown_"
BACKGROUND = "_background_noise_"
SILENCE = "_silence_"  # that's how background noise is called in test set archives
LABELS_V1 = WORDS + UNKNOWN_WORDS_V1 + [UNKNOWN, SILENCE]
LABELS_V2 = WORDS + UNKNOWN_WORDS_V2 + [UNKNOWN, SILENCE]


class SpeechCommandsConfig(datasets.BuilderConfig):
    """BuilderConfig for SpeechCommands."""

    def __init__(self, labels, **kwargs):
        super(SpeechCommandsConfig, self).__init__(**kwargs)
        self.labels = labels


class SpeechCommands(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        SpeechCommandsConfig(
            name="v0.01",
            description=textwrap.dedent(
                """\
                Version 0.01 of the SpeechCommands dataset. Contains 30 words
                (20 of them are auxiliary) and background noise.
                """
            ),
            labels=LABELS_V1,
            version=datasets.Version("0.1.0"),
        ),
        SpeechCommandsConfig(
            name="v0.02",
            description=textwrap.dedent(
                """\
                Version 0.02 of the SpeechCommands dataset.
                Contains 35 words (25 of them are auxiliary) and background noise.
                """
            ),
            labels=LABELS_V2,
            version=datasets.Version("0.2.0"),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=16_000),
                    "label": datasets.ClassLabel(names=self.config.labels),
                    "is_unknown": datasets.Value("bool"),
                    "speaker_id": datasets.Value("string"),
                    "utterance_id": datasets.Value("int8"),
                }
            ),
            homepage=_URL,
            citation=_CITATION,
            license=_LICENSE,
            version=self.config.version,
        )

    def _split_generators(self, dl_manager):

        archive_paths = dl_manager.download(
            {
                "train_val_test": _DL_URL.format(name=self.config.name),
                "test": _DL_URL.format(name=f"test_set_{self.config.name}"),
            }
        )

        train_paths, val_paths = _get_train_val_filenames(dl_manager.iter_archive(archive_paths["train_val_test"]))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["train_val_test"]),
                    "split_files": train_paths,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["train_val_test"]),
                    "split_files": val_paths,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["test"]),
                    "split_files": None,
                },
            ),
        ]

    def _generate_examples(self, archive, split_files):
        for path, file in archive:
            path = path.lstrip("./")
            # file is either from train or val iterators but its not in corresponding split's filenames list
            if split_files is not None and path not in split_files:
                continue
            if not path.endswith(".wav"):
                continue

            relpath, audio_filename = os.path.split(path)
            word = os.path.split(relpath)[-1]
            is_unknown = False
            if word in [BACKGROUND, SILENCE]:
                yield path, {
                    "file": path,
                    "audio": {"path": path, "bytes": file.read()},
                    "label": SILENCE,  # not BACKGROUND for the convention purposes
                    "is_unknown": is_unknown,
                    "speaker_id": None,
                    "utterance_id": 0,
                }
                continue
            else:  # word is either in WORDS or unknown
                label = word
                if word not in WORDS:
                    is_unknown = True

            if not split_files and label == "_unknown_":
                # test archives have a bit different structure where unknown samples are stored in `_unknown_` folder
                # their filenames look like `backward_0c540988_nohash_0.wav`
                label, speaker_id, _, utterance_id = audio_filename.split(".wav")[0].split("_")
            else:
                # a standard filename looks like `0bac8a71_nohash_0.wav`
                speaker_id, _, utterance_id = audio_filename.split(".wav")[0].split("_")

            yield path, {
                "file": path,
                "audio": {"path": path, "bytes": file.read()},
                "label": label,
                "is_unknown": is_unknown,
                "speaker_id": speaker_id,
                "utterance_id": utterance_id,
            }


def _get_train_val_filenames(archive):
    train_paths, test_paths, val_paths = [], [], []

    for path, file in archive:
        if os.path.split(path)[-1] == "testing_list.txt":
            test_paths = [filename.decode("utf-8").strip() for filename in file.readlines() if filename.strip()]

        elif os.path.split(path)[-1] == "validation_list.txt":
            val_paths = [filename.decode("utf-8").strip() for filename in file.readlines() if filename.strip()]

        elif path.endswith(".wav"):
            train_paths.append(path.lstrip("./"))

    # original validation files do not include silence - add it manually here
    # see https://github.com/tensorflow/datasets/blob/master/tensorflow_datasets/audio/speech_commands.py#L182
    val_paths.append(os.path.join(BACKGROUND, "running_tap.wav"))

    # all files that are not listed in either test or validation sets belong to train set
    train_paths = list(set(train_paths) - set(val_paths) - set(test_paths))

    return train_paths, val_paths
