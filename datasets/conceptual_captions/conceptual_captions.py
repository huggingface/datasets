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
import os

import datasets


_DESCRIPTION = """\
Image captioning dataset
The resulting dataset (version 1.1) has been split into Training, Validation, and Test splits. The Training split consists of 3,318,333 image-URL/caption pairs, with a total number of 51,201 total token types in the captions (i.e., total vocabulary). The average number of tokens per captions is 10.3 (standard deviation of 4.5), while the median is 9.0 tokens per caption. The Validation split consists of 15,840 image-URL/caption pairs, with similar statistics.
"""
_HOMEPAGE_URL = "http://data.statmt.org/cc-100/"
_CITATION = """\
@inproceedings{sharma-etal-2018-conceptual,
    title = "Conceptual Captions: A Cleaned, Hypernymed, Image Alt-text Dataset For Automatic Image Captioning",
    author = "Sharma, Piyush  and
      Ding, Nan  and
      Goodman, Sebastian  and
      Soricut, Radu",
    booktitle = "Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = jul,
    year = "2018",
    address = "Melbourne, Australia",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P18-1238",
    doi = "10.18653/v1/P18-1238",
    pages = "2556--2565",
    abstract = "We present a new dataset of image caption annotations, Conceptual Captions, which contains an order of magnitude more images than the MS-COCO dataset (Lin et al., 2014) and represents a wider variety of both images and image caption styles. We achieve this by extracting and filtering image caption annotations from billions of webpages. We also present quantitative evaluations of a number of image captioning models and show that a model architecture based on Inception-ResNetv2 (Szegedy et al., 2016) for image-feature extraction and Transformer (Vaswani et al., 2017) for sequence modeling achieves the best performance when trained on the Conceptual Captions dataset.",
}
"""

_VERSION = "1.1.0"
_TRAIN_FILENAME = "Train_GCC-training.tsv"
_VALID_FILENAME = "Validation_GCC-1.1.0-Validation.tsv"


class ConceptualCaptions(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version(_VERSION)

    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://ai.google.com/research/ConceptualCaptions/download,
    and manually download the dataset. Once it is completed,
    two files named Train_GCC-training.tsv and Validation_GCC-1.1.0-Validation.tsv
    will appear in your Downloads folder or whichever folder your browser chooses to save files to.
    You then have to move these files under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    conceptual_captions can then be loaded using the following command
    `datasets.load_dataset("conceptual_captions", data_dir="<path/to/folder>")`.
    """

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "caption": datasets.Value("string"),
                    "url": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "datapath": os.path.join(path_to_manual_file, _TRAIN_FILENAME)
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "datapath": os.path.join(path_to_manual_file, _VALID_FILENAME)
                },
            ),
        ]

    def _generate_examples(self, datapath):
        sentence_counter = 0
        with open(datapath, encoding="utf-8") as f:
            for row in f:
                caption, url = row.split("\t")
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "caption": caption,
                        "url": url,
                    },
                )
                sentence_counter += 1
                yield result
