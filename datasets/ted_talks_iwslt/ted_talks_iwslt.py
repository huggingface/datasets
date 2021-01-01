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


# TODO: Add BibTeX citation
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

# TODO: Add description of the dataset here
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


class TedTalksIWSLTConfig(datasets.BuilderConfig):
    """"Builder Config for the TedTalks IWSLT dataset"""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for TedTalks IWSLT dataset.
        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
            language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings. First will be used at source and second
            as target in supervised mode. For example: ("pl", "en").
          **kwargs: keyword arguments forwarded to super.
        """
        # Validate language pair.
        name = "%s_%s" % (language_pair[0], language_pair[1])
        source, target = language_pair
        assert source in _LANGUAGES, ("Invalid source language in pair: %s", source)
        assert target in _LANGUAGES, ("Invalid source language in pair: %s", source)
        assert source != target, ("Source(%s) and Target(%s) language pairs cannot be the same!", source, target)

        description = f"Translation Ted Talks dataset (WIT3) between {source} and {target}"
        super(TedTalksIWSLTConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.1.0", ""),
            **kwargs,
        )

        self.language_pair = language_pair


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class TedTalksIWSLT(datasets.GeneratorBasedBuilder):
    """TedTalks IWSLT Dataset. 109 language translations"""

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
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        TedTalksIWSLTConfig(language_pair=(source, target))
        for source in _LANGUAGES
        for target in _LANGUAGES
        if source != target
    ]

    # DEFAULT_CONFIG_NAME = (
    #     "ted_talks_2016_all"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    # )

    def _info(self, language_pair=(None, None), **kwargs):
        features = datasets.Features(
            {"translation": datasets.features.Translation(languages=self.config.language_pair)}
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

        language_pair = self.config.name.split("_")
        #print(language_pair)
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
                    "filepath": [
                        os.path.join(path_to_manual_file, f"xml-20140120/ted_{language_pair[0]}-20140120.zip"),
                        os.path.join(path_to_manual_file, f"xml-20140120/ted_{language_pair[1]}-20140120.zip"),
                    ],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": [
                        os.path.join(path_to_manual_file, f"xml/ted_{language_pair[0]}-20160408.zip"),
                        os.path.join(path_to_manual_file, f"xml/ted_{language_pair[1]}-20160408.zip"),
                    ],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": [
                        os.path.join(path_to_manual_file, f"xml-20150616/ted_{language_pair[0]}-20150530.zip"),
                        os.path.join(path_to_manual_file, f"xml-20150616/ted_{language_pair[1]}-20150530.zip"),
                    ],
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)
        source = filepath[0]
        target = filepath[1]

        #print(filepath)
        language_pair = self.config.name.split("_")

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

        if os.path.exists(source) and os.path.exists(target):
            
            with zipfile.ZipFile(source) as zf_source:
                with zipfile.ZipFile(target) as zf_target:
                    try:
                        tree_source = ET.parse(zf_source.open(source.split("/")[-1][:-3] + "xml"))
                        root_source = tree_source.getroot()
                        source_talks = et_to_dict(root_source).get("xml").get("file")

                        tree_target = ET.parse(zf_target.open(target.split("/")[-1][:-3] + "xml"))
                        root_target = tree_target.getroot()
                        target_talks = et_to_dict(root_target).get("xml").get("file")

                        source_ids = [talk.get("head")[0].get("talkid") for talk in source_talks]
                        target_ids = [talk.get("head")[0].get("talkid") for talk in target_talks]
                    except Exception as pe:
                        print(f"ERROR: {pe}")
                        print(f"Which likely means that you have a malformed XML file!\nEither {source} or {target}\n")
                        source_ids = list()
                        target_ids = list()
        else:
            print(f"File doesn't exist {source} or {target}")
            source_ids = list()
            target_ids = list()

        comm_talkids = [talkid for talkid in target_ids if talkid in source_ids]

        translation = list()

        for talkid in comm_talkids:
            source = list(filter(lambda talk: talk.get("head")[0].get("talkid") == talkid, source_talks))
            target = list(filter(lambda talk: talk.get("head")[0].get("talkid") == talkid, target_talks))

            if len(source) == 0 or len(target) == 0:
                pass
            else:
                #                 print(f"Source: {len(source)}")
                #                 print(f"Target: {len(target)}")

                source = source[0]
                target = target[0]

            if source.get("head")[0].get("description") and target.get("head")[0].get("description"):
                if source.get("head")[0].get("description")[0] and target.get("head")[0].get("description")[0]:
                    temp_dict = dict()
                    temp_dict["id"] = source.get("head")[0].get("talkid")[0] + "_1"
                    temp_dict[language_pair[0]] = (
                        source.get("head")[0].get("description")[0].replace("TED Talk Subtitles and Transcript: ", "")
                    )
                    temp_dict[language_pair[1]] = (
                        target.get("head")[0].get("description")[0].replace("TED Talk Subtitles and Transcript: ", "")
                    )
                    translation.append(temp_dict)

            if source.get("head")[0].get("title") and target.get("head")[0].get("title"):
                if source.get("head")[0].get("title")[0] and target.get("head")[0].get("title")[0]:
                    temp_dict = dict()
                    temp_dict["id"] = source.get("head")[0].get("talkid")[0] + "_2"
                    temp_dict[language_pair[0]] = source.get("head")[0].get("title")[0]
                    temp_dict[language_pair[1]] = target.get("head")[0].get("title")[0]
                    translation.append(temp_dict)

            if source.get("head")[0].get("seekvideo") and target.get("head")[0].get("seekvideo"):
                source_transc = source.get("head")[0].get("transcription")[0].get("seekvideo")
                target_transc = target.get("head")[0].get("transcription")[0].get("seekvideo")

                transc = zip(source_transc, target_transc)
                transcriptions = [
                    {"id": s.get("id"), language_pair[0]: s.get("text"), language_pair[1]: t.get("text")}
                    for s, t in transc
                ]
                translation.extend(transcriptions)
        # print(translation)
        for talk_segment in translation:
            result = {
                "translation": {
                    language_pair[0]: talk_segment[language_pair[0]],
                    language_pair[1]: talk_segment[language_pair[1]],
                }
            }
            yield talk_segment["id"], result
