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
"""CIFAR-10 Data Set"""

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
The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images
per class. There are 50000 training images and 10000 test images.
"""

_DATA_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"


class Cifar10(datasets.GeneratorBasedBuilder):
    """CIFAR-10 Data Set"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of CIFAR-10 Data Set",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "img": datasets.Array3D(shape=(32, 32, 3), dtype="uint8"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "airplane",
                            "automobile",
                            "bird",
                            "cat",
                            "deer",
                            "dog",
                            "frog",
                            "horse",
                            "ship",
                            "truck",
                        ]
                    ),
                }
            ),
            supervised_keys=("img", "label"),
            homepage="https://www.cs.toronto.edu/~kriz/cifar.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        final_dir = os.path.join(dl_dir, "cifar-10-batches-py")

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": final_dir, "split": "train"}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": final_dir, "split": "test"}),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""

        if split == "train":
            batches = ["data_batch_1", "data_batch_2", "data_batch_3", "data_batch_4", "data_batch_5"]

        if split == "test":
            batches = ["test_batch"]

        for batch in batches:

            file = os.path.join(filepath, batch)

            with open(file, "rb") as fo:

                dict = pickle.load(fo, encoding="bytes")

                labels = dict[b"labels"]
                images = dict[b"data"]

                for idx, _ in enumerate(images):

                    img_reshaped = np.transpose(np.reshape(images[idx], (3, 32, 32)), (1, 2, 0))

                    yield idx, {
                        "img": img_reshaped,
                        "label": labels[idx],
                    }
