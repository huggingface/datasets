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
"""ASLG-PC12: Synthetic English-ASL Gloss Parallel Corpus 2012"""

from __future__ import absolute_import, division, print_function

import datasets


_DESCRIPTION = """\
A large synthetic collection of parallel English and ASL-Gloss texts.
There are two string features: text, and gloss.
"""

_CITATION = """\
@inproceedings{othman2012english,
  title={English-asl gloss parallel corpus 2012: Aslg-pc12},
  author={Othman, Achraf and Jemni, Mohamed},
  booktitle={5th Workshop on the Representation and Processing of Sign Languages: Interactions between Corpus and Lexicon LREC},
  year={2012}
}
"""

_GLOSS_URL = "https://www.achrafothman.net/aslsmt/corpus/sample-corpus-asl-en.asl"
_TEXT_URL = "https://www.achrafothman.net/aslsmt/corpus/sample-corpus-asl-en.en"

_HOMEPAGE = "https://achrafothman.net/site/asl-smt/"


class ASLGPC12(datasets.GeneratorBasedBuilder):
    """ASLG-PC12: Synthetic English-ASL Gloss Parallel Corpus 2012"""

    VERSION = datasets.Version("0.0.1")  # sample corpus

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "gloss": datasets.Value("string"),  # American sign language gloss
                    "text": datasets.Value("string"),  # English text
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        gloss_path, text_path = dl_manager.download([_GLOSS_URL, _TEXT_URL])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"gloss_path": gloss_path, "text_path": text_path},
            )
        ]

    def _generate_examples(self, gloss_path, text_path):
        """ Yields examples. """

        gloss_f = open(gloss_path, "r", encoding="utf-8")
        text_f = open(text_path, "r", encoding="utf-8")

        for i, (gloss, text) in enumerate(zip(gloss_f, text_f)):
            yield i, {"gloss": gloss, "text": text}

        gloss_f.close()
        text_f.close()
