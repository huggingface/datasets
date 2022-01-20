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
"""MultiDoc2Dial: Modeling Dialogues Grounded in Multiple Documents"""


import json
import os

import datasets


logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@inproceedings{feng2021multidoc2dial,
    title={MultiDoc2Dial: Modeling Dialogues Grounded in Multiple Documents},
    author={Feng, Song and Patel, Siva Sankalp and Wan, Hui and Joshi, Sachindra},
    booktitle={EMNLP},
    year={2021}
}
"""

_DESCRIPTION = """\
MultiDoc2Dial is a new task and dataset on modeling goal-oriented dialogues grounded in multiple documents. \
Most previous works treat document-grounded dialogue modeling as a machine reading comprehension task based on a \
single given document or passage. We aim to address more realistic scenarios where a goal-oriented information-seeking \
conversation involves multiple topics, and hence is grounded on different documents.
"""

_HOMEPAGE = "https://doc2dial.github.io/multidoc2dial/"


_URL = "https://doc2dial.github.io/multidoc2dial/file/multidoc2dial.zip"


class MultiDoc2dial(datasets.GeneratorBasedBuilder):
    """MultiDoc2Dial v1.0"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="dialogue_domain",
            version=VERSION,
            description="This part of the dataset covers the dialogue domain that has questions, answers and the associated doc ids",
        ),
        datasets.BuilderConfig(
            name="document_domain",
            version=VERSION,
            description="This part of the dataset covers the document domain which details all the documents in the various domains",
        ),
        datasets.BuilderConfig(
            name="multidoc2dial",
            version=VERSION,
            description="Load MultiDoc2Dial dataset for machine reading comprehension tasks",
        ),
    ]

    DEFAULT_CONFIG_NAME = "multidoc2dial"

    def _info(self):

        if self.config.name == "dialogue_domain":
            features = datasets.Features(
                {
                    "dial_id": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "turns": [
                        {
                            "turn_id": datasets.Value("int32"),
                            "role": datasets.Value("string"),
                            "da": datasets.Value("string"),
                            "references": [
                                {
                                    "id_sp": datasets.Value("string"),
                                    "label": datasets.Value("string"),
                                    "doc_id": datasets.Value("string"),
                                }
                            ],
                            "utterance": datasets.Value("string"),
                        }
                    ],
                }
            )

        elif "document_domain" in self.config.name:
            features = datasets.Features(
                {
                    "domain": datasets.Value("string"),
                    "doc_id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "doc_text": datasets.Value("string"),
                    "spans": [
                        {
                            "id_sp": datasets.Value("string"),
                            "tag": datasets.Value("string"),
                            "start_sp": datasets.Value("int32"),
                            "end_sp": datasets.Value("int32"),
                            "text_sp": datasets.Value("string"),
                            "title": datasets.Value("string"),
                            "parent_titles": datasets.features.Sequence(
                                {
                                    "id_sp": datasets.Value("string"),
                                    "text": datasets.Value("string"),
                                    "level": datasets.Value("string"),
                                }
                            ),
                            "id_sec": datasets.Value("string"),
                            "start_sec": datasets.Value("int32"),
                            "text_sec": datasets.Value("string"),
                            "end_sec": datasets.Value("int32"),
                        }
                    ],
                    "doc_html_ts": datasets.Value("string"),
                    "doc_html_raw": datasets.Value("string"),
                }
            )

        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "da": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                    "utterance": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        data_dir = dl_manager.download_and_extract(_URL)

        if self.config.name == "dialogue_domain":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_dial_train.json"),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_dial_validation.json"),
                    },
                ),
            ]
        elif self.config.name == "document_domain":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_doc.json"),
                    },
                )
            ]
        elif "multidoc2dial_" in self.config.name:
            domain = self.config.name.split("_")[-1]
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir,
                            "multidoc2dial_domain",
                            domain,
                            "multidoc2dial_dial_validation.json",
                        ),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir,
                            "multidoc2dial_domain",
                            domain,
                            "multidoc2dial_dial_train.json",
                        ),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(
                            data_dir,
                            "multidoc2dial_domain",
                            domain,
                            "multidoc2dial_dial_test.json",
                        ),
                    },
                ),
            ]
        elif self.config.name == "multidoc2dial":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_dial_validation.json"),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_dial_train.json"),
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multidoc2dial/multidoc2dial_dial_test.json"),
                    },
                ),
            ]

    def _load_doc_data_rc(self, filepath):
        doc_filepath = os.path.join(os.path.dirname(filepath), "multidoc2dial_doc.json")
        with open(doc_filepath, encoding="utf-8") as f:
            data = json.load(f)["doc_data"]
        return data

    def _get_answers_rc(self, references, spans, doc_text):
        """Obtain the grounding annotation for a given dialogue turn"""
        if not references:
            return []
        start, end = -1, -1
        ls_sp = []
        for ele in references:
            id_sp = ele["id_sp"]
            start_sp, end_sp = spans[id_sp]["start_sp"], spans[id_sp]["end_sp"]
            if start == -1 or start > start_sp:
                start = start_sp
            if end < end_sp:
                end = end_sp
            ls_sp.append(doc_text[start_sp:end_sp])
        answer = {"text": doc_text[start:end], "answer_start": start}
        return [answer]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        if self.config.name == "dialogue_domain":
            logger.info("generating examples from = %s", filepath)
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                for domain in data["dial_data"]:
                    for dialogue in data["dial_data"][domain]:
                        x = {
                            "dial_id": dialogue["dial_id"],
                            "turns": dialogue["turns"],
                            "domain": domain,
                        }

                        yield dialogue["dial_id"], x

        elif self.config.name == "document_domain":

            logger.info("generating examples from = %s", filepath)
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                for domain in data["doc_data"]:
                    for doc_id in data["doc_data"][domain]:

                        yield doc_id, {
                            "domain": domain,
                            "doc_id": doc_id,
                            "title": data["doc_data"][domain][doc_id]["title"],
                            "doc_text": data["doc_data"][domain][doc_id]["doc_text"],
                            "spans": [
                                {
                                    "id_sp": data["doc_data"][domain][doc_id]["spans"][i]["id_sp"],
                                    "tag": data["doc_data"][domain][doc_id]["spans"][i]["tag"],
                                    "start_sp": data["doc_data"][domain][doc_id]["spans"][i]["start_sp"],
                                    "end_sp": data["doc_data"][domain][doc_id]["spans"][i]["end_sp"],
                                    "text_sp": data["doc_data"][domain][doc_id]["spans"][i]["text_sp"],
                                    "title": data["doc_data"][domain][doc_id]["spans"][i]["title"],
                                    "parent_titles": data["doc_data"][domain][doc_id]["spans"][i]["parent_titles"],
                                    "id_sec": data["doc_data"][domain][doc_id]["spans"][i]["id_sec"],
                                    "start_sec": data["doc_data"][domain][doc_id]["spans"][i]["start_sec"],
                                    "text_sec": data["doc_data"][domain][doc_id]["spans"][i]["text_sec"],
                                    "end_sec": data["doc_data"][domain][doc_id]["spans"][i]["end_sec"],
                                }
                                for i in data["doc_data"][domain][doc_id]["spans"]
                            ],
                            "doc_html_ts": data["doc_data"][domain][doc_id]["doc_html_ts"],
                            "doc_html_raw": data["doc_data"][domain][doc_id]["doc_html_raw"],
                        }

        elif "multidoc2dial" in self.config.name:
            logger.info("generating examples from = %s", filepath)
            doc_data = self._load_doc_data_rc(filepath)
            d_doc_data = {}
            for domain, d_doc in doc_data.items():
                for doc_id, data in d_doc.items():
                    d_doc_data[doc_id] = data
            with open(filepath, encoding="utf-8") as f:
                dial_data = json.load(f)["dial_data"]
                for domain, dialogues in dial_data.items():
                    for dial in dialogues:
                        all_prev_utterances = []
                        for idx, turn in enumerate(dial["turns"]):
                            doc_id = turn["references"][0]["doc_id"]
                            doc = d_doc_data[doc_id]
                            utterance_line = turn["utterance"].replace("\n", " ").replace("\t", " ")
                            all_prev_utterances.append("{}: {}".format(turn["role"], utterance_line))
                            if turn["role"] == "agent":
                                continue
                            if idx + 1 < len(dial["turns"]):
                                if (
                                    dial["turns"][idx + 1]["role"] == "agent"
                                    and dial["turns"][idx + 1]["da"] != "respond_no_solution"
                                ):
                                    turn_to_predict = dial["turns"][idx + 1]
                                else:
                                    continue
                            else:
                                continue
                            question_str = utterance_line + "[SEP]" + "||".join(reversed(all_prev_utterances[:-1]))
                            id_ = "{}_{}".format(dial["dial_id"], turn["turn_id"])
                            qa = {
                                "id": id_,
                                "title": doc_id,
                                "context": doc["doc_text"],
                                "question": question_str,
                                "da": turn["da"],
                                "answers": self._get_answers_rc(
                                    turn_to_predict["references"],
                                    doc["spans"],
                                    doc["doc_text"],
                                ),
                                "utterance": turn_to_predict["utterance"],
                                "domain": domain,
                            }
                            yield id_, qa
