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
"""MNIST Data Set"""


import struct

import numpy as np

import datasets
from datasets.tasks import ImageClassification


_CITATION = """\
@article{lecun2010mnist,
  title={MNIST handwritten digit database},
  author={LeCun, Yann and Cortes, Corinna and Burges, CJ},
  journal={ATT Labs [Online]. Available: http://yann.lecun.com/exdb/mnist},
  volume={2},
  year={2010}
}
"""

_DESCRIPTION = """\
The MNIST dataset consists of 70,000 28x28 black-and-white images in 10 classes (one for each digits), with 7,000
images per class. There are 60,000 training images and 10,000 test images.
"""

_URL = "https://storage.googleapis.com/cvdf-datasets/mnist/"
_URLS = {
    "train_images": "train-images-idx3-ubyte.gz",
    "train_labels": "train-labels-idx1-ubyte.gz",
    "test_images": "t10k-images-idx3-ubyte.gz",
    "test_labels": "t10k-labels-idx1-ubyte.gz",
}


class MNIST(datasets.GeneratorBasedBuilder):
    """MNIST Data Set"""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="mnist",
            version=datasets.Version("1.0.0"),
            description=_DESCRIPTION,
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.features.ClassLabel(names=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]),
                }
            ),
            supervised_keys=("image", "label"),
            homepage="http://yann.lecun.com/exdb/mnist/",
            citation=_CITATION,
            task_templates=[
                ImageClassification(
                    image_column="image",
                    label_column="label",
                    labels=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                )
            ],
        )

    def _split_generators(self, dl_manager):
        urls_to_download = {key: _URL + fname for key, fname in _URLS.items()}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": [downloaded_files["train_images"], downloaded_files["train_labels"]],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": [downloaded_files["test_images"], downloaded_files["test_labels"]],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw form."""
        # Images
        with open(filepath[0], "rb") as f:
            # First 16 bytes contain some metadata
            _ = f.read(4)
            size = struct.unpack(">I", f.read(4))[0]
            _ = f.read(8)
            images = np.frombuffer(f.read(), dtype=np.uint8).reshape(size, 28, 28)

        # Labels
        with open(filepath[1], "rb") as f:
            # First 8 bytes contain some metadata
            _ = f.read(8)
            labels = np.frombuffer(f.read(), dtype=np.uint8)

        for idx in range(size):
            yield idx, {"image": images[idx], "label": str(labels[idx])}
