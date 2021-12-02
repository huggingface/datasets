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

# Lint as: python3
"""COCO Dataset"""


import pickle

import numpy as np

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
               Piotr Doll{'{a} }r and
               C. Lawrence Zitnick},
  title     = {Microsoft {COCO:} Common Objects in Context},
  journal   = {CoRR},
  volume    = {abs/1405.0312},
  year      = {2014},
  url       = {http://arxiv.org/abs/1405.0312},
  archivePrefix = {arXiv},
  eprint    = {1405.0312},
  timestamp = {Mon, 13 Aug 2018 16:48:13 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/LinMBHPRDZ14},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
                The MS COCO (Microsoft Common Objects in Context) dataset is a large-scale object detection, 
                segmentation, key-point detection, and captioning dataset. The dataset consists of 328K images of variable shapes.
                """

_DATA_URL = "http://images.cocodataset.org/zips/"


class CocoConfig(datasets.BuilderConfig):
  """BuilderConfig for CocoConfig."""

  def __init__(self, split, has_panoptic=False,  **kwargs):
    super(CocoConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
    self.has_panoptic = has_panoptic
    self.split = split


class COCO(datasets.GeneratorBasedBuilder):
    """COCO2017 Dataset"""

    BUILDER_CONFIGS = [
        CocoConfig(name="train2014", split = {"name": "train", "images":"train2014", "annotations":'annotations_trainval2014',
                  "annotation_type":AnnotationType.BBOXES}), #alternatively, we could say "TRAIN" in the name such that it's default
        CocoConfig(name="validation2014", split = {"name": "validation", "images":"val2014", "annotations":'annotations_trainval2014',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="test2014",   split = {"name": "test", "images":"test2014", "annotations":'image_info_test2014',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="test2015", split = {"name": "test", "images":"test2015", "annotations":'image_info_test2015',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="train2017", split = {"name": "train2017", "images":"train2017", "annotations":'image_info_trainval2017',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="val2017", split = {"name": "val2017", "images":"val2017", "annotations":'image_info_trainval2017',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="test2017", split = {"name": "test2017", "images":"test2017", "annotations":'image_info_test2017',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="test2017", has_panoptic = True,  split = {"name": "train2017", "images":"train2017", "annotations":'panoptic_annotations_trainval2017',
                  "annotation_type":AnnotationType.PANOPTIC}),
        CocoConfig(name="test2017", has_panoptic = True, split = {"name": "val2017", "images":"val2017", "annotations":'panoptic_annotations_trainval2017',
                  "annotation_type":AnnotationType.PANOPTIC})]

    def _info(self):
      features=datasets.Features(
              {
                'image': {"filename": datasets.Value("string")},
                'image/id': datasets.Value("int64"),
            }
          )
      if self.builder_config.has_panoptic:
        features.update({
          'panoptic_image':
              datasets.Image(),
          'panoptic_image/filename':
              atasets.Value("string"),
          'panoptic_objects':
              datasets.Sequence({
                  'id': datasets.Value("int64"),
                  'area': datasets.Value("int64"),
                  'bbox': datasets.Sequence(dtype, length=4),
                  'label': datasets.ClassLabel(num_classes=133),
                  'is_crowd': datasets.Value("bool")
              })})

      return datasets.DatasetInfo(
          description=_DESCRIPTION,
          features=features,
          homepage="https://cocodataset.org/",
          citation=_CITATION,
      )
        
    def _download_dataset(self, dl_manager):

      urls = {}
      for config in BUILDER_CONFIGS:
          urls['{}_images'.format(config.name)] = 'zips/{}.zip'.format(config.split["images"])
          urls['{}_annotations'.format(config.name)] = 'annotations/{}.zip'.format(
              config.split["annotations"])
          
      extracted_paths = dl_manager.download_and_extract(
              {key: root_url + url for key, url in urls.items()})
      
      return extracted_paths
      