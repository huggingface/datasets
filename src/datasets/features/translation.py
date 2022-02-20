from dataclasses import dataclass, field
from typing import Any, ClassVar, List, Optional

import pyarrow as pa


@dataclass
class Translation:
    """`FeatureConnector` for translations with fixed languages per example.
    Here for compatiblity with tfds.

    Input: The Translate feature accepts a dictionary for each example mapping
        string language codes to string translations.

    Output: A dictionary mapping string language codes to translations as `Text`
        features.

    Example::

        # At construction time:

        datasets.features.Translation(languages=['en', 'fr', 'de'])

        # During data generation:

        yield {
                'en': 'the cat',
                'fr': 'le chat',
                'de': 'die katze'
        }
    """

    languages: List[str]
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="Translation", init=False, repr=False)

    def __call__(self):
        return pa.struct({lang: pa.string() for lang in sorted(self.languages)})


@dataclass
class TranslationVariableLanguages:
    """`FeatureConnector` for translations with variable languages per example.
    Here for compatiblity with tfds.

    Input: The TranslationVariableLanguages feature accepts a dictionary for each
        example mapping string language codes to one or more string translations.
        The languages present may vary from example to example.

    Output:
        language: variable-length 1D tf.Tensor of tf.string language codes, sorted
            in ascending order.
        translation: variable-length 1D tf.Tensor of tf.string plain text
            translations, sorted to align with language codes.

    Example::

        # At construction time:

        datasets.features.Translation(languages=['en', 'fr', 'de'])

        # During data generation:

        yield {
                'en': 'the cat',
                'fr': ['le chat', 'la chatte,']
                'de': 'die katze'
        }

        # Tensor returned :

        {
                'language': ['en', 'de', 'fr', 'fr'],
                'translation': ['the cat', 'die katze', 'la chatte', 'le chat'],
        }
    """

    languages: Optional[List] = None
    num_languages: Optional[int] = None
    id: Optional[str] = None
    # Automatically constructed
    dtype: ClassVar[str] = "dict"
    pa_type: ClassVar[Any] = None
    _type: str = field(default="TranslationVariableLanguages", init=False, repr=False)

    def __post_init__(self):
        self.languages = list(sorted(list(set(self.languages)))) if self.languages else None
        self.num_languages = len(self.languages) if self.languages else None

    def __call__(self):
        return pa.struct({"language": pa.list_(pa.string()), "translation": pa.list_(pa.string())})

    def encode_example(self, translation_dict):
        lang_set = set(self.languages)
        if self.languages and set(translation_dict) - lang_set:
            raise ValueError(
                f'Some languages in example ({", ".join(sorted(set(translation_dict) - lang_set))}) are not in valid set ({", ".join(lang_set)}).'
            )

        # Convert dictionary into tuples, splitting out cases where there are
        # multiple translations for a single language.
        translation_tuples = []
        for lang, text in translation_dict.items():
            if isinstance(text, str):
                translation_tuples.append((lang, text))
            else:
                translation_tuples.extend([(lang, el) for el in text])

        # Ensure translations are in ascending order by language code.
        languages, translations = zip(*sorted(translation_tuples))

        return {"language": languages, "translation": translations}
