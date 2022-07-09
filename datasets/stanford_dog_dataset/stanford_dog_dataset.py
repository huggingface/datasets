# coding=utf-8
# Copyright 2022 The TensorFlow Datasets Authors.
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

"""Stanford dogs dataset."""

import os

import datasets
from datasets.tasks import ImageClassification


logger = datasets.logging.get_logger(__name__)

_DESCRIPTION = """\
The Stanford Dogs dataset contains images of 120 breeds of dogs from around
the world. This dataset has been built using images and annotation from
ImageNet for the task of fine-grained image categorization. There are
20,580 images, out of which 12,000 are used for training and 8580 for
testing. Class labels and bounding box annotations are provided
for all the 12,000 images.
"""

_URL = "http://vision.stanford.edu/aditya86/ImageNetDogs/images.tar"

_HOMEPAGE = "http://vision.stanford.edu/aditya86/ImageNetDogs/"

_CITATION = """\
@inproceedings{KhoslaYaoJayadevaprakashFeiFei_FGVC2011,
author = "Aditya Khosla and Nityananda Jayadevaprakash and Bangpeng Yao and
          Li Fei-Fei",
title = "Novel Dataset for Fine-Grained Image Categorization",
booktitle = "First Workshop on Fine-Grained Visual Categorization,
             IEEE Conference on Computer Vision and Pattern Recognition",
year = "2011",
month = "June",
address = "Colorado Springs, CO",
}
"""


class StanfordDogsDataset(datasets.GeneratorBasedBuilder):
    """Stanford Dogs dataset."""

    VERSION = datasets.Version("0.2.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    # Images are of varying size
                    "image": datasets.Image(),
                    "labels": datasets.features.ClassLabel(num_classes=120),
                }
            ),
            supervised_keys=("image", "labels"),
            task_templates=[ImageClassification(image_column="image", label_column="labels")],
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dl_manager.iter_files([data_dir])},
            )
        ]

    def _generate_examples(self, files):
        labels_dict = {}
        dir_set = set()
        i = 0
        for file in files:
            dir_name = os.path.basename(os.path.dirname(file)).lower()
            if dir_name not in dir_set:
                dir_set.add(dir_name)
                labels_dict[dir_name] = i
                i += 1

        for i, file in enumerate(files):
            if os.path.basename(file).endswith(".jpg"):
                with open(file, "rb") as f:
                    if b"JFIF" in f.peek(10):
                        yield str(i), {
                            "image": file,
                            "labels": labels_dict[os.path.basename(os.path.dirname(file)).lower()],
                        }
