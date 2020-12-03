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
"""OPUS DOGC dataset."""

import xml.etree.ElementTree as ET

import datasets


_DESCRIPTION = """\
This is a collection of documents from the Official Journal of the Government of Catalonia, in Catalan and Spanish \
languages, provided by Antoni Oliver Gonzalez from the Universitat Oberta de Catalunya.
"""

_CITATION = """\
@inproceedings{tiedemann-2012-parallel,
    title = "Parallel Data, Tools and Interfaces in {OPUS}",
    author = {Tiedemann, J{\"o}rg},
    booktitle = "Proceedings of the Eighth International Conference on Language Resources and Evaluation ({LREC}'12)",
    month = may,
    year = "2012",
    address = "Istanbul, Turkey",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf",
    pages = "2214--2218",
    abstract = "This paper presents the current status of OPUS, a growing language resource of parallel corpora and related tools. The focus in OPUS is to provide freely available data sets in various formats together with basic annotation to be useful for applications in computational linguistics, translation studies and cross-linguistic corpus studies. In this paper, we report about new data sets and their features, additional annotation tools and models provided from the website and essential interfaces and on-line services included in the project.",
}
"""

_URL = "http://opus.nlpl.eu/DOGC.php"
_FILE_FORMATS = ["tmx"]
_URLS = {"tmx": "http://opus.nlpl.eu/download.php?f=DOGC/v2/tmx/ca-es.tmx.gz"}


class OpusDogcConfig(datasets.BuilderConfig):
    """ BuilderConfig for OpusDogcConfig."""

    def __init__(self, file_format=None, **kwargs):
        """

        Args:
            file_format: language of the subdataset.
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            name=file_format, description=f"OPUS DOGC dataset from source file format {file_format}.", **kwargs
        )
        self.file_format = file_format


class OpusDogc(datasets.GeneratorBasedBuilder):
    """OPUS DOGC dataset."""

    BUILDER_CONFIG_CLASS = OpusDogcConfig
    BUILDER_CONFIGS = [OpusDogcConfig(file_format=file_format) for file_format in _FILE_FORMATS]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=("ca", "es"))}),
            supervised_keys=("ca", "es"),
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        url_to_download = _URLS[self.config.file_format]
        downloaded_file = dl_manager.download_and_extract(url_to_download)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_file}),
        ]

    def _generate_examples(self, filepath):
        xml_lang = "{http://www.w3.org/XML/1998/namespace}lang"
        with open(filepath, encoding="utf-8") as f:
            id_ = 0
            for _, elem in ET.iterparse(f):
                if elem.tag == "tuv":
                    language = elem.attrib[xml_lang]
                    sentence = elem.find("seg").text
                    if language == "ca":
                        ca_sentence = sentence
                    elif language == "es":
                        es_sentence = sentence
                elif elem.tag == "tu":
                    yield id_, {
                        "translation": {"ca": ca_sentence, "es": es_sentence},
                    }
                    id_ += 1
