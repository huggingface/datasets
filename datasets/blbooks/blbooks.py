# coding=utf-8
# Copyright 2022 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
import gzip
import json
from datetime import datetime
from functools import lru_cache
from typing import Dict, List

import datasets
from datasets.tasks import LanguageModeling


_CITATION = """\
@misc{BritishLibraryBooks2021,
  author = {British Library Labs},
  title = {Digitised Books. c. 1510 - c. 1900. JSONL (OCR derived text + metadata)},
  year = {2021},
  publisher = {British Library},
  howpublished={https://doi.org/10.23636/r7w6-zy15}
"""

_DESCRIPTION = """\
A dataset comprising of text created by OCR from the 49,455 digitised books, equating to 65,227 volumes (25+ million pages), published between c. 1510 - c. 1900.
The books cover a wide range of subject areas including philosophy, history, poetry and literature.
"""

_BASE_URL = "https://bl.iro.bl.uk/downloads/"


_DATA_URLS = {
    "1510_1699": _BASE_URL + "61f58234-b370-422f-8591-8f98e46c2757?locale=en",
    "1700_1799": _BASE_URL + "78b4a8ec-395e-4383-831c-809faff85ad7?locale=en",
    "1800_1809": _BASE_URL + "91ae15cb-e08f-4abf-8396-e4742d9d4e37?locale=en",
    "1810_1819": _BASE_URL + "6d1a6e17-f28d-45b9-8f7a-a03cf3a96491?locale=en",
    "1820_1829": _BASE_URL + "ec764dbd-1ed4-4fc2-8668-b4df5c8ec451?locale=en",
    "1830_1839": _BASE_URL + "eab68022-0418-4df7-a401-78972514ed20?locale=en",
    "1840_1849": _BASE_URL + "d16d88b0-aa3f-4dfe-b728-c58d168d7b4d?locale=en",
    "1850_1859": _BASE_URL + "a6a44ea8-8d33-4880-8b17-f89c90e3d89a?locale=en",
    "1860_1869": _BASE_URL + "2e17f00f-52e6-4259-962c-b88ad60dec23?locale=en",
    "1870_1879": _BASE_URL + "899c3719-030c-4517-abd3-b28fdc85eed4?locale=en",
    "1880_1889": _BASE_URL + "ec3b8545-775b-47bd-885d-ce895263709e?locale=en",
    "1890_1899": _BASE_URL + "54ed2842-089a-439a-b751-2179b3ffba28?locale=en",
}

_ALL = list(_DATA_URLS.values())
_1800_1899 = [
    _DATA_URLS.get(subset)
    for subset in [
        "1800_1809",
        "1810_1819",
        "1820_1829",
        "1830_1839",
        "1840_1849",
        "1850_1859",
        "1860_1869",
        "1870_1879",
        "1880_1889",
        "1890_1899",
    ]
]
_1700_1799 = [_DATA_URLS.get(subset) for subset in ["1700_1799"]]
_1510_1699 = [_DATA_URLS.get(subset) for subset in ["1510_1699"]]

URL = "https://doi.org/10.23636/r7w6-zy15"

features = datasets.Features(
    {
        "record_id": datasets.Value("string"),
        "date": datasets.Value("timestamp[s]"),
        "raw_date": datasets.Value("string"),
        "title": datasets.Value("string"),
        "place": datasets.Value("string"),
        "empty_pg": datasets.Value("bool"),
        "text": datasets.Value("string"),
        "pg": datasets.Value("int32"),
        "mean_wc_ocr": datasets.Value("float32"),
        "std_wc_ocr": datasets.Value("float64"),
        "name": datasets.Value("string"),
        "all_names": datasets.Value("string"),
        "Publisher": datasets.Value("string"),
        "Country of publication 1": datasets.Value("string"),
        "all Countries of publication": datasets.Value("string"),
        "Physical description": datasets.Value("string"),
        "Language_1": datasets.Value("string"),
        "Language_2": datasets.Value("string"),
        "Language_3": datasets.Value("string"),
        "Language_4": datasets.Value("string"),
        "multi_language": datasets.Value("bool"),
    }
)


class BritishLibraryBooksConfig(datasets.BuilderConfig):
    """BuilderConfig for BritishLibraryBooks."""

    def __init__(self, data_urls, citation, url, skip_empty=False, **kwargs):
        """BuilderConfig for BritishLibraryBooks.

        Args:
        data_url: `string`, url to download the zip file from.
        citation: `string`, citation for the data set.
        url: `string`, url for information about the data set.
        skip_empty: `bool`, whether to skip empty pages.
        **kwargs: keyword arguments forwarded to super.
        """

        super(BritishLibraryBooksConfig, self).__init__(version=datasets.Version("1.0.2"), **kwargs)
        self.url: str = url
        self.data_urls: List[str] = data_urls
        self.citation: str = citation
        self.skip_empty: bool = skip_empty


class BritishLibraryBooks(datasets.GeneratorBasedBuilder):
    """The BritishLibraryBooks dataset."""

    BUILDER_CONFIGS = [
        BritishLibraryBooksConfig(
            name="1500_1899",
            description="All periods of" + _DESCRIPTION,
            data_urls=_ALL,
            citation=_CITATION,
            url=URL,
            skip_empty=True,
        ),
        BritishLibraryBooksConfig(
            name="1800_1899",
            description="A subset covering texts published during the 1800-1899 of" + _DESCRIPTION,
            data_urls=_1800_1899,
            citation=_CITATION,
            url=URL,
            skip_empty=True,
        ),
        BritishLibraryBooksConfig(
            name="1700_1799",
            description="Subset covering 1700-1799 of" + _DESCRIPTION,
            data_urls=_1700_1799,
            citation=_CITATION,
            url=URL,
            skip_empty=True,
        ),
        BritishLibraryBooksConfig(
            name="1510_1699",
            description="Subset covering 1510-1699 of " + _DESCRIPTION,
            data_urls=_1510_1699,
            citation=_CITATION,
            url=URL,
            skip_empty=True,
        ),
    ]

    DEFAULT_CONFIG_NAME = "1500_1899"

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage="https://www.bl.uk/collection-guides/digitised-printed-books",
            citation=_CITATION,
            task_templates=[LanguageModeling(text_column="text")],
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager):
        urls_to_download = self.config.data_urls
        downloaded_archives = dl_manager.download(urls_to_download)
        downloaded_archives = [dl_manager.iter_archive(archive) for archive in downloaded_archives]
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"data_dirs": downloaded_archives})]

    @lru_cache(maxsize=512)
    def _parse_date(self, date):
        if date is not None:
            date = datetime.strptime(str(date), "%Y")
        return date

    def _parse_data(self, data: Dict) -> Dict:
        mean_wc_ocr = data["mean_wc_ocr"]
        mean_wc_ocr = float(mean_wc_ocr) if mean_wc_ocr else None
        std_wc_ocr = data["std_wc_ocr"]
        std_wc_ocr = float(data["std_wc_ocr"]) if std_wc_ocr else None
        date = data["date"]
        if date is not None:
            date = datetime.strptime(str(date), "%Y")
        return {
            "record_id": data["record_id"],
            "date": date,
            "raw_date": data["raw_date"],
            "title": data["title"],
            "place": data["place"],
            "text": data["text"],
            "pg": int(data["pg"]),
            "mean_wc_ocr": data["mean_wc_ocr"],
            "std_wc_ocr": std_wc_ocr,
            "name": data["Name"],
            "all_names": data["All names"],
            "Publisher": data["Publisher"],
            "Country of publication 1": data["Country of publication 1"],
            "all Countries of publication": data["All Countries of publication"],
            "Physical description": data["Physical description"],
            "Language_1": data["Language_1"],
            "Language_2": data["Language_2"],
            "Language_3": data["Language_3"],
            "Language_4": data["Language_4"],
            "multi_language": data["multi_language"],
        }

    def _generate_examples(self, data_dirs):
        skip_empty = self.config.skip_empty
        id_ = 0
        for data_dir in data_dirs:
            for path, file in data_dir:
                if not path.endswith(".gz"):
                    continue
                with gzip.open(file) as json_l:
                    for row in json_l:
                        data = json.loads(row)
                        empty_pg = data["empty_pg"]
                        if skip_empty and empty_pg:
                            continue
                        parsed_data = self._parse_data(data)
                        yield id_, {**parsed_data, **{"empty_pg": empty_pg}}
                        id_ += 1
