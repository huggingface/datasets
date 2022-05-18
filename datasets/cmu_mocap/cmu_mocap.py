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


import glob
import json
import os

import datasets


_CITATION = "N/A"


_DESCRIPTION = """\
The CMU Graphics Lab Motion Capture Database is a dataset containing motion capture recordings of people performing different actions such as walking, jumping, dancing etc. The actions have been performed by over 140 subjects. There are a total of 2605 trials in 6 categories and 23 subcategories.
"""

_HOMEPAGE = "http://mocap.cs.cmu.edu/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "This data is free for use in research projects. You may include this data in commercially-sold products, but you may not resell this data directly, even in converted form."


_URLS = {
    "asf-amc": "http://mocap.cs.cmu.edu/allasfamc.zip",
    "c3d": [
        "http://mocap.cs.cmu.edu/allc3d_0.zip",
        "http://mocap.cs.cmu.edu/allc3d_1a.zip",
        "http://mocap.cs.cmu.edu/allc3d_1b.zip",
        "http://mocap.cs.cmu.edu/allc3d_234.zip",
        "http://mocap.cs.cmu.edu/allc3d_56789.zip",
    ],
    "mpg": [
        "http://mocap.cs.cmu.edu/allmpg/allmpg_0.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_13.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_14.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_15to19.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_20.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_30-1.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_30-2.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_30-3.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_40to50-1.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_40to50-2.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_40to50-3.zip",
        "http://mocap.cs.cmu.edu/allmpg/allmpg_60to90.zip",
    ],
    "avi": "http://mocap.cs.cmu.edu/allavi.zip",
}

_METADATA_URL = "https://huggingface.co/datasets/dnaveenr/cmu_mocap/raw/main/subject_to_details.json"

_CATEGORIES = {
    "1": "Human Interaction",
    "2": "Interaction with Environment",
    "3": "Locomotion",
    "4": "Physical Activities & Sports",
    "5": "Situations & Scenarios",
    "6": "Test Motions",
    "": "",
}

_SUB_CATEGORY_NAMES = {
    ("1", "1"): "two subjects",
    ("2", "1"): "playground",
    ("2", "2"): "uneven terrain",
    ("2", "3"): "path with obstacles",
    ("3", "1"): "running",
    ("3", "2"): "walking",
    ("3", "3"): "jumping",
    ("3", "4"): "varied",
    ("4", "0"): "golf",
    ("4", "1"): "frisbee",
    ("4", "2"): "dance",
    ("4", "3"): "gymnastics",
    ("4", "4"): "acrobatics",
    ("4", "5"): "martial arts",
    ("4", "6"): "racquet/paddle sports",
    ("4", "7"): "soccer",
    ("4", "8"): "boxing",
    ("4", "9"): "general exercise and stretching",
    ("5", "1"): "common behaviors and expressions",
    ("5", "2"): "pantomime",
    ("5", "3"): "communication gestures and signals",
    ("5", "4"): "cross-category variety",
    ("6", "1"): "",
    ("", ""): "",
}


class CmuMocapConfig(datasets.BuilderConfig):
    """BuilderConfig for CMU Mocap."""

    def __init__(
        self,
        **kwargs,
    ):
        """BuilderConfig for MetaShift.

        Args:
            **kwargs: keyword arguments forwarded to super.
        """
        super(CmuMocapConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class CmuMocap(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        CmuMocapConfig(
            name="asf-amc",
            description="""\
            The ASF file (Acclaim Skeleton File) is a skeleton file . AMC files (Acclaim Motion Capture data) are the motion files.
            """,
        ),
        CmuMocapConfig(
            name="c3d",
            description="""\
            The C3D format stores 3D coordinate information, analog data and associated information used in 3D motion data capture and subsequent analysis operations.
            """,
        ),
        CmuMocapConfig(
            name="mpg",
            description="""\
            The MPG format is a common video file that uses a digital video format standardized by the Moving Picture Experts Group (MPEG).
          """,
        ),
        CmuMocapConfig(
            name="avi",
            description="""\
            The AVI (Audio Video Interleave) format has been the long standing format to save and deliver movies and other video files.
            """,
        ),
    ]

    BUILDER_CONFIG_CLASS = CmuMocapConfig

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(self._get_feature_types()),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _get_feature_types(self):
        features = {
            "subject_id": datasets.Value("int32"),
            "categories": datasets.Sequence(datasets.Value("string")),
            "subcategories": datasets.Sequence(datasets.Value("string")),
            "descriptions": datasets.Sequence(datasets.Value("string")),
        }

        if self.config.name == "asf-amc":
            features.update(
                {
                    "motions": {
                        "amc_files" : datasets.Sequence(datasets.Value("string")),
                        "skeleton_file": datasets.Value("string"),
                    }
                }
            )
        else:
            features.update(
                {
                    "motions": datasets.Sequence(datasets.Value("string")),
                }
            )

        return features

    def _get_data_path(self, data_dir):
        if self.config.name == "asf-amc":
            data_path = os.path.join(data_dir, "all_asfamc", "subjects")
        else:
            data_path = os.path.join(data_dir, "subjects")

        return data_path

    def _split_generators(self, dl_manager):
        urls = _URLS[self.config.name]
        metadata_path = dl_manager.download(_METADATA_URL)
        data_dir = dl_manager.download_and_extract(urls)
        data_path = self._get_data_path(data_dir)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "data_path": data_path,
                    "metadata_path": metadata_path,
                    "split": "train",
                },
            ),
        ]

    @staticmethod
    def _get_category_subcategory_info(files, subject_id_to_details):
        categories = []
        subcategories = []
        descriptions = []

        for file_ in files:
            trial_number = os.path.basename(file_).split(".")[0]
            if trial_number not in subject_id_to_details:
                category_name = ""
                sub_category_name = ""
                description = ""
            else:
                category_id = str(subject_id_to_details[trial_number]["main_cat"])
                category_name = _CATEGORIES[category_id]
                sub_category_id = str(subject_id_to_details[trial_number]["sub_cat"])
                sub_category_name = _SUB_CATEGORY_NAMES[(category_id, sub_category_id)]
                description = subject_id_to_details[trial_number]["description"]
            categories.append(category_name)
            subcategories.append(sub_category_name)
            descriptions.append(description)

        return [categories, subcategories, descriptions]

    def _generate_examples(self, data_path, metadata_path, split):

        subject_dirs = os.listdir(data_path)

        with open(metadata_path, encoding="utf-8") as f:
            subject_id_to_details = json.load(f)

        idx = 0
        for subject in subject_dirs:
            subject_id = int(subject)
            subject_path = os.path.join(data_path, subject)

            if self.config.name == "asf-amc":
                asf_file = os.path.join(subject_path, subject + ".asf")
                files = glob.glob(os.path.join(subject_path, "*.amc"))

            if self.config.name == "c3d":
                files = glob.glob(os.path.join(subject_path, "*.c3d"))

            if self.config.name == "mpg":
                files = glob.glob(os.path.join(subject_path, "*.mpg"))

            if self.config.name == "avi":
                files = glob.glob(os.path.join(subject_path, "*.avi"))

            categories, subcategories, descriptions = self._get_category_subcategory_info(files, subject_id_to_details)

            features = {
                "subject_id": subject_id,
                "categories": categories,
                "subcategories": subcategories,
                "descriptions": descriptions,
            }

            if self.config.name == "asf-amc":
                features.update({
                    "motions": {
                        "amc_files": files,
                        "skeleton_file": asf_file,
                    }
                }
                )
            else:
                features.update({
                    "motions": files,
                })
                

            yield idx, features
            idx += 1
