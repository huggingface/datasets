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
"""COCO-Stuff dataset."""


import collections
import json
import os
from dataclasses import dataclass
from typing import List, Optional, Union

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

@article{DBLP:journals/corr/CaesarUF16a,
  author    = {Holger Caesar and
               Jasper R. R. Uijlings and
               Vittorio Ferrari},
  title     = {COCO-Stuff: Thing and Stuff Classes in Context},
  journal   = {CoRR},
  volume    = {abs/1612.03716},
  year      = {2016},
  url       = {http://arxiv.org/abs/1612.03716},
  eprinttype = {arXiv},
  eprint    = {1612.03716},
  timestamp = {Mon, 13 Aug 2018 16:47:38 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/CaesarUF16a.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


_DESCRIPTION = """\
The Common Objects in COntext-stuff (COCO-stuff) dataset is a dataset for scene understanding tasks like semantic segmentation, object detection and image captioning.
It is constructed by annotating the original COCO dataset, which originally annotated things while neglecting stuff annotations.
There are 164k images in COCO-stuff dataset that span over 172 categories including 80 things, 91 stuff, and 1 unlabeled class.
"""


_HOMEPAGE = "https://github.com/nightrome/cocostuff"


_LICENSE = "https://github.com/nightrome/cocostuff#licensing"


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
    Metadata needed to download and build the file paths for the COCO-Stuff dataset split.

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


class COCOStuffConfig(datasets.BuilderConfig):
    """BuilderConfig for COCO-Stuff dataset."""

    def __init__(self, name, split_path_infos: List[SplitPathInfo], **kwargs):
        assert "description" not in kwargs
        description = _CONFIG_NAME_TO_DESCRIPTION[name]
        super(COCOStuffConfig, self).__init__(
            version=datasets.Version("1.0.0"), name=name, description=description, **kwargs
        )
        self.split_path_infos = split_path_infos


class COCOStuff(datasets.GeneratorBasedBuilder):
    """Builder for COCO-Stuff dataset."""

    BUILDER_CONFIGS = [
        COCOStuffConfig(
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
                "date_captured": datasets.Value("timestamp[s, tz=UTC]"),
                "objects": datasets.Sequence(
                    {
                        "id": datasets.Value("int64"),
                        "area": datasets.Value("int64"),
                        "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                        "iscrowd": datasets.Value("bool"),
                        "segmentation": datasets.Sequence(datasets.Sequence(datasets.Value("uint8"))),
                        "fine_label": datasets.ClassLabel(names=_FINE_LABELS_STUFF),
                        "coarse_label": datasets.ClassLabel(names=_COARSE_LABELS_STUFF),
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
        downloaded_paths = dl_manager.download_and_extract(urls)

        splits = []
        for split, split_path_info in split_path_infos.items():
            images_dir = os.path.join(downloaded_paths[split]["images"], split_path_info.images)
            annotations_dir = downloaded_paths[split]["annotations"]
            annotations_file = os.path.join(
                annotations_dir, "annotations", f"{split_path_info.annotations_file_stem}.json"
            )

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
        if (
            self.config.name in {"2014", "2015", "2017"}
            or "stuff_segmentation" in self.config.name
            or "keypoint_detection" in self.config.name
        ):
            with open(annotations_file, encoding="utf-8") as f:
                annotation_data = json.load(f)
            images = annotation_data["images"]
            licenses = annotation_data["licenses"]
            id_to_license = {license["id"]: license for license in licenses}
            is_not_test = "annotations" in annotation_data and annotation_data["annotations"]
            if is_not_test:
                annotations = annotation_data["annotations"]
                # Multiple annotations per image
                image_id_to_annotations = get_image_id_to_annotations_mapping(self.config.name, annotations)
                categories = annotation_data["categories"]
                id_to_fine_label = {category["id"]: category["name"] for category in categories}
                id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
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
                        objects.append(object_)
                else:
                    objects = None
                example["objects"] = objects
                yield idx, example


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


def image_info_to_example(image_info, images_dir):
    """
    A helper function to create an example from image metadata.
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
