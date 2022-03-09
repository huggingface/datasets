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
# TODO: Address all TODOs and remove all explanatory comments

"""MetaShift Dataset."""


import csv
import json
import os

import datasets


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

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(names=_SELECTED_CLASSES),
                }
            ),
            supervised_keys=("image", "label"),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_path = dl_manager.download_and_extract(_URLS)
        metadata_path = dl_manager.download_and_extract(_METADATA_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "test.jsonl"), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    # Yields examples as (key, example) tuples
                    yield key, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield key, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
