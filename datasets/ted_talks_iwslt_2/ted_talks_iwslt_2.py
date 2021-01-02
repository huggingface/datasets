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
"""TED TALKS IWSLT: Web Inventory of Transcribed and Translated Ted Talks."""

from __future__ import absolute_import, division, print_function

import os
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@inproceedings{cettolo-etal-2012-wit3,
    title = "{WIT}3: Web Inventory of Transcribed and Translated Talks",
    author = "Cettolo, Mauro  and
      Girardi, Christian  and
      Federico, Marcello",
    booktitle = "Proceedings of the 16th Annual conference of the European Association for Machine Translation",
    month = may # " 28{--}30",
    year = "2012",
    address = "Trento, Italy",
    publisher = "European Association for Machine Translation",
    url = "https://www.aclweb.org/anthology/2012.eamt-1.60",
    pages = "261--268",
}
"""

# You can copy an official description
_DESCRIPTION = """\
The core of WIT3 is the TED Talks corpus, that basically redistributes the original content published by the TED Conference website (http://www.ted.com). Since 2007,
the TED Conference, based in California, has been posting all video recordings of its talks together with subtitles in English
and their translations in more than 80 languages. Aside from its cultural and social relevance, this content, which is published under the Creative Commons BYNC-ND license, also represents a precious
language resource for the machine translation research community, thanks to its size, variety of topics, and covered languages.
This effort repurposes the original content in a way which is more convenient for machine translation researchers.
"""
# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://wit3.fbk.eu/"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "CC-BY-NC-4.0"

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLs = "https://drive.google.com/file/d/1Cz1Un9p8Xn9IpEMMrg2kXSDt0dnjxc4z/view?usp=sharing"

_LANGUAGES = (
    "mr",
    "eu",
    "hr",
    "rup",
    "szl",
    "lo",
    "ms",
    "ht",
    "hy",
    "mg",
    "arq",
    "uk",
    "ku",
    "ig",
    "sr",
    "ug",
    "ne",
    "pt-br",
    "sq",
    "af",
    "km",
    "en",
    "tt",
    "ja",
    "inh",
    "mn",
    "eo",
    "ka",
    "nb",
    "fil",
    "uz",
    "fi",
    "tl",
    "el",
    "tg",
    "bn",
    "si",
    "gu",
    "sk",
    "kn",
    "ar",
    "hup",
    "zh-tw",
    "sl",
    "be",
    "bo",
    "fr",
    "ps",
    "tr",
    "ltg",
    "la",
    "ko",
    "lv",
    "nl",
    "fa",
    "ru",
    "et",
    "vi",
    "pa",
    "my",
    "sw",
    "az",
    "sv",
    "ga",
    "sh",
    "it",
    "da",
    "lt",
    "kk",
    "mk",
    "tlh",
    "he",
    "ceb",
    "bg",
    "fr-ca",
    "ha",
    "ml",
    "mt",
    "as",
    "pt",
    "zh-cn",
    "cnh",
    "ro",
    "hi",
    "es",
    "id",
    "bs",
    "so",
    "cs",
    "te",
    "ky",
    "hu",
    "th",
    "pl",
    "nn",
    "ca",
    "is",
    "ta",
    "de",
    "srp",
    "ast",
    "bi",
    "lb",
    "art-x-bork",
    "am",
    "oc",
    "zh",
    "ur",
    "gl",
)

_ALL_LANGUAGES = "all_languages"


class TedTalksIWSLT2Config(datasets.BuilderConfig):
    """"Builder Config for the TedTalks IWSLT dataset"""

    def __init__(self, language=None, **kwargs):
        """BuilderConfig for TedTalks IWSLT dataset.
        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
            language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings. First will be used at source and second
            as target in supervised mode. For example: ("pl", "en").
          **kwargs: keyword arguments forwarded to super.
        """
        # Validate language pair.
        if type(language) == str:
            name = "%s" % language
            source = language
            assert source in _LANGUAGES, ("Invalid source language in pair: %s", source)
            description = "Transcribed & Translation Ted Talks dataset (WIT3) for %s", source
        else:
            name = _ALL_LANGUAGES
            source = _LANGUAGES
            description = "Transcribed & Translation for Multi-Language Ted Talks (WIT3"

        super(TedTalksIWSLT2Config, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.1.0", ""),
            **kwargs,
        )

        self.language = language


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class TedTalksIWSLT2(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.1.0")

    @property
    def manual_download_instructions(self):
        return """\
        \nThe file can be downloaded from: https://drive.google.com/file/d/1Cz1Un9p8Xn9IpEMMrg2kXSDt0dnjxc4z/view?usp=sharing
        Unzip the file to obtain folder: XML_releases
        The folder structure is similar to this:

        XML_releases
            |
            |---xml
            |    |---ted_af-20160408.zip
            |    |---ted_am-20160408.zip
            |     ....
            |     ....
            |---xml-20150616
            |---xml-20140120
            |---wit3_data

        You can then specify the path to this folder for the __data_dir__ argument in the __datasets.load_dataset(...)__
        The data can then be loaded using the following command:
        __datasets.load_dataset("ted_talks_iwslt", data_dir="XML_releases", "en-hi")__
        """

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    BUILDER_CONFIG_CLASS = TedTalksIWSLT2Config

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    DEFAULT_CONFIG_NAME = (
        _ALL_LANGUAGES  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    BUILDER_CONFIGS = [
        TedTalksIWSLT2Config(language=source) for source in _LANGUAGES
    ]  # + [TedTalksIWSLT2Config(language=_LANGUAGES)]

    def _info(self):
        # TODO: Add for all languages (default config)
        features = datasets.Features(
            {
                "talk_id": datasets.Value("string"),
                "language": datasets.Value("string"),
                "title": datasets.Value("string"),
                "description": datasets.Value("string"),
                "transcription": [
                    {"seekvideo_id": datasets.Value("string"), "text": datasets.Value("string")},
                ],
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive

        language = self.config.language
        # print(language)
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                f"{path_to_manual_file} does not exist. Make sure you insert a manual directory",
                self.manual_download_instructions,
            )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, f"xml-20140120/ted_{language}-20140120.zip"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, f"xml/ted_{language}-20160408.zip"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, f"xml-20150616/ted_{language}-20150530.zip"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        source = filepath
        language = self.config.language
        print(filepath)

        def et_to_dict(tree):
            """This is used to convert the xml to a list of dicts"""

            dct = {tree.tag: {} if tree.attrib else None}
            children = list(tree)
            if children:
                dd = defaultdict(list)
                for dc in map(et_to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                dct = {tree.tag: dd}
            if tree.attrib:
                dct[tree.tag].update((k, v) for k, v in tree.attrib.items())
            if tree.text:
                text = tree.text.strip()
                if children or tree.attrib:
                    if text:
                        dct[tree.tag]["text"] = text
                else:
                    dct[tree.tag] = text
            return dct

        def get_talks(zipfile):
            filename = zipfile.namelist()[0]
            tree_source = ET.parse(zf_source.open(filename))
            root_source = tree_source.getroot()
            source_talks = et_to_dict(root_source).get("xml").get("file")

            return source_talks

        if os.path.exists(source):
            with zipfile.ZipFile(source) as zf_source:
                try:
                    source_talks = get_talks(zf_source)
                    # source_ids = [talk.get("head")[0].get("talkid")[0] for talk in source_talks]

                except Exception as pe:
                    print(f"ERROR: {pe}")
                    print(f"Which likely means that you have a malformed XML file:: {source}\n")
                    source_talks = list()
        else:
            print(f"File doesn't exist:: {source}")
            source_talks = list()

        translations = list()
        for source in source_talks:
            talk_dict = dict()
            talk_dict["talk_id"] = source.get("head")[0].get("talkid")[0]
            talk_dict["language"] = language

            if source.get("head")[0].get("description") and source.get("head")[0].get("description")[0]:
                talk_dict["description"] = source.get("head")[0].get("description")[0]
                talk_dict["description"] = talk_dict["description"].replace("TED Talk Subtitles and Transcript: ", "")
            else:
                talk_dict["description"] = ""

            if source.get("head")[0].get("title") and source.get("head")[0].get("title")[0]:
                talk_dict["title"] = source.get("head")[0].get("title")[0]
            else:
                talk_dict["title"] = ""

            if source.get("head")[0].get("transcription") and source.get("head")[0].get("transcription")[0]:
                source_transc = source.get("head")[0].get("transcription")[0].get("seekvideo")
                transcription = [{"seekvideo_id": s.get("id"), "text": s.get("text")} for s in source_transc]
                talk_dict["transcription"] = transcription
            else:
                talk_dict["transcription"] = list()

            translations.append(talk_dict)

        for talk in translations:
            yield talk["talk_id"], talk
