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
"""Answer-Sentence Natural Questions (ASNQ)

ASNQ is a dataset for answer sentence selection derived from Google Natural Questions (NQ)
dataset (Kwiatkowski et al. 2019). The dataset details can be found in the paper at
https://arxiv.org/abs/1911.04118

ASNQ is used to transfer the pre-trained models in the paper and can be downloaded at
https://wqa-public.s3.amazonaws.com/tanda-aaai-2020/data/asnq.tar
"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@article{garg2019tanda,
    title={TANDA: Transfer and Adapt Pre-Trained Transformer Models for Answer Sentence Selection},
    author={Siddhant Garg and Thuy Vu and Alessandro Moschitti},
    year={2019},
    eprint={1911.04118},
}
"""

_DESCRIPTION = """\
ASNQ is a dataset for answer sentence selection derived from
Google Natural Questions (NQ) dataset (Kwiatkowski et al. 2019).
"""

_URL = "https://wqa-public.s3.amazonaws.com/tanda-aaai-2020/data/asnq.tar"


class ASNQ(datasets.GeneratorBasedBuilder):
    """ASNQ is a dataset for answer sentence selection derived
    ASNQ is a dataset for answer sentence selection derived from
    Google Natural Questions (NQ) dataset (Kwiatkowski et al. 2019).

    The dataset details can be found in the `paper <https://arxiv.org/abs/1911.04118>`.
    """

    VERSION = datasets.Version("1.0.0")

    def _info(self):

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "sentence1": datasets.Value("string"),
                    "sentence2": datasets.Value("string"),
                    "label": datasets.Value("int32"),
                }
            ),
            # No default supervised_keys
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/alexa/wqa_tanda#answer-sentence-natural-questions-asnq",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "data", "asnq")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.tsv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.tsv"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as tsvfile:
            tsvreader = csv.reader(tsvfile, delimiter="\t")
            for id_, row in enumerate(tsvreader):
                sentence1, sentence2, label = row
                yield id_, {"sentence1": sentence1, "sentence2": sentence2, "label": label}
