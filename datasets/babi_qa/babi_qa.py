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
"""The bAbI tasks dataset."""


import datasets


_CITATION = """\
@misc{weston2015aicomplete,
      title={Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks},
      author={Jason Weston and Antoine Bordes and Sumit Chopra and Alexander M. Rush and Bart van Merriënboer and Armand Joulin and Tomas Mikolov},
      year={2015},
      eprint={1502.05698},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
"""


_DESCRIPTION = """\
The (20) QA bAbI tasks are a set of proxy tasks that evaluate reading
comprehension via question answering. Our tasks measure understanding
in several ways: whether a system is able to answer questions via chaining facts,
simple induction, deduction and many more. The tasks are designed to be prerequisites
for any system that aims to be capable of conversing with a human.
The aim is to classify these tasks into skill sets,so that researchers
can identify (and then rectify)the failings of their systems.
"""

_HOMEPAGE = "https://research.fb.com/downloads/babi/"

_LICENSE = """Creative Commons Attribution 3.0 License"""

ZIP_URL = "http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz"
paths = {
    "en": {
        "qa9": {
            "test": "tasks_1-20_v1-2/en/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/en/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/en/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/en/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/en/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/en/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/en/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/en/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa15_basic-deduction_train.txt",
        },
        "out.txt": {"out": "tasks_1-20_v1-2/en/out.txt"},
        "qa17": {
            "test": "tasks_1-20_v1-2/en/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/en/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/en/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/en/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/en/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/en/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/en/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/en/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/en/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/en/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/en/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/en/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/en/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/en/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/en/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/en/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/en/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/en/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/en/qa8_lists-sets_test.txt",
        },
    },
    "en-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/en-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/en-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/en-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/en-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/en-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/en-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/en-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/en-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/en-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/en-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/en-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/en-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa8_lists-sets_test.txt",
        },
    },
    "en-valid": {
        "qa5": {
            "train": "tasks_1-20_v1-2/en-valid/qa5_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa5_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa5_valid.txt",
        },
        "qa16": {
            "valid": "tasks_1-20_v1-2/en-valid/qa16_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa16_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa16_train.txt",
        },
        "qa2": {
            "valid": "tasks_1-20_v1-2/en-valid/qa2_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa2_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa2_train.txt",
        },
        "qa15": {
            "train": "tasks_1-20_v1-2/en-valid/qa15_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa15_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa15_valid.txt",
        },
        "qa9": {
            "test": "tasks_1-20_v1-2/en-valid/qa9_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa9_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa9_valid.txt",
        },
        "qa1": {
            "valid": "tasks_1-20_v1-2/en-valid/qa1_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa1_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa1_train.txt",
        },
        "qa4": {
            "test": "tasks_1-20_v1-2/en-valid/qa4_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa4_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa4_valid.txt",
        },
        "qa14": {
            "valid": "tasks_1-20_v1-2/en-valid/qa14_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa14_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa14_test.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-valid/qa3_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa3_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa3_valid.txt",
        },
        "qa6": {
            "valid": "tasks_1-20_v1-2/en-valid/qa6_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa6_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa6_train.txt",
        },
        "qa8": {
            "test": "tasks_1-20_v1-2/en-valid/qa8_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa8_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa8_train.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-valid/qa20_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa20_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa20_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-valid/qa11_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa11_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa11_valid.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-valid/qa12_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa12_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa12_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-valid/qa13_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa13_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa13_train.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-valid/qa7_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa7_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa7_valid.txt",
        },
        "qa19": {
            "valid": "tasks_1-20_v1-2/en-valid/qa19_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa19_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa19_train.txt",
        },
        "qa17": {
            "train": "tasks_1-20_v1-2/en-valid/qa17_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa17_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa17_valid.txt",
        },
        "qa10": {
            "test": "tasks_1-20_v1-2/en-valid/qa10_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa10_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa10_train.txt",
        },
        "qa18": {
            "valid": "tasks_1-20_v1-2/en-valid/qa18_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa18_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa18_test.txt",
        },
    },
    "en-valid-10k": {
        "qa5": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa5_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa5_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa5_valid.txt",
        },
        "qa16": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa16_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa16_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa16_train.txt",
        },
        "qa2": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa2_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa2_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa2_train.txt",
        },
        "qa15": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa15_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa15_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa15_valid.txt",
        },
        "qa9": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa9_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa9_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa9_valid.txt",
        },
        "qa1": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa1_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa1_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa1_train.txt",
        },
        "qa4": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa4_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa4_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa4_valid.txt",
        },
        "qa14": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa14_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa14_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa14_test.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa3_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa3_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa3_valid.txt",
        },
        "qa6": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa6_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa6_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa6_train.txt",
        },
        "qa8": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa8_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa8_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa8_train.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa20_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa20_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa20_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa11_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa11_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa11_valid.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa12_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa12_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa12_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa13_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa13_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa13_train.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa7_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa7_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa7_valid.txt",
        },
        "qa19": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa19_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa19_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa19_train.txt",
        },
        "qa17": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa17_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa17_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa17_valid.txt",
        },
        "qa10": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa10_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa10_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa10_train.txt",
        },
        "qa18": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa18_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa18_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa18_test.txt",
        },
    },
    "hn": {
        "qa9": {
            "test": "tasks_1-20_v1-2/hn/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/hn/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/hn/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/hn/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/hn/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/hn/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/hn/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/hn/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/hn/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/hn/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/hn/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/hn/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/hn/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/hn/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/hn/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/hn/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/hn/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/hn/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/hn/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/hn/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa8_lists-sets_test.txt",
        },
    },
    "hn-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/hn-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/hn-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/hn-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/hn-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/hn-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/hn-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/hn-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/hn-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/hn-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/hn-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/hn-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/hn-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/hn-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/hn-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/hn-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/hn-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/hn-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/hn-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/hn-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/hn-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa8_lists-sets_test.txt",
        },
    },
    "shuffled": {
        "qa9": {
            "test": "tasks_1-20_v1-2/shuffled/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/shuffled/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/shuffled/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/shuffled/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/shuffled/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/shuffled/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/shuffled/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/shuffled/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/shuffled/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/shuffled/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/shuffled/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/shuffled/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/shuffled/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/shuffled/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/shuffled/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/shuffled/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/shuffled/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/shuffled/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/shuffled/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/shuffled/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa8_lists-sets_test.txt",
        },
    },
    "shuffled-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa8_lists-sets_test.txt",
        },
    },
}


class BabiQaConfig(datasets.BuilderConfig):
    def __init__(self, *args, type=None, task_no=None, **kwargs):
        super().__init__(
            *args,
            name=f"{type}-{task_no}",
            **kwargs,
        )
        self.type = type
        self.task_no = task_no


class BabiQa(datasets.GeneratorBasedBuilder):
    """The bAbI QA (20) tasks Dataset"""

    VERSION = datasets.Version("1.2.0")

    BUILDER_CONFIG_CLASS = BabiQaConfig

    BUILDER_CONFIGS = [
        BabiQaConfig(
            type="en",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `shuffled-10k` dataset",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "story": datasets.Sequence(
                    {
                        "id": datasets.Value("string"),
                        "type": datasets.ClassLabel(names=["context", "question"]),
                        "text": datasets.Value("string"),
                        "supporting_ids": datasets.Sequence(datasets.Value("string")),
                        "answer": datasets.Value("string"),
                    }
                ),
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
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = ZIP_URL
        archive = dl_manager.download(my_urls)
        splits = [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": paths[self.config.type][self.config.task_no]["train"],
                    "files": dl_manager.iter_archive(archive),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": paths[self.config.type][self.config.task_no]["test"],
                    "files": dl_manager.iter_archive(archive),
                },
            ),
        ]
        if "valid" in self.config.type:
            splits += [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": paths[self.config.type][self.config.task_no]["valid"],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        return splits

    def _generate_examples(self, filepath, files):

        for path, f in files:
            if path == filepath:
                story = []
                example_idx = 0
                for idx, line in enumerate(f):
                    line = line.decode("utf-8")
                    if line.strip() == "":
                        if story != []:
                            yield example_idx, {"story": story}
                            example_idx += 1
                            story = []
                    elif line.strip().split()[0] == "1":  # New story
                        if story != []:  # Already some story, flush it out
                            yield example_idx, {"story": story}
                            example_idx += 1
                            story = []
                        line_no = line.split()[0]
                        line_split = line[len(line_no) :].strip().split("\t")
                        if len(line_split) > 1:
                            story.append(
                                {
                                    "id": line_no,
                                    "type": 1,  # question
                                    "supporting_ids": line_split[-1].split(" "),
                                    "text": line_split[0].strip(),
                                    "answer": line_split[1].strip(),
                                }
                            )
                        else:
                            story.append(
                                {
                                    "id": line_no,
                                    "type": 0,  # context
                                    "supporting_ids": [],
                                    "text": line_split[0].strip(),
                                    "answer": "",
                                }
                            )
                    else:
                        line_no = line.split()[0]
                        line_split = line[len(line_no) :].strip().split("\t")
                        if len(line_split) > 1:
                            story.append(
                                {
                                    "id": line_no,
                                    "type": 1,  # question
                                    "supporting_ids": line_split[-1].split(" "),
                                    "text": line_split[0].strip(),
                                    "answer": line_split[1].strip(),
                                }
                            )
                        else:
                            story.append(
                                {
                                    "id": line_no,
                                    "type": 0,  # context
                                    "supporting_ids": [],
                                    "text": line_split[0].strip(),
                                    "answer": "",
                                }
                            )
                else:  # After last line
                    if story != []:
                        yield example_idx, {"story": story}
                break
