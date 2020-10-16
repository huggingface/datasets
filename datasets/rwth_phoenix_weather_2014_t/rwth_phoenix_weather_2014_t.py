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
import numpy as np
from PIL import Image

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

_URL = "ftps://wasserstoff.informatik.rwth-aachen.de/pub/rwth-phoenix/2016/phoenix-2014-T.v3.tar.gz"

_HOMEPAGE = "https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/"


class RWTHPhoenixWeather2014T(datasets.GeneratorBasedBuilder):
    """RWTH-PHOENIX-Weather 2014 T: Parallel Corpus of Sign Language Video, Gloss and Translation"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features({
                # sequence of frames
                "video": datasets.features.Sequence(datasets.features.Array3D(shape=(260, 210, 3), dtype="uint8")),
                "signer": datasets.Value("string"),  # signer ID
                "gloss": datasets.Value("string"),  # German sign language gloss
                "text": datasets.Value("string")  # German translation
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

        with open(filepath, "r", encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter="|", quoting=csv.QUOTE_NONE)
            for row in data:
                frames_path = os.path.join(images_path, row["video"])[:-7]
                frames_paths = [os.path.join(frames_path, frame) for frame in os.listdir(frames_path)]
                frames = [np.asarray(Image.open(path)) for path in frames_paths]
                print(len(frames), frames[0].shape, frames[0].dtype)  # prints  5 (260, 210, 3) uint8

                yield row["name"], {
                    "video": frames,
                    "signer": row["speaker"],
                    "gloss": row["orth"],
                    "text": row["translation"]
                }
