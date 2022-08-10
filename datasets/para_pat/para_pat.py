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

_DESCRIPTION = """\
ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts

This dataset contains the developed parallel corpus from the open access Google
Patents dataset in 74 language pairs, comprising more than 68 million sentences
and 800 million tokens. Sentences were automatically aligned using the Hunalign algorithm
for the largest 22 language pairs, while the others were abstract (i.e. paragraph) aligned.

"""

_HOMEPAGE = (
    "https://figshare.com/articles/ParaPat_The_Multi-Million_Sentences_Parallel_Corpus_of_Patents_Abstracts/12627632"
)

_LICENSE = "CC BY 4.0"

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


class ParaPatConfig(datasets.BuilderConfig):
    """BuilderConfig for ParaPat."""

    def __init__(self, language_pair=(None, None), url=None, **kwargs):
        """BuilderConfig for ParaPat."""
        name = "%s-%s" % (language_pair[0], language_pair[1])

        description = ("Translation dataset from %s to %s") % (language_pair[0], language_pair[1])

        source, target = language_pair
        super(ParaPatConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.1.0", ""),
            **kwargs,
        )

        self.language_pair = language_pair
        self.url = url


class ParaPat(datasets.GeneratorBasedBuilder):
    """ParaPat: The Multi-Million Sentences Parallel Corpus of Patents Abstracts"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        ParaPatConfig(
            language_pair=("el", "en"),
            url="https://ndownloader.figshare.com/files/23748818",
        ),
        ParaPatConfig(
            language_pair=("cs", "en"),
            url="https://ndownloader.figshare.com/files/23748821",
        ),
        ParaPatConfig(
            language_pair=("en", "hu"),
            url="https://ndownloader.figshare.com/files/23748827",
        ),
        ParaPatConfig(
            language_pair=("en", "ro"),
            url="https://ndownloader.figshare.com/files/23748842",
        ),
        ParaPatConfig(
            language_pair=("en", "sk"),
            url="https://ndownloader.figshare.com/files/23748848",
        ),
        ParaPatConfig(
            language_pair=("en", "uk"),
            url="https://ndownloader.figshare.com/files/23748851",
        ),
        ParaPatConfig(
            language_pair=("es", "fr"),
            url="https://ndownloader.figshare.com/files/23748857",
        ),
        ParaPatConfig(
            language_pair=("fr", "ru"),
            url="https://ndownloader.figshare.com/files/23748863",
        ),
        ParaPatConfig(
            language_pair=("de", "fr"),
            url="https://ndownloader.figshare.com/files/23748872",
        ),
        ParaPatConfig(
            language_pair=("en", "ja"),
            url="https://ndownloader.figshare.com/files/23748626",
        ),
        ParaPatConfig(
            language_pair=("en", "es"),
            url="https://ndownloader.figshare.com/files/23748896",
        ),
        ParaPatConfig(
            language_pair=("en", "fr"),
            url="https://ndownloader.figshare.com/files/23748944",
        ),
        ParaPatConfig(
            language_pair=("de", "en"),
            url="https://ndownloader.figshare.com/files/23855657",
        ),
        ParaPatConfig(
            language_pair=("en", "ko"),
            url="https://ndownloader.figshare.com/files/23748689",
        ),
        ParaPatConfig(
            language_pair=("fr", "ja"),
            url="https://ndownloader.figshare.com/files/23748866",
        ),
        ParaPatConfig(
            language_pair=("en", "zh"),
            url="https://ndownloader.figshare.com/files/23748779",
        ),
        ParaPatConfig(
            language_pair=("en", "ru"),
            url="https://ndownloader.figshare.com/files/23748704",
        ),
        ParaPatConfig(
            language_pair=("fr", "ko"),
            url="https://ndownloader.figshare.com/files/23855408",
        ),
        ParaPatConfig(
            language_pair=("ru", "uk"),
            url="https://ndownloader.figshare.com/files/23855465",
        ),
        ParaPatConfig(
            language_pair=("en", "pt"),
            url="https://ndownloader.figshare.com/files/23855441",
        ),
    ]
    BUILDER_CONFIG_CLASS = ParaPatConfig

    def _info(self):
        source, target = self.config.language_pair

        if self.config.name in type1_datasets_features:
            features = datasets.Features(
                {
                    "index": datasets.Value("int32"),
                    "family_id": datasets.Value("int32"),
                    "translation": datasets.features.Translation(languages=(source, target)),
                }
            )
        elif self.config.name in type2_datasets_features:
            features = datasets.Features(
                {
                    "translation": datasets.features.Translation(languages=(source, target)),
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
            supervised_keys=(source, target),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        source, target = self.config.language_pair

        data_dir = dl_manager.download_and_extract(self.config.url)

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
        """Yields examples."""
        source, target = self.config.language_pair
        with open(filepath, encoding="utf-8") as f:
            if self.config.name in type1_datasets_features:
                data = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(data):
                    if row["src_lang"] + "-" + row["tgt_lang"] != self.config.name:
                        continue
                    yield id_, {
                        "index": row["index"],
                        "family_id": row["family_id"],
                        "translation": {source: row["src_abs"], target: row["tgt_abs"]},
                    }
            else:
                data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
                for id_, row in enumerate(data):
                    yield id_, {
                        "translation": {source: row[0], target: row[1]},
                    }
