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
The Multidocument Summarization for Literature Review (MSLR) Shared Task aims to study how medical
evidence from different clinical studies are summarized in literature reviews. Reviews provide the
highest quality of evidence for clinical care, but are expensive to produce manually.
(Semi-)automation via NLP may facilitate faster evidence synthesis without sacrificing rigor. The
MSLR shared task uses two datasets to assess the current state of multidocument summarization for
this task, and to encourage the development of modeling contributions, scaffolding tasks, methods
for model interpretability, and improved automated evaluation methods in this domain.
"""


import os

import pandas as pd

import datasets


_CITATION = """\
@inproceedings{DeYoung2021MS2MS,
    title        = {MSˆ2: Multi-Document Summarization of Medical Studies},
    author       = {Jay DeYoung and Iz Beltagy and Madeleine van Zuylen and Bailey Kuehl and Lucy Lu Wang},
    booktitle    = {EMNLP},
    year         = {2021}
}
@article{Wallace2020GeneratingN,
    title        = {Generating (Factual?) Narrative Summaries of RCTs: Experiments with Neural Multi-Document Summarization},
    author       = {Byron C. Wallace and Sayantani Saha and Frank Soboczenski and Iain James Marshall},
    year         = 2020,
    journal      = {AMIA Annual Symposium},
    volume       = {abs/2008.11293}
}
"""

_DATASETNAME = "mslr2022"

_DESCRIPTION = """\
The Multidocument Summarization for Literature Review (MSLR) Shared Task aims to study how medical
evidence from different clinical studies are summarized in literature reviews. Reviews provide the
highest quality of evidence for clinical care, but are expensive to produce manually.
(Semi-)automation via NLP may facilitate faster evidence synthesis without sacrificing rigor.
The MSLR shared task uses two datasets to assess the current state of multidocument summarization
for this task, and to encourage the development of modeling contributions, scaffolding tasks, methods
for model interpretability, and improved automated evaluation methods in this domain.
"""

_HOMEPAGE = "https://github.com/allenai/mslr-shared-task"

_LICENSE = "Apache-2.0"

_URLS = {
    _DATASETNAME: "https://ai2-s2-mslr.s3.us-west-2.amazonaws.com/mslr_data.tar.gz",
}


class MSLR2022(datasets.GeneratorBasedBuilder):
    """MSLR2022 Shared Task."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="ms2",
            version=VERSION,
            description="This dataset consists of around 20K reviews and 470K studies collected from PubMed. For details on dataset contents and construction, please read the MS^2 paper (https://arxiv.org/abs/2104.06486).",
        ),
        datasets.BuilderConfig(
            name="cochrane",
            version=VERSION,
            description="This is a dataset of 4.5K reviews collected from Cochrane systematic reviews. For details on dataset contents and construction, please read the AMIA paper (https://arxiv.org/abs/2008.11293).",
        ),
    ]

    def _info(self):
        fields = {
            "review_id": datasets.Value("string"),
            "pmid": datasets.Sequence(datasets.Value("string")),
            "title": datasets.Sequence(datasets.Value("string")),
            "abstract": datasets.Sequence(datasets.Value("string")),
            "target": datasets.Value("string"),
        }
        # These are unique to MS^2
        if self.config.name == "ms2":
            fields["background"] = datasets.Value("string")
            fields["reviews_info"] = datasets.Value("string")

        features = datasets.Features(fields)

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls = _URLS[_DATASETNAME]
        data_dir = dl_manager.download_and_extract(urls)
        mslr_data_dir = os.path.join(data_dir, "mslr_data", self.config.name)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data_dir": mslr_data_dir,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"data_dir": mslr_data_dir, "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "data_dir": mslr_data_dir,
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, data_dir, split):
        inputs_filepath = os.path.join(data_dir, f"{split}-inputs.csv")
        inputs_df = pd.read_csv(inputs_filepath, index_col=0)

        # Only the train and dev splits have targets
        if split != "test":
            targets_filepath = os.path.join(data_dir, f"{split}-targets.csv")
            targets_df = pd.read_csv(targets_filepath, index_col=0)
            # Only MS^2 has the *-reviews-info.csv files, and only for the train and dev splits.
            if self.config.name == "ms2":
                reviews_info_filepath = os.path.join(data_dir, f"{split}-reviews-info.csv")
                reviews_info_df = pd.read_csv(reviews_info_filepath, index_col=0)

        for review_id in inputs_df.ReviewID.unique():
            inputs = inputs_df[inputs_df.ReviewID == review_id]

            example = {
                "review_id": review_id,
                "pmid": inputs.PMID.values.tolist(),
                "title": inputs.Title.values.tolist(),
                "abstract": inputs.Abstract.values.tolist(),
                "target": "",
            }

            if self.config.name == "ms2":
                example["background"] = ""
                example["reviews_info"] = ""

            # Only the train and dev splits have targets
            if split != "test":
                targets = targets_df[targets_df.ReviewID == review_id]
                example["target"] = targets.Target.values[0]
                # Only MS^2 has these fields, and only for train and dev splits.
                if self.config.name == "ms2":
                    example["background"] = targets.Background.values[0]

                    reviews_info = reviews_info_df[reviews_info_df.ReviewID == review_id]
                    example["reviews_info"] = reviews_info.Background.values[0]

            yield review_id, example
