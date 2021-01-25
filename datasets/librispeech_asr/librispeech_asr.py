# coding=utf-8
# Copyright 2021 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Librispeech automatic speech recognition dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os

import datasets


_CITATION = """\
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an ASR corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={Acoustics, Speech and Signal Processing (ICASSP), 2015 IEEE International Conference on},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
"""

_DESCRIPTION = """\
LibriSpeech is a corpus of approximately 1000 hours of read English speech with sampling rate of 16 kHz,
prepared by Vassil Panayotov with the assistance of Daniel Povey. The data is derived from read
audiobooks from the LibriVox project, and has been carefully segmented and aligned.87

Note that in order to limit the required storage for preparing this dataset, the audio
is stored in the .flac format and is not converted to a float32 array. To convert, the audio
file to a float32 array, please make use of the `.map()` function as follows:


```python
import soundfile as sf

def map_to_array(batch):
    speech_array, _ = sf.read(batch["file"])
    batch["speech"] = speech_array
    return batch

dataset = dataset.map(map_to_array, remove_columns=["file"])
```
"""

_URL = "http://www.openslr.org/12"
_DL_URL = "http://www.openslr.org/resources/12/"

_DL_URLS = {
    "clean": {
        "dev": _DL_URL + "dev-clean.tar.gz",
        "test": _DL_URL + "test-clean.tar.gz",
        "train.100": _DL_URL + "train-clean-100.tar.gz",
        "train.360": _DL_URL + "train-clean-360.tar.gz",
    },
    "other": {
        "test": _DL_URL + "test-other.tar.gz",
        "dev": _DL_URL + "dev-other.tar.gz",
        "train.500": _DL_URL + "train-other-500.tar.gz",
    },
}


class LibrispeechASRConfig(datasets.BuilderConfig):
    """BuilderConfig for LibriSpeechASR."""

    def __init__(self, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(LibrispeechASRConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


class LibrispeechASR(datasets.GeneratorBasedBuilder):
    """Librispeech dataset."""

    BUILDER_CONFIGS = [
        LibrispeechASRConfig(name="clean", description="'Clean' speech."),
        LibrispeechASRConfig(name="other", description="'Other', more challenging, speech."),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "speaker_id": datasets.Value("int64"),
                    "chapter_id": datasets.Value("int64"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(_DL_URLS[self.config.name])

        if self.config.name == "clean":
            train_splits = [
                datasets.SplitGenerator(name="train.100", gen_kwargs={"archive_path": archive_path["train.100"]}),
                datasets.SplitGenerator(name="train.360", gen_kwargs={"archive_path": archive_path["train.360"]}),
            ]
        elif self.config.name == "other":
            train_splits = [
                datasets.SplitGenerator(name="train.500", gen_kwargs={"archive_path": archive_path["train.500"]}),
            ]

        return train_splits + [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"archive_path": archive_path["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"archive_path": archive_path["test"]}),
        ]

    def _generate_examples(self, archive_path):
        """Generate examples from a Librispeech archive_path."""
        transcripts_glob = os.path.join(archive_path, "LibriSpeech", "*/*/*/*.txt")
        for transcript_file in sorted(glob.glob(transcripts_glob)):
            path = os.path.dirname(transcript_file)
            with open(os.path.join(path, transcript_file), "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    key, transcript = line.split(" ", 1)
                    audio_file = f"{key}.flac"
                    speaker_id, chapter_id = [int(el) for el in key.split("-")[:2]]
                    example = {
                        "id": key,
                        "speaker_id": speaker_id,
                        "chapter_id": chapter_id,
                        "file": os.path.join(path, audio_file),
                        "text": transcript,
                    }
                    yield key, example
