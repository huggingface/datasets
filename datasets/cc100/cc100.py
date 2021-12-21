# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import datasets


_DESCRIPTION = """\
This corpus is an attempt to recreate the dataset used for training XLM-R. This corpus comprises of monolingual data for 100+ languages and also includes data for romanized languages (indicated by *_rom). This was constructed using the urls and paragraph indices provided by the CC-Net repository by processing January-December 2018 Commoncrawl snapshots. Each file comprises of documents separated by double-newlines and paragraphs within the same document separated by a newline. The data is generated using the open source CC-Net repository. No claims of intellectual property are made on the work of preparation of the corpus.
"""
_HOMEPAGE_URL = "http://data.statmt.org/cc-100/"
_CITATION = """\
@inproceedings{conneau-etal-2020-unsupervised,
    title = "Unsupervised Cross-lingual Representation Learning at Scale",
    author = "Conneau, Alexis  and
      Khandelwal, Kartikay  and
      Goyal, Naman  and
      Chaudhary, Vishrav  and
      Wenzek, Guillaume  and
      Guzm{'a}n, Francisco  and
      Grave, Edouard  and
      Ott, Myle  and
      Zettlemoyer, Luke  and
      Stoyanov, Veselin",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.747",
    doi = "10.18653/v1/2020.acl-main.747",
    pages = "8440--8451",
    abstract = "This paper shows that pretraining multilingual language models at scale leads to significant performance gains for a wide range of cross-lingual transfer tasks. We train a Transformer-based masked language model on one hundred languages, using more than two terabytes of filtered CommonCrawl data. Our model, dubbed XLM-R, significantly outperforms multilingual BERT (mBERT) on a variety of cross-lingual benchmarks, including +14.6{%} average accuracy on XNLI, +13{%} average F1 score on MLQA, and +2.4{%} F1 score on NER. XLM-R performs particularly well on low-resource languages, improving 15.7{%} in XNLI accuracy for Swahili and 11.4{%} for Urdu over previous XLM models. We also present a detailed empirical analysis of the key factors that are required to achieve these gains, including the trade-offs between (1) positive transfer and capacity dilution and (2) the performance of high and low resource languages at scale. Finally, we show, for the first time, the possibility of multilingual modeling without sacrificing per-language performance; XLM-R is very competitive with strong monolingual models on the GLUE and XNLI benchmarks. We will make our code and models publicly available.",
}
@inproceedings{wenzek-etal-2020-ccnet,
    title = "{CCN}et: Extracting High Quality Monolingual Datasets from Web Crawl Data",
    author = "Wenzek, Guillaume  and
      Lachaux, Marie-Anne  and
      Conneau, Alexis  and
      Chaudhary, Vishrav  and
      Guzm{'a}n, Francisco  and
      Joulin, Armand  and
      Grave, Edouard",
    booktitle = "Proceedings of the 12th Language Resources and Evaluation Conference",
    month = may,
    year = "2020",
    address = "Marseille, France",
    publisher = "European Language Resources Association",
    url = "https://www.aclweb.org/anthology/2020.lrec-1.494",
    pages = "4003--4012",
    abstract = "Pre-training text representations have led to significant improvements in many areas of natural language processing. The quality of these models benefits greatly from the size of the pretraining corpora as long as its quality is preserved. In this paper, we describe an automatic pipeline to extract massive high-quality monolingual datasets from Common Crawl for a variety of languages. Our pipeline follows the data processing introduced in fastText (Mikolov et al., 2017; Grave et al., 2018), that deduplicates documents and identifies their language. We augment this pipeline with a filtering step to select documents that are close to high quality corpora like Wikipedia.",
    language = "English",
    ISBN = "979-10-95546-34-4",
}
"""

_VERSION = "1.0.0"
_BASE_URL = "http://data.statmt.org/cc-100/{}.txt.xz"

# Please note: due to the size of the data, only few examples are provided.
# However, you can pass the lang parameter in config to fetch data of any language in the corpus
_LANGUAGES = ["am", "sr", "ka"]


class Cc100Config(datasets.BuilderConfig):
    def __init__(self, *args, lang=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang}",
            **kwargs,
        )
        self.lang = lang


class Cc100(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        Cc100Config(
            lang=lang,
            description=f"Language: {lang}",
            version=datasets.Version(_VERSION),
        )
        for lang in _LANGUAGES
    ]
    BUILDER_CONFIG_CLASS = Cc100Config

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                },
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        def _base_url(lang):
            return _BASE_URL.format(lang)

        download_url = _base_url(self.config.lang)
        path = dl_manager.download_and_extract(download_url)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": path},
            )
        ]

    def _generate_examples(self, datapath):
        with open(datapath, encoding="utf-8") as f:
            for sentence_counter, row in enumerate(f):
                result = (
                    sentence_counter,
                    {
                        "id": str(sentence_counter),
                        "text": row,
                    },
                )
                yield result
