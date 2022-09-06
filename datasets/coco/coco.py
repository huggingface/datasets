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
from typing import List

import pycocotools.mask as mask_util

import datasets


_CITATION = """\
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
"""


_DESCRIPTION = """\
The MS COCO (Microsoft Common Objects in Context) dataset is a large-scale object detection,
segmentation, key-point detection, and captioning dataset. The dataset consists of 328K images of variable shapes.
"""


_HOMEPAGE = "https://cocodataset.org/#home"


_LICENSE = "Creative Commons Attribution 4.0 License"


_IMAGES_URL_TEMPLATE = "http://images.cocodataset.org/zips/{}.zip"


_ANNOTATIONS_URL_TEMPLATE = "http://images.cocodataset.org/annotations/{}.zip"


def format_labels_str(labels):
    return [label for line in labels.strip().splitlines() for label in line.strip().split(",")]


_FINE_LABELS = format_labels_str(
    """\
    person,bicycle,car,motorcycle,airplane
    bus,train,truck,boat,traffic light
    fire hydrant,stop sign,parking meter,bench,bird
    cat,dog,horse,sheep,cow
    elephant,bear,zebra,giraffe,backpack
    umbrella,handbag,tie,suitcase,frisbee
    skis,snowboard,sports ball,kite,baseball bat
    baseball glove,skateboard,surfboard,tennis racket,bottle
    wine glass,cup,fork,knife,spoon
    bowl,banana,apple,sandwich,orange
    broccoli,carrot,hot dog,pizza,donut
    cake,chair,couch,potted plant,bed
    dining table,toilet,tv,laptop,mouse
    remote,keyboard,cell phone,microwave,oven
    toaster,sink,refrigerator,book,clock
    vase,scissors,teddy bear,hair drier,toothbrush
    """
)

_COARSE_LABELS = format_labels_str(
    """\
    person,vehicle,outdoor,animal,accessory
    sports,kitchen,food,furniture,electronic
    appliance,indoor
    """
)


_FINE_LABELS_PERSON = ["person"]


_COARSE_LABELS_PERSON = ["person"]


_FINE_LABELS_PANOPTIC = format_labels_str(
    """\
    person,bicycle,car,motorcycle,airplane
    bus,train,truck,boat,traffic light
    fire hydrant,stop sign,parking meter,bench,bird
    cat,dog,horse,sheep,cow
    elephant,bear,zebra,giraffe,backpack
    umbrella,handbag,tie,suitcase,frisbee
    skis,snowboard,sports ball,kite,baseball bat
    baseball glove,skateboard,surfboard,tennis racket,bottle
    wine glass,cup,fork,knife,spoon
    bowl,banana,apple,sandwich,orange
    broccoli,carrot,hot dog,pizza,donut
    cake,chair,couch,potted plant,bed
    dining table,toilet,tv,laptop,mouse
    remote,keyboard,cell phone,microwave,oven
    toaster,sink,refrigerator,book,clock
    vase,scissors,teddy bear,hair drier,toothbrush
    banner,blanket,bridge,cardboard,counter
    curtain,door-stuff,floor-wood,flower,fruit
    gravel,house,light,mirror-stuff,net
    pillow,platform,playingfield,railroad,river
    road,roof,sand,sea,shelf
    snow,stairs,tent,towel,wall-brick
    wall-stone,wall-tile,wall-wood,water-other,window-blind
    window-other,tree-merged,fence-merged,ceiling-merged,sky-other-merged
    cabinet-merged,table-merged,floor-other-merged,pavement-merged,mountain-merged
    grass-merged,dirt-merged,paper-merged,food-other-merged,building-other-merged
    rock-merged,wall-other-merged,rug-merged
    """
)


_COARSE_LABELS_PANOPTIC = format_labels_str(
    """\
    person,vehicle,outdoor,animal,accessory
    sports,kitchen,food,furniture,electronic
    appliance,indoor,textile,building,raw-material
    furniture-stuff,floor,plant,food-stuff,ground
    structural,water,wall,window,ceiling
    sky,solid
    """
)


@dataclass
class SplitPathInfo:
    """
    Metadata needed to download and build the file paths for the MS COCO dataset split.

    Attributes:
        images (:obj:`str` or :obj:`List[str]`): The image directory or directories (without extension) to download for a split.
        annotations (:obj:`str` or :obj:`List[str]`): The directory or directories with annotation data
            (without extension) to download for a split.
        annotations_file_stem (:obj:`str` or :obj:`List[str]`, optional): The file stem of the annotation file/files.
    """

    images: str
    annotations: str
    annotations_file_stem: str


_CONFIG_NAME_TO_DESCRIPTION = {
    "2014": "The first version of MS COCO dataset released in 2014 for the object detection task. It contains 164K images split into training (83K), validation (41K) and test (41K) sets.",
    "2014_keypoint_detection": "The 2014 version of MS COCO dataset for the keypoint detection task.",
    "2015": "The 2015 version of MS COCO dataset for the object detection task with improved test set of 81K images which includes all the previous test images and 40K new images.",
    "2017": "The 2017 version of MS COCO dataset with the changed training/validation split, from 83K/41K to 118K/5K. The new split uses the same images and annotations. The 2017 test set is a subset of 41K images of the 2015 test set.",
    "2017_keypoint_detection": "The 2017 version of MS COCO dataset for the the keypoint detection task.",
    "2017_panoptic_segmentation": "The 2017 version of MS COCO dataset for the panoptic segmentation task.",
    "2017_unlabeled": "A new unannotated dataset of 123K images released in 2017. The images follow the same class distribution as the labeled images and are useful for semi-supervised learning.",
}


class CocoConfig(datasets.BuilderConfig):
    """BuilderConfig for MS COCO dataset."""

    def __init__(self, name, split_path_infos: List[SplitPathInfo], **kwargs):
        assert "description" not in kwargs
        description = _CONFIG_NAME_TO_DESCRIPTION[name]
        super(CocoConfig, self).__init__(
            version=datasets.Version("1.0.0"), name=name, description=description, **kwargs
        )
        self.split_path_infos = split_path_infos


class COCO(datasets.GeneratorBasedBuilder):
    """MS COCO dataset."""

    BUILDER_CONFIGS = [
        CocoConfig(
            "2014",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="instances_train2014",
                ),
                "test": SplitPathInfo(
                    images="test2014",
                    annotations="image_info_test2014",
                    annotations_file_stem="image_info_test2014",
                ),
                "val": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="instances_val2014",
                ),
            },
        ),
        CocoConfig(
            "2014_keypoint_detection",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="person_keypoints_train2014",
                ),
                "val": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="person_keypoints_val2014",
                ),
            },
        ),
        CocoConfig(
            "2015",
            split_path_infos={
                "test": SplitPathInfo(
                    images="test2015",
                    annotations="image_info_test2015",
                    annotations_file_stem="image_info_test2015",
                ),
                "test_dev": SplitPathInfo(
                    images="test2015",
                    annotations="image_info_test2015",
                    annotations_file_stem="image_info_test-dev2015",
                ),
            },
        ),
        CocoConfig(
            "2017",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="instances_train2017",
                ),
                "test": SplitPathInfo(
                    images="test2017",
                    annotations="image_info_test2017",
                    annotations_file_stem="image_info_test2017",
                ),
                "test_dev": SplitPathInfo(
                    images="test2017",
                    annotations="image_info_test2017",
                    annotations_file_stem="image_info_test-dev2017",
                ),
                "val": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="instances_val2017",
                ),
            },
        ),
        CocoConfig(
            "2017_keypoint_detection",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="person_keypoints_train2017",
                ),
                "val": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="person_keypoints_val2017",
                ),
            },
        ),
        CocoConfig(
            "2017_panoptic_segmentation",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="panoptic_annotations_trainval2017",
                    annotations_file_stem="panoptic_train2017",
                ),
                "val": SplitPathInfo(
                    images="val2017",
                    annotations="panoptic_annotations_trainval2017",
                    annotations_file_stem="panoptic_val2017",
                ),
            },
        ),
        CocoConfig(
            "2017_unlabeled",
            split_path_infos={
                "train": SplitPathInfo(
                    images="unlabeled2017",
                    annotations="image_info_unlabeled2017",
                    annotations_file_stem="image_info_unlabeled2017",
                ),
            },
        ),
    ]

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
            }
        )
        if self.config.name in {"2014", "2015", "2017"} or "keypoint_detection" in self.config.name:
            object_dict = {
                "id": datasets.Value("int64"),
                "area": datasets.Value("int64"),
                "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                "iscrowd": datasets.Value("bool"),
                "segmentation": datasets.Sequence(datasets.Sequence(datasets.Value("uint8"))),
            }
            if self.config.name in {"2014", "2015", "2017"}:
                object_dict.update(
                    {
                        "category_id": datasets.Value("int32"),
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS),
                    }
                )
            else:  # keypoint detection
                object_dict.update(
                    {
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
                    }
                )
            features["objects"] = datasets.Sequence(object_dict)
        elif "panoptic_segmentation" in self.config.name:
            segment_dict = {
                "id": datasets.Value("int64"),
                "area": datasets.Value("int64"),
                "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                "iscrowd": datasets.Value("bool"),
                "category_id": datasets.Value("int32"),
                "fine_label": datasets.ClassLabel(names=_FINE_LABELS_PANOPTIC),
                "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_PANOPTIC),
                "isthing": datasets.Value("bool"),
            }
            features.update({"image_segmented": datasets.Image(), "segments": datasets.Sequence(segment_dict)})

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
        downloaded_paths = dl_manager.download_and_extract(urls)

        splits = []
        for split, split_path_info in split_path_infos.items():
            images_dir = os.path.join(downloaded_paths[split]["images"], split_path_info.images)
            annotations_dir = downloaded_paths[split]["annotations"]
            annotations_file = os.path.join(
                annotations_dir, "annotations", f"{split_path_info.annotations_file_stem}.json"
            )
            # Extract images for the panoptic segmentation task
            if "panoptic_segmentation" in self.config.name:
                images_panoptic_archive = os.path.join(
                    annotations_dir, "annotations", f"panoptic_{split_path_info.images}.zip"
                )
                images_dir_panoptic = dl_manager.extract(images_panoptic_archive)
                images_dir_panoptic = os.path.join(images_dir_panoptic, f"panoptic_{split_path_info.images}")
            else:
                images_dir_panoptic = None

            splits.append(
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "annotations_file": annotations_file,
                        "images_dir": images_dir,
                        "images_dir_panoptic": images_dir_panoptic,
                    },
                )
            )

        return splits

    def _generate_examples(self, annotations_file, images_dir, images_dir_panoptic):
        if self.config.name in {"2014", "2015", "2017"} or "keypoint_detection" in self.config.name:
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            is_not_test = "annotations" in annotation_data and annotation_data["annotations"]
            is_keypoint_detection = "keypoint_detection" in self.config.name
            if is_not_test:
                annotations = annotation_data["annotations"]
                # Multiple annotations per image
                image_id_to_annotations = get_image_id_to_annotations_mapping(self.config.name, annotations)
                categories = annotation_data["categories"]
                id_to_fine_label = {category["id"]: category["name"] for category in categories}
                id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
                if is_keypoint_detection:
                    id_to_keypoints = {category["id"]: category["keypoints"] for category in categories}
                    id_to_skeleton = {category["id"]: category["skeleton"] for category in categories}
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir)
                if is_not_test:
                    annotations = image_id_to_annotations[image_info["id"]]
                    objects = []
                    for annot in annotations:
                        del annot["image_id"]
                        category_id = annot["category_id"]
                        object_ = annot
                        object_["fine_label"] = id_to_fine_label[category_id]
                        object_["coarse_label"] = id_to_coarse_label[category_id]
                        object_["segmentation"] = decode_mask(
                            object_["segmentation"], image_info["height"], image_info["width"]
                        )
                        if is_keypoint_detection:
                            keypoints_values = object_["keypoints"]
                            object_["keypoints"] = [
                                {"part": keypoint, "value": keypoints_values[i * 3 : i * 3 + 3]}
                                for i, keypoint in enumerate(id_to_keypoints[category_id])
                            ]
                            object_["skeleton"] = id_to_skeleton[category_id]
                        objects.append(object_)
                else:
                    objects = None
                example["objects"] = objects
                yield idx, example
        elif "panoptic_segmentation" in self.config.name:
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            annotations = annotation_data["annotations"]
            categories = annotation_data["categories"]
            id_to_fine_label = {category["id"]: category["name"] for category in categories}
            id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
            id_to_isthing = {category["id"]: category["isthing"] for category in categories}
            # A single annotation per image
            image_id_to_annotation = get_image_id_to_annotations_mapping(self.config.name, annotations)
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir)
                annotation = image_id_to_annotation[image_info["id"]]
                image_file_panoptic = annotation["file_name"]
                segments = []
                for annot in annotation["segments_info"]:
                    category_id = annot["category_id"]
                    segment = annot
                    segment["fine_label"] = id_to_fine_label[category_id]
                    segment["coarse_label"] = id_to_coarse_label[category_id]
                    segment["isthing"] = id_to_isthing[category_id]
                    segments.append(segment)
                example.update(
                    {"image_segmented": os.path.join(images_dir_panoptic, image_file_panoptic), "segments": segments}
                )
                yield idx, example
        elif "unlabeled" in self.config.name:
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            for idx, image_info in enumerate(images):
                yield idx, image_info_to_example(image_info, images_dir)


def get_image_id_to_annotations_mapping(config_name, annotations):
    """
    A helper function to build a mapping from image ids to annotations.
    """
    if config_name in {"2014", "2015", "2017"} or "keypoint_detection" in config_name:
        image_id_to_annotations = collections.defaultdict(list)
        for annotation in annotations:
            image_id_to_annotations[annotation["image_id"]].append(annotation)
        return image_id_to_annotations
    elif "panoptic_segmentation" in config_name:
        return {annot["image_id"]: annot for annot in annotations}
    else:
        raise ValueError(
            f"Generating the image_id to annotations mapping is not supported for configuration {config_name}."
        )


def image_info_to_example(image_info, images_dir):
    """
    A helper function to create an example from image metadata.
    """
    example = {
        "image_id": image_info["id"],
        "image": os.path.join(images_dir, image_info["file_name"]),
        "width": image_info["width"],
        "height": image_info["height"],
        "flickr_url": image_info.get("flickr_url"),  # Not defined for test data
        "coco_url": image_info["coco_url"],
        "license": image_info["license"],
        "date_captured": image_info["date_captured"],
    }
    return example


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
