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
"""Introduction to the myPOS Corpus (Myanmar Part-of-Speech Corpus) for Myanmar language NLP Research and Developments"""

import logging

import datasets


_CITATION = """\
@inproceedings{khin-war-war-htike-2017-cicling,
    title = "Comparison of Six POS Tagging Methods on 10K Sentences Myanmar Language (Burmese) POS Tagged Corpus",
    author = "Khin War War Htike, Ye Kyaw Thu, Zuping Zhang, Win Pa Pa, Yoshinori Sagisaka and Naoto Iwahashi",
    booktitle = "Proceedings of the 18th International Conference on Computational Linguistics and Intelligent Text Processing",
    year = "2017",
}
"""

_DESCRIPTION = """\
myPOS Corpus (Myanmar Part-of-Speech Corpus) for Myanmar language NLP Research and Developments
"""

_URL = "https://raw.githubusercontent.com/hungluumfc/burmese-data/main/myPOS/"
_TRAINING_FILE = "train.txt"
_DEV_FILE = "dev.txt"
_TEST_FILE = "test.txt"


class myPOS2017Config(datasets.BuilderConfig):
    """BuilderConfig for myPOS2017"""

    def __init__(self, **kwargs):
        """BuilderConfig for myPOS2017.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(myPOS2017Config, self).__init__(**kwargs)


class Mypos(datasets.GeneratorBasedBuilder):
    """myPOS2017 dataset."""

    BUILDER_CONFIGS = [
        myPOS2017Config(name="myPOS2017", version=datasets.Version("1.0.0"), description="myPOS2017 dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "abb",
                                "adj",
                                "adv",
                                "conj",
                                "fw",
                                "int",
                                "n",
                                "num",
                                "part",
                                "ppm",
                                "pron",
                                "punc",
                                "sb",
                                "tn",
                                "v",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/ye-kyaw-thu/myPOS",
            citation=_CITATION,
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
            pos_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "pos_tags": pos_tags,
                        }
                        guid += 1
                        tokens = []
                        pos_tags = []
                else:
                    # conll2003 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    pos_tags.append(splits[1])
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "pos_tags": pos_tags,
            }
