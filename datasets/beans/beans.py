# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Beans leaf dataset with images of diseased and health leaves."""

import os

import datasets
from datasets.tasks import ImageClassification


_HOMEPAGE = "https://github.com/AI-Lab-Makerere/ibean/"

_CITATION = """\
@ONLINE {beansdata,
    author="Makerere AI Lab",
    title="Bean disease dataset",
    month="January",
    year="2020",
    url="https://github.com/AI-Lab-Makerere/ibean/"
}
"""

_DESCRIPTION = """\
Beans is a dataset of images of beans taken in the field using smartphone
cameras. It consists of 3 classes: 2 disease classes and the healthy class.
Diseases depicted include Angular Leaf Spot and Bean Rust. Data was annotated
by experts from the National Crops Resources Research Institute (NaCRRI) in
Uganda and collected by the Makerere AI research lab.
"""

_URLS = {
    "train": "https://storage.googleapis.com/ibeans/train.zip",
    "validation": "https://storage.googleapis.com/ibeans/validation.zip",
    "test": "https://storage.googleapis.com/ibeans/test.zip",
}

_NAMES = ["angular_leaf_spot", "bean_rust", "healthy"]


class Beans(datasets.GeneratorBasedBuilder):
    """Beans plant leaf images dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image_file_path": datasets.Value("string"),
                    "image": datasets.Image(),
                    "labels": datasets.features.ClassLabel(names=_NAMES),
                }
            ),
            supervised_keys=("image", "labels"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="labels")],
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["train"]]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["validation"]]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "files": dl_manager.iter_files([data_files["test"]]),
                },
            ),
        ]

    def _generate_examples(self, files):
        for i, path in enumerate(files):
            file_name = os.path.basename(path)
            if file_name.endswith(".jpg"):
                yield i, {
                    "image_file_path": path,
                    "image": path,
                    "labels": os.path.basename(os.path.dirname(path)).lower(),
                }
