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
"""CIFAR-100 Dataset"""

from __future__ import absolute_import, division, print_function

import os
import pickle

import numpy as np

import datasets


_CITATION = """\
@TECHREPORT{Krizhevsky09learningmultiple,
    author = {Alex Krizhevsky},
    title = {Learning multiple layers of features from tiny images},
    institution = {},
    year = {2009}
}
"""

_DESCRIPTION = """\
The CIFAR-100 dataset consists of 60000 32x32 colour images in 100 classes, with 600 images
per class. There are 500 training images and 100 testing images per class. There are 50000 training images and 10000 test images. The 100 classes are grouped into 20 superclasses.
There are two labels per image - fine label (actual class) and coarse label (superclass).
"""

_DATA_URL = "https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz"


class Cifar100(datasets.GeneratorBasedBuilder):
    """CIFAR-100 Dataset"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="cifar100",
            version=datasets.Version("1.0.0", ""),
            description="CIFAR-100 Dataset",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "img": datasets.Array3D(shape=(32, 32, 3), dtype="uint8"),
                    "fine_label": datasets.features.ClassLabel(
                        names=[
                            "apple",
                            "aquarium_fish",
                            "baby",
                            "bear",
                            "beaver",
                            "bed",
                            "bee",
                            "beetle",
                            "bicycle",
                            "bottle",
                            "bowl",
                            "boy",
                            "bridge",
                            "bus",
                            "butterfly",
                            "camel",
                            "can",
                            "castle",
                            "caterpillar",
                            "cattle",
                            "chair",
                            "chimpanzee",
                            "clock",
                            "cloud",
                            "cockroach",
                            "couch",
                            "cra",
                            "crocodile",
                            "cup",
                            "dinosaur",
                            "dolphin",
                            "elephant",
                            "flatfish",
                            "forest",
                            "fox",
                            "girl",
                            "hamster",
                            "house",
                            "kangaroo",
                            "keyboard",
                            "lamp",
                            "lawn_mower",
                            "leopard",
                            "lion",
                            "lizard",
                            "lobster",
                            "man",
                            "maple_tree",
                            "motorcycle",
                            "mountain",
                            "mouse",
                            "mushroom",
                            "oak_tree",
                            "orange",
                            "orchid",
                            "otter",
                            "palm_tree",
                            "pear",
                            "pickup_truck",
                            "pine_tree",
                            "plain",
                            "plate",
                            "poppy",
                            "porcupine",
                            "possum",
                            "rabbit",
                            "raccoon",
                            "ray",
                            "road",
                            "rocket",
                            "rose",
                            "sea",
                            "seal",
                            "shark",
                            "shrew",
                            "skunk",
                            "skyscraper",
                            "snail",
                            "snake",
                            "spider",
                            "squirrel",
                            "streetcar",
                            "sunflower",
                            "sweet_pepper",
                            "table",
                            "tank",
                            "telephone",
                            "television",
                            "tiger",
                            "tractor",
                            "train",
                            "trout",
                            "tulip",
                            "turtle",
                            "wardrobe",
                            "whale",
                            "willow_tree",
                            "wolf",
                            "woman",
                            "worm",
                        ]
                    ),
                    "coarse_label": datasets.features.ClassLabel(
                        names=[
                            "aquatic_mammals",
                            "fish",
                            "flowers",
                            "food_containers",
                            "fruit_and_vegetables",
                            "household_electrical_devices",
                            "household_furniture",
                            "insects",
                            "large_carnivores",
                            "large_man-made_outdoor_things",
                            "large_natural_outdoor_scenes",
                            "large_omnivores_and_herbivores",
                            "medium_mammals",
                            "non-insect_invertebrates",
                            "people",
                            "reptiles",
                            "small_mammals",
                            "trees",
                            "vehicles_1",
                            "vehicles_2",
                        ]
                    ),
                }
            ),
            supervised_keys=None,  # Probably needs to be fixed.
            homepage="https://www.cs.toronto.edu/~kriz/cifar.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        actual_path = os.path.join(dl_dir, "cifar-100-python")
        train_path = os.path.join(actual_path, "train")
        test_path = os.path.join(actual_path, "test")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the array form."""

        with open(filepath, "rb") as fo:

            dict = pickle.load(fo, encoding="bytes")

            fine_labels = dict[b"fine_labels"]
            coarse_labels = dict[b"coarse_labels"]
            images = dict[b"data"]

            for idx, _ in enumerate(images):

                img_reshaped = np.transpose(np.reshape(images[idx], (3, 32, 32)), (1, 2, 0))

                yield idx, {
                    "img": img_reshaped,
                    "fine_label": fine_labels[idx],
                    "coarse_label": coarse_labels[idx],
                }
