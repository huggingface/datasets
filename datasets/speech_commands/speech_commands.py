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

_DL_URL = "https://s3.amazonaws.com/datasets.huggingface.co/SpeechCommands/{name}/{name}_{split}.tar.gz"

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

SILENCE = "_silence_"  # background noise
LABELS_V1 = WORDS + UNKNOWN_WORDS_V1 + [SILENCE]
LABELS_V2 = WORDS + UNKNOWN_WORDS_V2 + [SILENCE]


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
                "train": _DL_URL.format(name=self.config.name, split="train"),
                "validation": _DL_URL.format(name=self.config.name, split="validation"),
                "test": _DL_URL.format(name=self.config.name, split="test"),
            }
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["train"]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["validation"]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive_paths["test"]),
                },
            ),
        ]

    def _generate_examples(self, archive):
        for path, file in archive:
            if not path.endswith(".wav"):
                continue

            word, audio_filename = path.split("/")
            is_unknown = False

            if word == SILENCE:
                speaker_id, utterance_id = None, 0

            else:  # word is either in WORDS or unknown
                if word not in WORDS:
                    is_unknown = True
                # an audio filename looks like `0bac8a71_nohash_0.wav`
                speaker_id, _, utterance_id = audio_filename.split(".wav")[0].split("_")

            yield path, {
                "file": path,
                "audio": {"path": path, "bytes": file.read()},
                "label": word,
                "is_unknown": is_unknown,
                "speaker_id": speaker_id,
                "utterance_id": utterance_id,
            }
