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

from pathlib import Path

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
                    "labels": datasets.features.ClassLabel(names=_NAMES),
                }
            ),
            supervised_keys=("image_file_path", "labels"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[
                ImageClassification(image_file_path_column="image_file_path", label_column="labels", labels=_NAMES)
            ],
        )

    def _split_generators(self, dl_manager):
        data_files = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "archive": data_files["train"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "archive": data_files["validation"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "archive": data_files["test"],
                },
            ),
        ]

    def _generate_examples(self, archive):
        for i, path in enumerate(Path(archive).glob("**/*")):
            if path.suffix == ".jpg":
                yield i, dict(image_file_path=str(path), labels=path.parent.name.lower())
