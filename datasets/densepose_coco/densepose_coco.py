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
"""MS COCO dataset."""


import collections
import json
import os
from dataclasses import dataclass

import pycocotools.mask as mask_util

import datasets


_CITATION = r"""\
@article{DBLP:journals/corr/LinMBHPRDZ14,
  author    = {Tsung{-}Yi Lin and
               Michael Maire and
               Serge J. Belongie and
               Lubomir D. Bourdev and
               Ross B. Girshick and
               James Hays and
               Pietro Perona and
               Deva Ramanan and
               Piotr Doll{\'{a}}r and
               C. Lawrence Zitnick},
  title     = {Microsoft {COCO:} Common Objects in Context},
  journal   = {CoRR},
  volume    = {abs/1405.0312},
  year      = {2014},
  url       = {http://arxiv.org/abs/1405.0312},
  eprinttype = {arXiv},
  eprint    = {1405.0312},
  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/LinMBHPRDZ14.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}

@inproceedings{guler2018densepose,
  title={Densepose: Dense human pose estimation in the wild},
  author={ G{\"u}ler, R{\i}za Alp and Neverova, Natalia and Kokkinos, Iasonas},
  booktitle={Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages={7297--7306},
  year={2018}
}
"""


_DESCRIPTION = """\
DensePose-COCO is a large-scale ground-truth dataset with image-to-surface correspondences manually annotated on 50K COCO images and train DensePose-RCNN, to densely regress part-specific UV coordinates within every human region at multiple frames per second.
"""


_HOMEPAGE = "http://densepose.org/"


_LICENSE = "CC BY-NC 2.0"


_IMAGES_URL_TEMPLATE = "http://images.cocodataset.org/zips/{}.zip"


_ANNOTATIONS_URL_TEMPLATE = "https://dl.fbaipublicfiles.com/densepose/{}.json"


_FINE_LABELS_PERSON = ["person"]


_COARSE_LABELS_PERSON = ["person"]


@dataclass
class SplitPathInfo:
    """
    Metadata needed to download and build the file paths for the COCO Captions dataset split.

    Attributes:
        images (:obj:`str`): The image directory (without extension) to download for a split.
        annotations (:obj:`str`): The directory with annotation data (without extension) to download for a split.
    """

    images: str
    annotations: str


class DensePoseCOCOConfig(datasets.BuilderConfig):
    """BuilderConfig for the DensePose-COCO dataset."""

    def __init__(self, **kwargs):
        super(DensePoseCOCOConfig, self).__init__(**kwargs)
        self.split_path_infos = {
            "train": SplitPathInfo(
                images="train2014",
                annotations="densepose_coco_2014_train",
            ),
            "test": SplitPathInfo(
                images="test2015",
                annotations="densepose_coco_2014_test",
            ),
            "minival": SplitPathInfo(
                images="val2014",
                annotations="densepose_coco_2014_minival",
            ),
            "valminusminival": SplitPathInfo(
                images="val2014",
                annotations="densepose_coco_2014_valminusminival",
            ),
        }


class DensePoseCOCO(datasets.GeneratorBasedBuilder):
    """Builder for DensePose-COCO dataset."""

    BUILDER_CONFIG_CLASS = DensePoseCOCOConfig

    def _info(self):
        features = datasets.Features(
            {
                "image_id": datasets.Value("int64"),
                "image": datasets.Image(),
                "width": datasets.Value("int32"),
                "height": datasets.Value("int32"),
                "flickr_url": datasets.Value("string"),
                "coco_url": datasets.Value("string"),
                "license": datasets.Value("int16"),
                "date_captured": datasets.Value("timestamp[s, tz=UTC]"),
                "poses": datasets.Sequence(
                    {
                        "id": datasets.Value("int64"),
                        "area": datasets.Value("int64"),
                        "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                        "iscrowd": datasets.Value("bool"),
                        "segmentation": datasets.Sequence(datasets.Sequence(datasets.Value("uint8"))),
                        "category_id": datasets.Value("int32"),
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS_PERSON),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_PERSON),
                        "num_keypoints": datasets.Value("int32"),
                        "keypoints": datasets.Sequence(
                            {
                                "part": datasets.Value("string"),
                                "value": datasets.Sequence(datasets.Value("int32"), length=3),
                            }
                        ),
                        "skeleton": datasets.Sequence(datasets.Sequence(datasets.Value("int32"), length=2)),
                        "dp_I": datasets.Sequence(datasets.Value("float32")),
                        "dp_U": datasets.Sequence(datasets.Value("float32")),
                        "dp_V": datasets.Sequence(datasets.Value("float32")),
                        "dp_x": datasets.Sequence(datasets.Value("float32")),
                        "dp_y": datasets.Sequence(datasets.Value("float32")),
                        "dp_masks": datasets.Array2D(shape=(256, 256), dtype="uint8"),
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
        split_path_infos = self.config.split_path_infos

        urls = {
            split: {
                "annotations": _ANNOTATIONS_URL_TEMPLATE.format(split_path_info.annotations),
                "images": _IMAGES_URL_TEMPLATE.format(split_path_info.images),
            }
            for split, split_path_info in split_path_infos.items()
        }
        downloaded_paths = dl_manager.download(urls)
        for split in downloaded_paths:
            downloaded_paths[split]["images"] = dl_manager.extract(downloaded_paths[split]["images"])

        splits = []
        for split, split_path_info in split_path_infos.items():
            images_dir = os.path.join(downloaded_paths[split]["images"], split_path_info.images)
            annotations_file = downloaded_paths[split]["annotations"]
            splits.append(
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "annotations_file": annotations_file,
                        "images_dir": images_dir,
                        "split": split,
                    },
                )
            )

        return splits

    def _generate_examples(self, annotations_file, images_dir, split):
        with open(annotations_file, encoding="utf8") as f:
            annotation_data = json.load(f)

        images = annotation_data["images"]

        if split == "test":
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir)
                example["poses"] = None
                yield idx, example
        else:
            annotations = annotation_data["annotations"]
            image_id_to_annotations = collections.defaultdict(list)
            for annotation in annotations:
                image_id_to_annotations[annotation["image_id"]].append(annotation)
            categories = annotation_data["categories"]
            id_to_fine_label = {category["id"]: category["name"] for category in categories}
            id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
            id_to_keypoints = {category["id"]: category["keypoints"] for category in categories}
            id_to_skeleton = {category["id"]: category["skeleton"] for category in categories}
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir)
                annotations = image_id_to_annotations[image_info["id"]]
                example["poses"] = [
                    annotation_to_pose(
                        annot,
                        id_to_fine_label,
                        id_to_coarse_label,
                        id_to_keypoints,
                        id_to_skeleton,
                        image_info["height"],
                        image_info["width"],
                    )
                    for annot in annotations
                ]
                yield idx, example


def image_info_to_example(image_info, images_dir):
    """
    A helper function to create an example from the image metadata.
    """
    return {
        "image_id": image_info["id"],
        "image": os.path.join(images_dir, image_info["file_name"]),
        "width": image_info["width"],
        "height": image_info["height"],
        "flickr_url": image_info.get("flickr_url"),  # Not defined for test data
        "coco_url": image_info["coco_url"],
        "license": image_info["license"],
        "date_captured": image_info["date_captured"],
    }


def annotation_to_pose(
    annotation, id_to_fine_label, id_to_coarse_label, id_to_keypoints, id_to_skeleton, image_height, image_width
):
    """
    A helper function to create a pose annotation from a raw annotation.
    """

    del annotation["image_id"]
    category_id = annotation["category_id"]
    pose = annotation
    keypoints_values = pose["keypoints"]
    pose["fine_label"] = id_to_fine_label[category_id]
    pose["coarse_label"] = id_to_coarse_label[category_id]
    pose["segmentation"] = decode_mask(pose["segmentation"], image_height, image_width)
    pose["keypoints"] = [
        {"part": keypoint, "value": keypoints_values[i * 3 : i * 3 + 3]}
        for i, keypoint in enumerate(id_to_keypoints[category_id])
    ]
    pose["skeleton"] = id_to_skeleton[category_id]
    pose["dp_I"] = pose.get("dp_I")
    pose["dp_U"] = pose.get("dp_U")
    pose["dp_V"] = pose.get("dp_V")
    pose["dp_x"] = pose.get("dp_x")
    pose["dp_y"] = pose.get("dp_y")
    pose["dp_masks"] = pose.get("dp_masks")
    if pose["dp_masks"] is not None:
        pose["dp_masks"] = [
            decode_mask(dp_mask, image_height, image_width) if dp_mask else dp_mask for dp_mask in pose["dp_masks"]
        ]
    return pose


def decode_mask(mask, image_height, image_width):
    """
    A helper function to convert an encoded mask to a human-readable format.
    """
    if isinstance(mask, dict):
        if type(mask["counts"]) == list:
            rle = mask_util.frPyObjects(mask, image_height, image_width)
        else:
            rle = mask
        mask = mask_util.decode(rle)
    return mask
