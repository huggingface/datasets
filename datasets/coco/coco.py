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
from typing import List, Optional, Union

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


_ANNOTATIONS_DENSEPOSE_URL_TEMPLATE = "https://dl.fbaipublicfiles.com/densepose/{}.json"


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


_FINE_LABELS_STUFF = format_labels_str(
    """\
    banner,blanket,branch,bridge,building-other
    bush,cabinet,cage,cardboard,carpet
    ceiling-other,ceiling-tile,cloth,clothes,clouds
    counter,cupboard,curtain,desk-stuff,dirt
    door-stuff,fence,floor-marble,floor-other,floor-stone
    floor-tile,floor-wood,flower,fog,food-other
    fruit,furniture-other,grass,gravel,ground-other
    hill,house,leaves,light,mat
    metal,mirror-stuff,moss,mountain,mud
    napkin,net,paper,pavement,pillow
    plant-other,plastic,platform,playingfield,railing
    railroad,river,road,rock,roof
    rug,salad,sand,sea,shelf
    sky-other,skyscraper,snow,solid-other,stairs
    stone,straw,structural-other,table,tent
    textile-other,towel,tree,vegetable,wall-brick
    wall-concrete,wall-other,wall-panel,wall-stone,wall-tile
    wall-wood,water-other,waterdrops,window-blind,window-other
    wood,other
    """
)


_COARSE_LABELS_STUFF = format_labels_str(
    """\
    textile,plant,building,furniture-stuff,structural
    raw-material,floor,ceiling,sky,ground
    water,food-stuff,solid,wall,window
    other
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
    annotations: Union[str, List[str]]
    annotations_file_stem: Optional[Union[str, List[str]]]


_CONFIG_NAME_TO_DESCRIPTION = {
    "2014": "The first version of MS COCO dataset released in 2014 for the object detection task. It contains 164K images split into training (83K), validation (41K) and test (41K) sets.",
    "2014_image_captioning": "The 2014 version of MS COCO dataset for the image captioning task.",
    "2014_keypoint_detection": "The 2014 version of MS COCO dataset for the keypoint detection task.",
    "2015": "The 2015 version of MS COCO dataset for the object detection task with improved test set of 81K images which includes all the previous test images and 40K new images.",
    "2017": "The 2017 version of MS COCO dataset with the changed training/validation split, from 83K/41K to 118K/5K. The new split uses the same images and annotations. The 2017 test set is a subset of 41K images of the 2015 test set.",
    "2017_image_captioning": "The 2017 version of MS COCO dataset for the stuff segmentation task.",
    "2017_keypoint_detection": "The 2017 version of MS COCO dataset for the the keypoint detection task.",
    "2017_stuff_segmentation": "The 2017 version of MS COCO dataset for the stuff segmentation task.",
    "2017_panoptic_segmentation": "The 2017 version of MS COCO dataset for the panoptic segmentation task.",
    "2017_unlabeled": "A new unannotated dataset of 123K images released in 2017. The images follow the same class distribution as the labeled images and are useful for semi-supervised learning.",
    "densepose": "The version of MS COCO dataset for the DensePose task.",
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
                "validation": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="instances_val2014",
                ),
            },
        ),
        CocoConfig(
            "2014_image_captioning",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_train2014",
                ),
                "validation": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_val2014",
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
                "validation": SplitPathInfo(
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
                "validation": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="instances_val2017",
                ),
            },
        ),
        CocoConfig(
            "2017_image_captioning",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="captions_train2017",
                ),
                "validation": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="captions_val2017",
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
                "validation": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="person_keypoints_val2017",
                ),
            },
        ),
        CocoConfig(
            "2017_stuff_segmentation",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="stuff_annotations_trainval2017",
                    annotations_file_stem="stuff_train2017",
                ),
                "validation": SplitPathInfo(
                    images="val2017",
                    annotations="stuff_annotations_trainval2017",
                    annotations_file_stem="stuff_val2017",
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
                "validation": SplitPathInfo(
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
        CocoConfig(
            "densepose",
            split_path_infos={
                "train": SplitPathInfo(
                    images=["train2014", "val2014"],
                    annotations=["densepose_coco_2014_train", "densepose_coco_2014_valminusminival"],
                    annotations_file_stem=None,
                ),
                "test": SplitPathInfo(
                    images="test2015",
                    annotations="densepose_coco_2014_test",
                    annotations_file_stem=None,
                ),
                "validation": SplitPathInfo(
                    images="val2014",
                    annotations="densepose_coco_2014_minival",
                    annotations_file_stem=None,
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
                "license": {
                    "url": datasets.Value("string"),
                    "id": datasets.Value("int16"),
                    "name": datasets.Value("string"),
                },
                "date_captured": datasets.Value("string"),
            }
        )
        object_dict = {
            "id": datasets.Value("int64"),
            "area": datasets.Value("int64"),
            "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
            "iscrowd": datasets.Value("bool"),  # always False for stuff segmentation task
            "segmentation": {
                # defined if iscrowd == False
                "polygon": datasets.Sequence(datasets.Sequence(datasets.Value("float32"))),
                # defined if iscrowd == True
                "RLE": {
                    "counts_str": datasets.Value("string"),
                    "counts_list": datasets.Sequence(datasets.Value("int32")),
                    "size": datasets.Sequence(datasets.Value("int32"), length=2),
                },
            },
        }
        if (
            self.config.name in {"2014", "2015", "2017"}
            or "stuff_segmentation" in self.config.name
            or "keypoint_detection" in self.config.name
        ):
            if self.config.name in {"2014", "2015", "2017"}:
                object_dict.update(
                    {
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS),
                    }
                )
            elif "stuff_segmentation" in self.config.name:
                object_dict.update(
                    {
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS_STUFF),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_STUFF),
                    }
                )
            else:
                object_dict.update(
                    {
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS_PERSON),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_PERSON),
                        "keypoints": datasets.Sequence(datasets.Value("int32")),
                        "num_keypoints": datasets.Value("int32"),
                        "keypoints_str": datasets.Sequence(datasets.Value("string")),
                        "skeleton": datasets.Sequence(datasets.Sequence(datasets.Value("int32"), length=2)),
                    }
                )
            features["objects"] = datasets.Sequence(object_dict)
        elif "panoptic_segmentation" in self.config.name:
            del object_dict["segmentation"]
            object_dict.update(
                {
                    "fine_label": datasets.ClassLabel(names=_FINE_LABELS_PANOPTIC),
                    "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_PANOPTIC),
                    "isthing": datasets.Value("bool"),
                }
            )
            features.update({"image_segmented": datasets.Image(), "segments": datasets.Sequence(object_dict)})
        elif "image_captioning" in self.config.name:
            features.update(
                {
                    "captions": datasets.Sequence(
                        {
                            "id": datasets.Value("int64"),
                            "caption": datasets.Value("string"),
                        }
                    ),
                }
            )
        elif "densepose" in self.config.name:
            features["license"] = datasets.Value("int32")
            object_dict.update(
                {
                    "fine_label": datasets.ClassLabel(names=_FINE_LABELS_PERSON),
                    "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_PERSON),
                    "keypoints": datasets.Sequence(datasets.Value("int32")),
                    "num_keypoints": datasets.Value("int32"),
                    "keypoints_str": datasets.Sequence(datasets.Value("string")),
                    "skeleton": datasets.Sequence(datasets.Sequence(datasets.Value("int32"), length=2)),
                    "dp_I": datasets.Sequence(datasets.Value("float32")),
                    "dp_U": datasets.Sequence(datasets.Value("float32")),
                    "dp_V": datasets.Sequence(datasets.Value("float32")),
                    "dp_x": datasets.Sequence(datasets.Value("float32")),
                    "dp_y": datasets.Sequence(datasets.Value("float32")),
                    "dp_masks": datasets.Sequence(
                        {
                            "counts": datasets.Value("string"),
                            "size": datasets.Sequence(datasets.Value("int32"), length=2),
                        }
                    ),
                }
            )
            features["poses"] = datasets.Sequence(object_dict)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        split_path_infos = self.config.split_path_infos

        if self.config.name == "densepose":
            # The annotation files for the DensePose task are not stored in an archive
            # and the train split references two image directories.
            def format_template_recursive(template, fill_value):
                if isinstance(fill_value, list):
                    return [format_template_recursive(template, v) for v in fill_value]
                else:
                    return template.format(fill_value)

            urls = {
                split: {
                    "annotations": format_template_recursive(
                        _ANNOTATIONS_DENSEPOSE_URL_TEMPLATE, split_path_info.annotations
                    ),
                    "images": format_template_recursive(_IMAGES_URL_TEMPLATE, split_path_info.images),
                }
                for split, split_path_info in split_path_infos.items()
            }
            downloaded_paths = dl_manager.download(urls)
            for split in downloaded_paths:
                downloaded_paths[split]["images"] = dl_manager.extract(downloaded_paths[split]["images"])
        else:
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
            if self.config.name == "densepose":
                images_dir = downloaded_paths[split]["images"]
                if isinstance(images_dir, list):
                    images_dir = [
                        os.path.join(image_dir, split_name)
                        for image_dir, split_name in zip(images_dir, split_path_info.images)
                    ]
                else:
                    images_dir = os.path.join(images_dir, split_path_info.images)
                annotations_paths = downloaded_paths[split]["annotations"]
                annotations_file = annotations_paths
                images_dir_panoptic = None
            else:
                images_dir = os.path.join(downloaded_paths[split]["images"], split_path_info.images)
                annotations_dir = downloaded_paths[split]["annotations"]
                annotations_file = os.path.join(
                    annotations_dir, "annotations", f"{split_path_info.annotations_file_stem}.json"
                )
                if "panoptic_segmentation" in self.config.name:
                    # If the task is panoptic segmentation, extract panoptic images
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
        if (
            self.config.name in {"2014", "2015", "2017"}
            or "stuff_segmentation" in self.config.name
            or "keypoint_detection" in self.config.name
        ):
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            licenses = annotation_data["licenses"]
            id_to_license = {license["id"]: license for license in licenses}
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
                    id_to_keypoints_str = {category["id"]: category["keypoints"] for category in categories}
                    id_to_skeleton = {category["id"]: category["skeleton"] for category in categories}
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir, id_to_license)
                if is_not_test:
                    annotations = image_id_to_annotations[image_info["id"]]
                    objects = []
                    for annot in annotations:
                        del annot["image_id"]
                        category_id = annot.pop("category_id")
                        object_ = annot
                        object_["fine_label"] = id_to_fine_label[category_id]
                        object_["coarse_label"] = id_to_coarse_label[category_id]
                        object_["segmentation"] = adjust_segmentation_format(object_["segmentation"])
                        if is_keypoint_detection:
                            object_["keypoints_str"] = id_to_keypoints_str[category_id]
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
            licenses = annotation_data["licenses"]
            id_to_license = {license["id"]: license for license in licenses}
            categories = annotation_data["categories"]
            id_to_fine_label = {category["id"]: category["name"] for category in categories}
            id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
            id_to_isthing = {category["id"]: category["isthing"] for category in categories}
            # A single annotation per image
            image_id_to_annotation = get_image_id_to_annotations_mapping(self.config.name, annotations)
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir, id_to_license)
                annotation = image_id_to_annotation[image_info["id"]]
                image_file_panoptic = annotation["file_name"]
                segments = []
                for annot in annotation["segments_info"]:
                    category_id = annot.pop("category_id")
                    segment = annot
                    segment["fine_label"] = id_to_fine_label[category_id]
                    segment["coarse_label"] = id_to_coarse_label[category_id]
                    segment["isthing"] = id_to_isthing[category_id]
                    segments.append(segment)
                example.update(
                    {"image_segmented": os.path.join(images_dir_panoptic, image_file_panoptic), "segments": segments}
                )
                yield idx, example
        elif "image_captioning" in self.config.name:
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            annotations = annotation_data["annotations"]
            licenses = annotation_data["licenses"]
            id_to_license = {license["id"]: license for license in licenses}
            # Multiple annotations per image
            image_id_to_annotations = get_image_id_to_annotations_mapping(self.config.name, annotations)
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir, id_to_license)
                annotations = image_id_to_annotations[image_info["id"]]
                captions = [{"id": annot["id"], "caption": annot["caption"]} for annot in annotations]
                example["captions"] = captions
                yield idx, example
        elif "unlabeled" in self.config.name:
            with open(annotations_file, encoding="utf8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            licenses = annotation_data["licenses"]
            id_to_license = {license["id"]: license for license in licenses}
            for idx, image_info in enumerate(images):
                yield idx, image_info_to_example(image_info, images_dir, id_to_license)
        else:  # DensePose

            def _generate(annotations_file_, images_dir_):
                with open(annotations_file_, encoding="utf8") as f:
                    annotation_data = json.load(f)
                images = annotation_data["images"]
                is_not_test = "annotations" in annotation_data and annotation_data["annotations"]
                if is_not_test:
                    annotations = annotation_data["annotations"]
                    image_id_to_annotations = get_image_id_to_annotations_mapping(self.config.name, annotations)
                    categories = annotation_data["categories"]
                    id_to_fine_label = {category["id"]: category["name"] for category in categories}
                    id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
                    id_to_keypoints_str = {category["id"]: category["keypoints"] for category in categories}
                    id_to_skeleton = {category["id"]: category["skeleton"] for category in categories}
                for image_info in images:
                    example = image_info_to_example(image_info, images_dir_)
                    if is_not_test:
                        annotations = image_id_to_annotations[image_info["id"]]
                        poses = []
                        for annot in annotations:
                            del annot["image_id"]
                            category_id = annot.pop("category_id")
                            pose = annot
                            pose["fine_label"] = id_to_fine_label[category_id]
                            pose["coarse_label"] = id_to_coarse_label[category_id]
                            pose["segmentation"] = adjust_segmentation_format(pose["segmentation"])
                            pose["keypoints_str"] = id_to_keypoints_str[category_id]
                            pose["skeleton"] = id_to_skeleton[category_id]
                            if "dp_I" not in pose:
                                pose["dp_I"] = None
                                pose["dp_U"] = None
                                pose["dp_V"] = None
                                pose["dp_x"] = None
                                pose["dp_y"] = None
                                pose["dp_masks"] = None
                            else:
                                pose["dp_masks"] = [dp_mask for dp_mask in pose["dp_masks"] if dp_mask]
                            poses.append(pose)
                    else:
                        poses = None
                    example["poses"] = poses
                    yield example

            if isinstance(annotations_file, str):
                annotations_file = [annotations_file]
                images_dir = [images_dir]

            idx = 0
            for annotations_file_, images_dir_ in zip(annotations_file, images_dir):
                for example in _generate(annotations_file_, images_dir_):
                    yield idx, example
                    idx += 1


def get_image_id_to_annotations_mapping(config_name, annotations):
    """
    A helper function to build a mapping from image ids to annotations.
    """
    if (
        config_name in {"2014", "2015", "2017"}
        or config_name == "densepose"
        or "stuff_segmentation" in config_name
        or "keypoint_detection" in config_name
        or "image_captioning" in config_name
    ):
        image_id_to_annotations = collections.defaultdict(list)
        for annotation in annotations:
            image_id_to_annotations[annotation["image_id"]].append(annotation)
        return image_id_to_annotations
    elif "panoptic_segmentation" in config_name:
        return {annot["image_id"]: annot for annot in annotations}
    else:
        raise ValueError(f"Generating mapping  for configuration {config_name} is not supported.")


def image_info_to_example(image_info, images_dir, id_to_license=None):
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
    if id_to_license is not None:
        # The DensePose annotations contain only license id information.
        example["license"] = id_to_license[example["license"]]
    return example


def adjust_segmentation_format(segmentation):
    """
    A helper function to adjust the format of the segmentation field in annotations.
    """
    if isinstance(segmentation, dict):
        if isinstance(segmentation["counts"], str):
            RLE = {
                "counts_str": segmentation["counts"],
                "counts_list": None,
                "size": segmentation["size"],
            }
        else:
            RLE = {
                "counts_str": None,
                "counts_list": segmentation["counts"],
                "size": segmentation["size"],
            }
        segmentation = {"polygon": None, "RLE": RLE}
    else:
        segmentation = {"polygon": segmentation, "RLE": None}
    return segmentation
