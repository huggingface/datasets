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
"""NCSLGR: a small American Sign Language corpus annotated with non-manual features"""

from __future__ import absolute_import, division, print_function

import os
import re
from dataclasses import dataclass

from tqdm import tqdm

import datasets


_DESCRIPTION = """
A small American Sign Language corpus annotated with non-manual features
"""

_CITATION = """\
@misc{dataset:databases2007volumes,
    title={Volumes 2--7},
    author={Databases, NCSLGR},
    year={2007},
    publisher={American Sign Language Linguistic Research Project (Distributed on CD-ROM~…}
}
"""

_URL_ANNOTATIONS = "http://asl.cs.depaul.edu/corpus/elanBUcorpus.zip"
_URL_VIDEOS = "http://asl.cs.depaul.edu/corpus/video.zip"

_HOMEPAGE = "https://www.bu.edu/asllrp/ncslgr.html"


@dataclass
class NCSLGRConfig(datasets.BuilderConfig):
    """BuilderConfig for NCSLGR."""

    videos: bool = True


class NCSLGR(datasets.GeneratorBasedBuilder):
    """NCSLGR: a small American Sign Language corpus annotated with non-manual features"""

    VERSION = datasets.Version("0.7.0")

    BUILDER_CONFIGS = [
        NCSLGRConfig(
            name="entire_dataset",
            version=datasets.Version("0.7.0"),
            description="Entire dataset containing both videos and annotations.",
            videos=True,
        ),
        NCSLGRConfig(
            name="annotations",
            version=datasets.Version("0.7.0"),
            description="Dataset including only annotations, without videos",
            videos=False,
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "eaf": datasets.Value("string"),  # EAF path
                    "videos": datasets.features.Sequence(datasets.Value("string")),  # Videos paths
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        eaf_path = os.path.join(dl_manager.download_and_extract(_URL_ANNOTATIONS), "elanBUcorpus")
        videos_path = dl_manager.download_and_extract(_URL_VIDEOS) if self.config.videos else None

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"eaf_path": eaf_path, "videos_path": videos_path, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"eaf_path": eaf_path, "videos_path": videos_path, "split": "dev"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"eaf_path": eaf_path, "videos_path": videos_path, "split": "test"},
            ),
        ]

    def _generate_examples(self, eaf_path: str, videos_path: str, split: str):
        """ Yields examples. """

        for i, eaf_file in enumerate(tqdm(os.listdir(eaf_path))):
            eaf_file_path = os.path.join(eaf_path, eaf_file)
            videos = []
            if self.config.videos:
                with open(eaf_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    videos_relative = re.findall('RELATIVE_MEDIA_URL="(.*)"', content)
                    videos = [os.path.join(videos_path, v[3:]) for v in videos_relative]

            if (i % 7 == 0 and split == "test") or (i % 7 == 1 and split == "dev") or (i % 7 > 1 and split == "train"):
                yield i, {"eaf": eaf_file_path, "videos": videos}
