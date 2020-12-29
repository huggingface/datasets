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
"""Arabic Billion Words Corpus"""

from __future__ import absolute_import, division, print_function

import os
import re

import datasets


_CITATION = """\
@article{el20161,
  title={1.5 billion words arabic corpus},
  author={El-Khair, Ibrahim Abu},
  journal={arXiv preprint arXiv:1611.04033},
  year={2016}
}
"""

_DESCRIPTION = """\
Abu El-Khair Corpus is an Arabic text corpus, that includes more than five million newspaper articles.
It contains over a billion and a half words in total, out of which, there are about three million unique words.
The corpus is encoded with two types of encoding, namely: UTF-8, and Windows CP-1256.
Also it was marked with two mark-up languages, namely: SGML, and XML.
"""

_HOMEPAGE = "http://abuelkhair.net/index.php/en/arabic/abu-el-khair-corpus"

_URL = "http://abuelkhair.net/corpus/"
_URLs = {
    "Alittihad": _URL + "Alittihad_XML_utf_8.rar",
    "Almasryalyoum": _URL + "Almasryalyoum_XML_utf_8.rar",
    "Almustaqbal": _URL + "Almustaqbal_XML_utf_8.rar",
    "Alqabas": _URL + "Alqabas_XML_utf_8.rar",
    "Echoroukonline": _URL + "Echoroukonline_XML_utf_8.rar",
    "Ryiadh": _URL + "Ryiadh_XML_utf_8.rar",
    "Sabanews": _URL + "Sabanews_XML_utf_8.rar",
    "SaudiYoum": _URL + "SaudiYoum_XML_utf_8.rar",
    "Techreen": _URL + "Techreen_XML_utf_8.rar",
    "Youm7": _URL + "Youm7_XML_utf_8.rar",
}

# some tags are misspelled
MISS_SPELLED_TAGS = {
    "Dateline": ["Dateline", "dateline"],
    "Headline": ["Headline", "Healine"],
    "Text": ["Text"],
    "URL": ["URL"],
}


class ArabicBillionWords(datasets.GeneratorBasedBuilder):
    """Arabic Billion Words Corpus"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="Alittihad", version=VERSION, description="This part of dataset covers Alittihad news paper"
        ),
        datasets.BuilderConfig(
            name="Almasryalyoum", version=VERSION, description="This part of dataset covers Almasryalyoum news paper"
        ),
        datasets.BuilderConfig(
            name="Almustaqbal", version=VERSION, description="This part of dataset covers Almustaqbal news paper"
        ),
        datasets.BuilderConfig(
            name="Alqabas", version=VERSION, description="This part of dataset covers Alqabas news paper"
        ),
        datasets.BuilderConfig(
            name="Echoroukonline", version=VERSION, description="This part of dataset covers Echoroukonline news paper"
        ),
        datasets.BuilderConfig(
            name="Ryiadh", version=VERSION, description="This part of dataset covers Ryiadh news paper"
        ),
        datasets.BuilderConfig(
            name="Sabanews", version=VERSION, description="This part of dataset covers Sabanews news paper"
        ),
        datasets.BuilderConfig(
            name="SaudiYoum", version=VERSION, description="This part of dataset covers SaudiYoum news paper"
        ),
        datasets.BuilderConfig(
            name="Techreen", version=VERSION, description="This part of dataset covers Techreen news paper"
        ),
        datasets.BuilderConfig(
            name="Youm7", version=VERSION, description="This part of dataset covers Youm7 news paper"
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "url": datasets.Value("string"),
                "head_line": datasets.Value("string"),
                "date": datasets.Value("string"),
                "text": datasets.Value("string"),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        my_file_name = f"{self.config.name}_utf_8.xml"
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, my_file_name),
                },
            ),
        ]

    def _extract_tags(self, sample, tag):

        # check if the tag is misspelled
        for tg in MISS_SPELLED_TAGS[tag]:
            pattern = f"<{tg}>(.*?)</{tg}>"
            out = re.findall(r"" + pattern, sample.group(0), re.MULTILINE | re.DOTALL)
            if len(out) > 0:
                break
        return out[0]

    def _clean_text(self, text):
        return text.replace("?", "")

    def _generate_examples(self, filepath):
        """ Yields examples. """
        current_multi_line = ""
        _idx = 0
        data_tag = self.config.name
        with open(filepath, mode="r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                current_multi_line += line
                if i % 8 == 0:
                    pattern = f"<{data_tag}(.*?)</{data_tag}>"
                    data = re.finditer(r"" + pattern, current_multi_line, re.MULTILINE | re.DOTALL)
                    text, url, head_line, date = ["", "", "", ""]
                    for _, record in enumerate(data):
                        try:
                            text = self._clean_text(self._extract_tags(record, "Text"))
                            url = self._extract_tags(record, "URL")
                            head_line = self._clean_text(self._extract_tags(record, "Headline"))
                            date = self._extract_tags(record, "Dateline")
                        except ValueError:
                            pass
                        yield str(_idx), {"url": url, "head_line": head_line, "date": date, "text": text}
                        _idx += 1
                    current_multi_line = ""
