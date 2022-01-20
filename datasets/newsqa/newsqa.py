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
"""This code is used to read and load NewsQA dataset."""


import csv
import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{trischler2017newsqa,
  title={NewsQA: A Machine Comprehension Dataset},
  author={Trischler, Adam and Wang, Tong and Yuan, Xingdi and Harris, Justin and Sordoni, Alessandro and Bachman, Philip and Suleman, Kaheer},
  booktitle={Proceedings of the 2nd Workshop on Representation Learning for NLP},
  pages={191--200},
  year={2017}
}

"""

# You can copy an official description
_DESCRIPTION = """\
NewsQA is a challenging machine comprehension dataset of over 100,000 human-generated question-answer pairs. \
Crowdworkers supply questions and answers based on a set of over 10,000 news articles from CNN, with answers consisting of spans of text from the corresponding articles.
"""

_HOMEPAGE = "https://www.microsoft.com/en-us/research/project/newsqa-dataset/"

_LICENSE = 'NewsQA Code\
Copyright (c) Microsoft Corporation\
All rights reserved.\
MIT License\
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\
THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\
© 2020 GitHub, Inc.'


class Newsqa(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="combined-csv",
            version=VERSION,
            description="This part of the dataset covers the whole dataset in the combined format of CSV as mentioned here: https://github.com/Maluuba/newsqa#csv",
        ),
        datasets.BuilderConfig(
            name="combined-json",
            version=VERSION,
            description="This part of the dataset covers the whole dataset in the combine format of JSON as mentioned here: https://github.com/Maluuba/newsqa#json",
        ),
        datasets.BuilderConfig(
            name="split",
            version=VERSION,
            description="This part of the dataset covers train, validation and test splits.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "split"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    @property
    def manual_download_instructions(self):
        return """ Due to legal restrictions with the CNN data and data extraction. The data has to be downloaded from several sources and compiled as per the instructions by Authors. \
        Upon obtaining the resulting data folders, it can be loaded easily using the datasets API. \
        Please refer to (https://github.com/Maluuba/newsqa) to download data from Microsoft Reseach site (https://msropendata.com/datasets/939b1042-6402-4697-9c15-7a28de7e1321) \
        and a CNN datasource (https://cs.nyu.edu/~kcho/DMQA/) and run the scripts present here (https://github.com/Maluuba/newsqa).\
        This will generate a folder named "split-data" and a file named "combined-newsqa-data-v1.csv".\
        Copy the above folder and the file to a directory where you want to store them locally.\
        They must be used to load the dataset via `datasets.load_dataset("narqa", data_dir="<path/to/folder>")."""

    def _info(self):

        if (
            self.config.name == "combined-csv"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "story_id": datasets.Value("string"),
                    "story_text": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer_char_ranges": datasets.Value("string"),
                }
            )
        elif (
            self.config.name == "combined-json"
        ):  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "storyId": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "type": datasets.Value("string"),
                    "questions": datasets.features.Sequence(
                        {
                            "q": datasets.Value("string"),
                            "isAnswerAbsent": datasets.Value("int32"),
                            "isQuestionBad": datasets.Value("int32"),
                            "consensus": datasets.Features(
                                {
                                    "s": datasets.Value("int32"),
                                    "e": datasets.Value("int32"),
                                    "badQuestion": datasets.Value("bool"),
                                    "noAnswer": datasets.Value("bool"),
                                }
                            ),
                            "answers": datasets.features.Sequence(
                                {
                                    "sourcerAnswers": datasets.features.Sequence(
                                        {
                                            "s": datasets.Value("int32"),
                                            "e": datasets.Value("int32"),
                                            "noAnswer": datasets.Value("bool"),
                                        }
                                    ),
                                }
                            ),
                            "validated_answers": datasets.features.Sequence(
                                {
                                    "sourcerAnswers": datasets.features.Sequence(
                                        {
                                            "s": datasets.Value("int32"),
                                            "e": datasets.Value("int32"),
                                            "noAnswer": datasets.Value("bool"),
                                            "count": datasets.Value("int32"),
                                        }
                                    ),
                                }
                            ),
                        }
                    ),
                }
            )
        else:  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "story_id": datasets.Value("string"),
                    "story_text": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer_token_ranges": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        path_to_manual_folder = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        combined_file_csv = os.path.join(path_to_manual_folder, "combined-newsqa-data-v1.csv")
        combined_file_json = os.path.join(path_to_manual_folder, "combined-newsqa-data-v1.json")
        split_files = os.path.join(path_to_manual_folder, "split_data")

        if not os.path.exists(path_to_manual_folder):
            raise FileNotFoundError(
                f"{path_to_manual_folder} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('newsqa', data_dir=...)` that includes files from the Manual download instructions: {self.manual_download_instructions}"
            )

        if self.config.name == "combined-csv":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": combined_file_csv,
                        "split": "combined",
                    },
                )
            ]
        elif self.config.name == "combined-json":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": combined_file_json,
                        "split": "combined",
                    },
                )
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(split_files, "train.csv"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={"filepath": os.path.join(split_files, "test.csv"), "split": "test"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(split_files, "dev.csv"),
                        "split": "dev",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        if self.config.name == "combined-csv":
            with open(filepath, encoding="utf-8") as csv_file:
                csv_reader = csv.reader(
                    csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
                )
                _ = next(csv_reader)
                for id_, row in enumerate(csv_reader):
                    if row:
                        yield row[0], {
                            "story_id": row[0],
                            "story_text": row[-1],
                            "question": row[1],
                            "answer_char_ranges": str(row[2:-2]),
                        }

        elif self.config.name == "combined-json":
            with open(filepath, encoding="utf-8") as f:
                d = json.load(f)
                data = d["data"]

                for iter in data:

                    questions = []

                    for ques in iter["questions"]:
                        dict1 = {}
                        dict1["q"] = ques["q"]
                        if "isAnswerAbsent" in ques.keys():
                            dict1["isAnswerAbsent"] = ques["isAnswerAbsent"]
                        else:
                            dict1["isAnswerAbsent"] = 0.0
                        if "isQuestionBad" in ques.keys():
                            dict1["isQuestionBad"] = ques["isQuestionBad"]
                        else:
                            dict1["isQuestionBad"] = 0.0
                        dict1["consensus"] = {"s": 0, "e": 0, "badQuestion": False, "noAnswer": False}

                        for keys in ques["consensus"]:
                            dict1["consensus"][keys] = ques["consensus"][keys]

                        answers = []
                        for ans in ques["answers"]:
                            dict2 = {}
                            dict2["sourcerAnswers"] = []
                            for index, i in enumerate(ans["sourcerAnswers"]):
                                dict_temp = {"s": 0, "e": 0, "noAnswer": False}
                                for keys in i.keys():
                                    dict_temp[keys] = i[keys]
                                dict2["sourcerAnswers"].append(dict_temp)

                            answers.append(dict2)

                        dict1["answers"] = answers

                        validated_answers = []
                        for ans in ques["answers"]:
                            dict2 = {}
                            dict2["sourcerAnswers"] = []
                            for index, i in enumerate(ans["sourcerAnswers"]):
                                dict_temp = {"s": 0, "e": 0, "noAnswer": False, "count": 0}
                                for keys in i.keys():
                                    dict_temp[keys] = i[keys]

                                dict2["sourcerAnswers"].append(dict_temp)

                            validated_answers.append(dict2)

                        dict1["validated_answers"] = validated_answers
                        questions.append(dict1)

                    yield iter["storyId"], {
                        "storyId": iter["storyId"],
                        "text": iter["text"],
                        "type": iter["type"],
                        "questions": questions,
                    }
        else:
            with open(filepath, encoding="utf-8") as csv_file:

                csv_reader = csv.reader(
                    csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
                )
                _ = next(csv_reader)
                for id_, row in enumerate(csv_reader):
                    if row:
                        # print (row)
                        yield row[0], {
                            "story_id": row[0],
                            "story_text": row[1],
                            "question": row[2],
                            "answer_token_ranges": row[3],
                        }
