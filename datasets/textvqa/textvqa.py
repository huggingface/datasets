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
"""TextVQA dataset"""

import copy
import json
import os

import datasets


_CITATION = """
@inproceedings{singh2019towards,
    title={Towards VQA Models That Can Read},
    author={Singh, Amanpreet and Natarjan, Vivek and Shah, Meet and Jiang, Yu and Chen, Xinlei and Batra, Dhruv and Parikh, Devi and Rohrbach, Marcus},
    booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
    pages={8317-8326},
    year={2019}
}
"""

_DESCRIPTION = """\
TextVQA requires models to read and reason about text in images to answer questions about them.
Specifically, models need to incorporate a new modality of text present in the images and reason
over it to answer TextVQA questions. TextVQA dataset contains 45,336 questions over 28,408 images
from the OpenImages dataset.
"""

_HOMEPAGE = "https://textvqa.org"

_LICENSE = "CC BY 4.0"

_SPLITS = ["train", "val", "test"]
_URLS = {
    f"{split}_annotations": f"https://dl.fbaipublicfiles.com/textvqa/data/TextVQA_0.5.1_{split}.json"
    for split in _SPLITS
}
# TextVQA val and train images are packed together
_URLS["train_val_images"] = "https://dl.fbaipublicfiles.com/textvqa/images/train_val_images.zip"
_URLS["test_images"] = "https://dl.fbaipublicfiles.com/textvqa/images/test_images.zip"
_NUM_ANSWERS_PER_QUESTION = 10


class Textvqa(datasets.GeneratorBasedBuilder):
    """TextVQA dataset."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="textvqa",
            version=datasets.Version("0.5.1"),
            description=_DESCRIPTION,
        )
    ]

    DEFAULT_CONFIG_NAME = "textvqa"

    def _info(self):
        features = datasets.Features(
            {
                "image_id": datasets.Value("string"),
                "question_id": datasets.Value("int32"),
                "question": datasets.Value("string"),
                "question_tokens": datasets.Sequence(datasets.Value("string")),
                "image": datasets.Image(),
                "image_width": datasets.Value("int32"),
                "image_height": datasets.Value("int32"),
                "flickr_original_url": datasets.Value("string"),
                "flickr_300k_url": datasets.Value("string"),
                "answers": datasets.Sequence(datasets.Value("string")),
                "image_classes": datasets.Sequence(datasets.Value("string")),
                "set_name": datasets.Value("string"),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annotations_path": downloaded_files["train_annotations"],
                    "images_path": downloaded_files["train_val_images"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "annotations_path": downloaded_files["val_annotations"],
                    "images_path": downloaded_files["train_val_images"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "annotations_path": downloaded_files["test_annotations"],
                    "images_path": downloaded_files["test_images"],
                },
            ),
        ]

    def _generate_examples(self, annotations_path: str, images_path: str):
        with open(annotations_path, "r", encoding="utf-8") as f:
            data = json.load(f)["data"]
            idx = 0
            for item in data:
                item = copy.deepcopy(item)
                item["answers"] = item.get("answers", ["" for _ in range(_NUM_ANSWERS_PER_QUESTION)])
                image_id = item["image_id"]
                image_subfolder = "train_images" if item["set_name"] != "test" else "test_images"
                item["image"] = os.path.join(images_path, image_subfolder, f"{image_id}.jpg")
                yield idx, item
                idx += 1
