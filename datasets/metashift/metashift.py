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

# _preprocess_groups(), _parse_node_str(), _load_candidate_subsets() adapted from here :
# https://github.com/Weixin-Liang/MetaShift/blob/main/dataset/generate_full_MetaShift.py

# MIT License

# Copyright (c) 2021 Weixin-Liang

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""MetaShift Dataset."""

import json
import os
import pickle
from collections import Counter, defaultdict

import datasets
from datasets.tasks import ImageClassification


_CITATION = """\
@InProceedings{liang2022metashift,
title={MetaShift: A Dataset of Datasets for Evaluating Contextual Distribution Shifts and Training Conflicts},
author={Weixin Liang and James Zou},
booktitle={International Conference on Learning Representations},
year={2022},
url={https://openreview.net/forum?id=MTex8qKavoS}
}
"""


_DESCRIPTION = """\
The MetaShift is a dataset of datasets for evaluating distribution shifts and training conflicts.
The MetaShift dataset is a collection of 12,868 sets of natural images across 410 classes.
It was created for understanding the performance of a machine learning model across diverse data distributions.
"""

_HOMEPAGE = "https://metashift.readthedocs.io/"


_LICENSE = "Creative Commons Attribution 4.0 International License"


_URLS = {
    "image_files": "https://nlp.stanford.edu/data/gqa/images.zip",
    "scene_graph_annotations": "https://nlp.stanford.edu/data/gqa/sceneGraphs.zip",
}

_METADATA_URLS = {
    "full_candidate_subsets": "https://github.com/Weixin-Liang/MetaShift/raw/main/dataset/meta_data/full-candidate-subsets.pkl",
}

_ATTRIBUTES_URLS = {
    "attributes_candidate_subsets": "https://github.com/Weixin-Liang/MetaShift/raw/main/dataset/attributes_MetaShift/attributes-candidate-subsets.pkl",
}


# See https://github.com/Weixin-Liang/MetaShift/blob/main/dataset/meta_data/class_hierarchy.json
# for the full object vocabulary and its hierarchy.
# Since the total number of all subsets is very large, all of the following scripts only generate a subset of MetaShift.

_CLASSES = [
    "cat",
    "dog",
    "bus",
    "truck",
    "elephant",
    "horse",
]


_ATTRIBUTES = [
    "cat(orange)",
    "cat(white)",
    "dog(sitting)",
    "dog(jumping)",
]


class MetashiftConfig(datasets.BuilderConfig):
    """BuilderConfig for MetaShift."""

    def __init__(
        self,
        selected_classes=None,
        attributes_dataset=False,
        attributes=None,
        with_image_metadata=False,
        image_subset_size_threshold=25,
        min_local_groups=5,
        **kwargs,
    ):
        """BuilderConfig for MetaShift.

        Args:
            selected_classes: `list[string]`, optional, list of the classes to generate the MetaShift dataset for.
                If `None`, the list is equal to `['cat', 'dog', 'bus', 'truck', 'elephant', 'horse']`.
            attributes_dataset: `bool`, default `False`, if `True`, the script generates the MetaShift-Attributes dataset.
            attributes: `list[string]`, optional, list of attributes classes included in the Attributes dataset.
                If `None` and `attributes_dataset` is `True`, it's equal to `["cat(orange)", "cat(white)", "dog(sitting)", "dog(jumping)"]`.
            with_image_metadata: `bool`, default `False`, whether to include image metadata.
                If set to `True`, this will give additional metadata about each image.
            image_subset_size_threshold: `int`, default `25`, the number of images required to be considered a subset.
                If the number of images is less than this threshold, the subset is ignored.
            min_local_groups: `int`, default `5`, the minimum number of local groups required to be considered an object class.
            **kwargs: keyword arguments forwarded to super.
        """
        super(MetashiftConfig, self).__init__(**kwargs)
        self.selected_classes = _CLASSES if selected_classes is None else selected_classes
        self.attributes_dataset = attributes_dataset
        if attributes_dataset:
            self.attributes = _ATTRIBUTES if attributes is None else attributes
        self.with_image_metadata = with_image_metadata
        self.IMAGE_SUBSET_SIZE_THRESHOLD = image_subset_size_threshold
        self.MIN_LOCAL_GROUPS = min_local_groups


class Metashift(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        MetashiftConfig(name="metashift", version=datasets.Version("1.0.0")),
    ]

    BUILDER_CONFIG_CLASS = MetashiftConfig

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(self._get_feature_types()),
            supervised_keys=("image", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _get_feature_types(self):
        features = {
            "image_id": datasets.Value("string"),
            "image": datasets.Image(),
        }

        if self.config.attributes_dataset:
            features.update({"label": datasets.ClassLabel(names=self.config.attributes)})
        else:
            features.update(
                {
                    "label": datasets.ClassLabel(names=self.config.selected_classes),
                    "context": datasets.Value("string"),
                }
            )

        if self.config.with_image_metadata:
            features.update(
                {
                    "width": datasets.Value("int64"),
                    "height": datasets.Value("int64"),
                    "location": datasets.Value("string"),
                    "weather": datasets.Value("string"),
                    "objects": datasets.Sequence(
                        {
                            "object_id": datasets.Value("string"),
                            "name": datasets.Value("string"),
                            "x": datasets.Value("int64"),
                            "y": datasets.Value("int64"),
                            "w": datasets.Value("int64"),
                            "h": datasets.Value("int64"),
                            "attributes": datasets.Sequence(datasets.Value("string")),
                            "relations": datasets.Sequence(
                                {
                                    "name": datasets.Value("string"),
                                    "object": datasets.Value("string"),
                                }
                            ),
                        }
                    ),
                }
            )

        return features

    @staticmethod
    def _parse_node_str(node_str):
        tag = node_str.split("(")[-1][:-1]
        subject_str = node_str.split("(")[0].strip()
        return subject_str, tag

    @staticmethod
    def _load_candidate_subsets(pkl_save_path):
        with open(pkl_save_path, "rb") as pkl_f:
            load_data = pickle.load(pkl_f)
            return load_data

    def _preprocess_groups(self, pkl_save_path, output_files_flag=False, subject_classes=_CLASSES):

        IMAGE_SUBSET_SIZE_THRESHOLD = self.config.IMAGE_SUBSET_SIZE_THRESHOLD
        trainsg_dupes = set()

        ##################################
        # Load cache data
        # Global data dict
        # Consult back to this dict for concrete image IDs.
        ##################################
        node_name_to_img_id = self._load_candidate_subsets(pkl_save_path)

        ##################################
        # Build a default counter first
        # Data Iteration
        ##################################
        group_name_counter = Counter()
        for node_name in node_name_to_img_id.keys():
            ##################################
            # Apply a threshold: e.g., 100
            ##################################
            imageID_set = node_name_to_img_id[node_name]
            imageID_set = imageID_set - trainsg_dupes
            node_name_to_img_id[node_name] = imageID_set
            if len(imageID_set) >= IMAGE_SUBSET_SIZE_THRESHOLD:
                group_name_counter[node_name] = len(imageID_set)
            else:
                pass

        most_common_list = group_name_counter.most_common()

        most_common_list = [(x, count) for x, count in group_name_counter.items()]

        ##################################
        # Build a subject dict
        ##################################

        subject_group_summary_dict = defaultdict(Counter)
        for node_name, imageID_set_len in most_common_list:
            subject_str, tag = self._parse_node_str(node_name)
            ##################################
            # TMP: inspect certain class
            ##################################
            if subject_str not in subject_classes:
                continue

            subject_group_summary_dict[subject_str][node_name] = imageID_set_len

        ##################################
        # Get the subject dict stats
        ##################################
        subject_group_summary_list = sorted(
            subject_group_summary_dict.items(), key=lambda x: sum(x[1].values()), reverse=True
        )

        new_subject_group_summary_list = list()
        subjects_to_all_set = defaultdict(set)

        ##################################
        # Subject filtering for dataset generation
        ##################################
        for subject_str, subject_data in subject_group_summary_list:

            ##################################
            # Discard an object class if it has too few local groups
            ##################################
            if len(subject_data) <= self.config.MIN_LOCAL_GROUPS:
                # if len(subject_data) <= 10:
                continue
            else:
                new_subject_group_summary_list.append((subject_str, subject_data))

            ##################################
            # Iterate all the subsets of the given subject
            ##################################
            for node_name in subject_data:
                subjects_to_all_set[node_name].update(node_name_to_img_id[node_name])

        return subjects_to_all_set

    @staticmethod
    def _load_scene_graph(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            scene_graph = json.load(f)
        return scene_graph

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract(_URLS)
        metadata_path = None
        subjects_to_all_set = None
        attributes_path = None
        if not self.config.attributes_dataset:
            metadata_path = dl_manager.download_and_extract(_METADATA_URLS)
            subjects_to_all_set = self._preprocess_groups(
                metadata_path["full_candidate_subsets"], subject_classes=self.config.selected_classes
            )
        else:
            attributes_path = dl_manager.download_and_extract(_ATTRIBUTES_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "images_path": os.path.join(data_path["image_files"], "images"),
                    "subjects_to_all_set": subjects_to_all_set,
                    "attributes_path": attributes_path,
                    "image_metadata_path": data_path["scene_graph_annotations"],
                },
            ),
        ]

    @staticmethod
    def _get_processed_image_metadata(image_id, scene_graph):
        image_metadata = scene_graph[image_id]
        objects = image_metadata["objects"]
        if isinstance(objects, list):
            return image_metadata
        processed_objects = []
        for object_id, object_details in objects.items():
            object_details["object_id"] = object_id
            processed_objects.append(object_details)
        image_metadata["objects"] = processed_objects
        if "location" not in image_metadata:
            image_metadata["location"] = None
        if "weather" not in image_metadata:
            image_metadata["weather"] = None

        return image_metadata

    def _generate_examples(self, images_path, subjects_to_all_set, attributes_path, image_metadata_path):
        idx = 0
        if self.config.with_image_metadata:
            train_scene_graph = os.path.join(image_metadata_path, "train_sceneGraphs.json")
            test_scene_graph = os.path.join(image_metadata_path, "val_sceneGraphs.json")

            scene_graph = self._load_scene_graph(train_scene_graph)
            scene_graph.update(self._load_scene_graph(test_scene_graph))

        if not self.config.attributes_dataset:
            for subset in subjects_to_all_set:
                class_name, context = self._parse_node_str(subset)
                for image_id in subjects_to_all_set[subset]:
                    image_filename = image_id + ".jpg"
                    src_image_path = os.path.join(images_path, image_filename)
                    features = {
                        "image_id": image_id,
                        "image": src_image_path,
                        "label": class_name,
                        "context": context,
                    }
                    if self.config.with_image_metadata:
                        image_metadata = self._get_processed_image_metadata(image_id, scene_graph)
                        features.update(image_metadata)
                    yield idx, features
                    idx += 1
        else:
            attributes_candidate_subsets = self._load_candidate_subsets(
                attributes_path["attributes_candidate_subsets"]
            )
            for attribute in self.config.attributes:
                image_IDs = attributes_candidate_subsets[attribute]
                for image_id in image_IDs:
                    image_filename = image_id + ".jpg"
                    src_image_path = os.path.join(images_path, image_filename)
                    features = {
                        "image_id": image_id,
                        "image": src_image_path,
                        "label": attribute,
                    }
                    if self.config.with_image_metadata:
                        image_metadata = self._get_processed_image_metadata(image_id, scene_graph)
                        features.update(image_metadata)
                    yield idx, features
                    idx += 1
