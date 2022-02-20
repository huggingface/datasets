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
"""LJ automatic speech recognition dataset."""


import csv
import os

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@misc{ljspeech17,
  author       = {Keith Ito and Linda Johnson},
  title        = {The LJ Speech Dataset},
  howpublished = {\\url{https://keithito.com/LJ-Speech-Dataset/}},
  year         = 2017
}
"""

_DESCRIPTION = """\
This is a public domain speech dataset consisting of 13,100 short audio clips of a single speaker reading
passages from 7 non-fiction books in English. A transcription is provided for each clip. Clips vary in length
from 1 to 10 seconds and have a total length of approximately 24 hours.

Note that in order to limit the required storage for preparing this dataset, the audio
is stored in the .wav format and is not converted to a float32 array. To convert the audio
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

_URL = "https://keithito.com/LJ-Speech-Dataset/"
_DL_URL = "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"


class LJSpeech(datasets.GeneratorBasedBuilder):
    """LJ Speech dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="main", version=VERSION, description="The full LJ Speech dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=22050),
                    "file": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "normalized_text": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        root_path = dl_manager.download_and_extract(_DL_URL)
        root_path = os.path.join(root_path, "LJSpeech-1.1")
        wav_path = os.path.join(root_path, "wavs")
        csv_path = os.path.join(root_path, "metadata.csv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"wav_path": wav_path, "csv_path": csv_path}
            ),
        ]

    def _generate_examples(self, wav_path, csv_path):
        """Generate examples from an LJ Speech archive_path."""

        with open(csv_path, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="|", quotechar=None, skipinitialspace=True)
            for row in csv_reader:
                uid, text, norm_text = row
                filename = f"{uid}.wav"
                example = {
                    "id": uid,
                    "file": os.path.join(wav_path, filename),
                    "audio": os.path.join(wav_path, filename),
                    "text": text,
                    "normalized_text": norm_text,
                }
                yield uid, example
