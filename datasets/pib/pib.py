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
        self.src, self.tgt = language_pair.split("-")


class Pib(datasets.GeneratorBasedBuilder):
    """This new dataset is the large scale sentence aligned corpus in 11 Indian languages, viz.
    CVIT-PIB corpus that is the largest multilingual corpus available for Indian languages.
    """

    BUILDER_CONFIG_CLASS = PibConfig
    BUILDER_CONFIGS = [PibConfig(name=pair, description=_DESCRIPTION, language_pair=pair) for pair in _LanguagePairs]

    def _info(self):
        # TODO: Specifies the datasets.DatasetInfo object
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=(self.config.src, self.config.tgt))}
            ),
            supervised_keys=(self.config.src, self.config.tgt),
            homepage="http://preon.iiit.ac.in/~jerin/bhasha/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_URL)

        data_dir = os.path.join(dl_dir, f"pib/{self.config.src}-{self.config.tgt}")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"train.{self.config.src}"),
                    "labelpath": os.path.join(data_dir, f"train.{self.config.tgt}"),
                },
            ),
        ]

    def _generate_examples(self, filepath, labelpath):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f1, open(labelpath, encoding="utf-8") as f2:
            src = f1.read().split("\n")[:-1]
            tgt = f2.read().split("\n")[:-1]
            for idx, (s, t) in enumerate(zip(src, tgt)):
                yield idx, {"translation": {self.config.src: s, self.config.tgt: t}}
