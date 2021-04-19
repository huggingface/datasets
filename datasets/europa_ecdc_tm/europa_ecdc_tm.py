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
"""European Center for Disease Prevention and Control Translation Memory dataset"""


import os
from xml.etree import ElementTree

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@Article{Steinberger2014,
        author={Steinberger, Ralf
                and Ebrahim, Mohamed
                and Poulis, Alexandros
                and Carrasco-Benitez, Manuel
                and Schl{\"u}ter, Patrick
                and Przybyszewski, Marek
                and Gilbro, Signe},
        title={An overview of the European Union's highly multilingual parallel corpora},
        journal={Language Resources and Evaluation},
        year={2014},
        month={Dec},
        day={01},
        volume={48},
        number={4},
        pages={679-707},
        issn={1574-0218},
        doi={10.1007/s10579-014-9277-0},
        url={https://doi.org/10.1007/s10579-014-9277-0}
}
"""

_DESCRIPTION = """\
In October 2012, the European Union (EU) agency 'European Centre for Disease Prevention and Control' (ECDC) released \
a translation memory (TM), i.e. a collection of sentences and their professionally produced translations, in \
twenty-five languages. This resource bears the name EAC Translation Memory, short EAC-TM.
ECDC-TM covers 25 languages: the 23 official languages of the EU plus Norwegian (Norsk) and Icelandic. ECDC-TM was \
created by translating from English into the following 24 languages: Bulgarian, Czech, Danish, Dutch, English, \
Estonian, Gaelige (Irish), German, Greek, Finnish, French, Hungarian, Icelandic, Italian, Latvian, Lithuanian, \
Maltese, Norwegian (NOrsk), Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish and Swedish.
All documents and sentences were thus originally written in English. They were then translated into the other \
languages by professional translators from the Translation Centre CdT in Luxembourg."""

_HOMEPAGE = "https://ec.europa.eu/jrc/en/language-technologies/ecdc-translation-memory"

_LICENSE = "\
Creative Commons Attribution 4.0 International(CC BY 4.0) licence \
Copyright © EU/ECDC, 1995-2020"

_VERSION = "1.0.0"

_DATA_URL = "http://optima.jrc.it/Resources/ECDC-TM/ECDC-TM.zip"

_AVAILABLE_LANGUAGES = (
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "es",
    "en",
    "et",
    "fi",
    "fr",
    "ga",
    "hu",
    "is",
    "it",
    "lt",
    "lv",
    "mt",
    "nl",
    "no",
    "pl",
    "pt",
    "ro",
    "sk",
    "sl",
    "sv",
)


def _find_sentence(translation, language):
    """Util that returns the sentence in the given language from translation, or None if it is not found

    Args:
        translation: `xml.etree.ElementTree.Element`, xml tree element extracted from the translation memory files.
        language: `str`, language of interest e.g. 'en'

    Returns: `str` or `None`, can be `None` if the language of interest is not found in the translation
    """
    # Retrieve the first <tuv> children of translation having xml:lang tag equal to language
    namespaces = {"xml": "http://www.w3.org/XML/1998/namespace"}
    seg_tag = translation.find(path=f".//tuv[@xml:lang='{language.upper()}']/seg", namespaces=namespaces)
    if seg_tag is not None:
        return seg_tag.text
    return None


class EuropaEcdcTMConfig(datasets.BuilderConfig):
    """BuilderConfig for EuropaEcdcTM"""

    def __init__(self, *args, language_pair=(None, None), **kwargs):
        """BuilderConfig for EuropaEcdcTM
        Args:
            language_pair: pair of languages that will be used for translation. Should
                contain 2-letter coded strings. First will be used at source and second
                as target in supervised mode. For example: ("se", "en").
            **kwargs: keyword arguments forwarded to super.
        """
        name = f"{language_pair[0]}2{language_pair[1]}"
        description = f"Translation dataset from {language_pair[0]} to {language_pair[1]}"
        super(EuropaEcdcTMConfig, self).__init__(
            *args,
            name=name,
            description=description,
            **kwargs,
        )
        source, target = language_pair
        assert source != target, "Source and target languages must be different}"
        assert (source in _AVAILABLE_LANGUAGES) and (
            target in _AVAILABLE_LANGUAGES
        ), f"Either source language {source} or target language {target} is not supported. Both must be one of : {_AVAILABLE_LANGUAGES}"
        self.language_pair = language_pair


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class EuropaEcdcTM(datasets.GeneratorBasedBuilder):
    """European Center for Disease Control and Prevention Translation Memory"""

    BUILDER_CONFIGS = [
        EuropaEcdcTMConfig(language_pair=("en", target), version=_VERSION) for target in ["bg", "fr", "sl"]
    ]
    BUILDER_CONFIG_CLASS = EuropaEcdcTMConfig

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "translation": datasets.features.Translation(languages=self.config.language_pair),
                }
            ),
            supervised_keys=(source, target),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        filepath = os.path.join(dl_dir, "ECDC-TM", "ECDC.tmx")
        source, target = self.config.language_pair
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": filepath,
                    "source_language": source,
                    "target_language": target,
                },
            ),
        ]

    def _generate_examples(
        self,
        filepath,
        source_language,
        target_language,
    ):
        logger.info(f"⏳ Generating examples from = {filepath}")
        xml_element_tree = ElementTree.parse(filepath)
        xml_body_tag = xml_element_tree.getroot().find("body")
        assert xml_body_tag is not None, f"Invalid data: <body></body> tag not found in {filepath}"

        # Translations are stored in <tu>...</tu> tags
        translation_units = xml_body_tag.iter("tu")

        # _ids may not be contiguous
        for _id, translation in enumerate(translation_units):
            source_sentence = _find_sentence(translation=translation, language=source_language)
            target_sentence = _find_sentence(translation=translation, language=target_language)
            if source_sentence is None or target_sentence is None:
                continue

            yield _id, {
                "translation": {source_language: source_sentence, target_language: target_sentence},
            }
