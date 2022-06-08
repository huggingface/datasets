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
"""Story Cloze datasets."""


import csv
import os

import datasets


_DESCRIPTION = """
Story Cloze Test' is a commonsense reasoning framework for evaluating story understanding,
story generation, and script learning.This test requires a system to choose the correct ending
to a four-sentence story.
"""

_CITATION = """\
@inproceedings{mostafazadeh2017lsdsem,
  title={Lsdsem 2017 shared task: The story cloze test},
  author={Mostafazadeh, Nasrin and Roth, Michael and Louis, Annie and Chambers, Nathanael and Allen, James},
  booktitle={Proceedings of the 2nd Workshop on Linking Models of Lexical, Sentential and Discourse-level Semantics},
  pages={46--51},
  year={2017}
}
"""


class StoryCloze(datasets.GeneratorBasedBuilder):
    """Story Cloze."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="2016", description="Story Cloze Test Spring 2016 set"),
        datasets.BuilderConfig(name="2018", description="Story Cloze Test Winter 2018 set"),
    ]

    @property
    def manual_download_instructions(self):
        return (
            "To use Story Cloze you have to download it manually. Please fill this "
            "google form (http://goo.gl/forms/aQz39sdDrO). Complete the form. "
            "Then you will recieve a download link for the dataset. Load it using: "
            "`datasets.load_dataset('story_cloze', data_dir='path/to/folder/folder_name')`"
        )

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "story_id": datasets.Value("string"),
                    "input_sentence_1": datasets.Value("string"),
                    "input_sentence_2": datasets.Value("string"),
                    "input_sentence_3": datasets.Value("string"),
                    "input_sentence_4": datasets.Value("string"),
                    "sentence_quiz1": datasets.Value("string"),
                    "sentence_quiz2": datasets.Value("string"),
                    "answer_right_ending": datasets.Value("int32"),
                }
            ),
            homepage="https://cs.rochester.edu/nlp/rocstories/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_to_manual_folder = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if self.config.name == "2016":
            test_file = os.path.join(path_to_manual_folder, "cloze_test_test__spring2016 - cloze_test_ALL_test.csv")
            val_file = os.path.join(path_to_manual_folder, "cloze_test_val__spring2016 - cloze_test_ALL_val.csv")
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": val_file,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": test_file,
                    },
                ),
            ]

        else:
            val_file = os.path.join(path_to_manual_folder, "cloze_test_val__winter2018-cloze_test_ALL_val - 1 - 1.csv")

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": val_file,
                    },
                ),
            ]

    def _generate_examples(self, filepath):
        """Generate Story Cloze examples."""
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            _ = next(csv_reader)
            for id_, row in enumerate(csv_reader):
                if row and len(row) == 8:
                    yield id_, {
                        "story_id": row[0],
                        "input_sentence_1": row[1],
                        "input_sentence_2": row[2],
                        "input_sentence_3": row[3],
                        "input_sentence_4": row[4],
                        "sentence_quiz1": row[5],
                        "sentence_quiz2": row[6],
                        "answer_right_ending": int(row[7]),
                    }
