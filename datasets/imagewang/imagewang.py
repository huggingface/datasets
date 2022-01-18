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
"""Imagewang dataset."""


import os

import datasets
from datasets.tasks import ImageClassification


_CITATION = """\
@misc{imagewang,
  author    = "Jeremy Howard",
  title     = "imagewang",
  url       = "https://github.com/fastai/imagenette/"
}
"""

_DESCRIPTION = """\
Image网 (pronounced Imagewang; 网 means "net" in Chinese) is an image classification dataset combined from Imagenette and Imagewoof datasets in a way to make it into a semi-supervised unbalanced classification problem:
    - the validation set is the same as the validation set of Imagewoof; there are no Imagenette images in the validation set (they're all in the training set),
    - only 10% of Imagewoof images are in the training set. The remaining images are in the "unsupervised" split.
"""

_HOMEPAGE = "https://github.com/fastai/imagenette"

_LICENSE = "Unknown"

_BASE_DOWNLOAD_URL = "https://s3.amazonaws.com/fast-ai-imageclas/{}.tgz"

_LABELS = [
    "n01440764",
    "n02086240",
    "n02087394",
    "n02088364",
    "n02089973",
    "n02093754",
    "n02096294",
    "n02099601",
    "n02102040",
    "n02105641",
    "n02111889",
    "n02115641",
    "n02979186",
    "n03000684",
    "n03028079",
    "n03394916",
    "n03417042",
    "n03425413",
    "n03445777",
    "n03888257",
]

_BASE_CONFIG_NAMES = ["full-size", "320px", "160px"]


class ImagewangConfig(datasets.BuilderConfig):
    """BuilderConfig for Imagewang dataset."""

    def __init__(self, name, **kwargs):
        assert "description" not in kwargs
        super().__init__(name=name, description=f"{name} variant.", version=datasets.Version("1.0.0"), **kwargs)

        base = "imagewang"
        suffix = {
            "full-size": "",
            "320px": "-320",
            "160px": "-160",
        }[name]
        self.url = _BASE_DOWNLOAD_URL.format(base + suffix)


class Imagewang(datasets.GeneratorBasedBuilder):
    """Imagewang dataset."""

    BUILDER_CONFIGS = [ImagewangConfig(name=name) for name in _BASE_CONFIG_NAMES]

    DEFAULT_CONFIG_NAME = "full-size"

    def _info(self):
        features = datasets.Features(
            {
                "image": datasets.Image(),
                "label": datasets.ClassLabel(names=_LABELS),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(self.config.url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "split": "val",
                },
            ),
            datasets.SplitGenerator(
                name="unsupervised",
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "split": "unsup",
                },
            ),
        ]

    def _generate_examples(self, files, split):
        for idx, (path, file) in enumerate(files):
            if split in path and path.endswith(".JPEG"):
                yield idx, {
                    "image": {"path": path, "bytes": file.read()},
                    "label": os.path.basename(os.path.dirname(path)) if split == "train" else None,
                }
