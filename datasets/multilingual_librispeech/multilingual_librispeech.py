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
"""Multilingual Librispeech automatic speech recognition dataset."""


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
        super(MultilingualLibrispeechConfig, self).__init__(
            version=datasets.Version("2.1.0", ""), name=name, data_dir=_DL_URL_FORMAT.format(name), **kwargs
        )


class MultilingualLibrispeech(datasets.GeneratorBasedBuilder):
    """Multilingual Librispeech dataset."""

    BUILDER_CONFIGS = [
        MultilingualLibrispeechConfig(name="german", description="German LibriSpeech dataset"),
        MultilingualLibrispeechConfig(name="dutch", description="Dutch LibriSpeech dataset"),
        MultilingualLibrispeechConfig(name="french", description="French LibriSpeech dataset"),
        MultilingualLibrispeechConfig(name="spanish", description="Spanish LibriSpeech dataset"),
        MultilingualLibrispeechConfig(name="italian", description="Italian LibriSpeech dataset"),
        MultilingualLibrispeechConfig(name="portuguese", description="Portuguese LibriSpeech dataset"),
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
        data_path = os.path.join(archive_path, "mls_" + self.config.name)

        train_splits = [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"data_dir": os.path.join(data_path, "train")}
            ),
            datasets.SplitGenerator(
                name="train.9h",
                gen_kwargs={"data_dir": os.path.join(data_path, "train"), "sub_folder": "limited_supervision/9hr"},
            ),
            datasets.SplitGenerator(
                name="train.1h",
                gen_kwargs={"data_dir": os.path.join(data_path, "train"), "sub_folder": "limited_supervision/1hr"},
            ),
        ]

        return train_splits + [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"data_dir": os.path.join(data_path, "dev")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"data_dir": os.path.join(data_path, "test")}
            ),
        ]

    def _generate_examples(self, data_dir, sub_folder=""):
        """Generate examples from a Multilingual LibriSpeech data dir."""
        transcript_path = os.path.join(data_dir, "transcripts.txt")
        key = 0

        all_ids = None
        if sub_folder != "":
            sub_path = os.path.join(data_dir, sub_folder)
            all_ids_paths = glob.glob(sub_path + "/*/*.txt") + glob.glob(sub_path + "/*.txt")
            all_ids = []
            for path in all_ids_paths:
                with open(path, "r", encoding="utf-8") as f:
                    all_ids += [line.strip() for line in f.readlines()]

            all_ids = set(all_ids)

        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                id_, transcript = line.split("\t")

                if all_ids is not None and id_ not in all_ids:
                    # this only holds true for train.9h and train.1h
                    continue

                audio_file = f"{id_}.flac"
                speaker_id, chapter_id = [int(el) for el in id_.split("_")[:2]]
                yield key, {
                    "id": id_,
                    "speaker_id": speaker_id,
                    "chapter_id": chapter_id,
                    "file": os.path.join(data_dir, "audio", str(speaker_id), str(chapter_id), audio_file),
                    "audio": os.path.join(data_dir, "audio", str(speaker_id), str(chapter_id), audio_file),
                    "text": transcript,
                }
                key += 1
