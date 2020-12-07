# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""Arabic Vocalized Words Dataset."""

from __future__ import absolute_import, division, print_function

import glob
import os

import datasets


_DESCRIPTION = """\
Arabic vocalized texts.
it contains 75 million of fully vocalized words mainly\
97 books from classical and modern Arabic language.
"""

_CITATION = """\
@article{zerrouki2017tashkeela,
  title={Tashkeela: Novel corpus of Arabic vocalized texts, data for auto-diacritization systems},
  author={Zerrouki, Taha and Balla, Amar},
  journal={Data in brief},
  volume={11},
  pages={147},
  year={2017},
  publisher={Elsevier}
}
"""

_DOWNLOAD_URL = "https://sourceforge.net/projects/tashkeela/files/latest/download"


class TashkeelaConfig(datasets.BuilderConfig):
    """BuilderConfig for Tashkeela."""

    def __init__(self, **kwargs):
        """BuilderConfig for Tashkeela.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(TashkeelaConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class Tashkeela(datasets.GeneratorBasedBuilder):
    """Tashkeela dataset."""

    BUILDER_CONFIGS = [
        TashkeelaConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "book": datasets.Value("string"),
                    "text": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://sourceforge.net/projects/tashkeela/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "directory": os.path.join(arch_path, "Tashkeela-arabic-diacritized-text-utf8-0.3/texts.txt")
                },
            ),
        ]

    def _generate_examples(self, directory):
        """Generate examples."""

        for id_, file_name in enumerate(sorted(glob.glob(os.path.join(directory, "**.txt")))):
            with open(file_name, encoding="UTF-8") as f:
                yield str(id_), {"book": file_name, "text": f.read()}
