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
"""Cyberbullying Classification Dataset in Polish"""


import os

import datasets


_DESCRIPTION = """\
    In Task 6-1, the participants are to distinguish between normal/non-harmful tweets (class: 0) and tweets
    that contain any kind of harmful information (class: 1). This includes cyberbullying, hate speech and
    related phenomena.

    In Task 6-2, the participants shall distinguish between three classes of tweets: 0 (non-harmful),
    1 (cyberbullying), 2 (hate-speech). There are various definitions of both cyberbullying and hate-speech,
    some of them even putting those two phenomena in the same group. The specific conditions on which we based
    our annotations for both cyberbullying and hate-speech, which have been worked out during ten years of research
    will be summarized in an introductory paper for the task, however, the main and definitive condition to 1
    distinguish the two is whether the harmful action is addressed towards a private person(s) (cyberbullying),
    or a public person/entity/large group (hate-speech).
"""

_HOMEPAGE = "http://2019.poleval.pl/index.php/tasks/task6"

_URL_TRAIN_TASK1 = "http://2019.poleval.pl/task6/task_6-1.zip"
_URL_TRAIN_TASK2 = "http://2019.poleval.pl/task6/task_6-2.zip"
_URL_TEST = "http://2019.poleval.pl/task6/task6_test.zip"

_CITATION = """\
@proceedings{ogr:kob:19:poleval,
  editor    = {Maciej Ogrodniczuk and Łukasz Kobyliński},
  title     = {{Proceedings of the PolEval 2019 Workshop}},
  year      = {2019},
  address   = {Warsaw, Poland},
  publisher = {Institute of Computer Science, Polish Academy of Sciences},
  url       = {http://2019.poleval.pl/files/poleval2019.pdf},
  isbn      = "978-83-63159-28-3"}
}
"""


class Poleval2019CyberBullyingConfig(datasets.BuilderConfig):
    """BuilderConfig for Poleval2019CyberBullying."""

    def __init__(
        self,
        text_features,
        label_classes,
        **kwargs,
    ):
        super(Poleval2019CyberBullyingConfig, self).__init__(version=datasets.Version("1.0.0"), **kwargs)
        self.text_features = text_features
        self.label_classes = label_classes


class Poleval2019CyberBullying(datasets.GeneratorBasedBuilder):
    """Cyberbullying Classification Dataset in Polish"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        Poleval2019CyberBullyingConfig(
            name="task01",
            text_features=["text"],
            label_classes=["0", "1"],
        ),
        Poleval2019CyberBullyingConfig(
            name="task02",
            text_features=["text"],
            label_classes=["0", "1", "2"],
        ),
    ]

    def _info(self):

        features = {text_feature: datasets.Value("string") for text_feature in self.config.text_features}
        features["label"] = datasets.features.ClassLabel(names=self.config.label_classes)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=("text", "label"),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        if self.config.name == "task01":
            train_path = dl_manager.download_and_extract(_URL_TRAIN_TASK1)

        if self.config.name == "task02":
            train_path = dl_manager.download_and_extract(_URL_TRAIN_TASK2)

        data_dir_test = dl_manager.download_and_extract(_URL_TEST)

        if self.config.name == "task01":
            test_path = os.path.join(data_dir_test, "Task6", "task 01")

        if self.config.name == "task02":
            test_path = os.path.join(data_dir_test, "Task6", "task 02")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": train_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": test_path,
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        if split == "train":
            text_path = os.path.join(filepath, "training_set_clean_only_text.txt")
            label_path = os.path.join(filepath, "training_set_clean_only_tags.txt")

        if split == "test":
            if self.config.name == "task01":
                text_path = os.path.join(filepath, "test_set_clean_only_text.txt")
                label_path = os.path.join(filepath, "test_set_clean_only_tags.txt")
            if self.config.name == "task02":
                text_path = os.path.join(filepath, "test_set_only_text.txt")
                label_path = os.path.join(filepath, "test_set_only_tags.txt")

        with open(text_path, encoding="utf-8") as text_file:
            with open(label_path, encoding="utf-8") as label_file:
                for id_, (text, label) in enumerate(zip(text_file, label_file)):
                    yield id_, {"text": text.strip(), "label": int(label.strip())}
