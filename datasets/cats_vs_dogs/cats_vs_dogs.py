# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""The Microsoft Cats vs. Dogs dataset"""

from pathlib import Path
from typing import List

import datasets
from datasets.tasks import ImageClassification


logger = datasets.logging.get_logger(__name__)

_URL = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip"

_HOMEPAGE = "https://www.microsoft.com/en-us/download/details.aspx?id=54765"

_DESCRIPTION = "A large set of images of cats and dogs. There are 1738 corrupted images that are dropped."

_CITATION = """\
@Inproceedings (Conference){asirra-a-captcha-that-exploits-interest-aligned-manual-image-categorization,
    author = {Elson, Jeremy and Douceur, John (JD) and Howell, Jon and Saul, Jared},
    title = {Asirra: A CAPTCHA that Exploits Interest-Aligned Manual Image Categorization},
    booktitle = {Proceedings of 14th ACM Conference on Computer and Communications Security (CCS)},
    year = {2007},
    month = {October},
    publisher = {Association for Computing Machinery, Inc.},
    url = {https://www.microsoft.com/en-us/research/publication/asirra-a-captcha-that-exploits-interest-aligned-manual-image-categorization/},
    edition = {Proceedings of 14th ACM Conference on Computer and Communications Security (CCS)},
}
"""


class CatsVsDogs(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image_file_path": datasets.Value("string"),
                    "labels": datasets.features.ClassLabel(names=["cat", "dog"]),
                }
            ),
            supervised_keys=("image_file_path", "labels"),
            task_templates=[
                ImageClassification(
                    image_file_path_column="image_file_path", label_column="labels", labels=["cat", "dog"]
                )
            ],
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        images_path = Path(dl_manager.download_and_extract(_URL)) / "PetImages"
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"images_path": images_path}),
        ]

    def _generate_examples(self, images_path):
        logger.info("generating examples from = %s", images_path)
        for i, filepath in enumerate(images_path.glob("**/*.jpg")):
            with filepath.open("rb") as f:
                if b"JFIF" in f.peek(10):
                    yield str(i), {
                        "image_file_path": str(filepath),
                        "labels": filepath.parent.name.lower(),
                    }
                    continue
