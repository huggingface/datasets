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
"""PASS dataset."""

import os
from datetime import datetime

import numpy as np
import pandas as pd

import datasets


_DESCRIPTION = """\
PASS (Pictures without humAns for Self-Supervision) is a large-scale dataset of 1,440,191 images that does not include any humans
and which can be used for high-quality pretraining while significantly reducing privacy concerns.
The PASS images are sourced from the YFCC-100M dataset.
"""

_CITATION = """\
@Article{asano21pass,
author = "Yuki M. Asano and Christian Rupprecht and Andrew Zisserman and Andrea Vedaldi",
title = "PASS: An ImageNet replacement for self-supervised pretraining without humans",
journal = "NeurIPS Track on Datasets and Benchmarks",
year = "2021"
}
"""

_HOMEPAGE = "https://www.robots.ox.ac.uk/~vgg/research/pass/"

_LICENSE = "Creative Commons Attribution 4.0 International"

_IMAGE_ARCHIVE_DOWNLOAD_URL_TEMPLATE = "https://zenodo.org/record/5570664/files/PASS.{idx}.tar?download=1"

_METADATA_DOWNLOAD_URL = "https://zenodo.org/record/5570664/files/pass_metadata.csv?download=1"


class PASS(datasets.GeneratorBasedBuilder):
    """PASS dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "creator_username": datasets.Value("string"),
                    "hash": datasets.Value("string"),
                    "gps_latitude": datasets.Value("float32"),
                    "gps_longitude": datasets.Value("float32"),
                    "date_taken": datasets.Value("timestamp[us]"),
                }
            ),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        metadata_file, *image_dirs = dl_manager.download(
            [_METADATA_DOWNLOAD_URL] + [_IMAGE_ARCHIVE_DOWNLOAD_URL_TEMPLATE.format(idx=i) for i in range(10)]
        )
        metadata = pd.read_csv(metadata_file, encoding="utf-8")
        metadata = metadata.replace(np.NaN, pd.NA).where(metadata.notnull(), None)
        metadata = metadata.set_index("hash")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "metadata": metadata,
                    "image_archives": [dl_manager.iter_archive(image_dir) for image_dir in image_dirs],
                },
            )
        ]

    def _generate_examples(self, metadata, image_archives):
        """Yields examples."""
        for image_archive in image_archives:
            for path, file in image_archive:
                img_hash = os.path.basename(path).split(".")[0]
                img_meta = metadata.loc[img_hash]
                yield img_hash, {
                    "image": {"path": path, "bytes": file.read()},
                    "creator_username": img_meta["unickname"],
                    "hash": img_hash,
                    "gps_latitude": img_meta["latitude"],
                    "gps_longitude": img_meta["longitude"],
                    "date_taken": datetime.strptime(img_meta["datetaken"], "%Y-%m-%d %H:%M:%S.%f")
                    if img_meta["datetaken"] is not None
                    else None,
                }
