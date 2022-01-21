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
"""QED: A Dataset for Explanations in Question Answering"""


import json

import datasets


_CITATION = """\
@misc{lamm2020qed,
    title={QED: A Framework and Dataset for Explanations in Question Answering},
    author={Matthew Lamm and Jennimaria Palomaki and Chris Alberti and Daniel Andor and Eunsol Choi and Livio Baldini Soares and Michael Collins},
    year={2020},
    eprint={2009.06354},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
QED, is a linguistically informed, extensible framework for explanations in question answering. \
A QED explanation specifies the relationship between a question and answer according to formal semantic notions \
such as referential equality, sentencehood, and entailment. It is an expertannotated dataset of QED explanations \
built upon a subset of the Google Natural Questions dataset.
"""

_HOMEPAGE = "https://github.com/google-research-datasets/QED"

_BASE_URL = "https://raw.githubusercontent.com/google-research-datasets/QED/master/"
_URLS = {
    "train": _BASE_URL + "qed-train.jsonlines",
    "dev": _BASE_URL + "qed-dev.jsonlines",
}


class Qed(datasets.GeneratorBasedBuilder):
    """QED: A Dataset for Explanations in Question Answering"""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="qed", version=datasets.Version("1.0.0")),
    ]

    def _info(self):
        span_features = {
            "start": datasets.Value("int32"),
            "end": datasets.Value("int32"),
            "string": datasets.Value("string"),
        }
        reference_features = {
            "start": datasets.Value("int32"),
            "end": datasets.Value("int32"),
            "bridge": datasets.Value("string"),
            "string": datasets.Value("string"),
        }
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "example_id": datasets.Value("int64"),
                    "title_text": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "paragraph_text": datasets.Value("string"),
                    "sentence_starts": datasets.Sequence(datasets.Value("int32")),
                    "original_nq_answers": [span_features],
                    "annotation": {
                        "referential_equalities": [
                            {
                                "question_reference": span_features,
                                "sentence_reference": reference_features,
                            }
                        ],
                        "answer": [
                            {
                                "sentence_reference": reference_features,
                                "paragraph_reference": span_features,
                            }
                        ],
                        "explanation_type": datasets.Value("string"),
                        "selected_sentence": span_features,
                    },
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_paths = dl_manager.download(_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": downloaded_paths["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": downloaded_paths["dev"]},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            examples = f.readlines()
            for example in examples:
                example = json.loads(example.strip())
                example["question"] = example.pop("question_text")

                # some examples have missing annotation, assign empty values to such examples
                if "answer" not in example["annotation"]:
                    example["annotation"]["answer"] = []
                if "selected_sentence" not in example["annotation"]:
                    example["annotation"]["selected_sentence"] = {
                        "start": -1,
                        "end": -1,
                        "string": "",
                    }
                if "referential_equalities" not in example["annotation"]:
                    example["annotation"]["referential_equalities"] = []
                else:
                    for referential_equalities in example["annotation"]["referential_equalities"]:
                        bridge = referential_equalities["sentence_reference"]["bridge"]
                        referential_equalities["sentence_reference"]["bridge"] = (
                            bridge if bridge is not False else None
                        )

                # remove the nested list
                example["original_nq_answers"] = example["original_nq_answers"][0]

                yield example["example_id"], example
