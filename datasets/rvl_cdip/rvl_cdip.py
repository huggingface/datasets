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
    "rvl-cdip": "https://drive.google.com/uc?export=download&id=0Bz1dfcnrpXM-MUt4cHNzUEFXcmc",
    "labels" : "https://huggingface.co/datasets/mariosasko/rvl_cdip/resolve/main/labels_only.tar.gz"
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

_IMAGES_DIR = 'images/'

class RvlCdip(datasets.GeneratorBasedBuilder):
    """Ryerson Vision Lab Complex Document Information Processing dataset."""

    VERSION = datasets.Version("1.0.0")
    
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
        archive_path = dl_manager.download(_URLS["rvl-cdip"])
        labels_path = dl_manager.download_and_extract(_URLS["labels"])

        # (Optional) In non-streaming mode, we can extract the archive locally to have actual local image files:
        local_extracted_archive = dl_manager.extract(archive_path) if not dl_manager.is_streaming else None
        
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(
                        archive_path
                    ),
                    "labels_filepath": os.path.join(labels_path, "labels", "train.txt"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(
                        archive_path
                    ),
                    "labels_filepath": os.path.join(labels_path, "labels", "test.txt"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(
                        archive_path
                    ),
                    "labels_filepath": os.path.join(labels_path, "labels", "val.txt"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, local_extracted_archive, archive_iterator, labels_filepath, split):

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
