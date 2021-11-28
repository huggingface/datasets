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
An audio dataset of spoken words designed to help train and evaluate keyword spotting systems. 
This is version 0.02 of the data set containing 105,829 audio files, released on
April 11th 2018.
The audio files were collected using crowdsourcing, see
[aiyprojects.withgoogle.com/open_speech_recording](https://github.com/petewarden/extract_loudest_section)
for some of the open source audio collection code we used (and please consider
contributing to enlarge this data set). The goal was to gather examples of
people speaking single-word commands, rather than conversational sentences, so
they were prompted for individual words over the course of a five minute
session. Twenty four core command words were recorded, with most speakers saying each
of them five times. The core words in version 0.02 are "Yes", "No", "Up", "Down", "Left",
"Right", "On", "Off", "Stop", "Go", "Zero", "One", "Two", "Three", "Four",
"Five", "Six", "Seven", "Eight", "Nine", "Backward", "Forward", "Follow", "Learn". 
To help distinguish unrecognized words, there are also several auxiliary ("_unknown_") words, which most speakers only said once.
These include "Bed", "Bird", "Cat", "Dog", "Happy", "House", "Marvin", "Sheila", "Tree", and "Wow".
Its primary goal is to provide a way to build and test small models that detect when a single word is spoken, 
from a set of target words, with as few false positives as possible from background noise or unrelated speech. 
Note that in the train and validation set, the label "unknown" is much more prevalent than the labels 
of the target words or background noise. One difference from the release version is the handling of silent segments. 
While in the test set the silence segments are regular 1 second files, in the training they are provided 
as long segments under "_background_noise_" folder. Here we split these background noise into 1 second clips, 
and also keep one of the files for the validation set.
"""

_LICENSE = "Creative Commons BY 4.0 License"

_URL = "https://www.tensorflow.org/datasets/catalog/speech_commands"  # TODO: check

_DL_URL = "http://download.tensorflow.org/data/speech_commands_{name}.tar.gz"

# _DL_TEST_URL = {
#     "v0.01": "http://download.tensorflow.org/data/speech_commands_test_set_v0.01.tar.gz",
#     "v0.02": "http://download.tensorflow.org/data/speech_commands_test_set_v0.02.tar.gz"
# }

WORDS_V1 = [
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

WORDS_V2 = WORDS_V1 + [
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
    "learn",
]
UNKNOWN = "_unknown_"
BACKGROUND = "_background_noise_"
SILENCE = "_silence_"  # that's how background noise is called in test set archive
LABELS_V1 = WORDS_V1 + [UNKNOWN, BACKGROUND]
LABELS_V2 = WORDS_V2 + [UNKNOWN, BACKGROUND]


class SpeechCommandsConfig(datasets.BuilderConfig):
    """BuilderConfig for SpeechCommands. """

    def __init__(self, labels, **kwargs):  # TODO: url?
        super(SpeechCommandsConfig, self).__init__(**kwargs)
        self.labels = labels


class SpeechCommands(datasets.GeneratorBasedBuilder):
    # DEFAULT_WRITER_BATCH_SIZE = 256  # TODO: do I need it?
    BUILDER_CONFIGS = [
        SpeechCommandsConfig(
            name="v0.01",
            description="",  # TODO
            labels=LABELS_V1,
            version=datasets.Version("0.0.1")
        ),
        SpeechCommandsConfig(
            name="v0.02",
            description="",  # TODO
            labels=LABELS_V2,
            version=datasets.Version("0.0.2")
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,  # TODO: or self.config.description?
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=16_000),
                    "label": datasets.ClassLabel(names=self.config.labels),
                    "speaker_id": datasets.Value("string"),
                    "utterance_id": datasets.Value("int8"),
                }
            ),
            supervised_keys=("file", "label"),  # TODO: understand what that means
            homepage=_URL,
            citation=_CITATION,
            license=_LICENSE,
            version=self.config.version,
        )

    def _split_generators(self, dl_manager):

        archive_paths = dl_manager.download_and_extract({
            "train_val_test": _DL_URL.format(name=self.config.name),
            "test": _DL_URL.format(name=f"test_set_{self.config.name}")
        })

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"archive_path": archive_paths["train_val_test"], "split": "train"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"archive_path": archive_paths["train_val_test"], "split": "val"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"archive_path": archive_paths["test"], "split": "test"}
            ),
        ]

    def _generate_examples(self, archive_path, split):
        filenames = _split_files(archive_path, split)
        for key, audio_file in enumerate(sorted(filenames)):
            base_dir, filename = os.path.split(audio_file)
            _, word = os.path.split(base_dir)
            if word in [BACKGROUND, SILENCE]:
                yield key, {
                    "file": audio_file,
                    "audio": audio_file,
                    "label": BACKGROUND,
                    "speaker_id": None,
                    "utterance_id": 0,
            }
                continue

            elif word in self.config.labels[:-2]:  # the last two labels are _unknown_ and _background_
                label = word
            else:
                label = UNKNOWN
                # TODO: or maybe I should preserve words outside the WORDS list too and
                # for example add another feature indicating if a word is unrecognized (_unknown_)
                # otherwise utterance_id don't make any sense

            speaker_id, _, utterance_id = filename.split(".wav")[0].split("_")[-3:]
            # take last 3 elements since while a standard filename looks like `0bac8a71_nohash_0.wav`
            # in test archives in _unknown_ folder filenames look like `backward_0c540988_nohash_0.wav`

            yield key, {
                "file": audio_file,
                "audio": audio_file,
                "label": label,
                "speaker_id": speaker_id,
                "utterance_id": utterance_id,
            }


def _split_files(archive_path, split):
    all_paths = glob.glob(os.path.join(archive_path, "**", "*.wav"))
    if split == "test":
        # there is a separate archive with test files, use all of its available files
        return all_paths

    val_list_file = os.path.join(archive_path, "validation_list.txt")
    test_list_file = os.path.join(archive_path, "testing_list.txt")

    with open(val_list_file, encoding="utf-8") as val_f, \
            open(test_list_file, encoding="utf-8") as test_f:
        val_paths = [os.path.join(archive_path, path.strip()) for path in val_f.readlines() if path.strip()]
        test_paths = [os.path.join(archive_path, path.strip()) for path in test_f.readlines() if path.strip()]

    if split == "val":
        return val_paths

    # all files that are not listed in either test or validation sets belong to train set
    return list(set(all_paths) - set(val_paths) - set(test_paths))
