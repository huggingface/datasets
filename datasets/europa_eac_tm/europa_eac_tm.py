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
"""European commission Joint Reasearch Center's Education And Culture Translation Memory dataset"""


import os
from itertools import repeat
from xml.etree import ElementTree

import datasets


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
In October 2012, the European Union's (EU) Directorate General for Education and Culture ( DG EAC) released a \
translation memory (TM), i.e. a collection of sentences and their professionally produced translations, in \
twenty-six languages. This resource bears the name EAC Translation Memory, short EAC-TM.

EAC-TM covers up to 26 languages: 22 official languages of the EU (all except Irish) plus Icelandic, Croatian, \
Norwegian and Turkish. EAC-TM thus contains translations from English into the following 25 languages: Bulgarian, \
Czech, Danish, Dutch, Estonian, German, Greek, Finnish, French, Croatian, Hungarian, Icelandic, Italian, Latvian, \
Lithuanian, Maltese, Norwegian, Polish, Portuguese, Romanian, Slovak, Slovenian, Spanish, Swedish and Turkish.

All documents and sentences were originally written in English (source language is English) and then translated into \
the other languages. The texts were translated by staff of the National Agencies of the Lifelong Learning and Youth in \
Action programmes. They are typically professionals in the field of education/youth and EU programmes. They are thus not \
professional translators, but they are normally native speakers of the target language.
"""

_HOMEPAGE = "https://ec.europa.eu/jrc/en/language-technologies/eac-translation-memory"

_LICENSE = "\
Creative Commons Attribution 4.0 International(CC BY 4.0) licence \
© European Union, 1995-2020"

_VERSION = "1.0.0"

_DATA_URL = "https://wt-public.emm4u.eu/Resources/EAC-TM/EAC-TM-all.zip"

_AVAILABLE_LANGUAGES = (
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
    "is",
    "it",
    "lt",
    "lv",
    "mt",
    "nb",
    "nl",
    "pl",
    "pt",
    "ro",
    "sk",
    "sl",
    "sv",
    "tr",
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
    seg_tag = translation.find(path=f".//tuv[@xml:lang='{language}']/seg", namespaces=namespaces)
    if seg_tag is not None:
        return seg_tag.text
    return None


class EuropaEacTMConfig(datasets.BuilderConfig):
    """BuilderConfig for EuropaEacTM"""

    def __init__(self, *args, language_pair=(None, None), **kwargs):
        """BuilderConfig for EuropaEacTM

        Args:
            language_pair: pair of languages that will be used for translation. Should
                contain 2-letter coded strings. First will be used at source and second
                as target in supervised mode. For example: ("ro", "en").
            **kwargs: keyword arguments forwarded to super.
        """
        name = f"{language_pair[0]}2{language_pair[1]}"
        description = f"Translation dataset from {language_pair[0]} to {language_pair[1]}"
        super(EuropaEacTMConfig, self).__init__(
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
class EuropaEacTM(datasets.GeneratorBasedBuilder):
    """European Commission Joint Research Center's EAC Translation Memory"""

    FORM_SENTENCE_TYPE = "form_data"
    REFERENCE_SENTENCE_TYPE = "sentence_data"

    # Only a few language pairs are listed here. You can use config to generate all language pairs !
    BUILDER_CONFIGS = [
        EuropaEacTMConfig(language_pair=("en", target), version=_VERSION) for target in ["bg", "es", "fr"]
    ]
    BUILDER_CONFIG_CLASS = EuropaEacTMConfig

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "translation": datasets.features.Translation(languages=self.config.language_pair),
                    "sentence_type": datasets.features.ClassLabel(
                        names=[self.FORM_SENTENCE_TYPE, self.REFERENCE_SENTENCE_TYPE]
                    ),
                }
            ),
            supervised_keys=(source, target),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        form_data_file = os.path.join(dl_dir, "EAC_FORMS.tmx")
        reference_data_file = os.path.join(dl_dir, "EAC_REFRENCE_DATA.tmx")
        source, target = self.config.language_pair
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "form_data_file": form_data_file,
                    "reference_data_file": reference_data_file,
                    "source_language": source,
                    "target_language": target,
                },
            ),
        ]

    def _generate_examples(
        self,
        form_data_file,
        reference_data_file,
        source_language,
        target_language,
    ):
        _id = 0
        for (sentence_type, filepath) in [
            (self.FORM_SENTENCE_TYPE, form_data_file),
            (self.REFERENCE_SENTENCE_TYPE, reference_data_file),
        ]:
            # Retrieve <tu></tu> tags in the tmx file
            xml_element_tree = ElementTree.parse(filepath)
            xml_body_tag = xml_element_tree.getroot().find("body")
            assert xml_body_tag is not None, f"Invalid data: <body></body> tag not found in {filepath}"
            translation_units = xml_body_tag.iter("tu")

            # Pair sentence_type and translation_units
            for sentence_type, translation in zip(repeat(sentence_type), translation_units):
                source_sentence = _find_sentence(translation=translation, language=source_language)
                target_sentence = _find_sentence(translation=translation, language=target_language)
                if source_sentence is None or target_sentence is None:
                    continue
                _id += 1
                sentence_label = 0 if sentence_type == self.FORM_SENTENCE_TYPE else 1
                yield _id, {
                    "translation": {source_language: source_sentence, target_language: target_sentence},
                    "sentence_type": sentence_label,
                }
