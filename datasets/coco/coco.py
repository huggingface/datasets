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

ANNOTATION_CLS = {
    AnnotationType.NONE: CocoAnnotation,
    AnnotationType.BBOXES: CocoAnnotationBBoxes,
    AnnotationType.PANOPTIC: CocoAnnotationPanoptic,
}
class CocoConfig(datasets.BuilderConfig):
  """BuilderConfig for CocoConfig."""

  def __init__(self, split, has_panoptic=False,  **kwargs):
    super(CocoConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
    self.has_panoptic = has_panoptic
    self.splits = splits


class COCO(datasets.GeneratorBasedBuilder):
    """COCO2017 Dataset"""

    BUILDER_CONFIGS = [
        CocoConfig(name="2014", split = {"name": "train", "images":"train2014", "annotations":'annotations_trainval2014',
                  "annotation_type":AnnotationType.BBOXES}), #alternatively, we could say "TRAIN" in the name such that it's default
        CocoConfig(name="2014", split = {"name": "validation", "images":"val2014", "annotations":'annotations_trainval2014',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="2014",   split = {"name": "test", "images":"test2014", "annotations":'image_info_test2014',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="2015", split = {"name": "test", "images":"test2015", "annotations":'image_info_test2015',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="2017", split = {"name": "train", "images":"train2017", "annotations":'image_info_trainval2017',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="2017", split = {"name": "validation", "images":"val2017", "annotations":'image_info_trainval2017',
                  "annotation_type":AnnotationType.BBOXES}),
        CocoConfig(name="2017", split = {"name": "test", "images":"test2017", "annotations":'image_info_test2017',
                  "annotation_type":AnnotationType.NONE}),
        CocoConfig(name="2017_panoptic", has_panoptic = True,  split = {"name": "train2017", "images":"train2017", "annotations":'panoptic_annotations_trainval2017',
                  "annotation_type":AnnotationType.PANOPTIC}),
        CocoConfig(name="2017_panoptic", has_panoptic = True, split = {"name": "val2017", "images":"val2017", "annotations":'panoptic_annotations_trainval2017',
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



    def _split_generators(self, dl_manager):

      urls = {}
      for config in BUILDER_CONFIGS:
          urls['{}_images'.format(config.name)] = 'zips/{}.zip'.format(config.splits["images"])
          urls['{}_annotations'.format(config.name)] = 'annotations/{}.zip'.format(
              config.splits["annotations"])
          
      extracted_paths = dl_manager.download_and_extract(
              {key: root_url + url for key, url in urls.items()})
        archive = dl_manager.download(_DATA_URL)

      return [
          datasets.SplitGenerator(
              name=datasets.Split.TRAIN, gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "train"}
          ),
          datasets.SplitGenerator(
              name=datasets.Split.TEST, gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "test"}
          ),
          datasets.SplitGenerator(
              name=datasets.Split.VALIDATION, gen_kwargs={"files": dl_manager.iter_archive(archive), "split": "validation"}
          ),
      ]

    def _generate_examples(self, image_dir, annotation_dir, split_name,
                          annotation_type, panoptic_dir):
      """Generate examples as dicts.
      Args:
        image_dir: `str`, directory containing the images
        annotation_dir: `str`, directory containing annotations
        split_name: `str`, <split_name><year> (ex: train2014, val2017)
        annotation_type: `AnnotationType`, the annotation format (NONE, BBOXES,
          PANOPTIC)
        panoptic_dir: If annotation_type is PANOPTIC, contains the panoptic image
          directory
      Yields:
        example key and data
      """

      if annotation_type == AnnotationType.BBOXES:
        instance_filename = 'instances_{}.json'
      elif annotation_type == AnnotationType.PANOPTIC:
        instance_filename = 'panoptic_{}.json'
      elif annotation_type == AnnotationType.NONE:  # No annotation for test sets
        instance_filename = 'image_info_{}.json'

      # Load the annotations (label names, images metadata,...)
      instance_path = os.path.join(
          annotation_dir,
          'annotations',
          instance_filename.format(split_name),
      )
      coco_annotation = ANNOTATION_CLS[annotation_type](instance_path)
      # Each category is a dict:
      # {
      #    'id': 51,  # From 1-91, some entry missing
      #    'name': 'bowl',
      #    'supercategory': 'kitchen',
      # }
      categories = coco_annotation.categories
      # Each image is a dict:
      # {
      #     'id': 262145,
      #     'file_name': 'COCO_train2017_000000262145.jpg'
      #     'flickr_url': 'http://farm8.staticflickr.com/7187/xyz.jpg',
      #     'coco_url': 'http://images.cocodataset.org/train2017/xyz.jpg',
      #     'license': 2,
      #     'date_captured': '2013-11-20 02:07:55',
      #     'height': 427,
      #     'width': 640,
      # }
      images = coco_annotation.images

      # TODO(b/121375022): ClassLabel names should also contains 'id' and
      # and 'supercategory' (in addition to 'name')
      # Warning: As Coco only use 80 out of the 91 labels, the c['id'] and
      # dataset names ids won't match.
      if self.builder_config.has_panoptic:
        objects_key = 'panoptic_objects'
      else:
        objects_key = 'objects'
      self.info.features[objects_key]['label'].names = [
          c['name'] for c in categories
      ]
      # TODO(b/121375022): Conversion should be done by ClassLabel
      categories_id2name = {c['id']: c['name'] for c in categories}

      # Iterate over all images
      annotation_skipped = 0
      for image_info in sorted(images, key=lambda x: x['id']):
        if annotation_type == AnnotationType.BBOXES:
          # Each instance annotation is a dict:
          # {
          #     'iscrowd': 0,
          #     'bbox': [116.95, 305.86, 285.3, 266.03],
          #     'image_id': 480023,
          #     'segmentation': [[312.29, 562.89, 402.25, ...]],
          #     'category_id': 58,
          #     'area': 54652.9556,
          #     'id': 86,
          # }
          instances = coco_annotation.get_annotations(img_id=image_info['id'])
        elif annotation_type == AnnotationType.PANOPTIC:
          # Each panoptic annotation is a dict:
          # {
          #     'file_name': '000000037777.png',
          #     'image_id': 37777,
          #     'segments_info': [
          #         {
          #             'area': 353,
          #             'category_id': 52,
          #             'iscrowd': 0,
          #             'id': 6202563,
          #             'bbox': [221, 179, 37, 27],
          #         },
          #         ...
          #     ]
          # }
          panoptic_annotation = coco_annotation.get_annotations(
              img_id=image_info['id'])
          instances = panoptic_annotation['segments_info']
        else:
          instances = []  # No annotations

        if not instances:
          annotation_skipped += 1

        #this needs to be changed
        def build_bbox(x, y, width, height):

          return tfds.features.BBox(
              ymin=y / image_info['height'],
              xmin=x / image_info['width'],
              ymax=(y + height) / image_info['height'],
              xmax=(x + width) / image_info['width'],
          )


        example = {
            'image': os.path.join(image_dir, split_name, image_info['file_name']),
            'image/filename': image_info['file_name'],
            'image/id': image_info['id'],
            objects_key: [{   
                'id': instance['id'],
                'area': instance['area'],
                'bbox': build_bbox(*instance['bbox']),
                'label': categories_id2name[instance['category_id']],
                'is_crowd': bool(instance['iscrowd']),
            } for instance in instances]
        }
        if self.builder_config.has_panoptic:
          panoptic_filename = panoptic_annotation['file_name']
          panoptic_image_path = os.path.join(panoptic_dir, panoptic_filename)
          example['panoptic_image'] = panoptic_image_path
          example['panoptic_image/filename'] = panoptic_filename

        yield image_info['file_name'], example
