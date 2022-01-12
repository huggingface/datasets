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
"""XCSR: A dataset for cross-lingual commonsense reasoning."""


import json
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
# X-CSR
@inproceedings{lin-etal-2021-xcsr,
    title = "Common Sense Beyond English: Evaluating and Improving Multilingual Language Models for Commonsense Reasoning",
    author = "Lin, Bill Yuchen and Lee, Seyeon and Qiao, Xiaoyang and Ren, Xiang",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL-IJCNLP 2021)",
    year = "2021",
    note={to appear}
}

# CSQA
@inproceedings{Talmor2019commonsenseqaaq,
    address = {Minneapolis, Minnesota},
    author = {Talmor, Alon  and Herzig, Jonathan  and Lourie, Nicholas and Berant, Jonathan},
    booktitle = {Proceedings of the 2019 Conference of the North {A}merican Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)},
    doi = {10.18653/v1/N19-1421},
    pages = {4149--4158},
    publisher = {Association for Computational Linguistics},
    title = {CommonsenseQA: A Question Answering Challenge Targeting Commonsense Knowledge},
    url = {https://www.aclweb.org/anthology/N19-1421},
    year = {2019}
}

# CODAH
@inproceedings{Chen2019CODAHAA,
    address = {Minneapolis, USA},
    author = {Chen, Michael  and D{'}Arcy, Mike  and Liu, Alisa  and Fernandez, Jared  and Downey, Doug},
    booktitle = {Proceedings of the 3rd Workshop on Evaluating Vector Space Representations for {NLP}},
    doi = {10.18653/v1/W19-2008},
    pages = {63--69},
    publisher = {Association for Computational Linguistics},
    title = {CODAH: An Adversarially-Authored Question Answering Dataset for Common Sense},
    url = {https://www.aclweb.org/anthology/W19-2008},
    year = {2019}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
To evaluate multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting (X-CSR), i.e., training in English and test in other languages, we create two benchmark datasets, namely X-CSQA and X-CODAH. Specifically, we automatically translate the original CSQA and CODAH datasets, which only have English versions, to 15 other languages, forming development and test sets for studying X-CSR. As our goal is to evaluate different ML-LMs in a unified evaluation protocol for X-CSR, we argue that such translated examples, although might contain noise, can serve as a starting benchmark for us to obtain meaningful analysis, before more human-translated datasets will be available in the future.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://inklab.usc.edu//XCSR/"

# TODO: Add the licence for the dataset here if you can find it
# _LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)

_URL = "https://inklab.usc.edu/XCSR/xcsr_datasets.zip"

_LANGUAGES = ("en", "zh", "de", "es", "fr", "it", "jap", "nl", "pl", "pt", "ru", "ar", "vi", "hi", "sw", "ur")


class XcsrConfig(datasets.BuilderConfig):
    """BuilderConfig for XCSR."""

    def __init__(self, name: str, language: str, languages=None, **kwargs):
        """BuilderConfig for XCSR.
        Args:
        language: One of {en, zh, de, es, fr, it, jap, nl, pl, pt, ru, ar, vi, hi, sw, ur}, or all_languages
          **kwargs: keyword arguments forwarded to super.
        """
        super(XcsrConfig, self).__init__(**kwargs)
        self.name = name
        self.language = language


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class Xcsr(datasets.GeneratorBasedBuilder):
    """XCSR: A dataset for evaluating multi-lingual language models (ML-LMs) for commonsense reasoning in a cross-lingual zero-shot transfer setting"""

    VERSION = datasets.Version("1.1.0", "")
    BUILDER_CONFIG_CLASS = XcsrConfig
    BUILDER_CONFIGS = [
        XcsrConfig(
            name="X-CSQA-" + lang,
            language="en",
            version=datasets.Version("1.1.0", ""),
            description=f"Plain text import of X-CSQA for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        XcsrConfig(
            name="X-CODAH-" + lang,
            language=lang,
            version=datasets.Version("1.1.0", ""),
            description=f"Plain text import of X-CODAH for the {lang} language",
        )
        for lang in _LANGUAGES
    ]

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name.startswith("X-CSQA"):
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "question": datasets.features.Sequence(
                        {
                            "stem": datasets.Value("string"),
                            "choices": datasets.features.Sequence(
                                {
                                    "label": datasets.Value("string"),
                                    "text": datasets.Value("string"),
                                }
                            ),
                        }
                    ),
                    "answerKey": datasets.Value("string"),
                }
            )
        elif self.config.name.startswith("X-CODAH"):
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "lang": datasets.Value("string"),
                    "question_tag": datasets.Value("string"),
                    "question": datasets.features.Sequence(
                        {
                            "stem": datasets.Value("string"),
                            "choices": datasets.features.Sequence(
                                {
                                    "label": datasets.Value("string"),
                                    "text": datasets.Value("string"),
                                }
                            ),
                        }
                    ),
                    "answerKey": datasets.Value("string"),
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
            # license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)
        if self.config.name.startswith("X-CSQA"):
            sub_test_path = "X-CSR_datasets/X-CSQA/" + self.config.language + "/test.jsonl"
            sub_dev_path = "X-CSR_datasets/X-CSQA/" + self.config.language + "/dev.jsonl"
        elif self.config.name.startswith("X-CODAH"):
            sub_test_path = "X-CSR_datasets/X-CODAH/" + self.config.language + "/test.jsonl"
            sub_dev_path = "X-CSR_datasets/X-CODAH/" + self.config.language + "/dev.jsonl"

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, sub_test_path),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, sub_dev_path),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        key = 0
        if self.config.name.startswith("X-CSQA"):
            with open(filepath, encoding="utf-8") as f:
                for _id, row in enumerate(f):
                    data = json.loads(row)

                    ID = data["id"]
                    lang = data["lang"]
                    question = data["question"]
                    stem = question["stem"]
                    choices = question["choices"]
                    labels = [label["label"] for label in choices]
                    texts = [text["text"] for text in choices]

                    if split == "test":
                        answerkey = ""
                    else:
                        answerkey = data["answerKey"]

                    yield key, {
                        "id": ID,
                        "lang": lang,
                        "question": {
                            "stem": stem,
                            "choices": [{"label": label, "text": text} for label, text in zip(labels, texts)],
                        },
                        "answerKey": answerkey,
                    }
                    key += 1
        elif self.config.name.startswith("X-CODAH"):
            with open(filepath, encoding="utf-8") as f:
                for _id, row in enumerate(f):
                    data = json.loads(row)
                    ID = data["id"]
                    lang = data["lang"]
                    question_tag = data["question_tag"]
                    question = data["question"]
                    stem = question["stem"]
                    choices = question["choices"]
                    labels = [label["label"] for label in choices]
                    texts = [text["text"] for text in choices]

                    if split == "test":
                        answerkey = ""
                    else:
                        answerkey = data["answerKey"]

                    yield key, {
                        "id": ID,
                        "lang": lang,
                        "question_tag": question_tag,
                        "question": {
                            "stem": stem,
                            "choices": [{"label": label, "text": text} for label, text in zip(labels, texts)],
                        },
                        "answerKey": answerkey,
                    }
                    key += 1
