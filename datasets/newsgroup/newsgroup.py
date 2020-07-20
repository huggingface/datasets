# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""20Newsgroup  dataset"""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


_CITATION = """
@inproceedings{Lang95,
    author = {Ken Lang},
    title = {Newsweeder: Learning to filter netnews}
    year = {1995}
    booktitle = {Proceedings of the Twelfth International Conference on Machine Learning}
    pages = {331-339}
    }
 """

_DESCRIPTION = """
The 20 Newsgroups data set is a collection of approximately 20,000 newsgroup documents, partitioned (nearly) evenly across 
20 different newsgroups. The 20 newsgroups collection has become a popular data set for experiments in text applications of 
machine learning techniques, such as text classification and text clustering.
"""

_DOWNLOAD_URL = {
    "bydate": "http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz",
    "19997": "http://qwone.com/~jason/20Newsgroups/20news-19997.tar.gz",
    "18828": "http://qwone.com/~jason/20Newsgroups/20news-18828.tar.gz",
}
_NEWS_GROUPS = [
    "comp.graphics",
    "comp.os.ms-windows.misc",
    "comp.sys.ibm.pc.hardware",
    "comp.sys.mac.hardware",
    "comp.windows.x",
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey",
    "sci.crypt",
    "sci.electronics",
    "sci.med",
    "sci.space",
    "misc.forsale",
    "talk.politics.misc",
    "talk.politics.guns",
    "talk.politics.mideast",
    "talk.religion.misc",
    "alt.atheism",
    "soc.religion.christian",
]
_VERSIONS = {"19997": "1.0.0", "bydate": "2.0.0", "18828": "3.0.0"}

_DESC = {
    "19997": "the original, unmodified version.",
    "bydate": "sorted by date into training(60%) and test(40%) sets, does not include cross-posts (duplicates) and does not include newsgroup-identifying headers (Xref, Newsgroups, Path, Followup-To, Date)",
    "18828": 'does not include cross-posts and includes only the "From" and "Subject" headers.',
}
_CONFIG_NAMES = []
for version in _VERSIONS:
    for group in _NEWS_GROUPS:
        _CONFIG_NAMES.append(version + "_" + group)

_CONFIG_NAMES = sorted(_CONFIG_NAMES)


class NewsgroupConfig(nlp.BuilderConfig):
    """BuilderConfig for 20Newsgroup."""

    def __init__(self, sub_dir, **kwargs):
        """Constructs a 20Newsgroup.

        Args:
        sub_dirs: str
        **kwargs: keyword arguments forwarded to super.
        """

        super(NewsgroupConfig, self).__init__(**kwargs)
        self.sub_dir = sub_dir


class Newsgroups(nlp.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        NewsgroupConfig(
            name=name,
            description=_DESC[name.split("_")[0]],
            sub_dir=name.split("_")[1],
            version=nlp.Version(_VERSIONS[name.split("_")[0]]),
        )
        for name in _CONFIG_NAMES
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=nlp.Features({"text": nlp.Value("string"),}),
            homepage="http://qwone.com/~jason/20Newsgroups/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        url = _DOWNLOAD_URL[self.config.name.split("_")[0]]
        path = dl_manager.download_and_extract(url)
        if self.config.name.startswith("bydate"):

            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    gen_kwargs={"files_path": os.path.join(path, "20news-bydate-train", self.config.sub_dir)},
                ),
                nlp.SplitGenerator(
                    name=nlp.Split.TEST,
                    gen_kwargs={"files_path": os.path.join(path, "20news-bydate-train", self.config.sub_dir)},
                ),
            ]
        elif self.config.name.startswith("19997"):
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    gen_kwargs={"files_path": os.path.join(path, "20_newsgroups", self.config.sub_dir)},
                )
            ]
        else:
            return [
                nlp.SplitGenerator(
                    name=nlp.Split.TRAIN,
                    gen_kwargs={"files_path": os.path.join(path, "20news-18828", self.config.sub_dir)},
                )
            ]

    def _generate_examples(self, files_path):
        """Yields examples."""
        files = sorted(os.listdir(files_path))
        for id_, file in enumerate(files):
            filepath = os.path.join(files_path, file)
            with open(
                filepath, encoding="utf8", errors="ignore"
            ) as f:  # here we can ignore byte encoded tokens. we only have a very few and in most case it happens at the end of the file (kind of \FF)
                text = f.read()
                yield id_, {"text": text}
