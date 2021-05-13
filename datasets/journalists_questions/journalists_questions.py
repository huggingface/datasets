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


import csv

import datasets


_CITATION = """\
@inproceedings{hasanain2016questions,
  title={What Questions Do Journalists Ask on Twitter?},
  author={Hasanain, Maram and Bagdouri, Mossaab and Elsayed, Tamer and Oard, Douglas W},
  booktitle={Tenth International AAAI Conference on Web and Social Media},
  year={2016}
}
"""

_DESCRIPTION = """\
The journalists_questions corpus (version 1.0) is a collection of 10K human-written Arabic
tweets manually labeled for question identification over Arabic tweets posted by journalists.
"""
_DATA_URL = "https://drive.google.com/uc?export=download&id=1CBrh-9OrSpKmPQBxTK_ji6mq6WTN_U9U"


class JournalistsQuestions(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Journalists tweet IDs and annotation by whether the tweet has a question",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "tweet_id": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["no", "yes"]),
                    "label_confidence": datasets.Value("float"),
                }
            ),
            homepage="http://qufaculty.qu.edu.qa/telsayed/datasets/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": dl_dir}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", fieldnames=["tweet_id", "label", "label_confidence"])
            for idx, row in enumerate(reader):
                yield idx, {
                    "tweet_id": row["tweet_id"],
                    "label": row["label"],
                    "label_confidence": float(row["label_confidence"]),
                }
