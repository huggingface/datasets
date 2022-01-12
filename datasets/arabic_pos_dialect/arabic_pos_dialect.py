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
"""TODO: Add a description here."""


import csv

import datasets


_CITATION = """
@InProceedings{DARWISH18.562,  author = {Kareem Darwish ,Hamdy Mubarak ,Ahmed Abdelali ,Mohamed Eldesouki ,Younes Samih ,Randah Alharbi ,Mohammed Attia ,Walid Magdy and Laura Kallmeyer},
title = {Multi-Dialect Arabic POS Tagging: A CRF Approach},
booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
year = {2018},
month = {may},
date = {7-12},
location = {Miyazaki, Japan},
editor = {Nicoletta Calzolari (Conference chair) and Khalid Choukri and Christopher Cieri and Thierry Declerck and Sara Goggi and Koiti Hasida and Hitoshi Isahara and Bente Maegaard and Joseph Mariani and Hélène Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis and Takenobu Tokunaga},
publisher = {European Language Resources Association (ELRA)},
address = {Paris, France},
isbn = {979-10-95546-00-9},
language = {english}
}
"""

_DESCRIPTION = """\
The Dialectal Arabic Datasets contain four dialects of Arabic, Etyptian (EGY), Levantine (LEV), Gulf (GLF), and Maghrebi (MGR). Each dataset consists of a set of 350 manually segmented and POS tagged tweets.
"""

_URL = "https://github.com/qcri/dialectal_arabic_resources/raw/master/"
_DIALECTS = ["egy", "lev", "glf", "mgr"]


class ArabicPosDialectConfig(datasets.BuilderConfig):
    """BuilderConfig for ArabicPosDialect"""

    def __init__(self, dialect=None, **kwargs):
        """

        Args:
            dialect: the 3-letter code string of the dialect set that will be used.
            Code should be one of the following: egy, lev, glf, mgr.
            **kwargs: keyword arguments forwarded to super.
        """
        super(ArabicPosDialectConfig, self).__init__(**kwargs)
        assert dialect in _DIALECTS, ("Invalid dialect code: %s", dialect)
        self.dialect = dialect


class ArabicPosDialect(datasets.GeneratorBasedBuilder):
    """POS-tagged Arabic tweets in four major dialects."""

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIG_CLASS = ArabicPosDialectConfig
    BUILDER_CONFIGS = [
        ArabicPosDialectConfig(
            name=dialect,
            dialect=dialect,
            description=f"A set of 350 tweets in the {dialect} dialect of Arabic that have been manually segmented and POS tagged.",
        )
        for dialect in _DIALECTS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "fold": datasets.Value("int32"),
                    "subfold": datasets.Value("string"),
                    "words": datasets.Sequence(datasets.Value("string")),
                    "segments": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(datasets.Value("string")),
                }
            ),
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            homepage="https://alt.qcri.org/resources/da_resources/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: Downloads the data and defines the splits
        # dl_manager is a datasets.download.DownloadManager that can be used to
        # download and extract URLs
        urls_to_download = {dialect: _URL + f"seg_plus_pos_{dialect}.txt" for dialect in _DIALECTS}
        dl_dir = dl_manager.download_and_extract(urls_to_download)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": dl_dir[self.config.dialect]},
            )
        ]

    def _generate_examples(self, filepath):
        """Yields examples in the raw (text) form."""
        with open(filepath, encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file, delimiter="\t", quoting=csv.QUOTE_NONE)
            fold = -1
            subfold = ""
            words = []
            segments = []
            pos_tags = []
            curr_sent = -1
            for idx, row in enumerate(reader):
                # first example
                if fold == -1:
                    fold = row["Fold"]
                    subfold = row["SubFold"]
                    curr_sent = int(row["SentID"])
                if int(row["SentID"]) != curr_sent:
                    yield curr_sent, {
                        "fold": fold,
                        "subfold": subfold,
                        "words": words,
                        "segments": segments,
                        "pos_tags": pos_tags,
                    }
                    fold = row["Fold"]
                    subfold = row["SubFold"]
                    words = [row["Word"]]
                    segments = [row["Segmentation"]]
                    pos_tags = [row["POS"]]
                    curr_sent = int(row["SentID"])
                else:
                    words.append(row["Word"])
                    segments.append(row["Segmentation"])
                    pos_tags.append(row["POS"])
            # last example
            yield curr_sent, {
                "fold": fold,
                "subfold": subfold,
                "words": words,
                "segments": segments,
                "pos_tags": pos_tags,
            }
