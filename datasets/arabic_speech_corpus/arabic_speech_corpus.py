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
"""Arabic Speech Corpus"""


import os

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@phdthesis{halabi2016modern,
  title={Modern standard Arabic phonetics for speech synthesis},
  author={Halabi, Nawar},
  year={2016},
  school={University of Southampton}
}
"""

_DESCRIPTION = """\
This Speech corpus has been developed as part of PhD work carried out by Nawar Halabi at the University of Southampton.
The corpus was recorded in south Levantine Arabic
(Damascian accent) using a professional studio. Synthesized speech as an output using this corpus has produced a high quality, natural voice.
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

_URL = "http://en.arabicspeechcorpus.com/arabic-speech-corpus.zip"


class ArabicSpeechCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for ArabicSpeechCorpu."""

    def __init__(self, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(ArabicSpeechCorpusConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


class ArabicSpeechCorpus(datasets.GeneratorBasedBuilder):
    """ArabicSpeechCorpus dataset."""

    BUILDER_CONFIGS = [
        ArabicSpeechCorpusConfig(name="clean", description="'Clean' speech."),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=48_000),
                    "phonetic": datasets.Value("string"),
                    "orthographic": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(_URL)
        archive_path = os.path.join(archive_path, "arabic-speech-corpus")
        return [
            datasets.SplitGenerator(name="train", gen_kwargs={"archive_path": archive_path}),
            datasets.SplitGenerator(name="test", gen_kwargs={"archive_path": os.path.join(archive_path, "test set")}),
        ]

    def _generate_examples(self, archive_path):
        """Generate examples from a Librispeech archive_path."""
        lab_dir = os.path.join(archive_path, "lab")
        wav_dir = os.path.join(archive_path, "wav")
        if "test set" in archive_path:
            phonetic_path = os.path.join(archive_path, "phonetic-transcript.txt")
        else:
            phonetic_path = os.path.join(archive_path, "phonetic-transcipt.txt")

        orthographic_path = os.path.join(archive_path, "orthographic-transcript.txt")

        phonetics = {}
        orthographics = {}

        with open(phonetic_path, "r", encoding="utf-8") as f:
            for line in f:
                wav_file, phonetic = line.split('"')[1::2]
                phonetics[wav_file] = phonetic

        with open(orthographic_path, "r", encoding="utf-8") as f:
            for line in f:
                wav_file, orthographic = line.split('"')[1::2]
                orthographics[wav_file] = orthographic

        for _id, lab_name in enumerate(sorted(os.listdir(lab_dir))):
            lab_path = os.path.join(lab_dir, lab_name)
            lab_text = open(lab_path, "r", encoding="utf-8").read()

            wav_name = lab_name[:-4] + ".wav"
            wav_path = os.path.join(wav_dir, wav_name)

            example = {
                "file": wav_path,
                "audio": wav_path,
                "text": lab_text,
                "phonetic": phonetics[wav_name],
                "orthographic": orthographics[wav_name],
            }
            yield str(_id), example
