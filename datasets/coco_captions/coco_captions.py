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
"""COCO Captions dataset."""


import collections
import json
import os
from dataclasses import dataclass
from typing import List, Optional

import datasets


_CITATION = """\
@misc{https://doi.org/10.48550/arxiv.1504.00325,
  doi = {10.48550/ARXIV.1504.00325},
  url = {https://arxiv.org/abs/1504.00325},
  author = {Chen, Xinlei and Fang, Hao and Lin, Tsung-Yi and Vedantam, Ramakrishna and Gupta, Saurabh and Dollar, Piotr and Zitnick, C. Lawrence},
  keywords = {Computer Vision and Pattern Recognition (cs.CV), Computation and Language (cs.CL), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Microsoft COCO Captions: Data Collection and Evaluation Server},
  publisher = {arXiv},
  year = {2015},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
"""

_KARPHATY_AND_LI_CITATION = """\
@inproceedings{DBLP:conf/cvpr/KarpathyL15,
  author    = {Andrej Karpathy and
               Fei{-}Fei Li},
  title     = {Deep visual-semantic alignments for generating image
               descriptions},
  booktitle = {{IEEE} Conference on Computer Vision and Pattern Recognition,
               {CVPR} 2015, Boston, MA, USA, June 7-12, 2015},
  pages     = {3128--3137},
  publisher = {{IEEE} Computer Society},
  year      = {2015},
  url       = {https://doi.org/10.1109/CVPR.2015.7298932},
  doi       = {10.1109/CVPR.2015.7298932},
  timestamp = {Wed, 16 Oct 2019 14:14:50 +0200},
  biburl    = {https://dblp.org/rec/conf/cvpr/KarpathyL15.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""


_DESCRIPTION = """\
The MS COCO Caption dataset contains human generated captions for images contained in the Microsoft Common Objects in COntext (COCO) dataset.
"""


_HOMEPAGE = "https://github.com/tylin/coco-caption"


_LICENSE = "Creative Commons Attribution 4.0 License"


_IMAGES_URL_TEMPLATE = "http://images.cocodataset.org/zips/{}.zip"


_ANNOTATIONS_URL_TEMPLATE = "http://images.cocodataset.org/annotations/{}.zip"


_KARPHATY_AND_LI_ANNOTATIONS_FILE = "https://cs.stanford.edu/people/karpathy/deepimagesent/caption_datasets.zip"


@dataclass
class SplitPathInfo:
    """
    Metadata needed to download and build the file paths for the COCO Captions dataset split.

    Attributes:
        images (:obj:`str`): The image directory (without extension) to download for a split.
        annotations (:obj:`str`): The directory with annotation data (without extension) to download for a split.
        annotations_file_stem (:obj:`str`, optional): The file stem of the annotation file.
    """

    images: str
    annotations: str
    annotations_file_stem: Optional[str]


_CONFIG_NAME_TO_DESCRIPTION = {
    "2014": "The COCO Captions dataset with 83K/41K train/val split.",
    "2017": "The COCO Captions dataset with 118K/5K for train/val. It has the same exact images as the 2014 version.",
    "karpathy_and_li": 'This version divides the original COCO 2014 validation data into new 5000-image validation and test sets, plus a "restval" set containing the remaining ~30k images.',
}


class COCOCaptionsConfig(datasets.BuilderConfig):
    """BuilderConfig for COCO Captions dataset."""

    def __init__(self, name, split_path_infos: List[SplitPathInfo], **kwargs):
        assert "description" not in kwargs
        description = _CONFIG_NAME_TO_DESCRIPTION[name]
        super(COCOCaptionsConfig, self).__init__(
            version=datasets.Version("1.0.0"), name=name, description=description, **kwargs
        )
        self.split_path_infos = split_path_infos


class COCOCaptions(datasets.GeneratorBasedBuilder):
    """Builder for COCO Captions dataset."""

    BUILDER_CONFIGS = [
        COCOCaptionsConfig(
            "2014",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_train2014",
                ),
                "val": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_val2014",
                ),
            },
        ),
        COCOCaptionsConfig(
            "2017",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="captions_train2017",
                ),
                "val": SplitPathInfo(
                    images="val2017",
                    annotations="annotations_trainval2017",
                    annotations_file_stem="captions_val2017",
                ),
            },
        ),
        COCOCaptionsConfig(
            "karpathy_and_li",
            split_path_infos={
                "train": SplitPathInfo(
                    images="train2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_train2014",
                ),
                "val": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_val2014",
                ),
                "test": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_val2014",
                ),
                "restval": SplitPathInfo(
                    images="val2014",
                    annotations="annotations_trainval2014",
                    annotations_file_stem="captions_val2014",
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
        if "karpathy_and_li" in self.config.name:
            captions = datasets.Sequence(
                {
                    "id": datasets.Value("int64"),
                    "caption": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:
            captions = datasets.Sequence(
                {
                    "id": datasets.Value("int64"),
                    "caption": datasets.Value("string"),
                }
            )

        features["captions"] = captions

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION + "\n" + _KARPHATY_AND_LI_CITATION
            if self.config.name == "kapathy_and_li"
            else _CITATION,
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

        if self.config.name == "karpathy_and_li":
            extra_annotations_file = dl_manager.download_and_extract(_KARPHATY_AND_LI_ANNOTATIONS_FILE)
            extra_annotations_file = os.path.join(extra_annotations_file, "dataset_coco.json")
            with open(extra_annotations_file, encoding="utf-8") as f:
                annotations = json.load(f)["images"]
            # split => image id => annotations
            extra_annotations = collections.defaultdict(dict)
            for annotation in annotations:
                extra_annotations[annotation["split"]][annotation["cocoid"]] = annotation
        else:
            extra_annotations = None

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
                        "extra_annotations": extra_annotations[split] if extra_annotations is not None else None,
                    },
                )
            )
        return splits

    def _generate_examples(self, annotations_file, images_dir, extra_annotations):
        with open(annotations_file, encoding="utf8") as f:
            annotation_data = json.load(f)
        images = annotation_data["images"]
        annotations = annotation_data["annotations"]
        # Multiple annotations per image
        image_id_to_annotations = collections.defaultdict(list)
        for annotation in annotations:
            image_id_to_annotations[annotation["image_id"]].append(annotation)

        if self.config.name == "karpathy_and_li":
            for idx, image_info in enumerate(images):
                annotations = extra_annotations.get(image_info["id"])
                if annotations is not None:
                    example = image_info_to_example(image_info, images_dir)
                    captions = [
                        {"id": annot["sentid"], "caption": annot["raw"], "tokens": annot["tokens"]}
                        for annot in annotations["sentences"]
                    ]
                    example["captions"] = captions
                    yield idx, example
        else:
            for idx, image_info in enumerate(images):
                example = image_info_to_example(image_info, images_dir)
                annotations = image_id_to_annotations[image_info["id"]]
                captions = [{"id": annot["id"], "caption": annot["caption"]} for annot in annotations]
                example["captions"] = captions
                yield idx, example


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
