# coding=utf-8
# Copyright 2020 the HuggingFace Datasets Authors.
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
"""MeDAL: Medical Abbreviation Disambiguation Dataset for Natural Language Understanding Pretraining"""

from __future__ import absolute_import, division, print_function

import csv
import logging

import datasets


logger = logging.getLogger(__name__)


_CITATION = """\
@inproceedings{wen-etal-2020-medal,
    title = "{M}e{DAL}: Medical Abbreviation Disambiguation Dataset for Natural Language Understanding Pretraining",
    author = "Wen, Zhi  and
      Lu, Xing Han  and
      Reddy, Siva",
    booktitle = "Proceedings of the 3rd Clinical Natural Language Processing Workshop",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.clinicalnlp-1.15",
    pages = "130--135",
    abstract = "One of the biggest challenges that prohibit the use of many current NLP methods in clinical settings is the availability of public datasets. In this work, we present MeDAL, a large medical text dataset curated for abbreviation disambiguation, designed for natural language understanding pre-training in the medical domain. We pre-trained several models of common architectures on this dataset and empirically showed that such pre-training leads to improved performance and convergence speed when fine-tuning on downstream medical tasks.",
}"""

_DESCRIPTION = """\
A large medical text dataset (14Go) curated to 4Go for abbreviation disambiguation, designed for natural language understanding pre-training in the medical domain. For example, DHF can be disambiguated to dihydrofolate, diastolic heart failure, dengue hemorragic fever or dihydroxyfumarate
"""

_URL = "https://zenodo.org/record/4276178/files/"
_URLS = {
    "train": _URL + "train.csv",
    "test": _URL + "test.csv",
    "valid": _URL + "valid.csv",
    "full": _URL + "full_data.csv",
}


class Medal(datasets.GeneratorBasedBuilder):
    """Medal: Medical Abbreviation Disambiguation Dataset for Natural Language Understanding Pretraining"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # datasets.features.FeatureConnectors
            features=datasets.Features(
                {
                    "abstract_id": datasets.Value("int32"),
                    "text": datasets.Value("string"),
                    "location": datasets.Sequence(datasets.Value("int32")),
                    "label": datasets.Sequence(datasets.Value("string")),
                    # These are the features of your dataset like images, labels ...
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage="https://github.com/BruceWen120/medal",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_dl = _URLS
        try:
            dl_dir = dl_manager.download_and_extract(urls_to_dl)
        except Exception:
            logger.warning(
                "This dataset is downloaded through Zenodo which is flaky. If this download failed try a few times before reporting an issue"
            )
            raise

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["train"], "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["test"], "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["valid"], "split": "val"},
            ),
            datasets.SplitGenerator(
                name="full",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir["full"], "split": "full"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f)
            # Skip header
            next(data)
            # print(split, filepath, next(data))
            if split == "full":
                id_ = 0
                for id_, row in enumerate(data):
                    yield id_, {
                        "abstract_id": -1,
                        "text": row[0],
                        "location": [int(location) for location in row[1].split("|")],
                        "label": row[2].split("|"),
                    }
            else:
                for id_, row in enumerate(data):
                    yield id_, {
                        "abstract_id": int(row[0]),
                        "text": row[1],
                        "location": [int(row[2])],
                        "label": [row[3]],
                    }
