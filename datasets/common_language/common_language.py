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
""" Common Language Dataset"""


import glob
import os

import datasets


_DATA_URL = "https://zenodo.org/record/5036977/files/CommonLanguage.tar.gz?download=1"

_CITATION = """\
@dataset{ganesh_sinisetty_2021_5036977,
  author       = {Ganesh Sinisetty and
                  Pavlo Ruban and
                  Oleksandr Dymov and
                  Mirco Ravanelli},
  title        = {CommonLanguage},
  month        = jun,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {0.1},
  doi          = {10.5281/zenodo.5036977},
  url          = {https://doi.org/10.5281/zenodo.5036977}
}
"""

_DESCRIPTION = """\
This dataset is composed of speech recordings from languages that were carefully selected from the CommonVoice database.
The total duration of audio recordings is 45.1 hours (i.e., 1 hour of material for each language).
The dataset has been extracted from CommonVoice to train language-id systems.
"""

_HOMEPAGE = "https://zenodo.org/record/5036977"

_LICENSE = "https://creativecommons.org/licenses/by/4.0/legalcode"

_LANGUAGES = [
    "Arabic",
    "Basque",
    "Breton",
    "Catalan",
    "Chinese_China",
    "Chinese_Hongkong",
    "Chinese_Taiwan",
    "Chuvash",
    "Czech",
    "Dhivehi",
    "Dutch",
    "English",
    "Esperanto",
    "Estonian",
    "French",
    "Frisian",
    "Georgian",
    "German",
    "Greek",
    "Hakha_Chin",
    "Indonesian",
    "Interlingua",
    "Italian",
    "Japanese",
    "Kabyle",
    "Kinyarwanda",
    "Kyrgyz",
    "Latvian",
    "Maltese",
    "Mangolian",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Romansh_Sursilvan",
    "Russian",
    "Sakha",
    "Slovenian",
    "Spanish",
    "Swedish",
    "Tamil",
    "Tatar",
    "Turkish",
    "Ukranian",
    "Welsh",
]


class CommonLanguage(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("0.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="full", version=VERSION, description="The entire Common Language dataset"),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "client_id": datasets.Value("string"),
                "path": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=48_000),
                "sentence": datasets.Value("string"),
                "age": datasets.Value("string"),
                "gender": datasets.Value("string"),
                "language": datasets.ClassLabel(names=_LANGUAGES),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_path = dl_manager.download_and_extract(_DATA_URL)
        archive_path = os.path.join(dl_path, "common_voice_kpd")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"archive_path": archive_path, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"archive_path": archive_path, "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"archive_path": archive_path, "split": "test"},
            ),
        ]

    def _generate_examples(self, archive_path, split):
        """Yields examples."""

        csv_path_glob = os.path.join(archive_path, "**", f"{split}.csv")

        key = 0
        for csv_path in sorted(glob.glob(csv_path_glob)):
            with open(csv_path, encoding="utf-16") as fin:
                next(fin)  # skip the header
                for line in fin:
                    client_id, wav_name, sentence, age, gender = line.strip().split("\t")[1:]
                    language = csv_path.split(os.sep)[-2]
                    path = os.path.join(os.path.splitext(csv_path)[0], client_id, wav_name)

                    yield key, {
                        "client_id": client_id,
                        "path": path,
                        "audio": path,
                        "sentence": sentence,
                        "age": age,
                        "gender": gender,
                        "language": language,
                    }
                    key += 1
