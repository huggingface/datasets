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
"""CRD3  dataset"""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import datasets


_CITATION = """
@inproceedings{
title = {Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset},
author = {Rameshkumar, Revanth  and Bailey, Peter},
year = {2020},
publisher = {Association for Computational Linguistics},
conference = {ACL}
}
 """

_DESCRIPTION = """
Storytelling with Dialogue: A Critical Role Dungeons and Dragons Dataset.
Critical Role is an unscripted, live-streamed show where a fixed group of people play Dungeons and Dragons, an open-ended role-playing game.
The dataset is collected from 159 Critical Role episodes transcribed to text dialogues, consisting of 398,682 turns. It also includes corresponding
abstractive summaries collected from the Fandom wiki. The dataset is linguistically unique in that the narratives are generated entirely through player
collaboration and spoken interaction. For each dialogue, there are a large number of turns, multiple abstractive summaries with varying levels of detail,
and semantic ties to the previous dialogues.
"""

_URL = "https://github.com/RevanthRameshkumar/CRD3/archive/master.zip"


def get_train_test_dev_files(files, test_split, train_split, dev_split):
    test_files = dev_files = train_files = []
    for file in files:
        filename = os.path.split(file)[1].split("_")[0]
        if filename in test_split:
            test_files.append(file)
        elif filename in train_split:
            train_files.append(file)
        elif filename in dev_split:
            dev_files.append(file)
        else:
            logging.info("skipped file {}".format(file))
    return test_files, train_files, dev_files


class CRD3(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "chunk": datasets.Value("string"),
                    "chunk_id": datasets.Value("int32"),
                    "turn_start": datasets.Value("int32"),
                    "turn_end": datasets.Value("int32"),
                    "alignment_score": datasets.Value("float32"),
                    "turn_num": datasets.Value("int32"),
                    "turns": datasets.features.Sequence(
                        {
                            "names": datasets.Value("string"),
                            "utterances": datasets.Value("string"),
                        }
                    ),
                }
            ),
            homepage="https://github.com/RevanthRameshkumar/CRD3",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_URL)
        test_file = os.path.join(path, "CRD3-master", "data", "aligned data", "test_files")
        train_file = os.path.join(path, "CRD3-master", "data", "aligned data", "train_files")
        dev_file = os.path.join(path, "CRD3-master", "data", "aligned data", "val_files")
        with open(test_file, encoding="utf-8") as f:
            test_splits = [file.replace("\n", "") for file in f.readlines()]

        with open(train_file, encoding="utf-8") as f:
            train_splits = [file.replace("\n", "") for file in f.readlines()]
        with open(dev_file, encoding="utf-8") as f:
            dev_splits = [file.replace("\n", "") for file in f.readlines()]
        c2 = "CRD3-master/data/aligned data/c=2"
        c3 = "CRD3-master/data/aligned data/c=3"
        c4 = "CRD3-master/data/aligned data/c=4"
        files = [os.path.join(path, c2, file) for file in sorted(os.listdir(os.path.join(path, c2)))]
        files.extend([os.path.join(path, c3, file) for file in sorted(os.listdir(os.path.join(path, c3)))])
        files.extend([os.path.join(path, c4, file) for file in sorted(os.listdir(os.path.join(path, c4)))])

        test_files, train_files, dev_files = get_train_test_dev_files(files, test_splits, train_splits, dev_splits)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files_path": train_files},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"files_path": test_files},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"files_path": dev_files},
            ),
        ]

    def _generate_examples(self, files_path):
        """Yields examples."""

        for file in files_path:
            with open(file, encoding="utf-8") as f:
                data = json.load(f)
                for id1, row in enumerate(data):
                    chunk = row["CHUNK"]
                    chunk_id = row["ALIGNMENT"]["CHUNK ID"]
                    turn_start = row["ALIGNMENT"]["TURN START"]
                    turn_end = row["ALIGNMENT"]["TURN END"]
                    score = row["ALIGNMENT"]["ALIGNMENT SCORE"]
                    for id2, turn in enumerate(row["TURNS"]):
                        turn_names = turn["NAMES"]
                        turn_utterances = turn["UTTERANCES"]
                        turn_num = turn["NUMBER"]
                        yield str(id1) + "_" + str(id2), {
                            "chunk": chunk,
                            "chunk_id": chunk_id,
                            "turn_start": turn_start,
                            "turn_end": turn_end,
                            "alignment_score": score,
                            "turn_num": turn_num,
                            "turns": {
                                "names": turn_names,
                                "utterances": turn_utterances,
                            },
                        }
