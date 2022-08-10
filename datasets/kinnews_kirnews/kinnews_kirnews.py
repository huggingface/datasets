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
"""Kinyarwanda and Kirundi news classification datasets."""


import csv
import os

import datasets


_CITATION = """\
@article{niyongabo2020kinnews,
  title={KINNEWS and KIRNEWS: Benchmarking Cross-Lingual Text Classification for Kinyarwanda and Kirundi},
  author={Niyongabo, Rubungo Andre and Qu, Hong and Kreutzer, Julia and Huang, Li},
  journal={arXiv preprint arXiv:2010.12174},
  year={2020}
}
"""

_DESCRIPTION = """\
Kinyarwanda and Kirundi news classification datasets
"""

_HOMEPAGE = "https://github.com/Andrews2017/KINNEWS-and-KIRNEWS-Corpus"
_LICENSE = "MIT License"

_URLs = {
    "kinnews": "https://github.com/saradhix/kinnews_kirnews/raw/master/KINNEWS.zip",
    "kirnews": "https://github.com/saradhix/kinnews_kirnews/raw/master/KIRNEWS.zip",
}


class KinnewsKirnews(datasets.GeneratorBasedBuilder):
    """This is Kinyarwanda and Kirundi news dataset called KINNEWS and KIRNEWS."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="kinnews_raw", description="Dataset for Kinyarwanda language"),
        datasets.BuilderConfig(name="kinnews_cleaned", description="Cleaned dataset for Kinyarwanda language"),
        datasets.BuilderConfig(name="kirnews_raw", description="Dataset for Kirundi language"),
        datasets.BuilderConfig(name="kirnews_cleaned", description="Cleaned dataset for Kirundi language"),
    ]
    class_labels = [
        "politics",
        "sport",
        "economy",
        "health",
        "entertainment",
        "history",
        "technology",
        "tourism",
        "culture",
        "fashion",
        "religion",
        "environment",
        "education",
        "relationship",
    ]
    label_columns = {"kinnews_raw": "kin_label", "kirnews_raw": "kir_label"}

    def _info(self):
        if "raw" in self.config.name:
            features = datasets.Features(
                {
                    "label": datasets.ClassLabel(names=self.class_labels),
                    self.label_columns[self.config.name]: datasets.Value("string"),
                    "en_label": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "label": datasets.ClassLabel(names=self.class_labels),
                    "title": datasets.Value("string"),
                    "content": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang, kind = self.config.name.split("_")
        data_dir = dl_manager.download_and_extract(_URLs[lang])
        lang_dir = lang.upper()

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang_dir, kind, "train.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, lang_dir, kind, "test.csv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(
                csv_file, quotechar='"', delimiter=",", quoting=csv.QUOTE_ALL, skipinitialspace=True
            )
            next(csv_reader)

            for id_, row in enumerate(csv_reader):
                if "raw" in self.config.name:
                    label, k_label, en_label, url, title, content = row
                    yield id_, {
                        "label": self.class_labels[int(label) - 1],
                        self.label_columns[self.config.name]: k_label,
                        "en_label": en_label,
                        "url": url,
                        "title": title,
                        "content": content,
                    }
                else:
                    label, title, content = row
                    yield id_, {
                        "label": self.class_labels[int(label) - 1],
                        "title": title,
                        "content": content,
                    }
