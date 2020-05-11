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
"""WikiHow Datasets."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from pathlib import Path

import csv
import os
import re

import nlp

_CITATION = """
@misc{koupaee2018wikihow,
    title={WikiHow: A Large Scale Text Summarization Dataset},
    author={Mahnaz Koupaee and William Yang Wang},
    year={2018},
    eprint={1810.09305},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """
WikiHow is a new large-scale dataset using the online WikiHow
(http://www.wikihow.com/) knowledge base.

There are two features:
  - text: wikihow answers texts.
  - headline: bold lines as summary.

There are two separate versions:
  - all: consisting of the concatenation of all paragraphs as the articles and
         the bold lines as the reference summaries.
  - sep: consisting of each paragraph and its summary.

Download "wikihowAll.csv" and "wikihowSep.csv" from
https://github.com/mahnazkoupaee/WikiHow-Dataset and place them in manual folder
https://www.tensorflow.org/datasets/api_docs/python/tfds/download/DownloadConfig.
Train/validation/test splits are provided by the authors.
Preprocessing is applied to remove short articles
(abstract length < 0.75 article length) and clean up extra commas.
"""

_DOCUMENT = "text"
_SUMMARY = "headline"

_URLS = {
    "train":
        "https://raw.githubusercontent.com/mahnazkoupaee/WikiHow-Dataset/master/all_train.txt",
    "validation":
        "https://raw.githubusercontent.com/mahnazkoupaee/WikiHow-Dataset/master/all_val.txt",
    "test":
        "https://raw.githubusercontent.com/mahnazkoupaee/WikiHow-Dataset/master/all_test.txt"
}


class WikihowConfig(nlp.BuilderConfig):
  """BuilderConfig for Wikihow."""

  def __init__(self, filename=None, **kwargs):
    """BuilderConfig for Wikihow.

    Args:
      filename: filename of different configs for the dataset.
      **kwargs: keyword arguments forwarded to super.
    """
    # Version 1.1.0 remove empty document and summary strings.
    # Version 1.2.0 add train validation test split, add cleaning & filtering.
    super(WikihowConfig, self).__init__(
        version=nlp.Version("1.2.0"), **kwargs)
    self.filename = filename


class Wikihow(nlp.GeneratorBasedBuilder):
  """WikiHow: A Large Scale Text Summarization Dataset."""

  MANUAL_DOWNLOAD_INSTRUCTIONS = """\
  You need to manually download wikihow. Links to files can be found on https://github.com/mahnazkoupaee/WikiHow-Dataset
  Please download both wikihowAll.csv and wikihowSep.csv in ~/wikihow or change the manual dir to your downloded folder path
  """

  BUILDER_CONFIGS = [
      WikihowConfig(
          name="all",
          filename="wikihowAll.csv",
          description="Use the concatenation of all paragraphs as the articles"
          " and the bold lines as the reference summaries"),
      WikihowConfig(
          name="sep",
          filename="wikihowSep.csv",
          description="use each paragraph and its summary.")
  ]

  def _info(self):
    feature_names = [_DOCUMENT, _SUMMARY, "title"]
    if self.config.name == "sep":
      feature_names.extend(["overview", "sectionLabel"])
    return nlp.DatasetInfo(
        description=_DESCRIPTION,
        features=nlp.Features(
            {k: nlp.Value('string') for k in feature_names}),
        supervised_keys=None,
        homepage="https://github.com/mahnazkoupaee/WikiHow-Dataset",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    dl_path = dl_manager.download_and_extract(_URLS)
    titles = {k: set() for k in dl_path}
    for k, path in dl_path.items():
      with open(path) as f:
        for line in f:
          titles[k].add(line.strip())
  
    home = str(Path.home())
    manual_dir = os.path.join(home, 'wikihow')
    if not os.path.exists(manual_dir):
        raise FileNotFoundError(self.MANUAL_DOWNLOAD_INSTRUCTIONS)
    return [
        nlp.SplitGenerator(
            name=nlp.Split.TRAIN,
            gen_kwargs={
                "path": os.path.join(manual_dir, self.config.filename),
                "title_set": titles["train"],
            },
        ),
        nlp.SplitGenerator(
            name=nlp.Split.VALIDATION,
            gen_kwargs={
                "path":os.path.join(manual_dir, self.config.filename),
                "title_set": titles["validation"],
            },
        ),
        nlp.SplitGenerator(
            name=nlp.Split.TEST,
            gen_kwargs={
                "path":os.path.join(manual_dir, self.config.filename),
                "title_set": titles["test"],
            },
        )
    ]

  def _generate_examples(self, path=None, title_set=None):
    """Yields examples."""
    with open(path) as f:
      reader = csv.reader(f)
      headers = next(reader)
      if self.config.name == "all" and headers != [
          "headline", "title", "text"
      ]:
        raise ValueError("Mismatched header in WikiAll.txt")
      if self.config.name == "sep" and headers != [
          "overview", "headline", "text", "sectionLabel", "title"
      ]:
        raise ValueError("Mismatched header in WikiSep.txt")
      key2id = {key: i for i, key in enumerate(headers)}
      for i, line in enumerate(reader):
        # skip empty line or insufficient line.
        if len(line) == len(key2id):
          summary = line[key2id[_SUMMARY]].strip()
          document = line[key2id[_DOCUMENT]].strip()
          summary, document = _filter_and_clean(summary, document)
          if summary and document:
            if line[key2id["title"]].strip().replace(" ", "") in title_set:
              d = {
                  k: line[v].strip()
                  for k, v in key2id.items()
                  if k not in [_SUMMARY, _DOCUMENT]
              }
              d[_DOCUMENT] = document
              d[_SUMMARY] = summary
              yield i, d


# This functions follow data processing acoording to original paper at
# https://github.com/mahnazkoupaee/WikiHow-Dataset/blob/master/process.py
def _filter_and_clean(abstract, article):
  """Remove short article and clean up commas in abstract and article."""
  # a threshold is used to remove short articles with long summaries
  # as well as articles with no summary
  if len(abstract) < (0.75 * len(article)):
    # remove extra commas in abstracts
    abstract = abstract.replace(".,", ".")
    # remove extra commas in articles
    article = re.sub(r"[.]+[\n]+[,]", ".\n", article)
    return abstract, article
  else:
    return "", ""
