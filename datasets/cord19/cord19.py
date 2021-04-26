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


import csv
import json
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
CORD19_DATASET_DATE = "2020-11-29"
_URL = (
    "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases/cord-19_"
    + CORD19_DATASET_DATE
    + ".tar.gz"
)


class Cord19(datasets.GeneratorBasedBuilder):
    """The Covid-19 Open Research Dataset (CORD-19) is a growing resource of scientific papers on Covid-19."""

    VERSION = datasets.Version("0.0.1")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="metadata",
            description="The set of documents but loading some metadata like title and " "abstract for each article.",
        ),
        datasets.BuilderConfig(
            name="fulltext",
            description="The set of documents loading some metadata like title and "
            "abstract and full text for each article.",
        ),
        datasets.BuilderConfig(
            name="embeddings",
            description="The set of documents loading some metadata like title and "
            "abstract and document embeddings for each article.",
        ),
    ]

    def _info(self):
        # default metadata only
        features_dict = {
            "cord_uid": datasets.Value("string"),
            "sha": datasets.Value("string"),
            "source_x": datasets.Value("string"),
            "title": datasets.Value("string"),
            "doi": datasets.Value("string"),
            "abstract": datasets.Value("string"),
            "publish_time": datasets.Value("string"),
            "authors": datasets.Value("string"),
            "journal": datasets.Value("string"),
            "url": datasets.Value("string"),
        }

        if "fulltext" in self.config.name:
            # adding full_text
            features_dict["fulltext"] = datasets.Value("string")

        if "embeddings" in self.config.name:
            # adding embeddings
            features_dict["doc_embeddings"] = datasets.Sequence(datasets.Value("float64"))

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=datasets.Features(features_dict),
            supervised_keys=None,
            homepage="https://www.semanticscholar.org/cord19/download",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URL
        data_dir = dl_manager.download_and_extract(my_urls)

        files = dict()
        files["metadata"] = os.path.join(data_dir, CORD19_DATASET_DATE, "metadata.csv")

        if "fulltext" in self.config.name:
            fulltext_dir_path = dl_manager.extract(
                os.path.join(data_dir, CORD19_DATASET_DATE, "document_parses.tar.gz")
            )
            files["fulltext"] = fulltext_dir_path

        if "embeddings" in self.config.name:
            embeddings_dir_path = dl_manager.extract(
                os.path.join(data_dir, CORD19_DATASET_DATE, "cord_19_embeddings.tar.gz")
            )
            files["embeddings"] = os.path.join(
                embeddings_dir_path, "cord_19_embeddings_" + CORD19_DATASET_DATE + ".csv"
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": files,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        metadata_filepath = filepath["metadata"]

        if "fulltext" in self.config.name:
            fulltext_dir_path = filepath["fulltext"]

        fh = None
        if "embeddings" in self.config.name:
            embeddings_filepath = filepath["embeddings"]
            fh = open(embeddings_filepath, mode="r", encoding="utf-8")

        with open(metadata_filepath, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            # skip headers
            next(reader, None)

            for i, line in enumerate(reader):
                doc_fields = {
                    "cord_uid": line[0],
                    "sha": line[1],
                    "source_x": line[2],
                    "title": line[3],
                    "doi": line[4],
                    "abstract": line[8],
                    "publish_time": line[9],
                    "authors": line[10],
                    "journal": line[11],
                    "url": line[17],
                }

                if "fulltext" in self.config.name:
                    doc_fields["fulltext"] = ""
                    json_filepath = line[15]
                    # some entry do not have pdf transcript
                    if len(json_filepath) > 0:
                        # possibly multiple json (matching multiple pdf) then take the first one arbitrarily
                        if ";" in json_filepath:
                            json_filepath = json_filepath.split(";")[0]

                        # load json file
                        with open(
                            os.path.join(fulltext_dir_path, json_filepath), mode="r", encoding="utf-8"
                        ) as json_file:
                            data = json.load(json_file)
                            doc_fields["fulltext"] = "\n".join(text_block["text"] for text_block in data["body_text"])

                if "embeddings" in self.config.name:
                    # synchronized reading of embeddings csv
                    data = fh.readline().split(",")
                    doc_id = data[0]

                    doc_fields["doc_embeddings"] = []

                    if doc_id == doc_fields["cord_uid"]:
                        doc_fields["doc_embeddings"] = [float(v) for v in data[1:-1]]

                yield i, doc_fields

            if "embeddings" in self.config.name and fh is not None:
                fh.close()
