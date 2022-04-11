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
"""pn_summary"""


import csv
import os

import datasets


_CITATION = """\
@article{pnSummary, title={Leveraging ParsBERT and Pretrained mT5 for Persian Abstractive Text Summarization},
author={Mehrdad Farahani, Mohammad Gharachorloo, Mohammad Manthouri},
year={2020},
eprint={2012.11204},
archivePrefix={arXiv},
primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
A well-structured summarization dataset for the Persian language consists of 93,207 records. It is prepared for Abstractive/Extractive tasks (like cnn_dailymail for English). It can also be used in other scopes like Text Generation, Title Generation, and News Category Classification.
It is imperative to consider that the newlines were replaced with the `[n]` symbol. Please interpret them into normal newlines (for ex. `t.replace("[n]", "\n")`) and then use them for your purposes.
"""

_HOMEPAGE = "https://github.com/hooshvare/pn-summary"
_LICENSE = "MIT License"

_URLs = {
    "1.0.0": {
        "data": "https://drive.google.com/u/0/uc?id=16OgJ_OrfzUF_i3ftLjFn9kpcyoi7UJeO&export=download",
        "features": [
            {"name": "id", "type": datasets.Value("string")},
            {"name": "title", "type": datasets.Value("string")},
            {"name": "article", "type": datasets.Value("string")},
            {"name": "summary", "type": datasets.Value("string")},
            {
                "name": "category",
                "type": datasets.ClassLabel(
                    names=[
                        "Economy",
                        "Roads-Urban",
                        "Banking-Insurance",
                        "Agriculture",
                        "International",
                        "Oil-Energy",
                        "Industry",
                        "Transportation",
                        "Science-Technology",
                        "Local",
                        "Sports",
                        "Politics",
                        "Art-Culture",
                        "Society",
                        "Health",
                        "Research",
                        "Education-University",
                        "Tourism",
                    ]
                ),
            },
            {"name": "categories", "type": datasets.Value("string")},
            {
                "name": "network",
                "type": datasets.ClassLabel(names=["Tahlilbazaar", "Imna", "Shana", "Mehr", "Irna", "Khabaronline"]),
            },
            {"name": "link", "type": datasets.Value("string")},
        ],
    }
}


class PnSummaryConfig(datasets.BuilderConfig):
    """BuilderConfig for pn_summary."""

    def __init__(self, **kwargs):
        """BuilderConfig for pn_summary."""

        super(PnSummaryConfig, self).__init__(**kwargs)


class PnSummary(datasets.GeneratorBasedBuilder):
    """A well-structured summarization dataset for the Persian language: pn_summary"""

    BUILDER_CONFIGS = [
        PnSummaryConfig(
            name="1.0.0", version=datasets.Version("1.0.0"), description="The first version of pn_summary"
        ),
    ]

    def _info(self):
        feature_names_types = _URLs[self.config.name]["features"]
        features = datasets.Features({f["name"]: f["type"] for f in feature_names_types})

        return datasets.DatasetInfo(
            description=_DESCRIPTION, features=features, homepage=_HOMEPAGE, citation=_CITATION
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls["data"])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "pn_summary", "train.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "pn_summary", "dev.csv"),
                    "split": "validation",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "pn_summary", "test.csv"),
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        feature_names_types = _URLs[self.config.name]["features"]
        features = [f["name"] for f in feature_names_types]
        with open(filepath, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, quotechar='"', delimiter="\t", quoting=csv.QUOTE_MINIMAL)

            for _id, row in enumerate(reader):
                if len(row) == len(features):
                    yield _id, {f: row[f] for f in features}
