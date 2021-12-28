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


import os

import datasets


_CITATION = """\
@inproceedings{siripragada-etal-2020-multilingual,
    title = "A Multilingual Parallel Corpora Collection Effort for {I}ndian Languages",
    author = "Siripragada, Shashank  and
      Philip, Jerin  and
      Namboodiri, Vinay P.  and
      Jawahar, C V",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://aclanthology.org/2020.lrec-1.462",
    pages = "3743--3751",
    abstract = "We present sentence aligned parallel corpora across 10 Indian Languages - Hindi, Telugu, Tamil, Malayalam, Gujarati, Urdu, Bengali, Oriya, Marathi, Punjabi, and English - many of which are categorized as low resource. The corpora are compiled from online sources which have content shared across languages. The corpora presented significantly extends present resources that are either not large enough or are restricted to a specific domain (such as health). We also provide a separate test corpus compiled from an independent online source that can be independently used for validating the performance in 10 Indian languages. Alongside, we report on the methods of constructing such corpora using tools enabled by recent advances in machine translation and cross-lingual retrieval using deep neural network based methods.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
@article{2020,
   title={Revisiting Low Resource Status of Indian Languages in Machine Translation},
   url={http://dx.doi.org/10.1145/3430984.3431026},
   DOI={10.1145/3430984.3431026},
   journal={8th ACM IKDD CODS and 26th COMAD},
   publisher={ACM},
   author={Philip, Jerin and Siripragada, Shashank and Namboodiri, Vinay P. and Jawahar, C. V.},
   year={2020},
   month={Dec}
}
"""

_DESCRIPTION = """\
Sentence aligned parallel corpus between 11 Indian Languages, crawled and extracted from the press information bureau
website.
"""

_URL = {
    "0.0.0": "http://preon.iiit.ac.in/~jerin/resources/datasets/pib-v0.tar",
    "1.3.0": "http://preon.iiit.ac.in/~jerin/resources/datasets/pib_v1.3.tar.gz",
}
_ROOT_DIR = {
    "0.0.0": "pib",
    "1.3.0": "pib-v1.3",
}

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

    def __init__(self, language_pair, version=datasets.Version("1.3.0"), **kwargs):
        super().__init__(version=version, **kwargs)
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
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f1, open(labelpath, encoding="utf-8") as f2:
            src = f1.read().split("\n")[:-1]
            tgt = f2.read().split("\n")[:-1]
            for idx, (s, t) in enumerate(zip(src, tgt)):
                yield idx, {"translation": {self.config.src: s, self.config.tgt: t}}
