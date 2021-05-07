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
""" ComplexWebQuestions: A dataset for answering complex questions that require reasoning over multiple web snippets. """

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{talmor18compwebq,
  author = {A. Talmor and J. Berant},
  booktitle = {North American Association for Computational Linguistics (NAACL)},
  title = {The Web as a Knowledge-base for Answering Complex Questions},
  year = {2018},
}
"""

_DESCRIPTION = """\
ComplexWebQuestions is a dataset for answering complex questions that require reasoning over multiple web snippets.
Th dataset contains a large set of complex questions in natural language, and can be used in multiple ways:
1. By interacting with a search engine, which is the focus of our paper (Talmor and Berant, 2018);
2. As a reading comprehension task: we release 12,725,989 web snippets that are relevant for the questions, and were collected during the development of our model; 
3. As a semantic parsing task: each question is paired with a SPARQL query that can be executed against Freebase to retrieve the answer.

The dataset contains 34,689 examples, each containing:
- A complex question
- Answers (including aliases)
- An average of 366.8 snippets per question
- A SPARQL query (against Freebase)
"""

readme_url = "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AACtJ0FYjL77u3-LQuzGER0Ha/README.txt?dl=1",

questions_urls = {
    "ComplexWebQuestions_dev": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AADH8beLbOUWxwvY_K38E3ADa/ComplexWebQuestions_dev.json?dl=1",
    "ComplexWebQuestions_test": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AABr4ysSy_Tg8Wfxww4i_UWda/ComplexWebQuestions_test.json?dl=1",
    "ComplexWebQuestions_train": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AAAIHeWX0cPpbpwK6w06BCxva/ComplexWebQuestions_train.json?dl=1",
}

web_snippets_urls = {
    "web_snippets_dev": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AABuih4kATNxTRLdDisIT-ESa/web_snippets_dev.json.zip?dl=1",
    "web_snippets_test": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AADDFa2IVU38XAoL9NHN-XJ-a/web_snippets_test.json.zip?dl=1",
    "web_snippets_train": "https://www.dropbox.com/sh/7pkwkrfnwqhsnpo/AABVENv_Q9rFtnM61liyzO0La/web_snippets_train.json.zip?dl=1",
}

class NewDataset(datasets.GeneratorBasedBuilder):
    """ ComplexWebQuestions: A dataset for answering complex questions that require reasoning over multiple web snippets."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="questions", description="Questions"),
        datasets.BuilderConfig(name="web_snippets", description="Web snippets"),
    ]

    def _info(self):
        if self.config.name == "questions":
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"), 
                    "answers": datasets.features.Sequence(
                        {
                            "aliases": [datasets.Value("string")], 
                            "answer": datasets.Value("string"), 
                            "answer_id": datasets.Value("string"),
                        }
                    ), 
                    "composition_answer": datasets.Value("string"), 
                    "compositionality_type": datasets.ClassLabel(names=["composition", "conjunction", "comparative", "superlative"]),
                    "created": datasets.Value("string"), 
                    "machine_question": datasets.Value("string"), 
                    "question": datasets.Value("string"), 
                    "sparql": datasets.Value("string"), 
                    "webqsp_ID": datasets.Value("string"), 
                    "webqsp_question": datasets.Value("string"),
                })
        else:
            features = datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "web_query": datasets.Value("string"),
                    "question_ID": datasets.Value("string"),
                    "split_source": [datasets.ClassLabel(names=["ptrnet split", "noisy supervision split"])],
                    "split_type": datasets.ClassLabel(names=["full_question", "split_part1", "split_part2"]), 
                    "web_snippets": datasets.features.Sequence(
                        {
                            "snippet": datasets.Value("string"),
                            "title": datasets.Value("string"),
                        }),
                })

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://www.tau-nlp.org/compwebq",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        if self.config.name == "questions":
            data = dl_manager.download_and_extract(questions_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": data['ComplexWebQuestions_train'],
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": data['ComplexWebQuestions_test'],
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": data['ComplexWebQuestions_dev'],
                        "split": "valid",
                    },
                ),
            ]
        else:
            data = dl_manager.download(web_snippets_urls)
            print("DATA:", data)
            data_extracted = dl_manager.extract(data)
            print("DATA EXTRACTED:", data_extracted)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_extracted['web_snippets_train'], "web_snippets_train.json"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_extracted['web_snippets_test'], "web_snippets_test.json"),
                        "split": "test",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_extracted['web_snippets_dev'], "web_snippets_dev.json"),
                        "split": "valid",
                    },
                ),
            ]


    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: Yields (key, example) tuples from the dataset
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                if split == "test" and self.config.name == "questions":
                    row['answers'] = []
                    row['composition_answer'] = ""
                yield (row["ID"] if self.config.name == "questions" else row["question_ID"],
                       row)
