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


import csv
import os

import datasets


# no BibTeX citation
_CITATION = """@inproceedings{abu-farha-magdy-2020-arabic,
    title = "From {A}rabic Sentiment Analysis to Sarcasm Detection: The {A}r{S}arcasm Dataset",
    author = "Abu Farha, Ibrahim  and Magdy, Walid",
    booktitle = "Proceedings of the 4th Workshop on Open-Source Arabic Corpora and Processing Tools, with a Shared Task on Offensive Language Detection",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resource Association",
    url = "https://www.aclweb.org/anthology/2020.osact-1.5",
    pages = "32--39",
    language = "English",
    ISBN = "979-10-95546-51-1",
}"""

_DESCRIPTION = """\
ArSarcasm is a new Arabic sarcasm detection dataset.
The dataset was created using previously available Arabic sentiment analysis datasets (SemEval 2017 and ASTD)
 and adds sarcasm and dialect labels to them. The dataset contains 10,547 tweets, 1,682 (16%) of which are sarcastic.
"""

_LICENSE = "MIT"

_URLs = {
    "default": "https://github.com/iabufarha/ArSarcasm/archive/master.zip",
}


class ArSarcasm(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "dialect": datasets.ClassLabel(names=["egypt", "gulf", "levant", "magreb", "msa"]),
                "sarcasm": datasets.ClassLabel(names=["non-sarcastic", "sarcastic"]),
                "sentiment": datasets.ClassLabel(names=["negative", "neutral", "positive"]),
                "original_sentiment": datasets.ClassLabel(names=["negative", "neutral", "positive"]),
                "tweet": datasets.Value("string"),
                "source": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://github.com/iabufarha/ArSarcasm",
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "ArSarcasm-master", "dataset", "ArSarcasm_train.csv"),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "ArSarcasm-master", "dataset", "ArSarcasm_test.csv"),
                },
            ),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            rdr = csv.reader(f, delimiter=",")
            next(rdr)
            for id_, row in enumerate(rdr):
                if len(row) < 6:
                    continue
                if row[4][0] == '"' and row[4][-1] == '"':
                    row[4] = row[4][1:-1]
                yield id_, {
                    "dialect": row[0],
                    "sarcasm": "sarcastic" if row[1] == "True" else "non-sarcastic",
                    "sentiment": row[2],
                    "original_sentiment": row[3],
                    "tweet": row[4],
                    "source": row[5],
                }
