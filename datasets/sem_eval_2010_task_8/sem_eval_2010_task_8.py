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
"""The SemEval-2010 Task 8 on Multi-way classification of semantic relations between pairs of nominals"""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@inproceedings{hendrickx-etal-2010-semeval,
    title = "{S}em{E}val-2010 Task 8: Multi-Way Classification of Semantic Relations between Pairs of Nominals",
    author = "Hendrickx, Iris  and
      Kim, Su Nam  and
      Kozareva, Zornitsa  and
      Nakov, Preslav  and
      {\'O} S{\'e}aghdha, Diarmuid  and
      Pad{\'o}, Sebastian  and
      Pennacchiotti, Marco  and
      Romano, Lorenza  and
      Szpakowicz, Stan",
    booktitle = "Proceedings of the 5th International Workshop on Semantic Evaluation",
    month = jul,
    year = "2010",
    address = "Uppsala, Sweden",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/S10-1006",
    pages = "33--38",
}
"""

_DESCRIPTION = """\
The SemEval-2010 Task 8 focuses on Multi-way classification of semantic relations between pairs of nominals.
The task was designed to compare different approaches to semantic relation classification
and to provide a standard testbed for future research.
"""

_URL = "https://github.com/JoelNiklaus/SemEval2010Task8/raw/main/SemEval2010_task8_all_data.zip"


class SemEval2010Task8(datasets.GeneratorBasedBuilder):
    """The SemEval-2010 Task 8 focuses on Multi-way classification of semantic relations between pairs of nominals.
    The task was designed to compare different approaches to semantic relation classification
    and to provide a standard testbed for future research."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "relation": datasets.ClassLabel(
                        names=[
                            "Cause-Effect(e1,e2)",
                            "Cause-Effect(e2,e1)",
                            "Component-Whole(e1,e2)",
                            "Component-Whole(e2,e1)",
                            "Content-Container(e1,e2)",
                            "Content-Container(e2,e1)",
                            "Entity-Destination(e1,e2)",
                            "Entity-Destination(e2,e1)",
                            "Entity-Origin(e1,e2)",
                            "Entity-Origin(e2,e1)",
                            "Instrument-Agency(e1,e2)",
                            "Instrument-Agency(e2,e1)",
                            "Member-Collection(e1,e2)",
                            "Member-Collection(e2,e1)",
                            "Message-Topic(e1,e2)",
                            "Message-Topic(e2,e1)",
                            "Product-Producer(e1,e2)",
                            "Product-Producer(e2,e1)",
                            "Other",
                        ]
                    ),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=datasets.info.SupervisedKeysData(input="sentence", output="relation"),
            # Homepage of the dataset for documentation
            homepage="https://semeval2.fbk.eu/semeval2.php?location=tasks&taskid=11",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "SemEval2010_task8_all_data")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "SemEval2010_task8_training/TRAIN_FILE.TXT"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "SemEval2010_task8_testing_keys/TEST_FILE_FULL.TXT"),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        """ Yields examples. """
        with open(filepath, "r", encoding="us-ascii") as file:
            lines = file.readlines()
            num_lines_per_sample = 4

            for i in range(0, len(lines), num_lines_per_sample):
                idx = int(lines[i].split("\t")[0])
                sentence = lines[i].split("\t")[1][1:-2]  # remove " at the start and "\n at the end
                relation = lines[i + 1][:-1]  # remove \n at the end
                yield idx, {
                    "sentence": sentence,
                    "relation": relation,
                }
