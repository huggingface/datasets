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

"""Biwi Kinect Head Pose Database."""


import glob
import os

import datasets


_CITATION = """\
@article{fanelli_IJCV,
  author = {Fanelli, Gabriele and Dantone, Matthias and Gall, Juergen and Fossati, Andrea and Van Gool, Luc},
  title = {Random Forests for Real Time 3D Face Analysis},
  journal = {Int. J. Comput. Vision},
  year = {2013},
  month = {February},
  volume = {101},
  number = {3},
  pages = {437--458}
}
"""


_DESCRIPTION = """\
The Biwi Kinect Head Pose Database is acquired with the Microsoft Kinect sensor, a structured IR light device.It contains 15K images of 20 people with 6 females and 14 males where 4 people were recorded twice.
"""


_HOMEPAGE = "https://icu.ee.ethz.ch/research/datsets.html"


_LICENSE = "This database is made available for non-commercial use such as university research and education."


_URLS = {
    "kinect_head_pose_db": "https://data.vision.ee.ethz.ch/cvl/gfanelli/kinect_head_pose_db.tgz",
}

_sequence_to_subject_map = {
    "01": "F01",
    "02": "F02",
    "03": "F03",
    "04": "F04",
    "05": "F05",
    "06": "F06",
    "07": "M01",
    "08": "M02",
    "09": "M03",
    "10": "M04",
    "11": "M05",
    "12": "M06",
    "13": "M07",
    "14": "M08",
    "15": "F03",
    "16": "M09",
    "17": "M10",
    "18": "F05",
    "19": "M11",
    "20": "M12",
    "21": "F02",
    "22": "M01",
    "23": "M13",
    "24": "M14",
}


class BiwiKinectHeadPose(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sequence_number": datasets.Value("string"),
                    "subject_id": datasets.Value("string"),
                    "rgb": datasets.Sequence(datasets.Image()),
                    "rgb_cal": {
                        "intrisic_mat": datasets.Array2D(shape=(3, 3), dtype="float64"),
                        "extrinsic_mat": {
                            "rotation": datasets.Array2D(shape=(3, 3), dtype="float64"),
                            "translation": datasets.Sequence(datasets.Value("float64"), length=3),
                        },
                    },
                    "depth": datasets.Sequence(datasets.Value("string")),
                    "depth_cal": {
                        "intrisic_mat": datasets.Array2D(shape=(3, 3), dtype="float64"),
                        "extrinsic_mat": {
                            "rotation": datasets.Array2D(shape=(3, 3), dtype="float64"),
                            "translation": datasets.Sequence(datasets.Value("float64"), length=3),
                        },
                    },
                    "head_pose_gt": datasets.Sequence(
                        {
                            "center": datasets.Sequence(datasets.Value("float64"), length=3),
                            "rotation": datasets.Array2D(shape=(3, 3), dtype="float64"),
                        }
                    ),
                    "head_template": datasets.Value("string"),
                }
            ),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        data_dir = dl_manager.download_and_extract(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "dataset_path": os.path.join(data_dir["kinect_head_pose_db"], "hpdb"),
                },
            ),
        ]

    @staticmethod
    def _get_calibration_information(cal_file_path):
        with open(cal_file_path, "r", encoding="utf-8") as f:
            cal_info = f.read().splitlines()

        intrisic_mat = []
        extrinsic_mat = []

        for data in cal_info[:3]:
            row = list(map(float, data.strip().split(" ")))
            intrisic_mat.append(row)

        for data in cal_info[6:9]:
            row = list(map(float, data.strip().split(" ")))
            extrinsic_mat.append(row)

        translation = list(map(float, cal_info[10].strip().split(" ")))

        return {
            "intrisic_mat": intrisic_mat,
            "extrinsic_mat": {
                "rotation": extrinsic_mat,
                "translation": translation,
            },
        }

    @staticmethod
    def _parse_head_pose_info(head_pose_file):
        with open(head_pose_file, "r", encoding="utf-8") as f:
            head_pose_info = f.read().splitlines()

        rotation = []
        for data in head_pose_info[:3]:
            row = list(map(float, data.strip().split(" ")))
            rotation.append(row)

        center = list(map(float, head_pose_info[4].strip().split(" ")))

        return {
            "center": center,
            "rotation": rotation,
        }

    @staticmethod
    def _get_head_pose_information(path):
        head_pose_files = sorted(glob.glob(os.path.join(path, "*_pose.txt")))

        head_poses_info = []

        for head_pose_file in head_pose_files:
            head_pose = BiwiKinectHeadPose._parse_head_pose_info(head_pose_file)
            head_poses_info.append(head_pose)

        return head_poses_info

    def _generate_examples(self, dataset_path):

        idx = 0
        folders = os.listdir(dataset_path)
        for item in folders:
            sequence_number = item
            sequence_base_path = os.path.join(dataset_path, sequence_number)
            if os.path.isdir(sequence_base_path):
                rgb_files = sorted(glob.glob(os.path.join(sequence_base_path, "*.png")))
                depth_files = sorted(glob.glob(os.path.join(sequence_base_path, "*.bin")))
                head_template_path = os.path.join(dataset_path, sequence_number + ".obj")
                rgb_cal = self._get_calibration_information(os.path.join(sequence_base_path, "rgb.cal"))
                depth_cal = self._get_calibration_information(os.path.join(sequence_base_path, "depth.cal"))
                head_pose_gt = self._get_head_pose_information(sequence_base_path)

                yield idx, {
                    "sequence_number": sequence_number,
                    "subject_id": _sequence_to_subject_map[sequence_number],
                    "rgb": rgb_files,
                    "rgb_cal": rgb_cal,
                    "depth": depth_files,
                    "depth_cal": depth_cal,
                    "head_pose_gt": head_pose_gt,
                    "head_template": head_template_path,
                }

                idx += 1
