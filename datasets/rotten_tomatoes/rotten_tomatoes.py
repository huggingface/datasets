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
"""Rotten tomatoes movie reviews dataset."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_DESCRIPTION = """\
Movie Review Dataset.
This is a dataset of containing 5,331 positive and 5,331 negative processed
sentences from Rotten Tomatoes movie reviews. This data was first used in Bo
Pang and Lillian Lee, ``Seeing stars: Exploiting class relationships for
sentiment categorization with respect to rating scales.'', Proceedings of the
ACL, 2005.
"""

_CITATION = """\
@InProceedings{Pang+Lee:05a,
  author =       {Bo Pang and Lillian Lee},
  title =        {Seeing stars: Exploiting class relationships for sentiment
                  categorization with respect to rating scales},
  booktitle =    {Proceedings of the ACL},
  year =         2005
}
"""

_DOWNLOAD_URL = "https://storage.googleapis.com/seldon-datasets/sentence_polarity_v1/rt-polaritydata.tar.gz"


class RottenTomatoesMovieReview(datasets.GeneratorBasedBuilder):
    """Cornell Rotten Tomatoes movie reviews dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"text": datasets.Value("string"), "label": datasets.features.ClassLabel(names=["neg", "pos"])}
            ),
            supervised_keys=[""],
            homepage="http://www.cs.cornell.edu/people/pabo/movie-review-data/",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, train_file):
        for _, ex in self._generate_examples(train_file):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        """ Downloads Rotten Tomatoes sentences. """
        extracted_folder_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split_key": "train", "data_dir": extracted_folder_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"split_key": "validation", "data_dir": extracted_folder_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"split_key": "test", "data_dir": extracted_folder_path},
            ),
        ]

    def _get_examples_from_split(self, split_key, data_dir):
        """Reads Rotten Tomatoes sentences and splits into 80% train,
        10% validation, and 10% test, as is the practice set out in Jinfeng
        Li, ``TEXTBUGGER: Generating Adversarial Text Against Real-world
        Applications.''
        """
        data_dir = os.path.join(data_dir, "rt-polaritydata")

        pos_samples = open(os.path.join(data_dir, "rt-polarity.pos"), encoding="latin-1").readlines()
        pos_samples = list(map(lambda t: t.strip(), pos_samples))

        neg_samples = open(os.path.join(data_dir, "rt-polarity.neg"), encoding="latin-1").readlines()
        neg_samples = list(map(lambda t: t.strip(), neg_samples))

        # 80/10/10 split
        i1 = int(len(pos_samples) * 0.8 + 0.5)
        i2 = int(len(pos_samples) * 0.9 + 0.5)
        train_samples = pos_samples[:i1] + neg_samples[:i1]
        train_labels = (["pos"] * i1) + (["neg"] * i1)
        validation_samples = pos_samples[i1:i2] + neg_samples[i1:i2]
        validation_labels = (["pos"] * (i2 - i1)) + (["neg"] * (i2 - i1))
        test_samples = pos_samples[i2:] + neg_samples[i2:]
        test_labels = (["pos"] * (len(pos_samples) - i2)) + (["neg"] * (len(pos_samples) - i2))

        if split_key == "train":
            return (train_samples, train_labels)
        if split_key == "validation":
            return (validation_samples, validation_labels)
        if split_key == "test":
            return (test_samples, test_labels)
        else:
            raise ValueError(f"Invalid split key {split_key}")

    def _generate_examples(self, split_key, data_dir):
        """Yields examples for a given split of MR."""
        split_text, split_labels = self._get_examples_from_split(split_key, data_dir)
        for text, label in zip(split_text, split_labels):
            data_key = split_key + "_" + text
            feature_dict = {"text": text, "label": label}
            yield data_key, feature_dict
