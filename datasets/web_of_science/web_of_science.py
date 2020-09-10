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
"""Web of science"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@inproceedings{kowsari2017HDLTex,
title={HDLTex: Hierarchical Deep Learning for Text Classification},
author={Kowsari, Kamran and Brown, Donald E and Heidarysafa, Mojtaba and Jafari Meimandi, Kiana and and Gerber, Matthew S and Barnes, Laura E},
booktitle={Machine Learning and Applications (ICMLA), 2017 16th IEEE International Conference on},
year={2017},
organization={IEEE}
}
"""

_DESCRIPTION = """\
The Web Of Science (WOS) dataset is a collection of data  of published papers
available from the Web of Science. WOS has been released in three versions: WOS-46985, WOS-11967 and WOS-5736. WOS-46985 is the
full dataset. WOS-11967 and WOS-5736 are two subsets of WOS-46985.

"""

_DATA_URL = (
    "https://data.mendeley.com/datasets/9rw3vkcfy4/6/files/c9ea673d-5542-44c0-ab7b-f1311f7d61df/WebOfScience.zip?dl=1"
)


class WebOfScienceConfig(datasets.BuilderConfig):
    """BuilderConfig for WebOfScience."""

    def __init__(self, **kwargs):
        """BuilderConfig for WebOfScience.

        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(WebOfScienceConfig, self).__init__(version=datasets.Version("6.0.0", ""), **kwargs)


class WebOfScience(datasets.GeneratorBasedBuilder):
    """Web of Science"""

    BUILDER_CONFIGS = [
        WebOfScienceConfig(
            name="WOS5736",
            description="""Web of Science Dataset WOS-5736: This dataset contains 5,736 documents with 11 categories which include 3 parents categories.""",
        ),
        WebOfScienceConfig(
            name="WOS11967",
            description="""Web of Science Dataset WOS-11967: This dataset contains 11,967 documents with 35 categories which include 7 parents categories.""",
        ),
        WebOfScienceConfig(
            name="WOS46985",
            description="""Web of Science Dataset WOS-46985: This dataset contains 46,985 documents with 134 categories which include 7 parents categories.""",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION + self.config.description,
            features=datasets.Features(
                {
                    "input_data": datasets.Value("string"),
                    "label": datasets.Value("int32"),
                    "label_level_1": datasets.Value("int32"),
                    "label_level_2": datasets.Value("int32"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://data.mendeley.com/datasets/9rw3vkcfy4/6",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        # dl_manager is a datasets.download.DownloadManager that can be used to

        dl_path = dl_manager.download_and_extract(_DATA_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "input_file": os.path.join(dl_path, self.config.name, "X.txt"),
                    "label_file": os.path.join(dl_path, self.config.name, "Y.txt"),
                    "label_level_1_file": os.path.join(dl_path, self.config.name, "YL1.txt"),
                    "label_level_2_file": os.path.join(dl_path, self.config.name, "YL2.txt"),
                },
            )
        ]

    def _generate_examples(self, input_file, label_file, label_level_1_file, label_level_2_file):
        """Yields examples."""
        with open(input_file, encoding="utf-8") as f:
            input_data = f.readlines()
        with open(label_file, encoding="utf-8") as f:
            label_data = f.readlines()
        with open(label_level_1_file, encoding="utf-8") as f:
            label_level_1_data = f.readlines()
        with open(label_level_2_file, encoding="utf-8") as f:
            label_level_2_data = f.readlines()
        for i in range(len(input_data)):
            yield i, {
                "input_data": input_data[i],
                "label": label_data[i],
                "label_level_1": label_level_1_data[i],
                "label_level_2": label_level_2_data[i],
            }
