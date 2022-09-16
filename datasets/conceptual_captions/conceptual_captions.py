# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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

# Lint as: python3
"""Conceptual Captions dataset."""

import csv
import textwrap

import datasets


_DESCRIPTION = """\
Google's Conceptual Captions dataset has more than 3 million images, paired with natural-language captions.
In contrast with the curated style of the MS-COCO images, Conceptual Captions images and their raw descriptions are harvested from the web,
and therefore represent a wider variety of styles. The raw descriptions are harvested from the Alt-text HTML attribute associated with web images.
The authors developed an automatic pipeline that extracts, filters, and transforms candidate image/caption pairs, with the goal of achieving a balance of cleanliness,
informativeness, fluency, and learnability of the resulting captions.
"""

_HOMEPAGE = "http://data.statmt.org/cc-100/"

_LICENSE = """\
The dataset may be freely used for any purpose, although acknowledgement of
Google LLC ("Google") as the data source would be appreciated. The dataset is
provided "AS IS" without any warranty, express or implied. Google disclaims all
liability for any damages, direct or indirect, resulting from the use of the
dataset.
"""

_CITATION = """\
@inproceedings{sharma2018conceptual,
  title = {Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning},
  author = {Sharma, Piyush and Ding, Nan and Goodman, Sebastian and Soricut, Radu},
  booktitle = {Proceedings of ACL},
  year = {2018},
}
"""

_URLS = {
    "unlabeled": {
        "train": "https://storage.googleapis.com/gcc-data/Train/GCC-training.tsv?_ga=2.191230122.-1896153081.1529438250",
        "validation": "https://storage.googleapis.com/gcc-data/Validation/GCC-1.1.0-Validation.tsv?_ga=2.141047602.-1896153081.1529438250",
    },
    "labeled": {
        "train": "https://storage.googleapis.com/conceptual-captions-v1-1-labels/Image_Labels_Subset_Train_GCC-Labels-training.tsv?_ga=2.234395421.-20118413.1607637118",
    },
}

_DESCRIPTIONS = {
    "unlabeled": textwrap.dedent(
        """\
        The basic version of the dataset split into Training, Validation, and Test splits.
        The Training split consists of 3,318,333 image-URL/caption pairs, with a total number of 51,201 total token types in the captions (i.e., total vocabulary).
        The average number of tokens per captions is 10.3 (standard deviation of 4.5), while the median is 9.0 tokens per caption.
        The Validation split consists of 15,840 image-URL/caption pairs, with similar statistics.
        """
    ),
    "labeled": textwrap.dedent(
        """\
        A subset of 2,007,090 image-URL/caption pairs from the training set with machine-generated image labels.
        The image labels are obtained using the Google Cloud Vision API.
        Each image label has a machine-generated identifier (MID) corresponding to the label's Google Knowledge Graph entry and a confidence score for its presence in the image.

        Note: 2,007,528 is the number of image-URL/caption pairs specified by the authors, but some rows are missing labels, so they are not included.
        """
    ),
}


class ConceptualCaptions(datasets.GeneratorBasedBuilder):
    """Builder for Conceptual Captions dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig("unlabeled", version=VERSION, description=_DESCRIPTIONS["unlabeled"]),
        datasets.BuilderConfig("labeled", version=VERSION, description=_DESCRIPTIONS["labeled"]),
    ]

    DEFAULT_CONFIG_NAME = "unlabeled"

    def _info(self):
        features = datasets.Features(
            {
                "image_url": datasets.Value("string"),
                "caption": datasets.Value("string"),
            },
        )
        if self.config.name == "labeled":
            features.update(
                {
                    "labels": datasets.Sequence(datasets.Value("string")),
                    "MIDs": datasets.Sequence(datasets.Value("string")),
                    "confidence_scores": datasets.Sequence(datasets.Value("float64")),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_data = dl_manager.download(_URLS[self.config.name])
        splits = [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"annotations_file": downloaded_data["train"]},
            ),
        ]
        if self.config.name == "unlabeled":
            splits += [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={"annotations_file": downloaded_data["validation"]},
                ),
            ]
        return splits

    def _generate_examples(self, annotations_file):
        if self.config.name == "unlabeled":
            with open(annotations_file, encoding="utf-8") as f:
                for i, row in enumerate(csv.reader(f, delimiter="\t")):
                    # Sanity check
                    assert len(row) == 2
                    caption, image_url = row
                    yield i, {
                        "image_url": image_url,
                        "caption": caption,
                    },
        else:
            with open(annotations_file, encoding="utf-8") as f:
                for i, row in enumerate(csv.reader(f, delimiter="\t")):
                    caption, image_url, labels, MIDs, confidence_scores = row
                    if not labels:
                        continue
                    yield i, {
                        "image_url": image_url,
                        "caption": caption,
                        "labels": labels.split(","),
                        "MIDs": MIDs.split(","),
                        "confidence_scores": [float(x) for x in confidence_scores.split(",")],
                    },
