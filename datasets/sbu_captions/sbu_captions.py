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
"""SBU Captioned Photo Dataset"""

import json

import datasets


_CITATION = """\
@inproceedings{NIPS2011_5dd9db5e,
 author = {Ordonez, Vicente and Kulkarni, Girish and Berg, Tamara},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {J. Shawe-Taylor and R. Zemel and P. Bartlett and F. Pereira and K.Q. Weinberger},
 pages = {},
 publisher = {Curran Associates, Inc.},
 title = {Im2Text: Describing Images Using 1 Million Captioned Photographs},
 url = {https://proceedings.neurips.cc/paper/2011/file/5dd9db5e033da9c6fb5ba83c7a7ebea9-Paper.pdf},
 volume = {24},
 year = {2011}
}
"""

_DESCRIPTION = """\
The SBU Captioned Photo Dataset is a collection of over 1 million images with associated text descriptions extracted from Flicker.
"""

_LICENSE = "unknown"

_HOMEPAGE = "http://www.cs.virginia.edu/~vicente/sbucaptions"

_URL = "http://www.cs.virginia.edu/~vicente/sbucaptions/sbu-captions-all.tar.gz"

_FEATURES = datasets.Features(
    {
        "image_url": datasets.Value("string"),
        "user_id": datasets.Value("string"),
        "caption": datasets.Value("string")
    }
)

_MAP_SBU_FEATURES_TO_DATASETS_FEATURES = {
    "image_urls": "image_url",
    "user_ids": "user_id",
    "captions": "caption"
}

class SBUCaptionedPhotoDatasetConfig(datasets.BuilderConfig):
    """BuilderConfig for COCO."""

    VERSION = datasets.Version("0.0.0")

    def __init__(self, version=None, *args, **kwargs):
        super().__init__(
            version=version or self.VERSION,
            *args,
            **kwargs,
        )


class SBUCaptionedPhotoDataset(datasets.GeneratorBasedBuilder):
    """SBU Captioned Photo dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=_FEATURES,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        # Download and extract `sbu-captions-all.tar.gz` file
        annotations_file = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annotations_file": f"{annotations_file}/sbu-captions-all.json",
                }
            )
        ]

    def _generate_examples(self, annotations_file):
        # Download all images
        with open(annotations_file, "r") as fi:
            annotations = json.load(fi)

        # Sanity check
        nb_samples = len(annotations[next(iter(annotations.keys()))])
        assert all(len(values) == nb_samples for values in annotations.values())
        keys = tuple(annotations.keys())

        for idx in range(nb_samples):
            yield idx, {
                _MAP_SBU_FEATURES_TO_DATASETS_FEATURES[key]: annotations[key][idx]
                for key in keys
            }
