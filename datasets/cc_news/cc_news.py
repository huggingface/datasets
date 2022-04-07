# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""The CC-News dataset is based on Common Crawl News Dataset by Sebastian Nagel"""

import json
import os
from fnmatch import fnmatch

import datasets


logger = datasets.logging.get_logger(__name__)


_DESCRIPTION = """\
CC-News containing news articles from news sites all over the world \
The data is available on AWS S3 in the Common Crawl bucket at /crawl-data/CC-NEWS/. \
This version of the dataset has 708241 articles. It represents a small portion of English  \
language subset of the CC-News dataset created using news-please(Hamborg et al.,2017) to \
collect and extract English language portion of CC-News.
"""

_CITATION = """\
@InProceedings{Hamborg2017,
  author     = {Hamborg, Felix and Meuschke, Norman and Breitinger, Corinna and Gipp, Bela},
  title      = {news-please: A Generic News Crawler and Extractor},
  year       = {2017},
  booktitle  = {Proceedings of the 15th International Symposium of Information Science},
  location   = {Berlin},
  doi        = {10.5281/zenodo.4120316},
  pages      = {218--223},
  month      = {March}
}
"""
_PROJECT_URL = "https://commoncrawl.org/2016/10/news-dataset-available/"
_DOWNLOAD_URL = "https://storage.googleapis.com/huggingface-nlp/datasets/cc_news/cc_news.tar.gz"


class CCNewsConfig(datasets.BuilderConfig):
    """BuilderConfig for CCNews."""

    def __init__(self, **kwargs):
        """BuilderConfig for CCNews.
        Args:
        **kwargs: keyword arguments forwarded to super.
        """
        super(CCNewsConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class CCNews(datasets.GeneratorBasedBuilder):
    """CC-News dataset."""

    BUILDER_CONFIGS = [
        CCNewsConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "title": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "domain": datasets.Value("string"),
                    "date": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "url": datasets.Value("string"),
                    "image_url": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_PROJECT_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"files": dl_manager.iter_archive(archive)}),
        ]

    def _generate_examples(self, files):
        id_ = 0
        for article_file_path, f in files:
            if fnmatch(os.path.basename(article_file_path), "*.json"):
                article = json.load(f)
                yield id_, {
                    "title": article["title"].strip() if article["title"] is not None else "",
                    "text": article["maintext"].strip() if article["maintext"] is not None else "",
                    "domain": article["source_domain"].strip() if article["source_domain"] is not None else "",
                    "date": article["date_publish"].strip() if article["date_publish"] is not None else "",
                    "description": article["description"].strip() if article["description"] is not None else "",
                    "url": article["url"].strip() if article["url"] is not None else "",
                    "image_url": article["image_url"].strip() if article["image_url"] is not None else "",
                }
                id_ += 1
