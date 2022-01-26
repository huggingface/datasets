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
from datasets.tasks import LanguageModeling


_CITATION = """\
@misc{bnl_newspapers,
title={Historical Newspapers},
url={https://data.bnl.lu/data/historical-newspapers/},
author={ Bibliothèque nationale du Luxembourg},
"""

_DESCRIPTION = """\
Digitised historic newspapers from the Bibliothèque nationale (BnL) - the National Library of Luxembourg.
"""

_HOMEPAGE = "https://data.bnl.lu/data/historical-newspapers/"

_LICENSE = "CC0"


_URLs = {"processed": "https://data.bnl.lu/open-data/digitization/newspapers/export01-newspapers1841-1878.zip"}


class BNLNewspapersConfig(datasets.BuilderConfig):
    """Builder config for BNLNewspapers"""

    def __init__(self, data_url, citation, url, **kwargs):
        """
        Args:
        data_url: `string`, url to download the zip file from.
        citation: `string`, citation for the data set.
        url: `string`, url for information about the data set.
        **kwargs: keyword arguments forwarded to super.
        """
        super(BNLNewspapersConfig, self).__init__(version=datasets.Version("1.17.0"), **kwargs)
        self.data_url = data_url
        self.citation = citation
        self.url = url


class BNLNewspapers(datasets.GeneratorBasedBuilder):
    """Historic newspapers from the BNL"""

    BUILDER_CONFIGS = [
        BNLNewspapersConfig(
            name="processed",
            description="""This dataset covers the 'processed newspapers' portion of the BnL newspapers.
These newspapers cover 38 years of news (1841-1878) and include 510,505 extracted articles.
""",
            data_url=_URLs["processed"],
            citation=_CITATION,
            url=_HOMEPAGE,
        ),
    ]

    DEFAULT_CONFIG_NAME = "processed"

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "source": datasets.Value("string"),
                "url": datasets.Value("string"),
                "title": datasets.Value("string"),
                "ispartof": datasets.Value("string"),
                "text": datasets.Value("string"),
                "pub_date": datasets.Value("timestamp[s]"),
                "publisher": datasets.Value("string"),
                "language": datasets.Value("string"),
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
            task_templates=[LanguageModeling(text_column="text")],
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        _URL = self.config.data_url
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
        ns = {
            "": "http://www.openarchives.org/OAI/2.0/",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "oai_dc": "http://www.openarchives.org/OAI/2.0/oai_dc/",
            "dc": "http://purl.org/dc/elements/1.1/",
            "dcterms": "http://purl.org/dc/terms/",
        }
        for id_, xml in enumerate(Path(dirpath).rglob("**/*.xml")):
            tree = ET.parse(open(xml, encoding="utf-8"))
            source = tree.find(".//dc:source", ns).text
            ark_id = tree.find(".//dc:identifier", ns).text
            ispartof = tree.find(".//dcterms:isPartOf", ns).text
            date = tree.find(".//dc:date", ns).text
            if date:
                date = datetime.strptime(date, "%Y-%m-%d")
            publisher = tree.find(".//dc:publisher", ns)
            if publisher is not None:
                publisher = publisher.text
            hasversion = tree.find(".//dcterms:hasVersion", ns).text
            description = tree.find(".//dc:description", ns).text
            title = tree.find(".//dc:title", ns).text
            article_type = tree.find(".//dc:type", ns).text
            extent = tree.find(".//dcterms:extent", ns).text
            language = tree.find(".//dc:language", ns)
            if language is not None:
                language = language.text
            yield id_, {
                "id": ark_id,
                "source": source,
                "url": hasversion,
                "title": title,
                "text": description,
                "pub_date": date,
                "publisher": publisher,
                "article_type": article_type,
                "extent": extent,
                "ispartof": ispartof,
                "language": language,
            }
