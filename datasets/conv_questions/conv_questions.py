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
"""
ConvQuestions is the first realistic benchmark for conversational question answering over
knowledge graphs. It contains 11,200 conversations which can be evaluated over Wikidata.
They are compiled from the inputs of 70 Master crowdworkers on Amazon Mechanical Turk,
with conversations from five domains: Books, Movies, Soccer, Music, and TV Series.
The questions feature a variety of complex question phenomena like comparisons, aggregations,
compositionality, and temporal reasoning. Answers are grounded in Wikidata entities to enable
fair comparison across diverse methods. The data gathering setup was kept as natural as
possible, with the annotators selecting entities of their choice from each of the five domains,
and formulating the entire conversation in one session. All questions in a conversation are
from the same Turker, who also provided gold answers to the questions. For suitability to knowledge
graphs, questions were constrained to be objective or factoid in nature, but no other restrictive
guidelines were set. A notable property of ConvQuestions is that several questions are not
answerable by Wikidata alone (as of September 2019), but the required facts can, for example,
be found in the open Web or in Wikipedia. For details, please refer to our CIKM 2019 full paper
(https://dl.acm.org/citation.cfm?id=3358016).
"""


import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{christmann2019look,
  title={Look before you hop: Conversational question answering over knowledge graphs using judicious context expansion},
  author={Christmann, Philipp and Saha Roy, Rishiraj and Abujabal, Abdalghani and Singh, Jyotsna and Weikum, Gerhard},
  booktitle={Proceedings of the 28th ACM International Conference on Information and Knowledge Management},
  pages={729--738},
  year={2019}
}
"""

# You can copy an official description
_DESCRIPTION = """\
ConvQuestions is the first realistic benchmark for conversational question answering over knowledge graphs.
It contains 11,200 conversations which can be evaluated over Wikidata. The questions feature a variety of complex
question phenomena like comparisons, aggregations, compositionality, and temporal reasoning."""

_HOMEPAGE = "https://convex.mpi-inf.mpg.de"

_LICENSE = "CC BY 4.0"

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "http://qa.mpi-inf.mpg.de/convex/"
_URLs = {
    "train": _URL + "ConvQuestions_train.zip",
    "dev": _URL + "ConvQuestions_dev.zip",
    "test": _URL + "ConvQuestions_test.zip",
}


class ConvQuestions(datasets.GeneratorBasedBuilder):
    """ConvQuestions is a realistic benchmark for conversational question answering over knowledge graphs."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        # This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "domain": datasets.Value("string"),
                "seed_entity": datasets.Value("string"),
                "seed_entity_text": datasets.Value("string"),
                "questions": datasets.features.Sequence(datasets.Value("string")),
                "answers": datasets.features.Sequence(datasets.features.Sequence(datasets.Value("string"))),
                "answer_texts": datasets.features.Sequence(datasets.Value("string")),
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
        # This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train"], "train_set/train_set_ALL.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir["dev"], "dev_set/dev_set_ALL.json"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir["test"], "test_set/test_set_ALL.json"), "split": "test"},
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for id_, instance in enumerate(data):
                yield id_, {
                    "domain": instance["domain"],
                    "seed_entity": instance["seed_entity"],
                    "seed_entity_text": instance["seed_entity_text"],
                    "questions": [turn["question"] for turn in instance["questions"]],
                    "answers": [turn["answer"].split(";") for turn in instance["questions"]],
                    "answer_texts": [turn["answer_text"] for turn in instance["questions"]],
                }
