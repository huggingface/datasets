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
"""Doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset v0.9"""

from __future__ import absolute_import, division, print_function

import json
import os
import logging

import datasets

_CITATION = """\
@inproceedings{feng-etal-2020-doc2dial,
    title = "doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset",
    author = "Feng, Song  and Wan, Hui  and Gunasekara, Chulaka  and Patel, Siva  and Joshi, Sachindra  and Lastras, Luis",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.652",
}
"""

_DESCRIPTION = """\
Doc2dial is dataset of goal-oriented dialogues that are grounded in the associated documents. \
It includes over 4500 annotated conversations with an average of 14 turns that are grounded \
in over 450 documents from four domains. Compared to the prior document-grounded dialogue datasets \
this dataset covers a variety of dialogue scenes in information-seeking conversations.
"""

# _URL = "https://doc2dial.github.io/file/doc2dial/"
_URL = "https://doc2dial.github.io/file/doc2dial.zip"
_URLS = {
    "train": _URL + "v.09/data/wOOD/doc2dial_dial_train.json",
    "dev": _URL + "v.09/data/wOOD/doc2dial_dial_dev.json",
}


class Doc2dialConfig(datasets.BuilderConfig):
    """BuilderConfig for Doc2dial."""

    def __init__(self, **kwargs):
        """BuilderConfig for Doc2dial.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Doc2dialConfig, self).__init__(**kwargs)


class Doc2dial(datasets.GeneratorBasedBuilder):
    "Doc2dial: A Goal-Oriented Document-Grounded Dialogue Dataset v0.9"

    BUILDER_CONFIGS = [
        Doc2dialConfig(
            name="plain_text",
            version=datasets.Version("0.9.0", ""),
            description="Plain text",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "dial_id": datasets.Value("string"),
                    "doc_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "turns": datasets.features.Sequence(
                        {
                            "turn_id": datasets.Value("int32"),
                            "role": datasets.Value("string"),
                            "da": datasets.Value("string"),
                            "reference": datasets.features.Sequence(
                                {
                                    "keys": datasets.Value("int32"),   
                                    "values": datasets.Value("string"), 
                                }
 
                            ),

                            "utternace": datasets.Value("string"),
                        }
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://doc2dial.github.io/file/doc2dial/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloads_dir =  dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(downloads_dir, "v.09/data/wOOD/doc2dial_dial_train.json")}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(downloads_dir, "v.09/data/wOOD/doc2dial_dial_dev.json")}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""

        filepath = '/Users/karimfoda/Downloads/doc2dial/v0.9/data/wOOD/doc2dial_dial_dev.json'
        logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for domain in data["dial_data"]:
                # print(domain)
                for doc_id in data["dial_data"][domain]:
                    # print(doc_id)
                    for dialogue in data["dial_data"][domain][doc_id]:
                        # print(conv_id)
                        print(dialogue["dial_id"])
                        for turn in dialogue['turns']:
                            # print(turn["turn_id"])

                            # Features currently used are "context", "question", and "answers".
                            # Others are extracted here for the ease of future expansions.
                            yield dialogue["dial_id"], {
                                    "dial_id":dialogue["dial_id"],
                                    "domain":domain,
                                    "doc_id": doc_id,
                                    "turns" : {
                                        "turn_id" : turn["turn_id"],
                                        "role" : turn["role"],
                                        "da" : turn["da"],
                                        "reference" : turn["reference"],
                                        "utternace" : turn["utterance"]
                                    }  
                                }
