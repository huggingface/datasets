# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""Introduction to People's Daily Dataset"""

import logging

import datasets


_DESCRIPTION = """\
People's Daily NER Dataset is a commonly used dataset for Chinese NER, with
text from People's Daily (人民日报), the largest official newspaper.

The dataset is in BIO scheme. Entity types are: PER (person), ORG (organization)
and LOC (location).
"""

_URL = "https://raw.githubusercontent.com/OYE93/Chinese-NLP-Corpus/master/NER/People's%20Daily/"
_TRAINING_FILE = "example.train"
_DEV_FILE = "example.dev"
_TEST_FILE = "example.test"


class PeoplesDailyConfig(datasets.BuilderConfig):
    """BuilderConfig for People's Daily NER"""

    def __init__(self, **kwargs):
        """BuilderConfig for People's Daily NER.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(PeoplesDailyConfig, self).__init__(**kwargs)


class PeoplesDailyNer(datasets.GeneratorBasedBuilder):
    """People's Daily NER dataset."""

    BUILDER_CONFIGS = [
        PeoplesDailyConfig(
            name="peoples_daily_ner", version=datasets.Version("1.0.0"), description="People's Daily NER dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/OYE93/Chinese-NLP-Corpus/tree/master/NER/People's%20Daily",
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                line_stripped = line.strip()
                if line_stripped == "":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    splits = line_stripped.split(" ")
                    if len(splits) == 1:
                        splits.append("O")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1])
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
