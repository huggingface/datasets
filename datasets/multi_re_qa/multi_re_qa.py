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
"""MultiReQA: A Cross-Domain Evaluation for Retrieval Question Answering Models."""


import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@misc{m2020multireqa,
    title={MultiReQA: A Cross-Domain Evaluation for Retrieval Question Answering Models},
    author={Mandy Guo and Yinfei Yang and Daniel Cer and Qinlan Shen and Noah Constant},
    year={2020},
    eprint={2005.02507},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}"""
# You can copy an official description
_DESCRIPTION = """MultiReQA contains the sentence boundary annotation from eight publicly available QA datasets including SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, BioASQ, RelationExtraction, and TextbookQA. Five of these datasets, including SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, contain both training and test data, and three, including BioASQ, RelationExtraction, TextbookQA, contain only the test data"""

_HOMEPAGE = "https://github.com/google-research-datasets/MultiReQA"

# License for the dataset is not available
_LICENSE = ""

# Official links to the data hosted on github are below
# Train and Dev sets are available only for SearchQA, TriviaQA, HotpotQA, SQuAD and NaturalQuestions
# Test sets are only available for BioASQ, RelationExtraction and TextbookQA

train_SearchQA = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/train/SearchQA/candidates.json.gz"
)
dev_SearchQA = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/dev/SearchQA/candidates.json.gz"

train_TriviaQA = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/train/TriviaQA/candidates.json.gz"
)
dev_TriviaQA = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/dev/TriviaQA/candidates.json.gz"

train_HotpotQA = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/train/HotpotQA/candidates.json.gz"
)
dev_HotpotQA = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/dev/HotpotQA/candidates.json.gz"

train_SQuAD = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/train/SQuAD/candidates.json.gz"
dev_SQuAD = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/dev/SQuAD/candidates.json.gz"

train_NaturalQuestions = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/train/NaturalQuestions/candidates.json.gz"
)
dev_NaturalQuestions = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/dev/NaturalQuestions/candidates.json.gz"
)

test_BioASQ = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/test/BioASQ/candidates.json.gz"

test_RelationExtraction = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/test/RelationExtraction/candidates.json.gz"
)

test_TextbookQA = (
    "https://github.com/google-research-datasets/MultiReQA/raw/master/data/test/TextbookQA/candidates.json.gz"
)

test_DuoRC = "https://github.com/google-research-datasets/MultiReQA/raw/master/data/test/DuoRC/candidates.json.gz"


class MultiReQa(datasets.GeneratorBasedBuilder):
    """MultiReQA contains the sentence boundary annotation from eight publicly available QA datasets including SearchQA, TriviaQA, HotpotQA, NaturalQuestions, SQuAD, BioASQ, RelationExtraction, and TextbookQA."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="SearchQA", version=VERSION, description="SearchQA"),
        datasets.BuilderConfig(name="TriviaQA", version=VERSION, description="TriviaQA"),
        datasets.BuilderConfig(name="HotpotQA", version=VERSION, description="HotpotQA"),
        datasets.BuilderConfig(name="SQuAD", version=VERSION, description="SQuAD"),
        datasets.BuilderConfig(name="NaturalQuestions", version=VERSION, description="NaturalQuestions"),
        datasets.BuilderConfig(name="BioASQ", version=VERSION, description="BioASQ"),
        datasets.BuilderConfig(name="RelationExtraction", version=VERSION, description="RelationExtraction"),
        datasets.BuilderConfig(name="TextbookQA", version=VERSION, description="TextbookQA"),
        datasets.BuilderConfig(name="DuoRC", version=VERSION, description="DuoRC"),
    ]

    # DEFAULT_CONFIG_NAME = "SearchQA"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        # This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        if self.config.name == "SearchQA":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "candidate_id": datasets.Value("string"),
                    "response_start": datasets.Value("int32"),
                    "response_end": datasets.Value("int32"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "candidate_id": datasets.Value("string"),
                    "response_start": datasets.Value("int32"),
                    "response_end": datasets.Value("int32"),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,
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

        if (
            self.config.name == "SearchQA"
            or self.config.name == "TriviaQA"
            or self.config.name == "HotpotQA"
            or self.config.name == "SQuAD"
            or self.config.name == "NaturalQuestions"
        ):
            if self.config.name == "SearchQA":
                train_file_url = train_SearchQA
                dev_file_url = dev_SearchQA

            elif self.config.name == "TriviaQA":
                train_file_url = train_TriviaQA
                dev_file_url = dev_TriviaQA

            elif self.config.name == "HotpotQA":
                train_file_url = train_HotpotQA
                dev_file_url = dev_HotpotQA

            elif self.config.name == "SQuAD":
                train_file_url = train_SQuAD
                dev_file_url = dev_SQuAD

            elif self.config.name == "NaturalQuestions":
                train_file_url = train_NaturalQuestions
                dev_file_url = dev_NaturalQuestions

            train_file = dl_manager.download_and_extract(train_file_url)
            dev_file = dl_manager.download_and_extract(dev_file_url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(train_file),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(dev_file),
                        "split": "dev",
                    },
                ),
            ]
        else:

            if self.config.name == "BioASQ":
                test_file_url = test_BioASQ

            elif self.config.name == "RelationExtraction":
                test_file_url = test_RelationExtraction

            elif self.config.name == "TextbookQA":
                test_file_url = test_TextbookQA

            elif self.config.name == "DuoRC":
                test_file_url = test_DuoRC

            test_file = dl_manager.download_and_extract(test_file_url)

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(test_file),
                        "split": "test",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        # This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                yield id_, {
                    "candidate_id": data["candidate_id"],
                    "response_start": data["response_start"],
                    "response_end": data["response_end"],
                }
