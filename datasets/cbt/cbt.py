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
""" Children's Book Test (CBT): Sentence completion given a few sentences as context from a children's book. """

from __future__ import absolute_import, division, print_function

import os
import re

import datasets


_CITATION = """\
@misc{hill2016goldilocks,
      title={The Goldilocks Principle: Reading Children's Books with Explicit Memory Representations},
      author={Felix Hill and Antoine Bordes and Sumit Chopra and Jason Weston},
      year={2016},
      eprint={1511.02301},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
The Children’s Book Test (CBT), designed to measure directly how well language models can exploit wider linguistic context.
The CBT is built from books that are freely available thanks to Project Gutenberg (https://www.gutenberg.org/). Details and baseline results on this dataset can be found in the paper.

After allocating books to either training, validation or test sets, example ‘questions’ are formed from chapters in the book by enumerating 21 consecutive sentences.
In each question, the first 20 sentences form the context, and a word is removed from the 21st sentence, which becomes the query.
Models must identify the answer word among a selection of 10 candidate answers appearing in the context sentences and the query.
For finer-grained analyses, four classes of question are evaluated by removing distinct types of word: Named Entities, (Common) Nouns, Verbs and Prepositions.

We use the data provided by the ParlAI project at https://github.com/facebookresearch/ParlAI.
"""

_LICENSE = ""

_URLs = "http://parl.ai/downloads/cbt/cbt.tar.gz"

CONFIG_TO_FILENAME = {
    "all_questions": ["cbtest_NE", "cbtest_CN", "cbtest_V", "cbtest_P"],
    "named_entities": "cbtest_NE",
    "nouns": "cbtest_CN",
    "verbs": "cbtest_V",
    "prepositions": "cbtest_P",
    "books": "cbt",
}

SPLIT_TO_FILESUFFIX = {
    datasets.Split.TRAIN: "train",
    datasets.Split.VALIDATION: "valid_2000ex",
    datasets.Split.TEST: "test_2500ex",
}

SPLIT_TO_FILESUFFIX_BOOKS = {
    datasets.Split.TRAIN: "train",
    datasets.Split.VALIDATION: "valid",
    datasets.Split.TEST: "test",
}


class CBT(datasets.GeneratorBasedBuilder):
    """ Children's Book Test (CBT): Sentence completion given a few sentences as context from a children's book."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="all_questions", description="All questions"),
        datasets.BuilderConfig(name="named_entities", description="Only questions over Named Entities"),
        datasets.BuilderConfig(name="nouns", description="Only questions over (Common) Nouns"),
        datasets.BuilderConfig(name="verbs", description="Only questions over Verbs"),
        datasets.BuilderConfig(name="prepositions", description="Only questions over Prepositions"),
        datasets.BuilderConfig(name="books", description="The books content in CBT (tokenized)."),
    ]

    DEFAULT_CONFIG_NAME = "all_questions"

    def _info(self):
        if self.config.name == "books":  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "book_id": datasets.Value("int32"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "context": datasets.Sequence(datasets.Value("string"), length=20),
                    "query": datasets.Value("string"),
                    "candidates": datasets.Sequence(datasets.Value("string")),
                    "answer": datasets.Value("string"),
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
            homepage="https://research.fb.com/downloads/babi/",
            # License for the dataset if available
            license=_LICENSE,
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
        data_dir = dl_manager.download_and_extract(_URLs)
        data_dir = os.path.join(data_dir, "CBTest", "data")
        file_prefix = CONFIG_TO_FILENAME[self.config.name]
        if self.config.name == "books":
            return [
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, f"{file_prefix}_{SPLIT_TO_FILESUFFIX_BOOKS[split]}.txt"),
                        "split": str(split),
                    },
                )
                for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
            ]
        elif self.config.name == "all_questions":
            return [
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "filepath": [
                            os.path.join(data_dir, f"{fp}_{SPLIT_TO_FILESUFFIX[split]}.txt") for fp in file_prefix
                        ],
                        "split": str(split),
                    },
                )
                for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=split,
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, f"{file_prefix}_{SPLIT_TO_FILESUFFIX[split]}.txt"),
                        "split": str(split),
                    },
                )
                for split in [datasets.Split.TRAIN, datasets.Split.VALIDATION, datasets.Split.TEST]
            ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        pattern = re.compile(r"(\d+)\s([^\t]+)\t?([^\t]*)?\t*([^\t]*)?")

        if not isinstance(filepath, (list, tuple)):
            filepath = [filepath]

        for file in filepath:
            with open(file) as f:
                data = f.read().splitlines()
                book_id = -1
                question_id = 0
                context_id = 1
                context = []
                query = None
                candidates = None
                answer = None
                for id_, row in enumerate(data):
                    if self.config.name != "books":
                        m = pattern.match(row)
                        if not m:
                            question_id += 1
                            context_id = 1
                            context = []
                            query = None
                            candidates = None
                            answer = None
                            continue
                        elif m.group(3):
                            query = m.group(2)
                            answer = m.group(3)
                            candidates = m.group(4).split("|")
                            yield id_, {
                                "id": question_id,
                                "context": context,
                                "query": query,
                                "candidates": candidates,
                                "answer": answer,
                            }
                        else:
                            assert context_id == int(m.group(1)), "Error with dataset file, context id not sequential"
                            context_id += 1
                            context.append(m.group(2))
                    else:
                        if row.startswith("_BOOK_TITLE_"):
                            book_id += 1
                        yield id_, {"text": row, "book_id": book_id}
