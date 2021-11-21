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
"""OneStopQA - a multiple choice reading comprehension dataset annotated
according to the STARC (Structured Annotations for Reading Comprehension) scheme"""


import csv
import json
import os

import datasets
from datasets.tasks import QuestionAnsweringExtractive

logger = datasets.logging.get_logger(__name__)


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{starc2020,  
      author    = {Berzak, Yevgeni and Malmaud, Jonathan and Levy, Roger},  
      title     = {STARC: Structured Annotations for Reading Comprehension},  
      booktitle = {ACL},  
      year      = {2020},  
      publisher = {Association for Computational Linguistics} 
      }
"""

_DESCRIPTION = """\
OneStopQA is a multiple choice reading comprehension dataset annotated according to the STARC 
(Structured Annotations for Reading Comprehension) scheme. 
The reading materials are Guardian articles taken from the 
[OneStopEnglish corpus](https://github.com/nishkalavallabhi/OneStopEnglishCorpus).
 Each article comes in three difficulty levels, Elementary, Intermediate and Advanced. 
 Each paragraph is annotated with three multiple choice reading comprehension questions. 
 The reading comprehension questions can be answered based on any of the three paragraph levels.
"""

_HOMEPAGE = "https://github.com/berzak/onestop-qa"

_LICENSE = "Creative Commons Attribution-ShareAlike 4.0 International License"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = {
    'first_domain': "https://huggingface.co/great-new-dataset-first_domain.zip",
    'second_domain': "https://huggingface.co/great-new-dataset-second_domain.zip",
}


class OneStopQA(datasets.GeneratorBasedBuilder):
    """OneStopQA - a multiple choice reading comprehension dataset annotated
    according to the STARC (Structured Annotations for Reading Comprehension) scheme"""

    VERSION = datasets.Version("1.1.0")

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
        datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    DEFAULT_CONFIG_NAME = "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        features = datasets.Features(
            {
                "title": datasets.Value("string"),
                "context": datasets.Value("string"),
                "question": datasets.Value("string"),
                "references": datasets.Value("int32"),
                "answers": datasets.features.Sequence(datasets.Value("string")),
                "a_span": datasets.features.Sequence(
                    datasets.features.Sequence(datasets.Value("int32"))),
                "d_span": datasets.features.Sequence(
                    datasets.features.Sequence(datasets.Value("int32"))),
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
            task_templates=[
                QuestionAnsweringExtractive(
                    question_column="question", context_column="context", answers_column="answers"
                )
            ],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(
        self, filepath, split  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.
        logger.info("generating examples from = %s", filepath)
        key = 0
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for article in squad["data"]:
                title = article.get("title", "")
                for paragraph in article["paragraphs"]:
                    paragraph_context_and_spans = paragraph['Adv']
                    context = paragraph_context_and_spans["context"]
                    a_spans = paragraph_context_and_spans["a_spans"]
                    d_spans = paragraph_context_and_spans["d_spans"]
                    qas = paragraph["qas"]
                    for qa, a_span, d_span in zip(qas, a_spans, d_spans):
                        yield key, {
                            "title": title,
                            "context": context,
                            "question": qa['question'],
                            "answers": qa['answers'],
                            "references": qa['references'],
                            "a_span": a_span,
                            "d_span": d_span,
                            },

                        key += 1
