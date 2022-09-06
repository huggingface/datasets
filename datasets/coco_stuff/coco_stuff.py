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
from typing import Optional

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
"""


_HOMEPAGE = "https://github.com/nightrome/cocostuff"


_LICENSE = "https://github.com/nightrome/cocostuff#licensing"


_IMAGES_URL_TEMPLATE = "http://images.cocodataset.org/zips/{}.zip"


_ANNOTATIONS_URL_TEMPLATE = "http://images.cocodataset.org/annotations/{}.zip"


def format_labels_str(labels):
    return [label for line in labels.strip().splitlines() for label in line.strip().split(",")]


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
    annotations: str
    annotations_file_stem: str
    pixel_maps: Optional[str] = None


SPLIT_PATH_INFOS = {
    "train": SplitPathInfo(
        images="train2017",
        annotations="stuff_annotations_trainval2017",
        annotations_file_stem="stuff_train2017",
        pixel_maps="stuff_train2017_pixelmaps",
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
        annotations="stuff_annotations_trainval2017",
        annotations_file_stem="stuff_val2017",
        pixel_maps="stuff_val2017_pixelmaps",
    ),
}



class COCOStuffConfig(datasets.BuilderConfig):
    """BuilderConfig for COCO-Stuff dataset."""

    def __init__(self, name, **kwargs):
        super(COCOStuffConfig, self).__init__(version=datasets.Version("1.0.0"), name=name, **kwargs)


class COCOStuff(datasets.GeneratorBasedBuilder):
    """Builder for COCO-Stuff dataset."""

    BUILDER_CONFIGS = [
        COCOStuffConfig(
            "coco-style_annotations", description="The version of MS COCO dataset for the stuff segmentation task."
        ),
        COCOStuffConfig(
            "png-style_annotations",
            description="The version of MS COCO dataset for the stuff segmentation task with segmentations in PNG format.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "coco-style_annotations"

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
                "stuff_segments": datasets.Sequence(
                    {
                        "id": datasets.Value("int64"),
                        "area": datasets.Value("int64"),
                        "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                        "iscrowd": datasets.Value("bool"),
                        "segmentation": datasets.Sequence(datasets.Sequence(datasets.Value("uint8")))
                        if self.config.name == "coco-style_annotations"
                        else datasets.Image(),
                        "category_id": datasets.Value("int32"),
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

        urls = {
            split: {
                "annotations": _ANNOTATIONS_URL_TEMPLATE.format(split_path_info.annotations),
                "images": _IMAGES_URL_TEMPLATE.format(split_path_info.images),
            }
            for split, split_path_info in SPLIT_PATH_INFOS.items()
        }
        downloaded_paths = dl_manager.download_and_extract(urls)

        splits = []
        for split, split_path_info in SPLIT_PATH_INFOS.items():
            images_dir = os.path.join(downloaded_paths[split]["images"], split_path_info.images)
            annotations_dir = downloaded_paths[split]["annotations"]
            annotations_file = os.path.join(
                annotations_dir, "annotations", f"{split_path_info.annotations_file_stem}.json"
            )

            if self.config.name == "png-style_annotations" and "test" not in split:
                segmentation_images_dir = dl_manager.extract(
                    os.path.join(annotations_dir, "annotations", split_path_info.pixel_maps + ".zip")
                )
                segmentation_images_dir = os.path.join(segmentation_images_dir, split_path_info.pixel_maps)
            else:
                segmentation_images_dir = None

            splits.append(
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "annotations_file": annotations_file,
                        "images_dir": images_dir,
                        "segmentation_images_dir": segmentation_images_dir,
                    },
                )
            )

        return splits

    def _generate_examples(self, annotations_file, images_dir, segmentation_images_dir):
        with open(annotations_file, encoding="utf-8") as f:
            annotation_data = json.load(f)
        images = annotation_data["images"]
        is_not_test = "annotations" in annotation_data and annotation_data["annotations"]
        if is_not_test:
            annotations = annotation_data["annotations"]
            # Multiple annotations per image
            image_id_to_annotations = get_image_id_to_annotations_mapping(annotations)
            categories = annotation_data["categories"]
            id_to_fine_label = {category["id"]: category["name"] for category in categories}
            id_to_coarse_label = {category["id"]: category["supercategory"] for category in categories}
        for idx, image_info in enumerate(images):
            example = image_info_to_example(image_info, images_dir)
            if is_not_test:
                annotations = image_id_to_annotations[image_info["id"]]
                stuff_segments = []
                for annot in annotations:
                    del annot["image_id"]
                    category_id = annot["category_id"]
                    segment_ = annot
                    segment_["fine_label"] = id_to_fine_label[category_id]
                    segment_["coarse_label"] = id_to_coarse_label[category_id]
                    segment_["segmentation"] = (
                        decode_mask(segment_["segmentation"], image_info["height"], image_info["width"])
                        if self.config.name == "coco-style_annotations"
                        else os.path.join(
                            segmentation_images_dir, os.path.splitext(image_info["file_name"])[0] + ".png"
                        )
                    )
                    stuff_segments.append(segment_)
            else:
                stuff_segments = None
            example["stuff_segments"] = stuff_segments
            yield idx, example


def get_image_id_to_annotations_mapping(annotations):
    """
    A helper function to build a mapping from image ids to annotations.
    """
    image_id_to_annotations = collections.defaultdict(list)
    for annotation in annotations:
        image_id_to_annotations[annotation["image_id"]].append(annotation)
    return image_id_to_annotations


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
