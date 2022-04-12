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
"""STSb-TR dataset is the machine translated version of English STS benchmark dataset using Google Cloud Translation API."""


import csv

import datasets


_CITATION = """\
@inproceedings{beken-fikri-etal-2021-semantic,
    title = "Semantic Similarity Based Evaluation for Abstractive News Summarization",
    author = "Beken Fikri, Figen  and Oflazer, Kemal and Yanikoglu, Berrin",
    booktitle = "Proceedings of the 1st Workshop on Natural Language Generation, Evaluation, and Metrics (GEM 2021)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.gem-1.3",
    doi = "10.18653/v1/2021.gem-1.3",
    pages = "24--33",
    abstract = "ROUGE is a widely used evaluation metric in text summarization. However, it is not suitable for the evaluation of abstractive summarization systems as it relies on lexical overlap between the gold standard and the generated summaries. This limitation becomes more apparent for agglutinative languages with very large vocabularies and high type/token ratios. In this paper, we present semantic similarity models for Turkish and apply them as evaluation metrics for an abstractive summarization task. To achieve this, we translated the English STSb dataset into Turkish and presented the first semantic textual similarity dataset for Turkish as well. We showed that our best similarity models have better alignment with average human judgments compared to ROUGE in both Pearson and Spearman correlations.",
}
"""


_DESCRIPTION = """\
STSb-TR dataset is the machine translated version of English STS benchmark dataset using Google Cloud Translation API.
"""

_HOMEPAGE = "https://github.com/verimsu/STSb-TR"


_URL = "https://raw.githubusercontent.com/verimsu/STSb-TR/main/data_splits/"
_TRAIN_FILE = "stsb_tr_train.tsv"
_VAL_FILE = "stsb_tr_dev.tsv"
_TEST_FILE = "stsb_tr_test.tsv"


class StsbTr(datasets.GeneratorBasedBuilder):
    """STSb-TR: The Turkish translation of English STSb dataset using Google Cloud Translation API."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="stsb_tr",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of the Turkish Machine Translated STSb",
        )
    ]

    def _info(self):
        features = datasets.Features(
            {
                "genre": datasets.Value("string"),
                "dataset": datasets.Value("string"),
                "year": datasets.Value("string"),
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "score": datasets.Value("float"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        urls = {"train": _URL + _TRAIN_FILE, "dev": _URL + _VAL_FILE, "test": _URL + _TEST_FILE}
        downloaded_files = dl_manager.download(urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                yield idx, {
                    "genre": row["genre"],
                    "dataset": row["dataset"],
                    "year": row["year"],
                    "sentence1": row["sentence1"],
                    "sentence2": row["sentence2"],
                    "score": row["score"],
                }
