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
'''
_preprocess_groups(), _parse_node_str(), _load_candidate_subsets() adapted from here :
https://github.com/Weixin-Liang/MetaShift/blob/main/dataset/generate_full_MetaShift.py

MIT License

Copyright (c) 2021 Weixin-Liang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


"""MetaShift Dataset."""


import json
import os
import datasets
import pickle
from collections import Counter, defaultdict


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
The MetaShift dataset is a collection of 12,868 sets of natural images across 410 classes . 
It was created for understanding the performance of a machine learning model across diverse data distributions.
"""

_HOMEPAGE = "https://metashift.readthedocs.io/"


_LICENSE = "https://github.com/Weixin-Liang/MetaShift/blob/main/LICENSE"


_URLS = {
    "image_files": "https://nlp.stanford.edu/data/gqa/images.zip",
    "scene_graph_annotations": "https://nlp.stanford.edu/data/gqa/sceneGraphs.zip",
}

_METADATA_URLS = {
    "full_candidate_subsets": "https://github.com/Weixin-Liang/MetaShift/raw/main/dataset/meta_data/full-candidate-subsets.pkl",
}

_ATTRIBUTES_URLS = {
    "attributes_candidate_subsets" : "https://github.com/Weixin-Liang/MetaShift/raw/main/dataset/attributes_MetaShift/attributes-candidate-subsets.pkl",
    "structured_attributes_candidate_subsets" : "https://github.com/Weixin-Liang/MetaShift/raw/main/dataset/attributes_MetaShift/structured-attributes-candidate-subsets.pkl",
}


# See https://github.com/Weixin-Liang/MetaShift/blob/main/dataset/meta_data/class_hierarchy.json
# for the full object vocabulary and its hierarchy.
# Since the total number of all subsets is very large, all of the following scripts only generate a subset of MetaShift.

_SELECTED_CLASSES = [
    'cat', 
    'dog', 
    'bus', 
    'truck', 
    'elephant', 
    'horse', 
    'bowl', 
    'cup', 
]


class Metashift(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image_id": datasets.Value("string"),
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(names=_SELECTED_CLASSES),
                    "context": datasets.Value('string'),
                }
            ),
            supervised_keys=("image", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )
    
    
    def _parse_node_str(self, node_str):
        tag = node_str.split('(')[-1][:-1]
        subject_str = node_str.split('(')[0].strip() 
        return subject_str, tag
    
    def _load_candidate_subsets(self, pkl_save_path):
        with open(pkl_save_path, "rb") as pkl_f:
            load_data = pickle.load( pkl_f )
            print('pickle load', len(load_data), pkl_save_path)
            # pprint.pprint(load_data) # only for debugging 
            return load_data
    
    def _preprocess_groups(self, pkl_save_path, output_files_flag=False, subject_classes = _SELECTED_CLASSES):
    
        IMAGE_SUBSET_SIZE_THRESHOLD = 25
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
            imageID_set = imageID_set-trainsg_dupes
            node_name_to_img_id[node_name] = imageID_set
            if len(imageID_set) >= IMAGE_SUBSET_SIZE_THRESHOLD:
                group_name_counter[node_name] = len(imageID_set)
            else:
                pass

        most_common_list = group_name_counter.most_common()

        most_common_list = [ (x, count) for x, count in group_name_counter.items()]

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

            subject_group_summary_dict[ subject_str ][ node_name ] = imageID_set_len

        ##################################
        # Print the subject dict stats
        ##################################
        subject_group_summary_list = sorted(subject_group_summary_dict.items(), key=lambda x:  sum(x[1].values()), reverse=True) 


        new_subject_group_summary_list = list()
        subjects_to_all_set = defaultdict(set)
        
        ##################################
        # Subject filtering for dataset generation
        ##################################
        for subject_str, subject_data in subject_group_summary_list:

            ##################################
            # Discard an object class if it has too few local groups
            ##################################
            if len(subject_data) <= 5:
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

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract(_URLS)
        metadata_path = dl_manager.download_and_extract(_METADATA_URLS)
        
        subjects_to_all_set = self._preprocess_groups(metadata_path['full_candidate_subsets'], subject_classes=_SELECTED_CLASSES)
        
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "images_path": data_path['image_files'],
                    "subjects_to_all_set": subjects_to_all_set,
                },
            ),
        ]


    def _generate_examples(self, images_path, subjects_to_all_set):
        
        idx = 0
        IMAGE_DATA_FOLDER = images_path + '/images/'
        for subset in subjects_to_all_set:
            class_name, context = self._parse_node_str(subset)
            for image_id in subjects_to_all_set[subset]:
                src_image_path = IMAGE_DATA_FOLDER + image_id + '.jpg'
                yield idx, {
                        "image_id": image_id,
                        "image": src_image_path,
                        "label": class_name,
                        "context" : context,
                    }
                idx += 1
