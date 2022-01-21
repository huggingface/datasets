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
"""VCTK dataset."""


import os
import re

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@inproceedings{Veaux2017CSTRVC,
    title        = {CSTR VCTK Corpus: English Multi-speaker Corpus for CSTR Voice Cloning Toolkit},
    author       = {Christophe Veaux and Junichi Yamagishi and Kirsten MacDonald},
    year         = 2017
}
"""

_DESCRIPTION = """\
The CSTR VCTK Corpus includes speech data uttered by 110 English speakers with various accents.
"""

_URL = "https://datashare.ed.ac.uk/handle/10283/3443"
_DL_URL = "https://datashare.is.ed.ac.uk/bitstream/handle/10283/3443/VCTK-Corpus-0.92.zip"


class VCTK(datasets.GeneratorBasedBuilder):
    """VCTK dataset."""

    VERSION = datasets.Version("0.9.2")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="main", version=VERSION, description="VCTK dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "speaker_id": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=48_000),
                    "file": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "text_id": datasets.Value("string"),
                    "age": datasets.Value("string"),
                    "gender": datasets.Value("string"),
                    "accent": datasets.Value("string"),
                    "region": datasets.Value("string"),
                    "comment": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        root_path = dl_manager.download_and_extract(_DL_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"root_path": root_path}),
        ]

    def _generate_examples(self, root_path):
        """Generate examples from the VCTK corpus root path."""

        meta_path = os.path.join(root_path, "speaker-info.txt")
        txt_root = os.path.join(root_path, "txt")
        wav_root = os.path.join(root_path, "wav48_silence_trimmed")
        # NOTE: "comment" is handled separately in logic below
        fields = ["speaker_id", "age", "gender", "accent", "region"]

        key = 0
        with open(meta_path, encoding="utf-8") as meta_file:
            _ = next(iter(meta_file))
            for line in meta_file:
                data = {}
                line = line.strip()
                search = re.search(r"\(.*\)", line)
                if search is None:
                    data["comment"] = ""
                else:
                    start, _ = search.span()
                    data["comment"] = line[start:]
                    line = line[:start]
                values = line.split()
                for i, field in enumerate(fields):
                    if field == "region":
                        data[field] = " ".join(values[i:])
                    else:
                        data[field] = values[i] if i < len(values) else ""
                speaker_id = data["speaker_id"]
                speaker_txt_path = os.path.join(txt_root, speaker_id)
                speaker_wav_path = os.path.join(wav_root, speaker_id)
                # NOTE: p315 does not have text
                if not os.path.exists(speaker_txt_path):
                    continue
                for txt_file in sorted(os.listdir(speaker_txt_path)):
                    filename, _ = os.path.splitext(txt_file)
                    _, text_id = filename.split("_")
                    for i in [1, 2]:
                        wav_file = os.path.join(speaker_wav_path, f"{filename}_mic{i}.flac")
                        # NOTE: p280 does not have mic2 files
                        if not os.path.exists(wav_file):
                            continue
                        with open(os.path.join(speaker_txt_path, txt_file), encoding="utf-8") as text_file:
                            text = text_file.readline().strip()
                            more_data = {
                                "file": wav_file,
                                "audio": wav_file,
                                "text": text,
                                "text_id": text_id,
                            }
                            yield key, {**data, **more_data}
                        key += 1
