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
"""The dataset contains a set of 31,030 Arabic newspaper articles alongwith metadata, extracted from various online Saudi newspapers."""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@misc{hagrima2015, author = "M. Alhagri", title = "Saudi Newspapers Arabic Corpus \
(SaudiNewsNet)", year = 2015, url = "http://github.com/ParallelMazen/SaudiNewsNet" }
"""


_DESCRIPTION = """\
The dataset contains a set of 31,030 Arabic newspaper articles alongwith metadata, \
extracted from various online Saudi newspapers and written in MSA. 
"""


_HOMEPAGE = "https://github.com/parallelfold/SaudiNewsNet"


_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."


#_URL = "https://github.com/parallelfold/SaudiNewsNet/blob/master/dataset/"

_URL = "https://github.com/parallelfold/SaudiNewsNet/blob/master/dataset/"

_URLs = {
    "batch1": _URL + "2015-07-21.zip",
    "batch2": _URL + "2015-07-22.zip",
    "batch3": _URL + "2015-07-23.zip",
    "batch4": _URL + "2015-07-24.zip",
    "batch5": _URL + "2015-07-25.zip",
    "batch6": _URL + "2015-07-26.zip",
    "batch7": _URL + "2015-07-27.zip",
    "batch8": _URL + "2015-07-31.zip",
    "batch9": _URL + "2015-08-01.zip",
    "batch10": _URL + "2015-08-02.zip",
    "batch11": _URL + "2015-08-03.zip",
    "batch12": _URL + "2015-08-04.zip",
    "batch13": _URL + "2015-08-06.zip",
    "batch14": _URL + "2015-08-07.zip",
    "batch15": _URL + "2015-08-08.zip",
    "batch16": _URL + "2015-08-09.zip",
    "batch17": _URL + "2015-08-10.zip",
    "batch18": _URL + "2015-08-11.zip"
}


class SaudiNewsNet(datasets.GeneratorBasedBuilder):
    """a set of 31,030 Arabic newspaper articles along with metadata"""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "source": datasets.Value("string"), #A string identifief of the newspaper from which the article was extracted. 
                    "url": datasets.Value("string"), #The full URL from which the article was extracted.
                    "date_extracted": datasets.Value("string"), #The timestamp of the date on which the article was extracted.
                    "title": datasets.Value("string"), #The title of the article. Can be empty.
                    "author": datasets.Value("string"), #The author of the article. Can be empty.
                    "content": datasets.Value("string") #The content of the article.
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            supervised_keys=None
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = _URLs
        datadir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": datadir,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        
        #logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8").read() as f:
            articles = json.loads(f)
            for article in articles:
                title = article.get("title", "").strip()
                source = article.get("source", "").strip()
                date = article.get("date_extracted", "").strip()
                link = article.get("url", "").strip()
                author = article.get("author", "").strip()
                content = article.get("content", "").strip()

                yield id_, {
                    "title": title,
                    "source": source,
                    "date": date,
                    "link": link,
                    "author": author,
                    "content": content
                }
                
