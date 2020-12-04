# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors.
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
"""Modified ShARC datatset"""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """\
@inproceedings{verma-etal-2020-neural,
    title = "Neural Conversational {QA}: Learning to Reason vs Exploiting Patterns",
    author = "Verma, Nikhil  and
      Sharma, Abhishek  and
      Madan, Dhiraj  and
      Contractor, Danish  and
      Kumar, Harshit  and
      Joshi, Sachindra",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.emnlp-main.589",
    pages = "7263--7269",
    abstract = "Neural Conversational QA tasks such as ShARC require systems to answer questions based on the contents of a given passage. On studying recent state-of-the-art models on the ShARC QA task, we found indications that the model(s) learn spurious clues/patterns in the data-set. Further, a heuristic-based program, built to exploit these patterns, had comparative performance to that of the neural models. In this paper we share our findings about the four types of patterns in the ShARC corpus and how the neural models exploit them. Motivated by the above findings, we create and share a modified data-set that has fewer spurious patterns than the original data-set, consequently allowing models to learn better.",
}
"""

_DESCRIPTION = """\
ShARC, a conversational QA task, requires a system to answer user questions based on rules expressed in natural language text. \
However, it is found that in the ShARC dataset there are multiple spurious patterns that could be exploited by neural models. \
SharcModified is a new dataset which reduces the patterns identified in the original dataset. \
To reduce the sensitivity of neural models, for each occurence of an instance conforming to any of the patterns, \
we automatically construct alternatives where we choose to either replace the current instance with an alternative \
instance which does not exhibit the pattern; or retain the original instance. \
The modified ShARC has two versions sharc-mod and history-shuffled. For morre details refer to Appendix A.3 .
"""

_BASE_URL = "https://raw.githubusercontent.com/nikhilweee/neural-conv-qa/master/datasets"


class SharcModifiedConfig(datasets.BuilderConfig):
    """BuilderConfig for SharcModified."""

    def __init__(self, **kwargs):
        """BuilderConfig for MedHop.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SharcModifiedConfig, self).__init__(**kwargs)


class SharcModified(datasets.GeneratorBasedBuilder):
    """Modified ShARC datatset"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        SharcModifiedConfig(
            name="mod",
            version=datasets.Version("1.0.0"),
            description="The modified ShARC dataset.",
        ),
        SharcModifiedConfig(
            name="mod_dev_multi",
            version=datasets.Version("1.0.0"),
            description="The modified ShARC dev dataset with multiple references.",
        ),
        SharcModifiedConfig(
            name="history", version=datasets.Version("1.0.0"), description="History-Shuffled ShARC dataset."
        ),
        SharcModifiedConfig(
            name="history_dev_multi",
            version=datasets.Version("1.0.0"),
            description="History-Shuffled dev dataset with multiple references.",
        ),
    ]
    BUILDER_CONFIG_CLASS = SharcModifiedConfig

    def _info(self):
        features = {
            "id": datasets.Value("string"),
            "utterance_id": datasets.Value("string"),
            "source_url": datasets.Value("string"),
            "snippet": datasets.Value("string"),
            "question": datasets.Value("string"),
            "scenario": datasets.Value("string"),
            "history": [
                {"follow_up_question": datasets.Value("string"), "follow_up_answer": datasets.Value("string")}
            ],
            "evidence": [
                {"follow_up_question": datasets.Value("string"), "follow_up_answer": datasets.Value("string")}
            ],
            "answer": datasets.Value("string"),
        }

        if self.config.name in ["mod_dev_multi", "history_dev_multi"]:
            features["all_answers"] = datasets.Sequence(datasets.Value("string"))

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage="https://github.com/nikhilweee/neural-conv-qa",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        if self.config.name in ["mod_dev_multi", "history_dev_multi"]:
            url = f"{_BASE_URL}/{self.config.name}.json"
            downloaded_file = dl_manager.download(url)
            return [datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_file})]

        urls = {
            "train": f"{_BASE_URL}/{self.config.name}_train.json",
            "dev": f"{_BASE_URL}/{self.config.name}_dev.json",
        }
        downloaded_files = dl_manager.download(urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_files["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_files["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = json.load(f)
            for i, example in enumerate(examples):
                example.pop("tree_id")
                example["id"] = example["utterance_id"]
                # the keys are misspelled for one of the example in dev set, fix it here
                for evidence in example["evidence"]:
                    if evidence.get("followup_answer") is not None:
                        evidence["follow_up_answer"] = evidence.pop("followup_answer")
                    if evidence.get("followup_question") is not None:
                        evidence["follow_up_question"] = evidence.pop("followup_question")
                yield example["id"], example
