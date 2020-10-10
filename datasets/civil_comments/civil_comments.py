# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""CivilComments from Jigsaw Unintended Bias Kaggle Competition."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """
@article{DBLP:journals/corr/abs-1903-04561,
  author    = {Daniel Borkan and
               Lucas Dixon and
               Jeffrey Sorensen and
               Nithum Thain and
               Lucy Vasserman},
  title     = {Nuanced Metrics for Measuring Unintended Bias with Real Data for Text
               Classification},
  journal   = {CoRR},
  volume    = {abs/1903.04561},
  year      = {2019},
  url       = {http://arxiv.org/abs/1903.04561},
  archivePrefix = {arXiv},
  eprint    = {1903.04561},
  timestamp = {Sun, 31 Mar 2019 19:01:24 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/abs-1903-04561},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """
The comments in this dataset come from an archive of the Civil Comments
platform, a commenting plugin for independent news sites. These public comments
were created from 2015 - 2017 and appeared on approximately 50 English-language
news sites across the world. When Civil Comments shut down in 2017, they chose
to make the public comments available in a lasting open archive to enable future
research. The original data, published on figshare, includes the public comment
text, some associated metadata such as article IDs, timestamps and
commenter-generated "civility" labels, but does not include user ids. Jigsaw
extended this dataset by adding additional labels for toxicity and identity
mentions. This data set is an exact replica of the data released for the
Jigsaw Unintended Bias in Toxicity Classification Kaggle challenge.  This
dataset is released under CC0, as is the underlying comment text.
"""

_DOWNLOAD_URL = "https://storage.googleapis.com/jigsaw-unintended-bias-in-toxicity-classification/civil_comments.zip"


class CivilComments(datasets.GeneratorBasedBuilder):
    """Classification and tagging of 2M comments on news sites.

    This version of the CivilComments Dataset provides access to the primary
    seven labels that were annotated by crowd workers, the toxicity and other
    tags are a value between 0 and 1 indicating the fraction of annotators that
    assigned these attributes to the comment text.

    The other tags, which are only available for a fraction of the input examples
    are currently ignored, as are all of the attributes that were part of the
    original civil comments release. See the Kaggle documentation for more
    details about the available features.
    """

    VERSION = datasets.Version("0.9.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "toxicity": datasets.Value("float32"),
                    "severe_toxicity": datasets.Value("float32"),
                    "obscene": datasets.Value("float32"),
                    "threat": datasets.Value("float32"),
                    "insult": datasets.Value("float32"),
                    "identity_attack": datasets.Value("float32"),
                    "sexual_explicit": datasets.Value("float32"),
                }
            ),
            # The supervised_keys version is very impoverished.
            supervised_keys=("text", "toxicity"),
            homepage="https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/data",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filename": os.path.join(dl_path, "train.csv"), "toxicity_label": "target"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filename": os.path.join(dl_path, "test_public_expanded.csv"),
                    "toxicity_label": "toxicity",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filename": os.path.join(dl_path, "test_private_expanded.csv"),
                    "toxicity_label": "toxicity",
                },
            ),
        ]

    def _generate_examples(self, filename, toxicity_label):
        """Yields examples.

        Each example contains a text input and then seven annotation labels.

        Args:
          filename: the path of the file to be read for this split.
          toxicity_label: indicates 'target' or 'toxicity' to capture the variation
            in the released labels for this dataset.

        Yields:
          A dictionary of features, all floating point except the input text.
        """
        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                example = {}
                example["text"] = row["comment_text"]
                example["toxicity"] = float(row[toxicity_label])
                for label in ["severe_toxicity", "obscene", "threat", "insult", "identity_attack", "sexual_explicit"]:
                    example[label] = float(row[label])
                yield row["id"], example
