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
"""RWTH-PHOENIX-Weather 2014 T: Parallel Corpus of Sign Language Video, Gloss and Translation"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets

_DESCRIPTION = """\
Parallel Corpus of Sign Language Video, Gloss and Translation
"""

_CITATION = """\
@inproceedings{cihan2018neural,
  title={Neural sign language translation},
  author={Cihan Camgoz, Necati and Hadfield, Simon and Koller, Oscar and Ney, Hermann and Bowden, Richard},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={7784--7793},
  year={2018}
}
@article{koller2015continuous,
  title={Continuous sign language recognition: 
  Towards large vocabulary statistical recognition systems handling multiple signers},
  author={Koller, Oscar and Forster, Jens and Ney, Hermann},
  journal={Computer Vision and Image Understanding},
  volume={141},
  pages={108--125},
  year={2015},
  publisher={Elsevier}
}
"""

_URL = "ftp://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/phoenix-2014-T.v3.tar.gz"

_HOMEPAGE = "https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/"


class RWTHPhoenixWeather2014T(datasets.GeneratorBasedBuilder):
    """RWTH-PHOENIX-Weather 2014 T: Parallel Corpus of Sign Language Video, Gloss and Translation"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        # TODO: Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features({
                "video": datasets.Value("string"),  # path to directory of images
                "start": datasets.Value("int32"),  # starting frame of the annotation
                "end": datasets.Value("int32"),  # ending frame of the annotation
                "signer": datasets.Value("string"),  # signer ID
                "gloss": datasets.Value("string"),  # German sign language gloss
                "translation": datasets.Value("string")  # German translation
            }),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(_URL)
        base_path = os.path.join(dl_dir, "PHOENIX-2014-T-release-v3", "PHOENIX-2014-T")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"base_path": base_path, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"base_path": base_path, "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"base_path": base_path, "split": "test"},
            ),
        ]

    def _generate_examples(self, base_path, split):
        """ Yields examples. """

        filepath = os.path.join(base_path, "annotations", "manual", "PHOENIX-2014-T." + split + ".corpus.csv")
        images_path = os.path.join(base_path, "features", "fullFrame-210x260px", split)

        with open(filepath) as f:
            data = csv.DictReader(f, delimiter="|", quoting=csv.QUOTE_NONE)
            for row in data:
                yield row["name"], {
                    "video": os.path.join(images_path, row["video"]),
                    "start": int(row["start"]),
                    "end": int(row["end"]),
                    "signer": row["speaker"],
                    "gloss": row["orth"],
                    "translation": row["translation"]
                }
