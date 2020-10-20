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
"""Corpus NGT: an open access online corpus of movies with annotations of Sign Language of the Netherlands"""

from __future__ import absolute_import, division, print_function

import json
import re
import urllib.request
from itertools import chain
from urllib.error import ContentTooShortError

import datasets
from tqdm import tqdm

_DESCRIPTION = """
An open access online corpus of movies with annotations of Sign Language of the Netherlands.
"""

_CITATION = """\
@inproceedings{dataset:Crasborn2008TheCN,
    title = {The Corpus NGT: An online corpus for professionals and laymen},
    author = {O. Crasborn and I. Zwitserlood},
    year = {2008}
}
"""

_URL = "https://nlp.biu.ac.il/~amit/datasets/ngt.json"

_HOMEPAGE = "https://www.ru.nl/corpusngtuk/"


class NGT(datasets.GeneratorBasedBuilder):
    """Corpus NGT: an open access online corpus of movies with annotations of Sign Language of the Netherlands"""

    VERSION = datasets.Version("0.4.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features({
                "eaf": datasets.Value("string"),  # EAF path
                "videos": datasets.features.Sequence(datasets.Value("string")),  # Videos paths
            }),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_path = dl_manager.download(_URL)

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Download annotation files
        eaf_file_paths = {key: url for (key, url) in data.items() if key.endswith("eaf")}
        eaf_local_paths = dl_manager.download(eaf_file_paths)

        # Check what mpg files are required
        eaf_mpg_map = {}
        for key, eaf in tqdm(list(eaf_local_paths.items())):
            with open(eaf, "r") as f:
                content = f.read()
                dependencies = re.findall('MEDIA_DESCRIPTOR MEDIA_URL=\"(.*)\" MIME_TYPE=\"video/mpeg\"', content)
                eaf_mpg_map[key] = [d.split("/")[-1] for d in dependencies]

        mpg_files = list(chain.from_iterable(eaf_mpg_map.values()))
        available_mpg_files = {f_name: data[f_name] for f_name in mpg_files if f_name in data}
        mpg_local_paths = dl_manager.download(available_mpg_files)

        local_data = {eaf: [mpg_local_paths[mpg] if mpg in mpg_local_paths else None for mpg in mpgs]
                      for eaf, mpgs in eaf_local_paths.items()}

        final_data_path = data_path + ".final.json"
        print("final_data_path", final_data_path)
        with open(final_data_path, "w", encoding="utf-8") as f:
            json.dump(local_data, f)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_path": final_data_path, "split": "train"},
            )
        ]

    def _generate_examples(self, data_path, split):
        """ Yields examples. """

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            for i, (eaf, videos) in enumerate(data.items()):
                yield i, {
                    "eaf": eaf,
                    "videos": videos
                }
