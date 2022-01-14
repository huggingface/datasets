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
"""CVIT PIB Multilingual Corpus"""

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

_HOMEPAGE = "http://preon.iiit.ac.in/~jerin/bhasha/"

_LICENSE = "Creative Commons Attribution-ShareAlike 4.0 International"

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
                {"translation": datasets.features.Translation(languages=[self.config.src, self.config.tgt])}
            ),
            supervised_keys=(self.config.src, self.config.tgt),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_URL[str(self.config.version)])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "archive": dl_manager.iter_archive(archive),
                },
            ),
        ]

    def _generate_examples(self, archive):
        root_dir = _ROOT_DIR[str(self.config.version)]
        data_dir = f"{root_dir}/{self.config.src}-{self.config.tgt}"
        src = tgt = None
        for path, file in archive:
            if data_dir in path:
                if f"{data_dir}/train.{self.config.src}" in path:
                    src = file.read().decode("utf-8").split("\n")[:-1]
                if f"{data_dir}/train.{self.config.tgt}" in path:
                    tgt = file.read().decode("utf-8").split("\n")[:-1]
            if src and tgt:
                break
        for idx, (s, t) in enumerate(zip(src, tgt)):
            yield idx, {"translation": {self.config.src: s, self.config.tgt: t}}
