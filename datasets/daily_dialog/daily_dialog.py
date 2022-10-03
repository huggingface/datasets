# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors
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
"""DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset"""


import os
from zipfile import ZipFile

import datasets


_CITATION = """\
@InProceedings{li2017dailydialog,
    author = {Li, Yanran and Su, Hui and Shen, Xiaoyu and Li, Wenjie and Cao, Ziqiang and Niu, Shuzi},
    title = {DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset},
    booktitle = {Proceedings of The 8th International Joint Conference on Natural Language Processing (IJCNLP 2017)},
    year = {2017}
}
"""

_DESCRIPTION = """\
We develop a high-quality multi-turn dialog dataset, DailyDialog, which is intriguing in several aspects.
The language is human-written and less noisy. The dialogues in the dataset reflect our daily communication way
and cover various topics about our daily life. We also manually label the developed dataset with communication
intention and emotion information. Then, we evaluate existing approaches on DailyDialog dataset and hope it
benefit the research field of dialog systems.
"""

_URL = "http://yanran.li/files/ijcnlp_dailydialog.zip"

act_label = {
    "0": "__dummy__",  # Added to be compatible out-of-the-box with datasets.ClassLabel
    "1": "inform",
    "2": "question",
    "3": "directive",
    "4": "commissive",
}

emotion_label = {
    "0": "no emotion",
    "1": "anger",
    "2": "disgust",
    "3": "fear",
    "4": "happiness",
    "5": "sadness",
    "6": "surprise",
}


class DailyDialog(datasets.GeneratorBasedBuilder):
    """DailyDialog: A Manually Labelled Multi-turn Dialogue Dataset"""

    VERSION = datasets.Version("1.0.0")

    __EOU__ = "__eou__"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "dialog": datasets.features.Sequence(datasets.Value("string")),
                    "act": datasets.features.Sequence(datasets.ClassLabel(names=list(act_label.values()))),
                    "emotion": datasets.features.Sequence(datasets.ClassLabel(names=list(emotion_label.values()))),
                }
            ),
            supervised_keys=None,
            homepage="http://yanran.li/dailydialog",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        dl_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(dl_dir, "ijcnlp_dailydialog")
        splits = [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "data_zip": os.path.join(data_dir, f"{split}.zip"),
                    "dialog_path": f"{split}/dialogues_{split}.txt",
                    "act_path": f"{split}/dialogues_act_{split}.txt",
                    "emotion_path": f"{split}/dialogues_emotion_{split}.txt",
                },
            )
            for split in splits
        ]

    def _generate_examples(self, data_zip, dialog_path, act_path, emotion_path):
        with open(data_zip, "rb") as data_file:
            with ZipFile(data_file) as zip_file:
                with zip_file.open(dialog_path) as dialog_file, zip_file.open(act_path) as act_file, zip_file.open(
                    emotion_path
                ) as emotion_file:
                    for idx, (dialog_line, act_line, emotion_line) in enumerate(
                        zip(dialog_file, act_file, emotion_file)
                    ):
                        if not dialog_line.strip():
                            break
                        dialog = dialog_line.decode().split(self.__EOU__)[:-1]
                        act = act_line.decode().split(" ")[:-1]
                        emotion = emotion_line.decode().split(" ")[:-1]
                        assert (
                            len(dialog) == len(act) == len(emotion)
                        ), "Different turns btw dialogue & emotion & action"
                        yield idx, {
                            "dialog": dialog,
                            "act": [act_label[x] for x in act],
                            "emotion": [emotion_label[x] for x in emotion],
                        }
