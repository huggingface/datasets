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
"""Conceptual 12M dataset."""

import datasets


_CITATION = """\
@inproceedings{changpinyo2021cc12m,
  title = {{Conceptual 12M}: Pushing Web-Scale Image-Text Pre-Training To Recognize Long-Tail Visual Concepts},
  author = {Changpinyo, Soravit and Sharma, Piyush and Ding, Nan and Soricut, Radu},
  booktitle = {CVPR},
  year = {2021},
}
"""

_DESCRIPTION = """\
Conceptual 12M is a large-scale dataset of 12 million
image-text pairs specifically meant to be used for visionand-language pre-training.
Its data collection pipeline is a relaxed version of the one used in Conceptual Captions 3M.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/conceptual-12m"

_LICENSE = """\
The dataset may be freely used for any purpose, although acknowledgement of
Google LLC ("Google") as the data source would be appreciated. The dataset is
provided "AS IS" without any warranty, express or implied. Google disclaims all
liability for any damages, direct or indirect, resulting from the use of the
dataset.
"""

_URL = "https://storage.googleapis.com/conceptual_12m/cc12m.tsv"


class Conceptual12M(datasets.GeneratorBasedBuilder):
    """Conceptual 12M dataset."""

    def _info(self):
        features = datasets.Features({"image_url": datasets.Value("string"), "caption": datasets.Value("string")})

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        file = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "file": file,
                },
            ),
        ]

    def _generate_examples(self, file):
        with open(file, "r", encoding="utf-8") as fi:
            for idx, line in enumerate(fi):
                image_url, caption = line.split("\t", maxsplit=1)
                yield idx, {"image_url": image_url, "caption": caption}
