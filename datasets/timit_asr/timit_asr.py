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
"""TIMIT automatic speech recognition dataset."""


import os

import pandas as pd

import datasets
from datasets.tasks import AutomaticSpeechRecognition


_CITATION = """\
@inproceedings{
  title={TIMIT Acoustic-Phonetic Continuous Speech Corpus},
  author={Garofolo, John S., et al},
  ldc_catalog_no={LDC93S1},
  DOI={https://doi.org/10.35111/17gk-bn40},
  journal={Linguistic Data Consortium, Philadelphia},
  year={1983}
}
"""

_DESCRIPTION = """\
The TIMIT corpus of reading speech has been developed to provide speech data for acoustic-phonetic research studies
and for the evaluation of automatic speech recognition systems.

TIMIT contains high quality recordings of 630 individuals/speakers with 8 different American English dialects,
with each individual reading upto 10 phonetically rich sentences.

More info on TIMIT dataset can be understood from the "README" which can be found here:
https://catalog.ldc.upenn.edu/docs/LDC93S1/readme.txt
"""

_URL = "https://data.deepai.org/timit.zip"
_HOMEPAGE = "https://catalog.ldc.upenn.edu/LDC93S1"


class TimitASRConfig(datasets.BuilderConfig):
    """BuilderConfig for TimitASR."""

    def __init__(self, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(TimitASRConfig, self).__init__(version=datasets.Version("2.0.1", ""), **kwargs)


class TimitASR(datasets.GeneratorBasedBuilder):
    """TimitASR dataset."""

    BUILDER_CONFIGS = [TimitASRConfig(name="clean", description="'Clean' speech.")]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "audio": datasets.Audio(sampling_rate=16_000),
                    "text": datasets.Value("string"),
                    "phonetic_detail": datasets.Sequence(
                        {
                            "start": datasets.Value("int64"),
                            "stop": datasets.Value("int64"),
                            "utterance": datasets.Value("string"),
                        }
                    ),
                    "word_detail": datasets.Sequence(
                        {
                            "start": datasets.Value("int64"),
                            "stop": datasets.Value("int64"),
                            "utterance": datasets.Value("string"),
                        }
                    ),
                    "dialect_region": datasets.Value("string"),
                    "sentence_type": datasets.Value("string"),
                    "speaker_id": datasets.Value("string"),
                    "id": datasets.Value("string"),
                }
            ),
            supervised_keys=("file", "text"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[AutomaticSpeechRecognition(audio_file_path_column="file", transcription_column="text")],
        )

    def _split_generators(self, dl_manager):
        archive_path = dl_manager.download_and_extract(_URL)

        train_csv_path = os.path.join(archive_path, "train_data.csv")
        test_csv_path = os.path.join(archive_path, "test_data.csv")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_info_csv": train_csv_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"data_info_csv": test_csv_path}),
        ]

    def _generate_examples(self, data_info_csv):
        """Generate examples from TIMIT archive_path based on the test/train csv information."""
        # Extract the archive path
        data_path = os.path.join(os.path.dirname(data_info_csv).strip(), "data")

        # Read the data info to extract rows mentioning about non-converted audio only
        data_info = pd.read_csv(open(data_info_csv, encoding="utf8"))
        # making sure that the columns having no information about the file paths are removed
        data_info.dropna(subset=["path_from_data_dir"], inplace=True)

        # filter out only the required information for data preparation
        data_info = data_info.loc[(data_info["is_audio"]) & (~data_info["is_converted_audio"])]

        # Iterating the contents of the data to extract the relevant information
        for audio_idx in range(data_info.shape[0]):
            audio_data = data_info.iloc[audio_idx]

            # extract the path to audio
            wav_path = os.path.join(data_path, *(audio_data["path_from_data_dir"].split("/")))

            # extract transcript
            with open(wav_path.replace(".WAV", ".TXT"), "r", encoding="utf-8") as op:
                transcript = " ".join(op.readlines()[0].split()[2:])  # first two items are sample number

            # extract phonemes
            with open(wav_path.replace(".WAV", ".PHN"), "r", encoding="utf-8") as op:
                phonemes = [
                    {
                        "start": i.split(" ")[0],
                        "stop": i.split(" ")[1],
                        "utterance": " ".join(i.split(" ")[2:]).strip(),
                    }
                    for i in op.readlines()
                ]

            # extract words
            with open(wav_path.replace(".WAV", ".WRD"), "r", encoding="utf-8") as op:
                words = [
                    {
                        "start": i.split(" ")[0],
                        "stop": i.split(" ")[1],
                        "utterance": " ".join(i.split(" ")[2:]).strip(),
                    }
                    for i in op.readlines()
                ]

            example = {
                "file": wav_path,
                "audio": wav_path,
                "text": transcript,
                "phonetic_detail": phonemes,
                "word_detail": words,
                "dialect_region": audio_data["dialect_region"],
                "sentence_type": audio_data["filename"][0:2],
                "speaker_id": audio_data["speaker_id"],
                "id": audio_data["filename"].replace(".WAV", ""),
            }

            yield audio_idx, example
