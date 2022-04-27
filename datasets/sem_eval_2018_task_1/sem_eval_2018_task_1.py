# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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

import os

import datasets


_CITATION = """\
@InProceedings{SemEval2018Task1,
 author = {Mohammad, Saif M. and Bravo-Marquez, Felipe and Salameh, Mohammad and Kiritchenko, Svetlana},
 title = {SemEval-2018 {T}ask 1: {A}ffect in Tweets},
 booktitle = {Proceedings of International Workshop on Semantic Evaluation (SemEval-2018)},
 address = {New Orleans, LA, USA},
 year = {2018}}
"""

_DESCRIPTION = """\
 SemEval-2018 Task 1: Affect in Tweets

 SubTask 2: Emotion Intensity Ordinal Classiﬁcation (EIoc).
 These are 4 emotion-specific datasets (anger, fear, joy, sadness) for emotional intensity regression.
 'Given a tweet and an emotion E, classify the tweet into one of four ordinal classes of intensity of E that best represents the mental state of the tweeter.'

 SubTask 5: Emotion Classification.
 This is a dataset for multilabel emotion classification for tweets.
 'Given a tweet, classify it as 'neutral or no emotion' or as one, or more, of eleven given emotions that best represent the mental state of the tweeter.'

 It contains tweets in three languages manually annotated by crowdworkers using Best–Worst Scaling.
"""

_HOMEPAGE = "https://competitions.codalab.org/competitions/17751"

_LICENSE = ""

_VERSION = datasets.Version("1.1.0")

_SUBSETS = [
    "subtask1.anger.english",
    "subtask1.fear.english",
    "subtask1.joy.english",
    "subtask1.sadness.english",
    "subtask1.anger.spanish",
    "subtask1.fear.spanish",
    "subtask1.joy.spanish",
    "subtask1.sadness.spanish",
    "subtask1.anger.arabic",
    "subtask1.fear.arabic",
    "subtask1.joy.arabic",
    "subtask1.sadness.arabic",
    "subtask2.anger.english",
    "subtask2.fear.english",
    "subtask2.joy.english",
    "subtask2.sadness.english",
    "subtask2.anger.spanish",
    "subtask2.fear.spanish",
    "subtask2.joy.spanish",
    "subtask2.sadness.spanish",
    "subtask2.anger.arabic",
    "subtask2.fear.arabic",
    "subtask2.joy.arabic",
    "subtask2.sadness.arabic",
    "subtask5.english",
    "subtask5.spanish",
    "subtask5.arabic",
]
_url = ["https://saifmohammad.com/WebDocs/AIT-2018/AIT2018-DATA/SemEval2018-Task1-all-data.zip"]
_URLs = {s: _url for s in _SUBSETS}


def parse_subset_string(s):
    d = {}
    d["task_id"] = int(s.split(".")[0][-1])
    d["language"] = s.split(".")[-1]
    if d["task_id"] in [1, 2]:
        d["emotion"] = s.split(".")[1]
    return d


def _generate_builder_configs():
    builder_configs = []
    for subset in _SUBSETS:
        # Get the task ID
        d = parse_subset_string(subset)
        task_id = d["task_id"]
        language = d["language"]
        if task_id == 5:
            builder_configs.append(
                datasets.BuilderConfig(
                    name=f"subtask{task_id}.{language}",
                    version=_VERSION,
                    description=f"This is the {language} dataset of subtask 5: E-c: Detecting Emotions.",
                )
            )
        elif task_id == 2:
            emotion = d["emotion"]
            builder_configs.append(
                datasets.BuilderConfig(
                    name=f"subtask{task_id}.{emotion}.{language}",
                    version=_VERSION,
                    description=f"This is the {language}-{emotion} dataset of subtask 2: EI-oc: Emotion Intensity Ordinal Classiﬁcation.",
                )
            )
        elif task_id == 1:
            emotion = d["emotion"]
            builder_configs.append(
                datasets.BuilderConfig(
                    name=f"subtask{task_id}.{emotion}.{language}",
                    version=_VERSION,
                    description=f"This is the {language}-{emotion} dataset of subtask 1: EI-reg: Emotion Intensity Regression.",
                )
            )
        else:
            raise ValueError()
    return builder_configs


class SemEval2018Task1(datasets.GeneratorBasedBuilder):
    VERSION = _VERSION
    BUILDER_CONFIGS = _generate_builder_configs()

    def _info(self):
        task_id = parse_subset_string(self.config.name)["task_id"]

        if task_id == 1:
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "Tweet": datasets.Value("string"),
                    "affect": datasets.Value("string"),
                    "intensity": datasets.Value("float"),
                }
            )
        elif task_id == 2:
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "Tweet": datasets.Value("string"),
                    "affect": datasets.Value("string"),
                    "intensity": datasets.Value("int8"),
                }
            )
        elif task_id == 5:
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "Tweet": datasets.Value("string"),
                    "anger": datasets.Value("bool"),
                    "anticipation": datasets.Value("bool"),
                    "disgust": datasets.Value("bool"),
                    "fear": datasets.Value("bool"),
                    "joy": datasets.Value("bool"),
                    "love": datasets.Value("bool"),
                    "optimism": datasets.Value("bool"),
                    "pessimism": datasets.Value("bool"),
                    "sadness": datasets.Value("bool"),
                    "surprise": datasets.Value("bool"),
                    "trust": datasets.Value("bool"),
                }
            )
        else:
            raise ValueError()

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def get_filepath(self, data_dir, split_file):
        d = parse_subset_string(self.config.name)
        if d["language"] == "english":
            lang_short = "En"
            lang_long = "English"
        elif d["language"] == "spanish":
            lang_short = "Es"
            lang_long = "Spanish"
        elif d["language"] == "arabic":
            lang_short = "Ar"
            lang_long = "Arabic"
        else:
            raise ValueError()

        if d["task_id"] in [1, 2]:

            if d["task_id"] == 2:
                task_code = "EI-oc"
            elif d["task_id"] == 1:
                task_code = "EI-reg"
            else:
                raise ValueError()

            subfolder_names = {
                "train": "training",
                "test-gold": "test-gold",
                "dev": "development",
            }
            subfolder_name = subfolder_names[split_file]
            base_subtask_path = f"{task_code}/{subfolder_name}/"

            if not (subfolder_name == "training" and lang_long == "English"):
                # NOTE: this is due to some weirdness in the dataset formatting, where English training
                #  is the only data that doesn't have `2018-` at the beginning of the filename
                base_subtask_path = base_subtask_path + "2018-"

            subtask_path = f"{base_subtask_path}{task_code}-{lang_short}-{d['emotion']}"

        elif d["task_id"] == 5:
            subtask_path = "E-c/2018-E-c-" + lang_short
        else:
            raise ValueError()
        return os.path.join(
            data_dir[0],
            f"SemEval2018-Task1-all-data/{lang_long}/{subtask_path}-{split_file}.txt",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        splits = {
            datasets.Split.TRAIN: "train",
            datasets.Split.TEST: "test-gold",
            datasets.Split.VALIDATION: "dev",
        }
        split_generators = []
        for split_type, split_file in splits.items():
            filepath = self.get_filepath(data_dir, split_file)
            sg = datasets.SplitGenerator(
                name=split_type,
                gen_kwargs={"filepath": filepath, "split": None},
            )
            split_generators.append(sg)

        return split_generators

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""
        task_id = parse_subset_string(self.config.name)["task_id"]

        with open(filepath, encoding="utf-8") as f:
            next(f)  # skip header
            for id_, row in enumerate(f):
                data = row.split("\t")

                if task_id == 1:
                    yield id_, {
                        "ID": data[0],
                        "Tweet": data[1],
                        "affect": data[2],
                        "intensity": float(data[3]),
                    }
                elif task_id == 2:
                    yield id_, {
                        "ID": data[0],
                        "Tweet": data[1],
                        "affect": data[2],
                        "intensity": int(data[3][0]),
                    }
                elif task_id == 5:
                    yield id_, {
                        "ID": data[0],
                        "Tweet": data[1],
                        "anger": int(data[2]),
                        "anticipation": int(data[3]),
                        "disgust": int(data[4]),
                        "fear": int(data[5]),
                        "joy": int(data[6]),
                        "love": int(data[7]),
                        "optimism": int(data[8]),
                        "pessimism": int(data[9]),
                        "sadness": int(data[10]),
                        "surprise": int(data[11]),
                        "trust": int(data[12]),
                    }
                else:
                    raise ValueError()
