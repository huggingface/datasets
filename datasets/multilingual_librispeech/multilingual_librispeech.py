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


import glob
import os

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@article{Pratap2020MLSAL,
  title={MLS: A Large-Scale Multilingual Dataset for Speech Research},
  author={Vineel Pratap and Qiantong Xu and Anuroop Sriram and Gabriel Synnaeve and Ronan Collobert},
  journal={ArXiv},
  year={2020},
  volume={abs/2012.03411}
}
"""

_DESCRIPTION = """\
Multilingual LibriSpeech (MLS) dataset is a large multilingual corpus suitable for speech research. The dataset is derived from read audiobooks from LibriVox and consists of 8 languages - English, German, Dutch, Spanish, French, Italian, Portuguese, Polish.
"""

_URL = "http://www.openslr.org/94"
_DL_URL_FORMAT = "https://dl.fbaipublicfiles.com/mls/mls_{}.tar.gz"


class MultilingualLibrispeechConfig(datasets.BuilderConfig):
    """BuilderConfig for MultilingualLibrispeech."""

    def __init__(self, name, **kwargs):
        """
        Args:
          name: `string`, name of dataset config
          **kwargs: keyword arguments forwarded to super.
        """
        self.data_dir = _DL_URL_FORMAT.format(name)
        super(MultilingualLibrispeechConfig, self).__init__(version=datasets.Version("2.1.0", ""), name=name, **kwargs)


class MultilingualLibrispeech(datasets.GeneratorBasedBuilder):
    """Multilingual Librispeech dataset."""

    BUILDER_CONFIGS = [
        MultilingualLibrispeechConfig(name="polish", description="Polish LibriSpeech dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.features.Audio(sampling_rate=16_000),
                    "text": datasets.Value("string"),
                    "speaker_id": datasets.Value("int64"),
                    "chapter_id": datasets.Value("int64"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_URL,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(self.config.data_dir)

        train_splits = [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"archive_path": archive_path["train"]}),
            datasets.SplitGenerator(name="train.9h", gen_kwargs={"archive_path": archive_path["limited_supervision"]}),
            datasets.SplitGenerator(name="train.1h", gen_kwargs={"archive_path": archive_path["train.360"]}),
        ]

        return train_splits + [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"archive_path": archive_path["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"archive_path": archive_path["test"]}),
        ]

    def _generate_examples(self, archive_path, **kwargs):
        """Generate examples from a LibriSpeech archive_path."""
        import ipdb; ipdb.set_trace()
        transcripts_glob = os.path.join(archive_path, "LibriSpeech", "*/*/*/*.txt")
        key = 0
        for transcript_path in sorted(glob.glob(transcripts_glob)):
            transcript_dir_path = os.path.dirname(transcript_path)
            with open(transcript_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    id_, transcript = line.split(" ", 1)
                    audio_file = f"{id_}.flac"
                    speaker_id, chapter_id = [int(el) for el in id_.split("-")[:2]]
                    yield key, {
                        "id": id_,
                        "speaker_id": speaker_id,
                        "chapter_id": chapter_id,
                        "file": os.path.join(transcript_dir_path, audio_file),
                        "audio": os.path.join(transcript_dir_path, audio_file),
                        "text": transcript,
                    }
                    key += 1
