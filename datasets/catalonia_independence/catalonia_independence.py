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
"""This dataset contains two corpora in Spanish and Catalan that consist of annotated Twitter messages for automatic stance detection."""


import csv
import os

import datasets


_CITATION = """\
@inproceedings{zotova-etal-2020-multilingual,
    title = "Multilingual Stance Detection in Tweets: The {C}atalonia Independence Corpus",
    author = "Zotova, Elena  and
      Agerri, Rodrigo  and
      Nunez, Manuel  and
      Rigau, German",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.171",
    pages = "1368--1375",
    abstract = "Stance detection aims to determine the attitude of a given text with respect to a specific topic or claim. While stance detection has been fairly well researched in the last years, most the work has been focused on English. This is mainly due to the relative lack of annotated data in other languages. The TW-10 referendum Dataset released at IberEval 2018 is a previous effort to provide multilingual stance-annotated data in Catalan and Spanish. Unfortunately, the TW-10 Catalan subset is extremely imbalanced. This paper addresses these issues by presenting a new multilingual dataset for stance detection in Twitter for the Catalan and Spanish languages, with the aim of facilitating research on stance detection in multilingual and cross-lingual settings. The dataset is annotated with stance towards one topic, namely, the ndependence of Catalonia. We also provide a semi-automatic method to annotate the dataset based on a categorization of Twitter users. We experiment on the new corpus with a number of supervised approaches, including linear classifiers and deep learning methods. Comparison of our new corpus with the with the TW-1O dataset shows both the benefits and potential of a well balanced corpus for multilingual and cross-lingual research on stance detection. Finally, we establish new state-of-the-art results on the TW-10 dataset, both for Catalan and Spanish.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

_DESCRIPTION = """\
This dataset contains two corpora in Spanish and Catalan that consist of annotated Twitter messages for automatic stance detection. The data was collected over 12 days during February and March of 2019 from tweets posted in Barcelona, and during September of 2018 from tweets posted in the town of Terrassa, Catalonia.

Each corpus is annotated with three classes: AGAINST, FAVOR and NEUTRAL, which express the stance towards the target - independence of Catalonia.
"""

_HOMEPAGE = "https://github.com/ixa-ehu/catalonia-independence-corpus"

_LICENSE = "CC BY-NC-SA 4.0"

_URLs = {
    "catalan": "https://github.com/ixa-ehu/catalonia-independence-corpus/raw/master/01_CIC_CA.zip",
    "spanish": "https://github.com/ixa-ehu/catalonia-independence-corpus/raw/master/02_CIC_ES.zip",
}


class CataloniaIndependence(datasets.GeneratorBasedBuilder):
    """This dataset contains two corpora in Spanish and Catalan that consist of annotated Twitter messages for automatic stance detection."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="catalan",
            version=VERSION,
            description="This part of the corpus contains annotated tweets posted in Catalan.",
        ),
        datasets.BuilderConfig(
            name="spanish",
            version=VERSION,
            description="This part of the corpus contains annotated tweets posted in Spanish.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "catalan"

    def _info(self):
        features = datasets.Features(
            {
                "id_str": datasets.Value("string"),
                "TWEET": datasets.Value("string"),
                "LABEL": datasets.ClassLabel(names=["AGAINST", "FAVOR", "NEUTRAL"]),
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
        data_dir = dl_manager.download_and_extract(_URLs[self.config.name])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, f"{self.config.name}_train.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, f"{self.config.name}_test.csv")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": os.path.join(data_dir, f"{self.config.name}_val.csv")},
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t")
            # skip header
            next(csv_reader)
            for _id, row in enumerate(csv_reader):
                yield _id, {"id_str": row[0], "TWEET": row[1], "LABEL": row[2]}
