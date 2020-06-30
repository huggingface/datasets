# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""OSCAR The Open Super-large Crawled ALMAnaCH coRpus."""

from __future__ import absolute_import, division, print_function

import collections
import logging

import nlp


_DESCRIPTION = """\
The Open Super-large Crawled ALMAnaCH coRpus is a huge multilingual corpus \
obtained by language classification and filtering of the Common Crawl corpus \
using the goclassy architecture.\
"""

_URL = "https://oscar-corpus.com"

_LICENSE = """
    These data are released under this licensing scheme
    We do not own any of the text from which these data has been extracted.
    We license the actual packaging of these data under the Creative Commons CC0 license \
    (\"no rights reserved\") http://creativecommons.org/publicdomain/zero/1.0/
    To the extent possible under law, Inria has waived all copyright \
    and related or neighboring rights to OSCAR
    This work is published from: France.

    Should you consider that our data contains material that is owned by you \
    and should therefore not be reproduced here, please:
    * Clearly identify yourself, with detailed contact data such as an address, \
    telephone number or email address at which you can be contacted.
    * Clearly identify the copyrighted work claimed to be infringed.
    * Clearly identify the material that is claimed to be infringing and \
    information reasonably sufficient to allow us to locate the material.
    
    We will comply to legitimate requests by removing the affected sources \
    from the next release of the corpus. \
"""

_CITATION = """\
@inproceedings{ortiz-suarez-etal-2020-monolingual,
    title = "A Monolingual Approach to Contextualized Word Embeddings for Mid-Resource Languages",
    author = "Ortiz Su{\'a}rez, Pedro Javier  and
      Romary, Laurent  and
      Sagot, Beno{\^\i}t",
    booktitle = "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.acl-main.156",
    pages = "1703--1714",
    abstract = "We use the multilingual OSCAR corpus, extracted from Common Crawl via language classification, filtering and cleaning, to train monolingual contextualized word embeddings (ELMo) for five mid-resource languages. We then compare the performance of OSCAR-based and Wikipedia-based ELMo embeddings for these languages on the part-of-speech tagging and parsing tasks. We show that, despite the noise in the Common-Crawl-based OSCAR data, embeddings trained on OSCAR perform much better than monolingual embeddings trained on Wikipedia. They actually equal or improve the current state of the art in tagging and parsing for all five languages. In particular, they also improve over multilingual Wikipedia-based contextual embeddings (multilingual BERT), which almost always constitutes the previous state of the art, thereby showing that the benefit of a larger, more diverse corpus surpasses the cross-lingual benefit of multilingual embedding architectures.",
}

@inproceedings{OrtizSuarezSagotRomary2019,
  author    = {Pedro Javier {Ortiz Su{\´a}rez} and Beno{\^i}t Sagot and Laurent Romary},
  title     = {Asynchronous pipelines for processing huge corpora on medium to low resource infrastructures},
  series = {Proceedings of the Workshop on Challenges in the Management of Large Corpora (CMLC-7) 2019. Cardiff, 22nd July 2019},
  editor    = {Piotr Bański and Adrien Barbaresi and Hanno Biber and Evelyn Breiteneder and Simon Clematide and Marc Kupietz and Harald L{\"u}ngen and Caroline Iliadi},
  publisher = {Leibniz-Institut f{\"u}r Deutsche Sprache},
  address   = {Mannheim},
  doi       = {10.14618/ids-pub-9021},
  url       = {http://nbn-resolving.de/urn:nbn:de:bsz:mh39-90215},
  pages     = {9 -- 16},
  year      = {2019},
  abstract  = {Common Crawl is a considerably large, heterogeneous multilingual corpus comprised of crawled documents from the internet, surpassing 20TB of data and distributed as a set of more than 50 thousand plain text files where each contains many documents written in a wide variety of languages. Even though each document has a metadata block associated to it, this data lacks any information about the language in which each document is written, making it extremely difficult to use Common Crawl for monolingual applications. We propose a general, highly parallel, multithreaded pipeline to clean and classify Common Crawl by language; we specifically design it so that it runs efficiently on medium to low resource infrastructures where I/O speeds are the main constraint. We develop the pipeline so that it can be easily reapplied to any kind of heterogeneous corpus and so that it can be parameterised to a wide range of infrastructures. We also distribute a 6.3TB version of Common Crawl, filtered, classified by language, shuffled at line level in order to avoid copyright issues, and ready to be used for NLP applications.},
  language  = {en}
}
"""

_BASE_DATA_URL_FORMAT_STR = "https://oscar-public.huma-num.fr/" "{shuffled}/{language}{deduplicated}." "txt.gz"


def _languages():
    """Create the sorted dictionary of language codes, and language names.

  Returns:
    The sorted dictionary as an instance of `collections.OrderedDict`.
  """
    langs = {
        "af": "Afrikaans",
        "als": "Tosk Albanian",
        "am": "Amharic",
        "an": "Aragonese",
        "ar": "Arabic",
        "arz": "Egyptian Arabic",
        "ast": "Asturian",
        "as": "Assamese",
        "av": "Avaric",
        "azb": "South Azerbaijani",
        "az": "Azerbaijani",
        "bar": "Bavarian",
        "ba": "Bashkir",
        "bcl": "Central Bikol",
        "be": "Belarusian",
        "bg": "Bulgarian",
        "bh": "Bihari",
        "bn": "Bengali",
        "bo": "Tibetan",
        "bpy": "Bishnupriya",
        "br": "Breton",
        "bs": "Bosnian",
        "bxr": "Russia Buriat",
        "ca": "Catalan",
        "cbk": "Chavacano",
        "ceb": "Cebuano",
        "ce": "Chechen",
        "ckb": "Central Kurdish",
        "cs": "Czech",
        "cv": "Chuvash",
        "cy": "Welsh",
        "da": "Danish",
        "de": "German",
        "diq": "Dimli",
        "dsb": "Lower Sorbian",
        "dv": "Dhivehi",
        "el": "Modern Greek",
        "eml": "Emilian-Romagnol",
        "en": "English",
        "eo": "Esperanto",
        "es": "Spanish",
        "et": "Estonian",
        "eu": "Basque",
        "fa": "Persian",
        "fi": "Finnish",
        "frr": "Northern Frisian",
        "fr": "French",
        "fy": "Western Frisian",
        "ga": "Irish",
        "gd": "Scottish Gaelic",
        "gl": "Galician",
        "gn": "Guarani",
        "gom": "Goan Konkani",
        "gu": "Gujarati",
        "he": "Hebrew",
        "hi": "Hindi",
        "hr": "Croatian",
        "hsb": "Upper Sorbian",
        "ht": "Haitian",
        "hu": "Hungarian",
        "hy": "Armenian",
        "ia": "Interlingua",
        "id": "Indonesian",
        "ie": "Interlingue",
        "ilo": "Iloko",
        "io": "Ido",
        "is": "Icelandic",
        "it": "Italian",
        "ja": "Japanese",
        "jbo": "Lojban",
        "jv": "Javanese",
        "ka": "Georgian",
        "kk": "Kazakh",
        "km": "Central Khmer",
        "kn": "Kannada",
        "ko": "Korean",
        "krc": "Karachay-Balkar",
        "ku": "Kurdish",
        "kv": "Komi",
        "kw": "Cornish",
        "ky": "Kirghiz",
        "la": "Latin",
        "lb": "Luxembourgish",
        "lez": "Lezghian",
        "li": "Limburgan",
        "lmo": "Lombard",
        "lo": "Lao",
        "lrc": "Northern Luri",
        "lt": "Lithuanian",
        "lv": "Latvian",
        "mai": "Maithili",
        "mg": "Malagasy",
        "mhr": "Eastern Mari",
        "min": "Minangkabau",
        "mk": "Macedonian",
        "ml": "Malayalam",
        "mn": "Mongolian",
        "mrj": "Western Mari",
        "mr": "Marathi",
        "ms": "Malay",
        "mt": "Maltese",
        "mwl": "Mirandese",
        "my": "Burmese",
        "myv": "Erzya",
        "mzn": "Mazanderani",
        "nah": "Nahuatl languages",
        "nap": "Neapolitan",
        "nds": "Low German",
        "ne": "Nepali",
        "new": "Newari",
        "nl": "Dutch",
        "nn": "Norwegian Nynorsk",
        "no": "Norwegian",
        "oc": "Occitan",
        "or": "Oriya",
        "os": "Ossetian",
        "pam": "Pampanga",
        "pa": "Panjabi",
        "pl": "Polish",
        "pms": "Piemontese",
        "pnb": "Western Panjabi",
        "ps": "Pushto",
        "pt": "Portuguese",
        "qu": "Quechua",
        "rm": "Romansh",
        "ro": "Romanian",
        "ru": "Russian",
        "sah": "Yakut",
        "sa": "Sanskrit",
        "scn": "Sicilian",
        "sd": "Sindhi",
        "sh": "Serbo-Croatian",
        "si": "Sinhala",
        "sk": "Slovak",
        "sl": "Slovenian",
        "so": "Somali",
        "sq": "Albanian",
        "sr": "Serbian",
        "su": "Sundanese",
        "sv": "Swedish",
        "sw": "Swahili",
        "ta": "Tamil",
        "te": "Telugu",
        "tg": "Tajik",
        "th": "Thai",
        "tk": "Turkmen",
        "tl": "Tagalog",
        "tr": "Turkish",
        "tt": "Tatar",
        "tyv": "Tuvinian",
        "ug": "Uighur",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "uz": "Uzbek",
        "vec": "Venetian",
        "vi": "Vietnamese",
        "vo": "Volapük",
        "war": "Waray",
        "wa": "Walloon",
        "wuu": "Wu Chinese",
        "xal": "Kalmyk",
        "xmf": "Mingrelian",
        "yi": "Yiddish",
        "yo": "Yoruba",
        "yue": "Yue Chinese",
        "zh": "Chinese",
    }
    return collections.OrderedDict(sorted(langs.items()))


class OscarConfig(nlp.BuilderConfig):
    """OSCAR corpus."""

    def __init__(self, language=None, shuffled=True, deduplicated=True, **kwargs):
        """BuilderConfig for OSCAR.

    Args:
        for the `nlp.features.text.TextEncoder` used for the features feature.
        It has to contain 2-letter
        or 3-letter coded strings. For example: "se", "hu", "eml".
      **kwargs: Keyword arguments forwarded to super.
    """
        # Validate the language.
        if language not in _languages():
            raise ValueError("Invalid language: %s " % language)

        # Initialize the base class.
        name = "{}_{}_{}".format(
            "shuffled" if shuffled else "unshuffled", "deduplicated" if deduplicated else "original", language
        )

        # TODO(oscar): Implement unshuffled OSCAR
        # shuf = "shuffled" if shuffled else "unshuffled"
        dedup = "_dedup" if deduplicated else ""

        description = "{} and {}, {} OSCAR dataset".format(
            "Shuffled" if shuffled else "Unshuffled",
            "deduplicated" if deduplicated else "original",
            _languages()[language],
        )

        super(OscarConfig, self).__init__(name=name, description=description, **kwargs)

        # Store the attributes.

        self.language = language

        # Always returns the shuffled dataset for the moment

        self.shuffled = "shuffled"
        self.deduplicated = deduplicated
        self.data_url = _BASE_DATA_URL_FORMAT_STR.format(shuffled="shuffled", language=language, deduplicated=dedup)


class Oscar(nlp.GeneratorBasedBuilder):
    """OSCAR The Open Super-large Crawled ALMAnaCH coRpus."""

    # Version history:
    # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
    # 0.1.0: Initial version.
    BUILDER_CONFIGS = [
        OscarConfig(  # pylint: disable=g-complex-comprehension
            language=language, shuffled=True, deduplicated=True, version=nlp.Version("1.0.0"),
        )
        for language in _languages()
    ] + [
        OscarConfig(  # pylint: disable=g-complex-comprehension
            language=language, shuffled=True, deduplicated=False, version=nlp.Version("1.0.0"),
        )
        for language in _languages()
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"id": nlp.Value("string"), "text": nlp.Value("string"),}),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
            license=_LICENSE,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = {
            self.config.name: self.config.data_url,
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        return [
            nlp.SplitGenerator(name=self.config.name, gen_kwargs={"filepath": downloaded_files[self.config.name]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        with open(filepath) as f:
            id_ = 0
            for line in f:
                line = line.rstrip()
                feature = id_, {"id": str(id_), "text": line}
                id_ += 1
                yield feature
