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
"""Mann Ki Baat (mkb) Corpus"""


import os

import datasets


_CITATION = """\
@misc{siripragada2020multilingual,
      title={A Multilingual Parallel Corpora Collection Effort for Indian Languages},
      author={Shashank Siripragada and Jerin Philip and Vinay P. Namboodiri and C V Jawahar},
      year={2020},
      eprint={2007.07691},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
The Prime Minister's speeches - Mann Ki Baat, on All India Radio, translated into many languages.
"""

_URL = "http://preon.iiit.ac.in/~jerin/resources/datasets/mkb-v0.tar"

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
    "bn-hi",
    "gu-te",
    "hi-ml",
    "or-te",
    "en-ml",
    "en-hi",
    "mr-te",
    "bn-te",
    "gu-hi",
    "ta-ur",
    "te-ur",
    "gu-ml",
    "hi-te",
    "en-te",
    "ml-te",
    "hi-ur",
    "mr-or",
    "en-ur",
    "ml-ur",
    "bn-mr",
    "gu-ta",
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


class MkbConfig(datasets.BuilderConfig):
    """BuilderConfig for Mkb"""

    def __init__(self, language_pair, **kwargs):
        super().__init__(**kwargs)
        """

        Args:
            language_pair: language pair, you want to load
            **kwargs: keyword arguments forwarded to super.
        """
        self.language_pair = language_pair


class Mkb(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("0.0.0")

    BUILDER_CONFIG_CLASS = MkbConfig
    BUILDER_CONFIGS = [MkbConfig(name=pair, description=_DESCRIPTION, language_pair=pair) for pair in _LanguagePairs]

    def _info(self):
        src_tag, tgt_tag = self.config.language_pair.split("-")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=(src_tag, tgt_tag))}),
            supervised_keys=(src_tag, tgt_tag),
            homepage="http://preon.iiit.ac.in/~jerin/resources/datasets/mkb-v0.tar",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        lang_pair = self.config.language_pair
        src_tag, tgt_tag = lang_pair.split("-")

        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "mkb", lang_pair)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, f"mkb.{src_tag}"),
                    "labelpath": os.path.join(data_dir, f"mkb.{tgt_tag}"),
                },
            )
        ]

    def _generate_examples(self, filepath, labelpath):
        """Yields examples."""
        src_tag, tgt_tag = self.config.language_pair.split("-")
        with open(filepath, encoding="utf-8") as f1, open(labelpath, encoding="utf-8") as f2:
            src = f1.read().split("\n")[:-1]
            tgt = f2.read().split("\n")[:-1]
            for idx, (s, t) in enumerate(zip(src, tgt)):
                yield idx, {"translation": {src_tag: s, tgt_tag: t}}
