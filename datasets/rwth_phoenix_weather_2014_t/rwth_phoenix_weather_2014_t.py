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
from dataclasses import dataclass

import numpy as np
from PIL import Image

import datasets
from tqdm import tqdm

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

_HOMEPAGE = "https://www-i6.informatik.rwth-aachen.de/~koller/RWTH-PHOENIX-2014-T/"


@dataclass
class RWTHPhoenixWeather2014TConfig(datasets.BuilderConfig):
    """BuilderConfig for RWTHPhoenixWeather2014T."""

    download_url: str = None
    load_images: bool = True


class RWTHPhoenixWeather2014T(datasets.GeneratorBasedBuilder):
    """RWTH-PHOENIX-Weather 2014 T: Parallel Corpus of Sign Language Video, Gloss and Translation"""

    _writer_batch_size = 10  # Keeping a large batch can face memory constraints

    BUILDER_CONFIGS = [
        RWTHPhoenixWeather2014TConfig(
            name="entire_dataset",
            version=datasets.Version("3.0.0"),
            description="Entire dataset containing both videos and annotations.",
            download_url="https://www-i6.informatik.rwth-aachen.de/ftp/pub/rwth-phoenix/2016/phoenix-2014-T.v3.tar.gz",
        ),
        RWTHPhoenixWeather2014TConfig(
            name="annotations",
            version=datasets.Version("3.0.0"),
            description="Dataset including only annotations, without videos",
            download_url="https://nlp.biu.ac.il/~amit/datasets/phoenix-2014-T.v3.txt.tar.gz",
            load_images=False,
        ),
    ]

    def _info(self):
        # TODO set arrow batch size
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    # sequence of frames
                    # "video": datasets.features.Sequence(datasets.features.Array3D(shape=(260, 210, 3), dtype="uint8")),
                    "id": datasets.Value("string"),  # signer ID
                    "video": datasets.Value("string"),
                    "signer": datasets.Value("string"),  # signer ID
                    "gloss": datasets.Value("string"),  # German sign language gloss
                    "text": datasets.Value("string"),  # German translation
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(self.config.download_url)
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
            for row in tqdm(data):
                # np_frames = []
                # if self.config.load_images:
                #     frames_path = os.path.join(images_path, row["video"])[:-7]
                #     for frame_name in os.listdir(frames_path):
                #         frame_path = os.path.join(frames_path, frame_name)
                #         im = Image.open(frame_path)
                #         np_frames.append(np.asarray(im))
                #         im.close()
                frames_path = os.path.join(images_path, row["video"])[:-7]

                yield row["name"], {
                    "id": row["name"],
                    "video": frames_path,
                    "signer": row["speaker"],
                    "gloss": row["orth"],
                    "text": row["translation"],
                }
