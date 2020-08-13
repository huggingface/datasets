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
"""Hyperpartisan News Detection"""

from __future__ import absolute_import, division, print_function

import os
import textwrap
import xml.etree.ElementTree as ET
import glob

import nlp


_CITATION = """\
@article{kiesel2019data,
  title={Data for pan at semeval 2019 task 4: Hyperpartisan news detection},
  author={Kiesel, Johannes and Mestre, Maria and Shukla, Rishabh and Vincent, Emmanuel and Corney, David and Adineh, Payam and Stein, Benno and Potthast, Martin},
  year={2019}
}
"""

_DESCRIPTION = """\
Hyperpartisan News Detection was a dataset created for PAN @ SemEval 2019 Task 4.
Given a news article text, decide whether it follows a hyperpartisan argumentation, i.e., whether it exhibits blind, prejudiced, or unreasoning allegiance to one party, faction, cause, or person.

There are 2 parts:
- byarticle: Labeled through crowdsourcing on an article basis. The data contains only articles for which a consensus among the crowdsourcing workers existed.
- bypublisher: Labeled by the overall bias of the publisher as provided by BuzzFeed journalists or MediaBiasFactCheck.com.
"""
_URL_BASE = "https://zenodo.org/record/1489920/files/"


class HyperpartisanNewsDetection(nlp.GeneratorBasedBuilder):
    """Hyperpartisan News Detection Dataset."""

    VERSION = nlp.Version("1.0.0")
    BUILDER_CONFIGS = [
        nlp.BuilderConfig(
            name="byarticle",
            version=nlp.Version("1.0.0", "Version Training and validation v1"),
            description=textwrap.dedent(
                """
                    This part of the data (filename contains "byarticle") is labeled through crowdsourcing on an article basis.
                    The data contains only articles for which a consensus among the crowdsourcing workers existed. It contains
                    a total of 645 articles. Of these, 238 (37%) are hyperpartisan and 407 (63%) are not, We will use a similar
                    (but balanced!) test set. Again, none of the publishers in this set will occur in the test set.
                """
            ),
        ),
        nlp.BuilderConfig(
            name="bypublisher",
            version=nlp.Version("1.0.0", "Version Training and validation v1"),
            description=textwrap.dedent(
                """
                    This part of the data (filename contains "bypublisher") is labeled by the overall bias of the publisher as provided
                    by BuzzFeed journalists or MediaBiasFactCheck.com. It contains a total of 750,000 articles, half of which (375,000)
                    are hyperpartisan and half of which are not. Half of the articles that are hyperpartisan (187,500) are on the left side
                    of the political spectrum, half are on the right side. This data is split into a training set (80%, 600,000 articles) and
                    a validation set (20%, 150,000 articles), where no publisher that occurs in the training set also occurs in the validation
                    set. Similarly, none of the publishers in those sets will occur in the test set.
                """
            ),
        ),
    ]


    def _info(self):
        features = {
            "text": nlp.Value("string"),
            "title": nlp.Value("string"),
            "hyperpartisan": nlp.Value("bool"),
            "url": nlp.Value("string"),
            "published_at": nlp.Value("string"),
        }

        if self.config.name == "bypublisher":
            # Bias is only included in the bypublisher config
            features["bias"] = nlp.ClassLabel(names=["right", "right-center", "least", "left-center", "left"])

        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(features),
            supervised_keys=("text", "label"),
            homepage="https://pan.webis.de/semeval19/semeval19-web/",
            citation=_CITATION,
        )


    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls = {
            nlp.Split.TRAIN:{
                "articles_file": _URL_BASE + "articles-training-" + self.config.name + "-20181122.zip?download=1",
                "labels_file": _URL_BASE + "ground-truth-training-" + self.config.name + "-20181122.zip?download=1",
            },
        }
        if self.config.name == "bypublisher":
            urls[nlp.Split.VALIDATION] = {
                "articles_file": _URL_BASE + "articles-training-" + self.config.name + "-20181122.zip?download=1",
                "labels_file": _URL_BASE + "ground-truth-training-" + self.config.name + "-20181122.zip?download=1",
            }

        data_dir = {}
        for key in urls:
            data_dir[key] = dl_manager.download_and_extract(urls[key])

        splits = []
        for split in data_dir:
            for key in data_dir[split]:
                data_dir[split][key] = os.path.join(
                        data_dir[split][key],
                        os.listdir(data_dir[split][key])[0]
                    )
            splits.append(
                nlp.SplitGenerator(
                    name=split,
                    gen_kwargs = data_dir[split]
                )
            )
        return splits


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
            for idx, article in enumerate(root):
                example = {}
                example["title"] = article.attrib["title"]
                example["published_at"] = article.attrib.get("published-at", "")
                example["id"] = article.attrib["id"]
                example = {**example, **labels[example["id"]]}
                example["hyperpartisan"] = example["hyperpartisan"] == "true"

                example["text"] = ""
                for child in article.getchildren():
                    example["text"] += ET.tostring(child).decode() + "\n"
                example["text"] = example["text"].strip()
                del example["id"]
                yield idx, example
