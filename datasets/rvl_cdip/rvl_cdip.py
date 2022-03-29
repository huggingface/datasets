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

"""RVL-CDIP (Ryerson Vision Lab Complex Document Information Processing) dataset"""


import csv
import json
import os

import datasets
from datasets.tasks import ImageClassification


_CITATION = """\
@inproceedings{harley2015icdar,
    title = {Evaluation of Deep Convolutional Nets for Document Image Classification and Retrieval},
    author = {Adam W Harley and Alex Ufkes and Konstantinos G Derpanis},
    booktitle = {International Conference on Document Analysis and Recognition ({ICDAR})}},
    year = {2015}
}
"""


_DESCRIPTION = """\
The RVL-CDIP (Ryerson Vision Lab Complex Document Information Processing) dataset consists of 400,000 grayscale images in 16 classes, with 25,000 images per class. There are 320,000 training images, 40,000 validation images, and 40,000 test images.
"""


_HOMEPAGE = "https://www.cs.cmu.edu/~aharley/rvl-cdip/"


_LICENSE = "https://www.industrydocuments.ucsf.edu/help/copyright/"


_URLS = {
    "rvl-cdip": "https://docs.google.com/uc?id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc&export=download",
}

_CLASSES = [
    "letter",
    "form",
    "email",
    "handwritten",
    "advertisement",
    "scientific report",
    "scientific publication",
    "specification",
    "file folder",
    "news article",
    "budget",
    "invoice",
    "presentation",
    "questionnaire",
    "resume",
    "memo",
]


class RvlCdip(datasets.GeneratorBasedBuilder):
    """Ryerson Vision Lab Complex Document Information Processing dataset."""

    VERSION = datasets.Version("1.0.0")
    
    @property
    def manual_download_instructions(self):
        return """
        You need to
        1. Manually download `rvl-cdip.tar.gz` from https://docs.google.com/uc?id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc&export=download
        2. Extract the `rvl-cdip.tar.gz` at a folder <path/to/folder>.
        The <path/to/folder> can e.g. be `~/RVL-CDIP_Dataset`.
        After extracting the files, the structure of the <path/to/folder> would be as follows :
        <path/to/folder> :
            - images
            - labels
        RVL-CDIP can then be loaded using the following command `datasets.load_dataset("rvl_cdip", data_dir="<path/to/folder>")`.
        """

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(names=_CLASSES),
                }
            ),
            supervised_keys=("image", "label"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        local_data_path = dl_manager.manual_dir
        if not os.path.exists(local_data_path):
            raise FileNotFoundError(
                f"{local_data_path} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('rvl_cdip', data_dir=...)`. Manual download instructions: {self.manual_download_instructions})"
        )
        
        images_dir = os.path.join(local_data_path, "images")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "images_dir": images_dir,
                    "filepath": os.path.join(local_data_path, "labels", "train.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "images_dir": images_dir,
                    "filepath": os.path.join(local_data_path, "labels", "test.txt"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "images_dir": images_dir,
                    "filepath": os.path.join(local_data_path, "labels", "val.txt"),
                    "split": "dev",
                },
            ),
        ]


    def _generate_examples(self, images_dir, filepath, split):

        with open(filepath, encoding="utf-8") as f:
            data = f.read().splitlines()

        idx = 0
        for item in data:
            image_path, class_index = item.split(" ")
            image_path = os.path.join(images_dir, image_path)
            class_name = _CLASSES[int(class_index)]
            yield idx, {
                "image": image_path,
                "label": class_name,
            }
            idx += 1
