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
    "rvl-cdip": "https://huggingface.co/datasets/mariosasko/rvl_cdip/resolve/main/rvl-cdip.tar.gz",
}

_METADATA_URLS = {
    "train": "https://huggingface.co/datasets/mariosasko/rvl_cdip/resolve/main/train.txt",
    "test": "https://huggingface.co/datasets/mariosasko/rvl_cdip/resolve/main/test.txt",
    "val": "https://huggingface.co/datasets/mariosasko/rvl_cdip/resolve/main/val.txt",
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

_IMAGES_DIR = "images/"


class RvlCdip(datasets.GeneratorBasedBuilder):
    """Ryerson Vision Lab Complex Document Information Processing dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "path": datasets.Value("string"),
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
        labels_path = dl_manager.download(_METADATA_URLS)

        # (Optional) In non-streaming mode, we can extract the archive locally to have actual local image files:
        local_extracted_archive = dl_manager.extract(archive_path) if not dl_manager.is_streaming else None

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(archive_path),
                    "labels_filepath": labels_path["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(archive_path),
                    "labels_filepath": labels_path["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "local_extracted_archive": local_extracted_archive,
                    "archive_iterator": dl_manager.iter_archive(archive_path),
                    "labels_filepath": labels_path["val"],
                    "split": "dev",
                },
            ),
        ]

    @staticmethod
    def _get_image_to_class_map(data):
        image_to_class_id = {}
        for item in data:
            image_path, class_id = item.split(" ")
            image_path = os.path.join(_IMAGES_DIR, image_path)
            image_to_class_id[image_path] = int(class_id)

        return image_to_class_id

    def _generate_examples(self, local_extracted_archive, archive_iterator, labels_filepath, split):

        with open(labels_filepath, encoding="utf-8") as f:
            data = f.read().splitlines()

        image_to_class_id = self._get_image_to_class_map(data)

        for file_path, file_obj in archive_iterator:
            if file_path.startswith(_IMAGES_DIR):
                if file_path in image_to_class_id:
                    class_id = image_to_class_id[file_path]
                    label = _CLASSES[class_id]
                    if local_extracted_archive is not None:
                        yield {"image": os.path.join(local_extracted_archive, file_path), "label": label}
                    else:
                        yield {"image": {"path": file_path, "bytes": file_obj.read()}, "label": label}
