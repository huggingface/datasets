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
"""GrailQA: The Strongly Generalizable Question Answering Dataset"""


import json
import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@misc{gu2020iid,
    title={Beyond I.I.D.: Three Levels of Generalization for Question Answering on Knowledge Bases},
    author={Yu Gu and Sue Kase and Michelle Vanni and Brian Sadler and Percy Liang and Xifeng Yan and Yu Su},
    year={2020},
    eprint={2011.07743},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Strongly Generalizable Question Answering (GrailQA) is a new large-scale, \
high-quality dataset for question answering on knowledge bases (KBQA) on Freebase with 64,331 questions annotated \
with both answers and corresponding logical forms in different syntax (i.e., SPARQL, S-expression, etc.). \
It can be used to test three levels of generalization in KBQA: i.i.d., compositional, and zero-shot.
"""

_URL = "https://dl.orangedox.com/WyaCpL?dl=1"


class GrailQA(datasets.GeneratorBasedBuilder):
    """GrailQA: The Strongly Generalizable Question Answering Dataset"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "qid": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answer": datasets.features.Sequence(
                        {
                            "answer_type": datasets.Value("string"),
                            "answer_argument": datasets.Value("string"),
                            "entity_name": datasets.Value("string"),
                        }
                    ),
                    "function": datasets.Value("string"),
                    "num_node": datasets.Value("int32"),
                    "num_edge": datasets.Value("int32"),
                    "graph_query": {
                        "nodes": datasets.features.Sequence(
                            {
                                "nid": datasets.Value("int32"),
                                "node_type": datasets.Value("string"),
                                "id": datasets.Value("string"),
                                "class": datasets.Value("string"),
                                "friendly_name": datasets.Value("string"),
                                "question_node": datasets.Value("int32"),
                                "function": datasets.Value("string"),
                            }
                        ),
                        "edges": datasets.features.Sequence(
                            {
                                "start": datasets.Value("int32"),
                                "end": datasets.Value("int32"),
                                "relation": datasets.Value("string"),
                                "friendly_name": datasets.Value("string"),
                            }
                        ),
                    },
                    "sparql_query": datasets.Value("string"),
                    "domains": datasets.features.Sequence(datasets.Value("string")),
                    "level": datasets.Value("string"),
                    "s_expression": datasets.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://dki-lab.github.io/GrailQA/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_path = os.path.join(dl_manager.download_and_extract(_URL), "GrailQA_v1.0")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(dl_path, "grailqa_v1.0_train.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(dl_path, "grailqa_v1.0_dev.json")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(dl_path, "grailqa_v1.0_test_public.json")},
            ),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            samples = json.load(f)
            for sample in samples:
                features = {
                    "qid": str(sample["qid"]),
                    "question": sample["question"],
                    "function": sample.get("function", ""),
                    "num_node": sample.get("num_node", -1),
                    "num_edge": sample.get("num_edge", -1),
                    "graph_query": sample.get("graph_query", {"nodes": [], "edges": []}),
                    "sparql_query": sample.get("sparql_query", ""),
                    "domains": sample.get("domains", []),
                    "level": sample.get("level", ""),
                    "s_expression": sample.get("s_expression", ""),
                }

                answers = sample.get("answer", [])
                for answer in answers:
                    if "entity_name" not in answer:
                        answer["entity_name"] = ""

                features["answer"] = answers
                yield sample["qid"], features
