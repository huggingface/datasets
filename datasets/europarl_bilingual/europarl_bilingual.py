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


import os
import xml.etree.ElementTree as ET

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = "http://www.lrec-conf.org/proceedings/lrec2012/pdf/463_Paper.pdf"

# You can copy an official description
_DESCRIPTION = """\
A parallel corpus extracted from the European Parliament web site by Philipp Koehn (University of Edinburgh). The main intended use is to aid statistical machine translation research.
"""

# Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://opus.nlpl.eu/Europarl.php"

#  Add the licence for the dataset here if you can find it
_LICENSE = """\
The data set comes with the same license
as the original sources.
Please, check the information about the source
that is given on
http://opus.nlpl.eu/Europarl-v8.php
"""

# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
LANGUAGES = [
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "hu",
    "it",
    "lt",
    "lv",
    "nl",
    "pl",
    "pt",
    "ro",
    "sk",
    "sl",
    "sv",
]

ALL_PAIRS = []
for i in range(len(LANGUAGES)):
    for j in range(i + 1, len(LANGUAGES)):
        ALL_PAIRS.append((LANGUAGES[i], LANGUAGES[j]))

_VERSION = "8.0.0"
_BASE_URL_DATASET = "https://opus.nlpl.eu/download.php?f=Europarl/v8/raw/{}.zip"
_BASE_URL_RELATIONS = "https://opus.nlpl.eu/download.php?f=Europarl/v8/xml/{}-{}.xml.gz"


class EuroparlBilingualConfig(datasets.BuilderConfig):
    """Slightly custom config to require source and target languages."""

    def __init__(self, *args, lang1=None, lang2=None, **kwargs):
        super().__init__(
            *args,
            name=f"{lang1}-{lang2}",
            **kwargs,
        )
        self.lang1 = lang1
        self.lang2 = lang2

    def _lang_pair(self):
        return (self.lang1, self.lang2)

    def _is_valid(self):
        return self._lang_pair() in ALL_PAIRS


class EuroparlBilingual(datasets.GeneratorBasedBuilder):
    """Europarl contains aligned sentences in multiple west language pairs."""

    VERSION = datasets.Version(_VERSION)

    BUILDER_CONFIG_CLASS = EuroparlBilingualConfig
    BUILDER_CONFIGS = [
        EuroparlBilingualConfig(lang1=lang1, lang2=lang2, version=datasets.Version(_VERSION))
        for lang1, lang2 in ALL_PAIRS[:5]
    ]

    def _info(self):
        """This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset."""
        features = datasets.Features(
            {
                "translation": datasets.Translation(languages=(self.config.lang1, self.config.lang2)),
            }
        )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        if not self.config._is_valid():
            raise ValueError(f"{self.config._lang_pair()} is not a supported language pair. Choose among: {ALL_PAIRS}")

        # download data files
        path_datafile_1 = dl_manager.download_and_extract(_BASE_URL_DATASET.format(self.config.lang1))
        path_datafile_2 = dl_manager.download_and_extract(_BASE_URL_DATASET.format(self.config.lang2))

        # download relations file
        path_relation_file = dl_manager.download_and_extract(
            _BASE_URL_RELATIONS.format(self.config.lang1, self.config.lang2)
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "path_datafiles": (path_datafile_1, path_datafile_2),
                    "path_relation_file": path_relation_file,
                },
            )
        ]

    @staticmethod
    def _parse_xml_datafile(filepath):
        """
        Parse and return a Dict[sentence_id, text] representing data with the following structure:
        """
        document = ET.parse(filepath).getroot()
        return {tag.attrib["id"]: tag.text for tag in document.iter("s")}

    def _generate_examples(self, path_datafiles, path_relation_file):
        """Yields examples.
        In parenthesis the useful attributes

        Lang files XML
        - document
            - CHAPTER ('ID')
                - P ('id')
                    - s ('id')

        Relation file XML
        - cesAlign
            - linkGrp ('fromDoc', 'toDoc')
                - link ('xtargets': '1;1')
        """

        # my counter
        _id = 0
        relations_root = ET.parse(path_relation_file).getroot()

        for linkGroup in relations_root:
            # retrieve files and remove .gz extension because 'datasets' library already decompress them
            from_doc_dict = EuroparlBilingual._parse_xml_datafile(
                os.path.splitext(os.path.join(path_datafiles[0], "Europarl", "raw", linkGroup.attrib["fromDoc"]))[0]
            )

            to_doc_dict = EuroparlBilingual._parse_xml_datafile(
                os.path.splitext(os.path.join(path_datafiles[1], "Europarl", "raw", linkGroup.attrib["toDoc"]))[0]
            )

            for link in linkGroup:
                from_sentence_ids, to_sentence_ids = link.attrib["xtargets"].split(";")
                from_sentence_ids = [i for i in from_sentence_ids.split(" ") if i]
                to_sentence_ids = [i for i in to_sentence_ids.split(" ") if i]

                if not len(from_sentence_ids) or not len(to_sentence_ids):
                    continue

                # in rare cases, there is not entry for some key pairs
                sentence_lang1 = " ".join(from_doc_dict[i] for i in from_sentence_ids if i in from_doc_dict)
                sentence_lang2 = " ".join(to_doc_dict[i] for i in to_sentence_ids if i in to_doc_dict)

                yield _id, {"translation": {self.config.lang1: sentence_lang1, self.config.lang2: sentence_lang2}}
                _id += 1
