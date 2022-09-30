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
"""CPPE-5 dataset."""


import collections
import json
import os

import datasets


_CITATION = """\
@misc{dagli2021cppe5,
      title={CPPE-5: Medical Personal Protective Equipment Dataset},
      author={Rishit Dagli and Ali Mustufa Shaikh},
      year={2021},
      eprint={2112.09569},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
"""

_DESCRIPTION = """\
CPPE - 5 (Medical Personal Protective Equipment) is a new challenging dataset with the goal
to allow the study of subordinate categorization of medical personal protective equipments,
which is not possible with other popular data sets that focus on broad level categories.
"""

_HOMEPAGE = "https://sites.google.com/view/cppe5"

_LICENSE = "Unknown"

_URL = "https://storage.googleapis.com/cppe-5/dataset.tar.gz"

_CATEGORIES = ["Coverall", "Face_Shield", "Gloves", "Goggles", "Mask"]


class CPPE5(datasets.GeneratorBasedBuilder):
    """CPPE - 5 dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "image_id": datasets.Value("int64"),
                "image": datasets.Image(),
                "width": datasets.Value("int32"),
                "height": datasets.Value("int32"),
                "objects": datasets.Sequence(
                    {
                        "id": datasets.Value("int64"),
                        "area": datasets.Value("int64"),
                        "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                        "category": datasets.ClassLabel(names=_CATEGORIES),
                    }
                ),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annotation_file_path": "annotations/train.json",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "annotation_file_path": "annotations/test.json",
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, annotation_file_path, files):
        def process_annot(annot, category_id_to_category):
            return {
                "id": annot["id"],
                "area": annot["area"],
                "bbox": annot["bbox"],
                "category": category_id_to_category[annot["category_id"]],
            }

        image_id_to_image = {}
        idx = 0
        # This loop relies on the ordering of the files in the archive:
        # Annotation files come first, then the images.
        for path, f in files:
            file_name = os.path.basename(path)
            if path == annotation_file_path:
                annotations = json.load(f)
                category_id_to_category = {category["id"]: category["name"] for category in annotations["categories"]}
                image_id_to_annotations = collections.defaultdict(list)
                for annot in annotations["annotations"]:
                    image_id_to_annotations[annot["image_id"]].append(annot)
                image_id_to_image = {annot["file_name"]: annot for annot in annotations["images"]}
            elif file_name in image_id_to_image:
                image = image_id_to_image[file_name]
                objects = [
                    process_annot(annot, category_id_to_category) for annot in image_id_to_annotations[image["id"]]
                ]
                yield idx, {
                    "image_id": image["id"],
                    "image": {"path": path, "bytes": f.read()},
                    "width": image["width"],
                    "height": image["height"],
                    "objects": objects,
                }
                idx += 1
