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
"""SEMPRE dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = r"""
    @article{DBLP:journals/corr/DunnSHGCC17,
    author    = {Matthew Dunn and
                Levent Sagun and
                Mike Higgins and
                V. Ugur G{\"{u}}ney and
                Volkan Cirik and
                Kyunghyun Cho},
    title     = {SearchQA: {A} New Q{\&}A Dataset Augmented with Context from a
                Search Engine},
    journal   = {CoRR},
    volume    = {abs/1704.05179},
    year      = {2017},
    url       = {http://arxiv.org/abs/1704.05179},
    archivePrefix = {arXiv},
    eprint    = {1704.05179},
    timestamp = {Mon, 13 Aug 2018 16:47:09 +0200},
    biburl    = {https://dblp.org/rec/journals/corr/DunnSHGCC17.bib},
    bibsource = {dblp computer science bibliography, https://dblp.org}
    }

"""
# pylint: disable=line-too-long
_DESCRIPTION = """
We publicly release a new large-scale dataset, called SearchQA, for machine comprehension, or question-answering. Unlike recently released datasets, such as DeepMind
CNN/DailyMail and SQuAD, the proposed SearchQA was constructed to reflect a full pipeline of general question-answering. That is, we start not from an existing article
and generate a question-answer pair, but start from an existing question-answer pair, crawled from J! Archive, and augment it with text snippets retrieved by Google.
Following this approach, we built SearchQA, which consists of more than 140k question-answer pairs with each pair having 49.6 snippets on average. Each question-answer-context
 tuple of the SearchQA comes with additional meta-data such as the snippet's URL, which we believe will be valuable resources for future research. We conduct human evaluation
 as well as test two baseline methods, one simple word selection and the other deep learning based, on the SearchQA. We show that there is a meaningful gap between the human
 and machine performances. This suggests that the proposed dataset could well serve as a benchmark for question-answering.
"""

_DL_URLS = {
    "raw_jeopardy": "https://drive.google.com/uc?export=download&id=1U7WdBpd9kJ85S7BbBhWUSiy9NnXrKdO6",
    "train_test_val": "https://drive.google.com/uc?export=download&id=1aHPVfC5TrlnUjehtagVZoDfq4VccgaNT",
}
# pylint: enable=line-too-long


class SearchQaConfig(datasets.BuilderConfig):
    """BuilderConfig for SearchQA."""

    def __init__(self, data_url, **kwargs):
        """BuilderConfig for SearchQA

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SearchQaConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.data_url = data_url


class SearchQa(datasets.GeneratorBasedBuilder):
    """Search QA Dataset."""

    BUILDER_CONFIGS = [SearchQaConfig(name=name, description="", data_url=_DL_URLS[name]) for name in _DL_URLS.keys()]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(
                {
                    "category": datasets.Value("string"),
                    "air_date": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "value": datasets.Value("string"),
                    "answer": datasets.Value("string"),
                    "round": datasets.Value("string"),
                    "show_number": datasets.Value("int32"),
                    "search_results": datasets.features.Sequence(
                        {
                            "urls": datasets.Value("string"),
                            "snippets": datasets.Value("string"),
                            "titles": datasets.Value("string"),
                            "related_links": datasets.Value("string"),
                        }
                    )
                    # These are the features of your dataset like images, labels ...
                }
            ),
            homepage="https://github.com/nyu-dl/dl4ir-searchQA",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO(jeopardy): Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs

        if self.config.name == "raw_jeopardy":
            filepath = dl_manager.download_and_extract(_DL_URLS["raw_jeopardy"])
            sub_folders = sorted(os.listdir(os.path.join(filepath, "jeopardy")))
            all_files = []
            for zip_folder in sub_folders:
                if "lock" in zip_folder:
                    continue
                zip_folder_path = os.path.join(filepath, "jeopardy", zip_folder)
                file_path = dl_manager.extract(zip_folder_path)
                zip_folder = zip_folder.split(".")[0]
                if os.path.isdir(os.path.join(file_path, zip_folder)):
                    file_path = os.path.join(file_path, zip_folder)

                else:
                    # in some cases the subfolder name contains sapces as 050000 - 059999   and 050000-059999
                    parts = zip_folder.split("-")
                    zip_folder = parts[0] + " - " + parts[1]
                    if os.path.isdir(os.path.join(file_path, zip_folder)):
                        file_path = os.path.join(file_path, zip_folder)

                files = sorted(os.listdir(file_path))

                files_paths = [os.path.join(file_path, file) for file in files if "__MACOSX" not in file]
                all_files.extend(files_paths)

            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": all_files}),
            ]
        elif self.config.name == "train_test_val":
            filepath = dl_manager.download_and_extract(_DL_URLS["train_test_val"])
            train_path = dl_manager.extract(os.path.join(filepath, "data_json", "train.zip"))
            test_path = dl_manager.extract(os.path.join(filepath, "data_json", "test.zip"))
            val_path = dl_manager.extract(os.path.join(filepath, "data_json", "val.zip"))

            train_files = [os.path.join(train_path, file) for file in sorted(os.listdir(train_path))]
            test_files = [os.path.join(test_path, file) for file in sorted(os.listdir(test_path))]
            val_files = [os.path.join(val_path, file) for file in sorted(os.listdir(val_path))]
            return [
                datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": train_files}),
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepaths": test_files}),
                datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepaths": val_files}),
            ]

    def _generate_examples(self, filepaths):
        """Yields examples."""
        # TODO(searchQa): Yields (key, example) tuples from the dataset
        for i, filepath in enumerate(filepaths):
            with open(filepath, encoding="utf-8") as f:

                data = json.load(f)
                category = data["category"]
                air_date = data["air_date"]
                question = data["question"]
                value = data["value"]
                answer = data["answer"]
                round_ = data["round"]
                show_number = int(data["show_number"])
                search_results = data["search_results"]
                urls = [result["url"] for result in search_results]
                snippets = [result["snippet"] for result in search_results]
                titles = [result["title"] for result in search_results]
                related_links = [
                    result["related_links"] if result["related_links"] else "" for result in search_results
                ]
                yield i, {
                    "category": category,
                    "air_date": air_date,
                    "question": question,
                    "value": value,
                    "answer": answer,
                    "round": round_,
                    "category": category,
                    "show_number": show_number,
                    "search_results": {
                        "urls": urls,
                        "snippets": snippets,
                        "titles": titles,
                        "related_links": related_links,
                    },
                }
