# coding=utf-8
# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""ImageNet-Sketch data set for evaluating model's ability in learning (out-of-domain) semantics at ImageNet scale"""

import os

import datasets
from datasets.tasks import ImageClassification

from .classes import IMAGENET2012_CLASSES


_HOMEPAGE = "https://github.com/HaohanWang/ImageNet-Sketch"

_CITATION = """\
@inproceedings{wang2019learning,
        title={Learning Robust Global Representations by Penalizing Local Predictive Power},
        author={Wang, Haohan and Ge, Songwei and Lipton, Zachary and Xing, Eric P},
        booktitle={Advances in Neural Information Processing Systems},
        pages={10506--10518},
        year={2019}
}
"""

_DESCRIPTION = """\
ImageNet-Sketch data set consists of 50000 images, 50 images for each of the 1000 ImageNet classes.
We construct the data set with Google Image queries "sketch of __", where __ is the standard class name.
We only search within the "black and white" color scheme. We initially query 100 images for every class,
and then manually clean the pulled images by deleting the irrelevant images and images that are for similar
but different classes. For some classes, there are less than 50 images after manually cleaning, and then we
augment the data set by flipping and rotating the images.
"""

_URL = "https://huggingface.co/datasets/imagenet_sketch/resolve/main/data/ImageNet-Sketch.zip"


class ImageNetSketch(datasets.GeneratorBasedBuilder):
    """ImageNet-Sketch - a dataset of sketches of ImageNet classes"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.features.ClassLabel(names=list(IMAGENET2012_CLASSES.values())),
                }
            ),
            supervised_keys=("image", "label"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files]),
                },
            ),
        ]

    def _generate_examples(self, files):
        for i, path in enumerate(files):
            file_name = os.path.basename(path)
            if file_name.endswith(".JPEG"):
                yield i, {
                    "image": path,
                    "label": IMAGENET2012_CLASSES[os.path.basename(os.path.dirname(path)).lower()],
                }
