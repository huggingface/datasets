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
CORD-19 dataset implementation initiated by @ggdupont
"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{Wang2020CORD19TC,
  title={CORD-19: The Covid-19 Open Research Dataset},
  author={Lucy Lu Wang and Kyle Lo and Yoganand Chandrasekhar and Russell Reas and Jiangjiang Yang and Darrin Eide and
  K. Funk and Rodney Michael Kinney and Ziyang Liu and W. Merrill and P. Mooney and D. Murdick and Devvret Rishi and
  Jerry Sheehan and Zhihong Shen and B. Stilson and A. Wade and K. Wang and Christopher Wilhelm and Boya Xie and
  D. Raymond and Daniel S. Weld and Oren Etzioni and Sebastian Kohlmeier},
  journal={ArXiv},
  year={2020}
}
"""

# You can copy an official description
_DESCRIPTION = """\
The Covid-19 Open Research Dataset (CORD-19) is a growing resource of scientific papers on Covid-19 and related
historical coronavirus research. CORD-19 is designed to facilitate the development of text mining and information
retrieval systems over its rich collection of metadata and structured full text papers. Since its release, CORD-19
has been downloaded over 75K times and has served as the basis of many Covid-19 text mining and discovery systems.

The dataset itself isn't defining a specific task, but there is a Kaggle challenge that define 17 open research
questions to be solved with the dataset: https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/tasks
"""

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases/cord-19_2020-11-29.tar.gz"


class Cord19(datasets.GeneratorBasedBuilder):
    """The Covid-19 Open Research Dataset (CORD-19) is a growing resource of scientific papers on Covid-19."""

    VERSION = datasets.Version("0.0.1")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="cord-19",
            description="The whole dataset in a compressed file. Only title and "
            "abstract of each article are loaded for now.",
        ),
        # datasets.BuilderConfig(name="second_domain", description="This part of my dataset covers a second domain"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            # metadata headers
            # cord_uid,sha,source_x,title,doi,pmcid,pubmed_id,license,abstract,publish_time,authors,journal,mag_id,
            # who_covidence_id,arxiv_id,pdf_json_files,pmc_json_files,url,s2_id
            features=datasets.Features(
                {
                    "cord_uid": datasets.Value("string"),
                    "sha": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    # TODO "authors list" (complex nested json)
                    "abstract": datasets.Value("string"),
                    # TODO "full_text" (complex nested json)
                    # TODO "bib_entries" (complex nested json)
                    # TODO "doc_embeddings" (separated file to be link by paper_id?)
                }
            ),
            supervised_keys=None,
            homepage="https://www.semanticscholar.org/cord19/download",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "2020-11-29/metadata.csv"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            # headers
            # cord_uid,sha,source_x,title,doi,pmcid,pubmed_id,license,abstract,publish_time,authors,journal,mag_id,
            # who_covidence_id,arxiv_id,pdf_json_files,pmc_json_files,url,s2_id
            for i, line in enumerate(reader):
                yield i, {
                    "cord_uid": line[0],
                    "sha": line[1],
                    "title": line[3],
                    "abstract": line[8],
                }
