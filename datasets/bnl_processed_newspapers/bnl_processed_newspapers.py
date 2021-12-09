# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Digitised historic newspapers from the BNL"""

import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import datasets


_CITATION = """\
@misc{bnl_newspapers,
title={Historical Newspapers},
url={https://data.bnl.lu/data/historical-newspapers/},
author={ Bibliothèque nationale du Luxembourg},
"""

_DESCRIPTION = """\
Digitised historic newspapers from the Bibliothèque nationale (BnL) - the National Library of Luxembourg.
This datet covers the 'processed newspapers' collection from these newspapers.
These newspapers cover 38 years of news (1841-1878) and include 510,505 extracted articles.
"""

_HOMEPAGE = "https://data.bnl.lu/data/historical-newspapers/"

_LICENSE = "CC0"


_URL = "https://data.bnl.lu/open-data/digitization/newspapers/export01-newspapers1841-1878.zip"


class BNLProcessedNewspapers(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "ark_id": datasets.Value("string"),
                "source": datasets.Value("string"),
                "url": datasets.Value("string"),
                "title": datasets.Value("string"),
                "ispartof": datasets.Value("string"),
                "text": datasets.Value("string"),
                "pub_date": datasets.Value("timestamp[s]"),
                "publisher": datasets.Value("string"),
                "article_type": datasets.ClassLabel(
                    names=[
                        "ADVERTISEMENT_SECTION",
                        "BIBLIOGRAPHY",
                        "CHAPTER",
                        "INDEX",
                        "CONTRIBUTION",
                        "TABLE_OF_CONTENTS",
                        "WEATHER",
                        "SHIPPING",
                        "SECTION",
                        "ARTICLE",
                        "TITLE_SECTION",
                        "DEATH_NOTICE",
                        "SUPPLEMENT",
                        "TABLE",
                        "ADVERTISEMENT",
                        "CHART_DIAGRAM",
                        "ILLUSTRATION",
                        "ISSUE",
                    ]
                ),
                "extent": datasets.Value("int32"),
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
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "dirpath": data_dir,
                },
            ),
        ]

    def _generate_examples(
        self,
        dirpath,
    ):
        """Yields examples as (key, example) tuples."""
        for id_, xml in enumerate(Path(dirpath).rglob("**/*.xml")):
            tree = ET.parse(xml)
            root = tree.getroot()
            source = tree.findall(".//{http://purl.org/dc/elements/1.1/}source")[0].text
            metadata = root.find(".//{http://www.openarchives.org/OAI/2.0/}metadata")
            ispartof = metadata.find(".//{http://purl.org/dc/terms/}isPartOf").text
            date = metadata.find(".//{http://purl.org/dc/elements/1.1/}date").text
            if date:
                date = datetime.strptime(date, "%Y-%m-%d")
            publisher = root.findall(".//{http://purl.org/dc/elements/1.1/}publisher")
            if publisher:
                publisher = publisher[0].text
            hasversion = metadata.find(".//{http://purl.org/dc/terms/}hasVersion").text

            description = tree.findall(".//{http://purl.org/dc/elements/1.1/}description")[0].text
            ark_id = tree.findall(".//{http://purl.org/dc/elements/1.1/}identifier")[0].text
            title = metadata.find(".//{http://purl.org/dc/elements/1.1/}title").text
            article_type = metadata.find(".//{http://purl.org/dc/elements/1.1/}type").text
            extent = metadata.find(".//{http://purl.org/dc/terms/}extent").text
            language = tree.find('.//{http://purl.org/dc/elements/1.1/}language')
            if language is not None:
                language = language.text
            yield id_, {
                "ark_id": ark_id,
                "source": source,
                "url": hasversion,
                "title": title,
                "text": description,
                "pub_date": date,
                "publisher": publisher,
                "article_type": article_type,
                "extent": extent,
                "ispartof": ispartof,
                "language": language
            }
