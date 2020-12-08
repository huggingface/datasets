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
"""ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts"""

from __future__ import absolute_import, division, print_function

import csv
import os

import datasets


_CITATION = """\
@inproceedings{soares-etal-2020-parapat,
    title = "{P}ara{P}at: The Multi-Million Sentences Parallel Corpus of Patents Abstracts",
    author = "Soares, Felipe  and
      Stevenson, Mark  and
      Bartolome, Diego  and
      Zaretskaya, Anna",
    booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.465",
    pages = "3769--3774",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts

This dataset contains the developed parallel corpus from the open access Google
Patents dataset in 74 language pairs, comprising more than 68 million sentences
and 800 million tokens. Sentences were automatically aligned using the Hunalign algorithm
for the largest 22 language pairs, while the others were abstract (i.e. paragraph) aligned.

We demonstrate the capabilities of our corpus by training Neural Machine Translation
(NMT) models for the main 9 language pairs, with a total of 18 models.
"""

_HOMEPAGE = (
    "https://figshare.com/articles/ParaPat_The_Multi-Million_Sentences_Parallel_Corpus_of_Patents_Abstracts/12627632"
)

_LICENSE = "CC BY 4.0"

_URLs = {
    "el-en": "https://ndownloader.figshare.com/files/23748818",
    "cs-en": "https://ndownloader.figshare.com/files/23748821",
    "en-hu": "https://ndownloader.figshare.com/files/23748827",
    "en-ro": "https://ndownloader.figshare.com/files/23748842",
    "en-sk": "https://ndownloader.figshare.com/files/23748848",
    "en-uk": "https://ndownloader.figshare.com/files/23748851",
    "es-fr": "https://ndownloader.figshare.com/files/23748857",
    "fr-ru": "https://ndownloader.figshare.com/files/23748863",
    "de-fr": "https://ndownloader.figshare.com/files/23748872",
    "en-ja": "https://ndownloader.figshare.com/files/23748626",
    "en-es": "https://ndownloader.figshare.com/files/23748896",
    "en-fr": "https://ndownloader.figshare.com/files/23748944",
    "de-en": "https://ndownloader.figshare.com/files/23855657",
    "en-ko": "https://ndownloader.figshare.com/files/23748689",
    "fr-ja": "https://ndownloader.figshare.com/files/23748866",
    "en-zh": "https://ndownloader.figshare.com/files/23748779",
    "en-ru": "https://ndownloader.figshare.com/files/23748704",
    "fr-ko": "https://ndownloader.figshare.com/files/23855408",
    "ru-uk": "https://ndownloader.figshare.com/files/23855465",
    "en-pt": "https://ndownloader.figshare.com/files/23855441",
}

type1_datasets_file = ["el-en", "cs-en", "en-hu", "en-ro", "en-sk", "en-uk", "es-fr", "fr-ru"]
type2_datasets_file = [
    "de-fr",
    "en-ja",
    "en-es",
    "en-fr",
    "de-en",
    "en-ko",
    "fr-ja",
    "en-zh",
    "en-ru",
    "fr-ko",
    "ru-uk",
    "en-pt",
]

type1_datasets_features = [
    "el-en",
    "cs-en",
    "en-hu",
    "en-ro",
    "en-sk",
    "en-uk",
    "es-fr",
    "fr-ru",
    "fr-ko",
    "ru-uk",
    "en-pt",
]
type2_datasets_features = ["de-fr", "en-ja", "en-es", "en-fr", "de-en", "en-ko", "fr-ja", "en-zh", "en-ru"]


class ParaPat(datasets.GeneratorBasedBuilder):
    """ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="el-en", version=VERSION, description="This part of dataset covers el-en domain"),
        datasets.BuilderConfig(name="cs-en", version=VERSION, description="This part of dataset covers cs-en domain"),
        datasets.BuilderConfig(name="en-hu", version=VERSION, description="This part of dataset covers en-hu domain"),
        datasets.BuilderConfig(name="en-ro", version=VERSION, description="This part of dataset covers en-ro domain"),
        datasets.BuilderConfig(name="en-sk", version=VERSION, description="This part of dataset covers en-sk domain"),
        datasets.BuilderConfig(name="en-uk", version=VERSION, description="This part of dataset covers en-uk domain"),
        datasets.BuilderConfig(name="es-fr", version=VERSION, description="This part of dataset covers es-fr domain"),
        datasets.BuilderConfig(name="fr-ru", version=VERSION, description="This part of dataset covers fr-ru domain"),
        datasets.BuilderConfig(name="fr-ko", version=VERSION, description="This part of dataset covers fr-ko domain"),
        datasets.BuilderConfig(name="ru-uk", version=VERSION, description="This part of dataset covers ru-uk domain"),
        datasets.BuilderConfig(name="en-pt", version=VERSION, description="This part of dataset covers en-pt domain"),
        datasets.BuilderConfig(name="de-fr", version=VERSION, description="This part of dataset covers de-fr domain"),
        datasets.BuilderConfig(name="en-ja", version=VERSION, description="This part of dataset covers en-ja domain"),
        datasets.BuilderConfig(name="en-es", version=VERSION, description="This part of dataset covers en-es domain"),
        datasets.BuilderConfig(name="en-fr", version=VERSION, description="This part of dataset covers en-fr domain"),
        datasets.BuilderConfig(name="de-en", version=VERSION, description="This part of dataset covers de-en domain"),
        datasets.BuilderConfig(name="en-ko", version=VERSION, description="This part of dataset covers en-ko domain"),
        datasets.BuilderConfig(name="fr-ja", version=VERSION, description="This part of dataset covers fr-ja domain"),
        datasets.BuilderConfig(name="en-zh", version=VERSION, description="This part of dataset covers en-zh domain"),
        datasets.BuilderConfig(name="en-ru", version=VERSION, description="This part of dataset covers en-ru domain"),
    ]

    def _info(self):
        if self.config.name in type1_datasets_features:
            features = datasets.Features(
                {
                    "index": datasets.Value("int32"),
                    "family_id": datasets.Value("int32"),
                    "src_lang": datasets.Value("string"),
                    "src_abs": datasets.Value("string"),
                    "tgt_lang": datasets.Value("string"),
                    "tgt_abs": datasets.Value("string"),
                }
            )
        elif self.config.name in type2_datasets_features:
            features = datasets.Features(
                {
                    "src_lang": datasets.features.Sequence(datasets.Value("string")),
                    "tgt_lang": datasets.features.Sequence(datasets.Value("string")),
                }
            )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)

        if self.config.name in type1_datasets_file:
            _TRAIN_FILE_NAME = data_dir
        else:
            name = self.config.name.replace("-", "_")
            _TRAIN_FILE_NAME = os.path.join(data_dir, f"{name}.tsv")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": _TRAIN_FILE_NAME,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        with open(filepath, encoding="utf-8") as f:
            data = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for id_, row in enumerate(data):
                if self.config.name in type1_datasets_features:
                    if row["src_lang"] + "-" + row["tgt_lang"] != self.config.name:
                        continue
                    yield id_, {
                        "index": row["index"],
                        "family_id": row["family_id"],
                        "src_lang": row["src_lang"],
                        "src_abs": row["src_abs"],
                        "tgt_lang": row["tgt_lang"],
                        "tgt_abs": row["tgt_abs"],
                    }
                else:
                    row = list(row.items())
                    yield id_, {
                        "src_lang": list(row[0]),
                        "tgt_lang": list(row[1]),
                    }
