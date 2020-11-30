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
"""CVIT IIIT-H PIB Multilingual Corpus"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@InProceedings{cvit-pib:multilingual-corpus,
title = {Revisiting Low Resource Status of Indian Languages in Machine Translation},
authors={Jerin Philip, Shashank Siripragada, Vinay P. Namboodiri, C.V. Jawahar
},
year={2020}
}
"""

_DESCRIPTION = """\
This new dataset is the large scale sentence aligned corpus in 11 Indian languages, 
viz. CVIT-PIB corpus that is the largest multilingual corpus available for Indian languages.
"""

_URL = "http://preon.iiit.ac.in/~jerin/resources/datasets/pib-v0.tar"

_LanguagePairs = [
    "or-ur",
    "ml-or",
    "bn-ta",
    "gu-mr",
    "hi-or",
    "en-or",
    "mr-ur",
    "en-ta",
    "hi-ta",
    "bn-en",
    "bn-or",
    "ml-ta",
    "gu-ur",
    "bn-ml",
    "ml-pa",
    "en-pa",
    "bn-hi",
    "hi-pa",
    "gu-te",
    "pa-ta",
    "hi-ml",
    "or-te",
    "en-ml",
    "en-hi",
    "bn-pa",
    "mr-te",
    "mr-pa",
    "bn-te",
    "gu-hi",
    "ta-ur",
    "te-ur",
    "or-pa",
    "gu-ml",
    "gu-pa",
    "hi-te",
    "en-te",
    "ml-te",
    "pa-ur",
    "hi-ur",
    "mr-or",
    "en-ur",
    "ml-ur",
    "bn-mr",
    "gu-ta",
    "pa-te",
    "bn-gu",
    "bn-ur",
    "ml-mr",
    "or-ta",
    "ta-te",
    "gu-or",
    "en-gu",
    "hi-mr",
    "mr-ta",
    "en-mr",
]


class PibConfig(datasets.BuilderConfig):
    """BuilderConfig for PIB"""

    def __init__(self, language_pair, **kwargs):
        super().__init__(**kwargs)
        """

        Args:
            language_pair: language pair, you want to load
            **kwargs: keyword arguments forwarded to super.
        """
        self.language_pair = language_pair


class Pib(datasets.GeneratorBasedBuilder):
    """This new dataset is the large scale sentence aligned corpus in 11 Indian languages, viz.
    CVIT-PIB corpus that is the largest multilingual corpus available for Indian languages.
    """

    BUILDER_CONFIG_CLASS = PibConfig
    BUILDER_CONFIGS = [PibConfig(name=pair, description=_DESCRIPTION, language_pair=pair) for pair in _LanguagePairs]

    def _info(self):
        # TODO: Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION + f" Available language pairs are {_LanguagePairs}",
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "src_lang": datasets.Value("string"),
                    "tgt_lang": datasets.Value("string")
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="http://preon.iiit.ac.in/~jerin/bhasha/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)
        src, tgt = self.config.language_pair.split("-")
        data_dir = os.path.join(dl_dir, f"pib/{src}-{tgt}")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"train.{src}"),
                    "labelpath": os.path.join(data_dir, f"train.{tgt}"),
                },
            ),
        ]

    def _generate_examples(self, filepath, labelpath):
        """ Yields examples. """
        with open(filepath) as f1, open(labelpath) as f2:
            src = f1.read().split("\n")[:-1]
            tgt = f2.read().split("\n")[:-1]
            for idx, (s, t) in enumerate(zip(src, tgt)):
                yield idx, {
                    "src_lang": s,
                    "tgt_lang": t,
                }
