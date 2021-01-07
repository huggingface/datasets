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
"""Indonesian Newspapers 2018"""

from __future__ import absolute_import, division, print_function

import glob
import json
import logging
import os

import datasets


_CITATION = """\
@inproceedings{id_newspapers_2018,
  author    = {},
  title     = {Indonesian Newspapers 2018},
  year      = {2019},
  url       = {https://github.com/feryandi/Dataset-Artikel},
}
"""

_DESCRIPTION = """\
The dataset contains around 500K articles (136M of words) from 7 Indonesian newspapers: Detik, Kompas, Tempo,
CNN Indonesia, Sindo, Republika and Poskota. The articles are dated between 1st January 2018 and 20th August 2018
(with few exceptions dated earlier). The size of uncompressed 500K json files (newspapers-json.tgz) is around 2.2GB,
and the cleaned uncompressed in a big text file (newspapers.txt.gz) is about 1GB. The original source in Google Drive
contains also a dataset in html format which include raw data (pictures, css, javascript, ...)
from the online news website
"""

_HOMEPAGE = "https://github.com/feryandi/Dataset-Artikel"

_LICENSE = "Creative Commons Attribution-ShareAlike 4.0 International Public License"

_URLs = ["http://cloud.uncool.ai/index.php/s/kF83dQHfGeS2LX2/download"]


class IdNewspapers2018Config(datasets.BuilderConfig):
    """BuilderConfig for IdNewspapers2018"""

    def __init__(self, **kwargs):
        """BuilderConfig for IdNewspapers2018.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdNewspapers2018Config, self).__init__(**kwargs)


class IdNewspapers2018(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdNewspapers2018Config(
            name="id_newspapers_2018",
            version=VERSION,
            description="IdNewspapers2018 dataset",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "url": datasets.Value("string"),
                "date": datasets.Value("string"),
                "title": datasets.Value("string"),
                "content": datasets.Value("string"),
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
        my_urls = _URLs[0]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, "newspapers"),
                    "split": "train",
                },
            )
        ]

    def _generate_examples(self, article_dir, split):
        logging.info("⏳ Generating %s examples from = %s", split, article_dir)
        id = 0
        for path in sorted(glob.glob(os.path.join(article_dir, "**/*.json"), recursive=True)):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                yield id, {
                    "id": str(id),
                    "url": data["url"],
                    "date": data["date"],
                    "title": data["title"],
                    "content": data["content"],
                }
            id += 1
