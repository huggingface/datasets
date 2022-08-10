# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors, Stack Overflow, the authors of the questions and answers, and the current dataset script contributor.
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
"""StackSample: 10% of Stack Overflow Q&A"""


import csv
import os

import datasets


_DESCRIPTION = """\
Dataset with the text of 10% of questions and answers from the Stack Overflow programming Q&A website.

This is organized as three tables:

Questions contains the title, body, creation date, closed date (if applicable), score, and owner ID for all non-deleted Stack Overflow questions whose Id is a multiple of 10.
Answers contains the body, creation date, score, and owner ID for each of the answers to these questions. The ParentId column links back to the Questions table.
Tags contains the tags on each of these questions.
"""

_HOMEPAGE = "https://www.kaggle.com/stackoverflow/stacksample"

_LICENSE = "All Stack Overflow user contributions are licensed under CC-BY-SA 3.0 with attribution required."


class SOStackSample(datasets.GeneratorBasedBuilder):
    """StackSample: 10% of Stack Overflow Q&A"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="Answers",
            version=VERSION,
            description="This part of the dataset contains only posts that are answers.",
        ),
        datasets.BuilderConfig(
            name="Questions",
            version=VERSION,
            description="This part of the dataset contains only posts that are questions.",
        ),
        datasets.BuilderConfig(
            name="Tags",
            version=VERSION,
            description="This part of the dataset contains only tags of the questions in the question part of the StackSample dataset.",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
        You must have a kaggle account. Go to https://www.kaggle.com/stackoverflow/stacksample
        and manually download the language of your interest. Once it is downloaded,
        go to the place where you downloaded it and unzip the folder. Three files named
        `Answers.csv`, `Questions.csv`, and `Tags.csv` will have appeared in your Downloads folder
        or whichever folder your browser chooses to save files to.
        so_stacksample can then be loaded using the following command
        `datasets.load_dataset("so_stacksample", "<csv_file_name>",data_dir="<path/to/folder>")`,
        where `<path/to/folder> is the path to the unzipped folder. Example if you downloaded
        and unzipped the folder in your downloads folder:
        `datasets.load_dataset("so_stacksample", "Answers", data_dir="/home/<user>/Downloads")`
        will load the `Answers.csv` dataset.
        """

    def _info(self):
        if self.config.name == "Answers":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "Id": datasets.Value("int32"),
                    "OwnerUserId": datasets.Value("int32"),
                    "CreationDate": datasets.Value("string"),
                    "ParentId": datasets.Value("int32"),
                    "Score": datasets.Value("int32"),
                    "Body": datasets.Value("string"),
                }
            )
        elif self.config.name == "Questions":
            features = datasets.Features(
                {
                    "Id": datasets.Value("int32"),
                    "OwnerUserId": datasets.Value("int32"),
                    "CreationDate": datasets.Value("string"),
                    "ClosedDate": datasets.Value("string"),
                    "Score": datasets.Value("int32"),
                    "Title": datasets.Value("string"),
                    "Body": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "Id": datasets.Value("int32"),
                    "Tag": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.join(
            os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), self.config.name + ".csv"
        )
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('so_stacksample', '{self.config.name}', data_dir=...)` that includes a file name {self.config.name + '.csv'}. Manual download instructions: \n{self.manual_download_instructions})"
            )

        return [
            datasets.SplitGenerator(
                name=self.config.name,
                gen_kwargs={
                    "filepath": path_to_manual_file,
                    "split": self.config.name,
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="ISO-8859-1") as f:
            csv_reader = csv.reader(f, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True)
            next(csv_reader, None)
            for row_id, row in enumerate(csv_reader):
                if split == "Answers":
                    id_, owner_user_id, creation_date, parent_id, score, body = row
                    if owner_user_id == "NA":
                        owner_user_id = -1  # Set N/A's to default -1 value
                    yield row_id, {
                        "Id": id_,
                        "OwnerUserId": owner_user_id,
                        "CreationDate": creation_date,
                        "ParentId": parent_id,
                        "Score": score,
                        "Body": body,
                    }
                elif split == "Questions":
                    id_, owner_user_id, creation_date, closed_date, score, title, body = row
                    if owner_user_id == "NA":
                        owner_user_id = -1  # Set N/A's to default -1 value
                    yield row_id, {
                        "Id": id_,
                        "OwnerUserId": owner_user_id,
                        "CreationDate": creation_date,
                        "ClosedDate": closed_date,
                        "Score": score,
                        "Title": title,
                        "Body": body,
                    }
                else:
                    id_, tag = row
                    yield row_id, {
                        "Id": id_,
                        "Tag": tag,
                    }
