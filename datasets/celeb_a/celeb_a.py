# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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

# Taken from https://github.com/tensorflow/datasets/blob/master/tensorflow_datasets/image/celeba.py

"""CelebA dataset.
Large-scale CelebFaces Attributes (CelebA) Dataset
Deep Learning Face Attributes in the Wild
Ziwei Liu and Ping Luo and Xiaogang Wang and Xiaoou Tang
"""

from __future__ import absolute_import, division, print_function

import json
import os
import gc
import numpy as np
from PIL import Image
import datasets

LANDMARK_HEADINGS = ("lefteye_x lefteye_y righteye_x righteye_y "
                     "nose_x nose_y leftmouth_x leftmouth_y rightmouth_x "
                     "rightmouth_y").split()
ATTR_HEADINGS = (
    "5_o_Clock_Shadow Arched_Eyebrows Attractive Bags_Under_Eyes Bald Bangs "
    "Big_Lips Big_Nose Black_Hair Blond_Hair Blurry Brown_Hair "
    "Bushy_Eyebrows Chubby Double_Chin Eyeglasses Goatee Gray_Hair "
    "Heavy_Makeup High_Cheekbones Male Mouth_Slightly_Open Mustache "
    "Narrow_Eyes No_Beard Oval_Face Pale_Skin Pointy_Nose Receding_Hairline "
    "Rosy_Cheeks Sideburns Smiling Straight_Hair Wavy_Hair Wearing_Earrings "
    "Wearing_Hat Wearing_Lipstick Wearing_Necklace Wearing_Necktie Young"
).split()


_CITATION = """\
@inproceedings{conf/iccv/LiuLWT15,
  added-at = {2018-10-09T00:00:00.000+0200},
  author = {Liu, Ziwei and Luo, Ping and Wang, Xiaogang and Tang, Xiaoou},
  biburl = {https://www.bibsonomy.org/bibtex/250e4959be61db325d2f02c1d8cd7bfbb/dblp},
  booktitle = {ICCV},
  crossref = {conf/iccv/2015},
  ee = {http://doi.ieeecomputersociety.org/10.1109/ICCV.2015.425},
  interhash = {3f735aaa11957e73914bbe2ca9d5e702},
  intrahash = {50e4959be61db325d2f02c1d8cd7bfbb},
  isbn = {978-1-4673-8391-2},
  keywords = {dblp},
  pages = {3730-3738},
  publisher = {IEEE Computer Society},
  timestamp = {2018-10-11T11:43:28.000+0200},
  title = {Deep Learning Face Attributes in the Wild.},
  url = {http://dblp.uni-trier.de/db/conf/iccv/iccv2015.html#LiuLWT15},
  year = 2015
}
"""

_DESCRIPTION = """\
CelebFaces Attributes Dataset (CelebA) is a large-scale face attributes dataset\
 with more than 200K celebrity images, each with 40 attribute annotations. The \
images in this dataset cover large pose variations and background clutter. \
CelebA has large diversities, large quantities, and rich annotations, including\
 - 10,177 number of identities,
 - 202,599 number of face images, and
 - 5 landmark locations, 40 binary attributes annotations per image.
The dataset can be employed as the training and test sets for the following \
computer vision tasks: face attribute recognition, face detection, and landmark\
 (or facial part) localization.
"""


_HOMEPAGE = "http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html"


_LICENSE = ""


_URLs = {
    "img_align_celeba": "https://drive.google.com/uc?export=download&id=0B7EVK8r0v71pZjFTYXZWM3FlRnM",
    "list_eval_partition": "https://drive.google.com/uc?export=download&id=0B7EVK8r0v71pY0NSMzRuSXJEVkk",
    "landmarks_celeba": "https://drive.google.com/uc?export=download&id=0B7EVK8r0v71pd0FJY3Blby1HUTQ",
    "list_attr_celeba": "https://drive.google.com/uc?export=download&id=0B7EVK8r0v71pblRyaVFSWGxPY0U"
}

class CelebA(datasets.GeneratorBasedBuilder):
    """CelebA dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="default", version=VERSION, description="This part of the dataset covers the entire CelebA dataset."),
    ]

   
    def _info(self):
        features = datasets.Features(
                {
                    "image": datasets.Array3D((218,718,3),dtype="uint8"),
                    "landmarks": {name: datasets.Value("int64") for name in LANDMARK_HEADINGS},
                    "attributes": {name: datasets.Value("bool") for name in ATTR_HEADINGS}
                    # These are the features of your dataset like images, labels ...
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        
        data_dir = dl_manager.download_and_extract(_URLs)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "file_id": 0,
                    "data_dir": data_dir,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "file_id": 1,
                    "data_dir": data_dir,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "file_id": 2,
                    "data_dir": data_dir,
                },
            ),
        ]

    def _process_celeba_config_file(self, file_path):
        """Unpack the celeba config file.
        The file starts with the number of lines, and a header.
        Afterwards, there is a configuration for each file: one per line.
        Args:
        file_path: Path to the file with the configuration.
        Returns:
        keys: names of the attributes
        values: map from the file name to the list of attribute values for
                this file.
        """
        with open(file_path, encoding="utf-8") as f:
            data_raw = f.read()
        lines = data_raw.split("\n")

        keys = lines[1].strip().split()
        values = {}
        # Go over each line (skip the last one, as it is empty).
        for line in lines[2:-1]:
            row_values = line.strip().split()
            # Each row start with the 'file_name' and then space-separated values.
            values[row_values[0]] = [int(v) for v in row_values[1:]]
        return keys, values

    def _generate_examples(self, file_id, data_dir):
        """ Yields examples."""
       
        img_list_path = data_dir["list_eval_partition"]
        landmarks_path = data_dir["landmarks_celeba"]
        attr_path = data_dir["list_attr_celeba"]
        print(attr_path)

        with open(img_list_path,encoding="utf-8") as f:
            files = [
                line.split()[0]
                for line in f.readlines()
                if int(line.split()[1]) == file_id
            ]
        
        attributes = self._process_celeba_config_file(attr_path)
        landmarks = self._process_celeba_config_file(landmarks_path)

        for file_name in sorted(files):
            record = {
                "image": Image.open(os.path.join(data_dir['img_align_celeba'], 'img_align_celeba',file_name)),
                "landmarks": {
                    k: v for k, v in zip(landmarks[0], landmarks[1][file_name])
                },
                "attributes": {
                    # atributes value are either 1 or -1, so convert to bool
                    k: v > 0 for k, v in zip(attributes[0], attributes[1][file_name])
                },
            }
            gc.collect()
            yield file_name,record
