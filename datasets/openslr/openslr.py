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
""" OpenSLR Dataset"""

from __future__ import absolute_import, division, print_function

import os
import re

import datasets


_DATA_URL = "http://openslr.org/resources/{}"

_CITATION = """\

"""

_DESCRIPTION = """\
OpenSLR
"""

_HOMEPAGE = "http://openslr.org/"

_LICENSE = ""

_RESOURCES = {
    "SLR41": {
        "Language": "Javanese",
        "LongName": "High quality TTS data for Javanese",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Javanese (jv-ID)",
        "Files": ["jv_id_female.zip", "jv_id_male.zip"],
    },
    "SLR42": {
        "Language": "Khmer",
        "LongName": "High quality TTS data for Khmer",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Khmer (km-KH)",
        "Files": ["km_kh_male.zip"],
    },
    "SLR43": {
        "Language": "Nepali",
        "LongName": "High quality TTS data for Nepali",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Nepali (ne-NP)",
        "Files": ["ne_np_female.zip"],
    },
    "SLR44": {
        "Language": "Sundanese",
        "LongName": "High quality TTS data for Sundanese",
        "Category": "Speech",
        "Summary": "Multi-speaker TTS data for Javanese Sundanese (su-ID)",
        "Files": ["su_id_female.zip", "su_id_male.zip"],
    },
}


class OpenSlrConfig(datasets.BuilderConfig):
    """BuilderConfig for OpenSlr."""

    def __init__(self, name, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        self.language = kwargs.pop("language", None)
        self.long_name = kwargs.pop("long_name", None)
        self.category = kwargs.pop("category", None)
        self.summary = kwargs.pop("summary", None)
        self.files = kwargs.pop("files", None)
        description = f"Open Speech and Language Resources dataset in {self.language}. Name: {self.name}, Summary: {self.summary}."
        super(OpenSlrConfig, self).__init__(name=name, description=description, **kwargs)


class OpenSlr(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        OpenSlrConfig(
            name=resource_id,
            language=_RESOURCES[resource_id]["Language"],
            long_name=_RESOURCES[resource_id]["LongName"],
            category=_RESOURCES[resource_id]["Category"],
            summary=_RESOURCES[resource_id]["Summary"],
            files=_RESOURCES[resource_id]["Files"],
        )
        for resource_id in _RESOURCES.keys()
    ]

    def _info(self):
        features = datasets.Features(
            {
                "path": datasets.Value("string"),
                "sentence": datasets.Value("string"),
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
        resource_number = self.config.name.replace("SLR", "")
        urls = [f"{_DATA_URL.format(resource_number)}/{file}" for file in self.config.files]
        dl_paths = dl_manager.download_and_extract(urls)
        abs_path_to_datas = [
            os.path.join(path, f'{self.config.files[i].split(".")[0]}', "line_index.tsv")
            for i, path in enumerate(dl_paths)
        ]
        abs_path_to_wavs = [
            os.path.join(path, f'{self.config.files[i].split(".")[0]}', "wavs") for i, path in enumerate(dl_paths)
        ]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepaths": abs_path_to_datas,
                    "path_to_wavs": abs_path_to_wavs,
                },
            ),
        ]

    def _generate_examples(self, filepaths, path_to_wavs):
        """ Yields examples. """
        data_fields = list(self._info().features.keys())

        counter = -1
        for i, path in enumerate(filepaths):
            with open(path, encoding="utf-8") as f:
                lines = f.readlines()
                for id_, line in enumerate(lines):
                    field_values = re.split(r"\t4?\t?", line.strip())
                    # set absolute path for audio file
                    field_values[0] = os.path.join(path_to_wavs[i], f"{field_values[0]}.wav")
                    counter += 1
                    yield counter, {key: value for key, value in zip(data_fields, field_values)}
