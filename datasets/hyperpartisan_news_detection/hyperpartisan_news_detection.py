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
"""Hyperparisan News Detection"""

from __future__ import absolute_import, division, print_function

import os
import xml.etree.ElementTree as ET

import nlp


_CITATION = """
"""

_DESCRIPTION = """
Hyperparisan News Detection was a dataset created for PAN @ SemEval 2019 Task 4: Hyperparisan News Detection.
Given a news article text, decide whether it follows a hyperpartisan argumentation, i.e., whether it exhibits blind, prejudiced, or unreasoning allegiance to one party, faction, cause, or person.

There are 2 datasets:
- By article: Labeled through crowdsourcing on an article basis. The data contains only articles for which a consensus among the crowdsourcing workers existed.
- By Publisher: Labeled by the overall bias of the publisher as provided by BuzzFeed journalists or MediaBiasFactCheck.com.

Access to the dataset needs to be requested.
"""


class HyperpartisanNewsDetection(nlp.GeneratorBasedBuilder):
    """Hyperparisan News Detection Dataset."""

    VERSION = nlp.Version("1.0.0")

    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from https://zenodo.org/record/1489920
  The dataset needs requesting.

  Download each file, extract it and place in a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dirs/hyperpartisan_news_detection`
  Hyperparisan News Detection can then be loaded via:
  `nlp.load_dataset("hyperpartisan_news_detection", data_dir="~/.manual_dirs/hyperpartisan_news_detection")`.
  """

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({
                "text": nlp.Value("string"),
                "title": nlp.Value("string"),
                "hyperpartisan": nlp.Value("bool"),
                "bias": nlp.ClassLabel(names=["right","right-center","least","left-center","left"]),
                "url": nlp.Value("string"),
                "published_at": nlp.Value("string"),
            }),
            supervised_keys=("text","label"),
            homepage="https://pan.webis.de/semeval19/semeval19-web/",
            #citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `nlp.load_dataset('hyperpartisan_news_detection', data_dir=...)` that includes files unzipped from the zenodo page. Manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, gen_kwargs={
                    "articles_file": os.path.join(data_dir, "articles-training-bypublisher-20181122.xml"),
                    "labels_file": os.path.join(data_dir, "ground-truth-training-bypublisher-20181122.xml")
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={
                    "articles_file": os.path.join(data_dir, "articles-validation-bypublisher-20181122.xml"),
                    "labels_file": os.path.join(data_dir, "ground-truth-validation-bypublisher-20181122.xml")
                },
            ),
        ]

    def _generate_examples(self, articles_file=None, labels_file=None):
        """Yields examples."""

        labels = {}
        with open(labels_file, "rb") as f_labels:
            tree = ET.parse(f_labels)
            root = tree.getroot()
            for label in root:
                article_id = label.attrib["id"]
                del label.attrib["labeled-by"]
                labels[article_id] = label.attrib

        with open(articles_file, "rb") as f_articles:
            tree = ET.parse(f_articles)
            root = tree.getroot()
            for idx,article in enumerate(root):
                example = {}
                example["title"] = article.attrib["title"]
                example["published_at"] = article.attrib.get("published-at","")
                example["id"] = article.attrib["id"]
                example = {**example,**labels[example["id"]]}
                example["hyperpartisan"] = example["hyperpartisan"] == "true"

                example["text"] = ""
                for child in article.getchildren():
                    example["text"] += ET.tostring(child).decode()+"\n"
                example["text"] = example["text"].strip()
                del example["id"]
                yield idx, example
