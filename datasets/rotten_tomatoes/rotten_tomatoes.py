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

import datasets
from datasets.tasks import TextClassification


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
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        """Downloads Rotten Tomatoes sentences."""
        archive = dl_manager.download(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"split_key": "train", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"split_key": "validation", "files": dl_manager.iter_archive(archive)},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"split_key": "test", "files": dl_manager.iter_archive(archive)},
            ),
        ]

    def _get_examples_from_split(self, split_key, files):
        """Reads Rotten Tomatoes sentences and splits into 80% train,
        10% validation, and 10% test, as is the practice set out in Jinfeng
        Li, ``TEXTBUGGER: Generating Adversarial Text Against Real-world
        Applications.''
        """
        data_dir = "rt-polaritydata/"
        pos_samples, neg_samples = None, None
        for path, f in files:
            if path == data_dir + "rt-polarity.pos":
                pos_samples = [line.decode("latin-1").strip() for line in f]
            elif path == data_dir + "rt-polarity.neg":
                neg_samples = [line.decode("latin-1").strip() for line in f]
            if pos_samples is not None and neg_samples is not None:
                break

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

    def _generate_examples(self, split_key, files):
        """Yields examples for a given split of MR."""
        split_text, split_labels = self._get_examples_from_split(split_key, files)
        for text, label in zip(split_text, split_labels):
            data_key = split_key + "_" + text
            feature_dict = {"text": text, "label": label}
            yield data_key, feature_dict
