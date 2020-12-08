# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""Yahoo Non-Factoid Question Dataset"""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import datasets


_DESCRIPTION = """\
Yahoo Non-Factoid Question Dataset is derived from Yahoo's Webscope L6 collection using machine learning techiques such \
that the questions would contain non-factoid answers.The dataset contains 87,361 questions and their corresponding answers. \
Each question contains its best answer along with additional other answers submitted by users. \
Only the best answer was reviewed in determining the quality of the question-answer pair.
"""

_URL = "https://ciir.cs.umass.edu/downloads/nfL6/nfL6.json.gz"


class YahooAnswersQa(datasets.GeneratorBasedBuilder):
    """Yahoo Non-Factoid Question Dataset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [datasets.BuilderConfig(name="yahoo_answers_qa", version=datasets.Version("1.0.0"))]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "nbestanswers": datasets.features.Sequence(datasets.Value("string")),
                    "main_category": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://ciir.cs.umass.edu/downloads/nfL6/index.html",
        )

    def _split_generators(self, dl_manager):
        downloaded_file = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_file}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        if os.path.isdir(filepath):
            filepath = os.path.join(filepath, "nfL6.json")
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for example in data:
                yield example["id"], example
