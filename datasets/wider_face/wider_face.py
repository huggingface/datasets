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
"""WIDER FACE dataset."""

import os

import datasets


_HOMEPAGE = "http://shuoyang1213.me/WIDERFACE/"

_LICENSE = "Unknown"

_CITATION = """\
@inproceedings{yang2016wider,
    Author = {Yang, Shuo and Luo, Ping and Loy, Chen Change and Tang, Xiaoou},
    Booktitle = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
    Title = {WIDER FACE: A Face Detection Benchmark},
    Year = {2016}}
"""

_DESCRIPTION = """\
WIDER FACE dataset is a face detection benchmark dataset, of which images are
selected from the publicly available WIDER dataset. We choose 32,203 images and
label 393,703 faces with a high degree of variability in scale, pose and
occlusion as depicted in the sample images. WIDER FACE dataset is organized
based on 61 event classes. For each event class, we randomly select 40%/10%/50%
data as training, validation and testing sets. We adopt the same evaluation
metric employed in the PASCAL VOC dataset. Similar to MALF and Caltech datasets,
we do not release bounding box ground truth for the test images. Users are
required to submit final prediction files, which we shall proceed to evaluate.
"""

_TRAIN_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=15hGDLhsx8bLgLcIRD5DhYt5iBxnjNF1M&export=download"
_TEST_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1HIfDbVEWKmsYKJZm4lchTBDLW5N7dY5T&export=download"
_VALIDATION_DOWNLOAD_URL = "https://drive.google.com/u/0/uc?id=1GUCogbp16PMGa39thoMMeWxp7Rp5oM8Q&export=download"
_ANNOT_DOWNLOAD_URL = "http://shuoyang1213.me/WIDERFACE/support/bbx_annotation/wider_face_split.zip"


class WiderFace(datasets.GeneratorBasedBuilder):
    """WIDER FACE dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "faces": datasets.Sequence(
                        {
                            "bbox": datasets.Sequence(datasets.Value("float32"), length=4),
                            "blur": datasets.ClassLabel(names=["clear", "normal", "heavy"]),
                            "expression": datasets.ClassLabel(names=["typical", "exaggerate"]),
                            "illumination": datasets.ClassLabel(names=["normal", "exaggerate "]),
                            "occlusion": datasets.ClassLabel(names=["no", "partial", "heavy"]),
                            "pose": datasets.ClassLabel(names=["typical", "atypical"]),
                            "invalid": datasets.Value("bool"),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        train_dir, test_dir, validation_dir, annot_dir = dl_manager.download_and_extract(
            [_TRAIN_DOWNLOAD_URL, _TEST_DOWNLOAD_URL, _VALIDATION_DOWNLOAD_URL, _ANNOT_DOWNLOAD_URL]
        )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "split": "train",
                    "data_dir": train_dir,
                    "annot_dir": annot_dir,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "split": "test",
                    "data_dir": test_dir,
                    "annot_dir": annot_dir,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "split": "val",
                    "data_dir": validation_dir,
                    "annot_dir": annot_dir,
                },
            ),
        ]

    def _generate_examples(self, split, data_dir, annot_dir):
        image_dir = os.path.join(data_dir, "WIDER_" + split, "images")
        annot_fname = "wider_face_test_filelist.txt" if split == "test" else f"wider_face_{split}_bbx_gt.txt"
        with open(os.path.join(annot_dir, "wider_face_split", annot_fname), "r", encoding="utf-8") as f:
            idx = 0
            while True:
                line = f.readline()
                line = line.rstrip()
                if not line.endswith(".jpg"):
                    break
                image_file_path = os.path.join(image_dir, line)
                faces = []
                if split != "test":
                    # Read number of bounding boxes
                    nbboxes = int(f.readline())
                    # Cases with 0 bounding boxes, still have one line with all zeros.
                    # So we have to read it and discard it.
                    if nbboxes == 0:
                        f.readline()
                    else:
                        for _ in range(nbboxes):
                            line = f.readline()
                            line = line.rstrip()
                            line_split = line.split()
                            assert len(line_split) == 10, f"Cannot parse line: {line_split}"
                            line_parsed = [int(n) for n in line_split]
                            (
                                xmin,
                                ymin,
                                wbox,
                                hbox,
                                blur,
                                expression,
                                illumination,
                                invalid,
                                occlusion,
                                pose,
                            ) = line_parsed
                            faces.append(
                                {
                                    "bbox": [xmin, ymin, wbox, hbox],
                                    "blur": blur,
                                    "expression": expression,
                                    "illumination": illumination,
                                    "occlusion": occlusion,
                                    "pose": pose,
                                    "invalid": invalid,
                                }
                            )
                yield idx, {"image": image_file_path, "faces": faces}
                idx += 1
