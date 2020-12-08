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
"""GLUCOSE: GeneraLized and COntextualized Story Explanations, is a novel conceptual framework and dataset for commonsense reasoning. Given a short story and a sentence X in the story, GLUCOSE captures ten dimensions of causal explanation related to X. These dimensions, inspired by human cognitive psychology, cover often-implicit causes and effects of X, including events, location, possession, and other attributes."""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{mostafazadeh2020glucose,
      title={GLUCOSE: GeneraLized and COntextualized Story Explanations},
      author={Nasrin Mostafazadeh and Aditya Kalyanpur and Lori Moon and David Buchanan and Lauren Berkowitz and Or Biran and Jennifer Chu-Carroll},
      year={2020},
      booktitle={The Conference on Empirical Methods in Natural Language Processing},
      publisher={Association for Computational Linguistics}
}
"""

# You can copy an official description
_DESCRIPTION = """\
When humans read or listen, they make implicit commonsense inferences that frame their understanding of what happened and why. As a step toward AI systems that can build similar mental models, we introduce GLUCOSE, a large-scale dataset of implicit commonsense causal knowledge, encoded as causal mini-theories about the world, each grounded in a narrative context.
"""

_HOMEPAGE = "https://github.com/ElementalCognition/glucose"

_LICENSE = "Creative Commons Attribution-NonCommercial 4.0 International Public License"

_URLs = {
    "glucose": {
        "test": "https://raw.githubusercontent.com/ElementalCognition/glucose/master/test/test_set_no_answers.csv",
        "train": "https://github.com/TevenLeScao/glucose/blob/master/GLUCOSE_training_data.zip?raw=true",
    }
}


class Glucose(datasets.GeneratorBasedBuilder):
    """GLUCOSE: GeneraLized and COntextualized Story Explanations, is a novel conceptual framework and dataset for commonsense reasoning. """

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="glucose", description="Main dataset"),
    ]

    def _info(self):
        feature_dict = {
            "experiment_id": datasets.Value("string"),
            "story_id": datasets.Value("string"),
            # The train set contains only one ID in numeric form
            "worker_id": datasets.Value("int64"),
            # The test set contains several IDs in string form
            "worker_ids": datasets.Value("string"),
            "submission_time_normalized": datasets.Value("string"),
            "worker_quality_assessment": datasets.Value("int64"),
            "selected_sentence_index": datasets.Value("int64"),
            "story": datasets.Value("string"),
            "selected_sentence": datasets.Value("string"),
            "number_filled_in": datasets.Value("int64"),
        }
        for i in range(1, 11):
            feature_dict[f"{i}_specificNL"] = datasets.Value("string")
            feature_dict[f"{i}_specificStructured"] = datasets.Value("string")
            feature_dict[f"{i}_generalNL"] = datasets.Value("string")
            feature_dict[f"{i}_generalStructured"] = datasets.Value("string")
        features = datasets.Features(feature_dict)
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_url = _URLs[self.config.name]["train"]
        test_url = _URLs[self.config.name]["test"]
        train_data = dl_manager.download_and_extract(train_url)
        test_data = dl_manager.download_and_extract(test_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(train_data, "GLUCOSE_training_data_final.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": test_data, "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        with open(filepath, encoding="utf8") as f:
            data = csv.reader(f)
            next(data)
            for id_, row in enumerate(data):
                if split == "train":
                    yield id_, train_dict_from_row(row)
                else:
                    yield id_, test_dict_from_row(row)


def train_dict_from_row(row):
    return_dict = {
        "experiment_id": row[0],
        "story_id": row[1],
        "worker_id": row[2],
        "worker_ids": "",
        "submission_time_normalized": row[3],
        "worker_quality_assessment": row[4],
        "selected_sentence_index": row[5],
        "story": row[6],
        "selected_sentence": row[7],
        "number_filled_in": row[48],
    }
    for i in range(1, 11):
        return_dict[f"{i}_specificNL"] = row[4 * i + 4]
        return_dict[f"{i}_specificStructured"] = row[4 * i + 5]
        return_dict[f"{i}_generalNL"] = row[4 * i + 6]
        return_dict[f"{i}_generalStructured"] = row[4 * i + 7]
    return return_dict


def test_dict_from_row(row):
    return_dict = {
        "experiment_id": "",
        "story_id": row[0],
        "worker_id": -1,
        "worker_ids": row[3],
        "submission_time_normalized": "",
        "worker_quality_assessment": -1,
        "selected_sentence_index": -1,
        "story": row[1],
        "selected_sentence": row[2],
        "number_filled_in": -1,
    }
    for i in range(1, 11):
        return_dict[f"{i}_specificNL"] = row[2 * i + 2]
        return_dict[f"{i}_generalNL"] = row[2 * i + 3]
        return_dict[f"{i}_specificStructured"] = ""
        return_dict[f"{i}_generalStructured"] = ""
    return return_dict
