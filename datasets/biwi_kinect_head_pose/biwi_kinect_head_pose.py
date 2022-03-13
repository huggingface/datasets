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


class BiwiKinectHeadPose(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "person_id": datasets.Value("string"),
                    "frame_number": datasets.Value("string"),
                    "depth_image": datasets.Value("string"),
                    "rgb_image": datasets.Image(),
                    "3D_head_center": datasets.Array2D(shape=(3, 3), dtype="float"),
                    "3D_head_rotation": datasets.Value("float"),
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

    def _generate_examples(self, dataset_path):
        # TO-DO
        pass
