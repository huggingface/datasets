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
"""Dataset for ProtoQA ("family feud") data. The dataset is gathered from an existing set of questions played in a long-running international game show – FAMILY-FEUD."""


import json

import datasets


_CITATION = """\
@InProceedings{huggingface:dataset,
title = {ProtoQA: A Question Answering Dataset for Prototypical Common-Sense Reasoning},
authors={Michael Boratko, Xiang Lorraine Li, Tim O’Gorman, Rajarshi Das, Dan Le, Andrew McCallum},
year={2020},
publisher = {GitHub},
journal = {GitHub repository},
howpublished={\\url{https://github.com/iesl/protoqa-data}},
}
"""

_DESCRIPTION = """\
This dataset is for studying computational models trained to reason about prototypical situations. Using deterministic filtering a sampling from a larger set of all transcriptions was built. It contains 9789 instances where each instance represents a survey question from Family Feud game. Each instance exactly is a question, a set of answers, and a count associated with each answer.
Each line is a json dictionary, in which:
1. question - contains the question (in original and a normalized form)
2. answerstrings - contains the original answers provided by survey respondents (when available), along with the counts for each string. Because the FamilyFeud data has only cluster names rather than strings, those cluster names are included with 0 weight.
3. answer-clusters - lists clusters, with the count of each cluster and the strings included in that cluster. Each cluster is given a unique ID that can be linked to in the assessment files.

"""

_HOMEPAGE = "https://github.com/iesl/protoqa-data"

_LICENSE = "cc-by-4.0"

_URLs = {
    "proto_qa": {
        "dev": "https://raw.githubusercontent.com/iesl/protoqa-data/9fb72b4e7d41a7d3a9766c33ef66c78d7a100b41/data/dev/protoqa_scraped_dev.jsonl",
        "train": "https://raw.githubusercontent.com/iesl/protoqa-data/9fb72b4e7d41a7d3a9766c33ef66c78d7a100b41/data/train/protoqa_train.jsonl",
    },
    "proto_qa_cs": "https://raw.githubusercontent.com/iesl/protoqa-data/9fb72b4e7d41a7d3a9766c33ef66c78d7a100b41/data/dev/crowdsource_dev.jsonl",
    "proto_qa_cs_assessments": "https://raw.githubusercontent.com/iesl/protoqa-data/9fb72b4e7d41a7d3a9766c33ef66c78d7a100b41/data/dev/crowdsource_dev.assessments.jsonl",
}


class ProtoQA(datasets.GeneratorBasedBuilder):
    """This is a question answering dataset for Prototypical Common-Sense Reasoning"""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="proto_qa",
            version=VERSION,
            description="This is a question answering dataset for Prototypical Common-Sense Reasoning",
        ),
        datasets.BuilderConfig(
            name="proto_qa_cs",
            version=VERSION,
            description="Prototypical Common-Sense Reasoning, 51 questions collected with exhaustive answer collection and manual clustering, matching the details of the eval test set",
        ),
        datasets.BuilderConfig(
            name="proto_qa_cs_assessments",
            version=VERSION,
            description="Prototypical Common-Sense Reasoning, assessment file for study of assessment methods",
        ),
    ]

    DEFAULT_CONFIG_NAME = "proto_qa"

    def _info(self):
        if self.config.name == "proto_qa_cs_assessments":
            features = datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "assessments": datasets.Sequence(datasets.Value("string")),
                }
            )
        else:

            if self.config.name == "proto_qa_cs":
                label = "answers-cleaned"
            else:
                label = "answer-clusters"
            features = datasets.Features(
                {
                    "normalized-question": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    label: datasets.Sequence(
                        {
                            "count": datasets.Value("int32"),
                            "clusterid": datasets.Value("string"),
                            "answers": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                    "answerstrings": datasets.Sequence(datasets.Value("string")),
                    "totalcount": datasets.Value("int32"),
                    "id": datasets.Value("string"),
                    "source": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
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

        if self.config.name == "proto_qa":
            train_fpath = dl_manager.download(_URLs[self.config.name]["train"])
            dev_fpath = dl_manager.download(_URLs[self.config.name]["dev"])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": train_fpath,
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": dev_fpath,
                    },
                ),
            ]
        else:
            filepath = dl_manager.download(_URLs[self.config.name])
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": filepath,
                    },
                )
            ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        if self.config.name == "proto_qa_cs_assessments":
            with open(filepath, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    question = data["question"]
                    assessments = data["assessments"]

                    yield id_, {"question": question, "assessments": assessments}

        else:
            if self.config.name == "proto_qa_cs":
                label = "answers-cleaned"
            else:
                label = "answer-clusters"

            with open(filepath, encoding="utf-8") as f:

                for id_, row in enumerate(f):

                    data = json.loads(row)

                    normalized_question = data["question"]["normalized-question"]
                    question = data["question"]["question"]

                    answer_clusters = data[label]

                    details = []
                    for answer_cluster in answer_clusters:
                        count = answer_cluster["count"]
                        answers = answer_cluster["answers"]
                        clusterid = answer_cluster["clusterid"]
                        details.append({"count": count, "answers": answers, "clusterid": clusterid})

                    answerstrings = data["answerstrings"]
                    metadata = data["metadata"]
                    yield id_, {
                        "normalized-question": normalized_question,
                        "question": question,
                        label: details,
                        "answerstrings": answerstrings,
                        "totalcount": metadata["totalcount"],
                        "id": metadata["id"],
                        "source": metadata["source"],
                    }
