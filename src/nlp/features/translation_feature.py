# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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
"""Translation feature that supports multiple languages."""

from .features_dict import FeaturesDict, Sequence
from .text_feature import Text
try:
    # This fallback applies for all versions of Python before 3.3
    import collections.abc as collections_abc  # pylint:disable=g-import-not-at-top
except ImportError:
    import collections as collections_abc  # pylint:disable=g-import-not-at-top


class Translation(FeaturesDict):
    """`FeatureConnector` for translations with fixed languages per example.

    Input: The Translate feature accepts a dictionary for each example mapping
        string language codes to string translations.

    Output: A dictionary mapping string language codes to translations as `Text`
        features.

    Example:
    At construction time:

    ```
    nlp.features.Translation(languages=['en', 'fr', 'de'])
    ```

    During data generation:

    ```
    yield {
            'en': 'the cat',
            'fr': 'le chat',
            'de': 'die katze'
    }
    ```

    Tensor returned by `.as_dataset()`:

    ```
    {
            'en': tf.Tensor(shape=(), dtype=tf.string, numpy='the cat'),
            'fr': tf.Tensor(shape=(), dtype=tf.string, numpy='le chat'),
            'de': tf.Tensor(shape=(), dtype=tf.string, numpy='die katze'),
    }
    ```
    """

    def __init__(self, languages, encoder=None, encoder_config=None):
        """Constructs a Translation FeatureConnector.

        Args:
            languages: `list<string>` Full list of languages codes.
            encoder: `nlp.features.text.TextEncoder` or
                list<nlp.features.text.TextEncoder> (optional), an encoder that can
                convert text to integer. One can be shared one per language provided. If
                None, the text will be utf-8 byte-encoded.
            encoder_config: `nlp.features.text.TextEncoderConfig` or
                `list<nlp.features.text.TextEncoderConfig>` (optional), needed
                if restoring from a file with `load_metadata`. One config can be shared
                or one per language can be provided.
        """
        # If encoder and encoder_config aren't lists, use the same values for all
        # languages.
        if not isinstance(encoder, collections_abc.Iterable):
            encoder = [encoder] * len(languages)
        if not isinstance(encoder_config, collections_abc.Iterable):
            encoder_config = [encoder_config] * len(languages)

        super(Translation, self).__init__(
                {lang: Text(enc, enc_conf) for lang, enc, enc_conf in zip(
                        languages, encoder, encoder_config)})

    @property
    def languages(self):
        """List of languages."""
        return sorted(self.keys())


class TranslationVariableLanguages(Sequence):
    """`FeatureConnector` for translations with variable languages per example.

    Input: The TranslationVariableLanguages feature accepts a dictionary for each
        example mapping string language codes to one or more string translations.
        The languages present may vary from example to example.

    Output:
        language: variable-length 1D tf.Tensor of tf.string language codes, sorted
            in ascending order.
        translation: variable-length 1D tf.Tensor of tf.string plain text
            translations, sorted to align with language codes.

    Example (fixed language list):
    At construction time:

    ```
    nlp.features.Translation(languages=['en', 'fr', 'de'])
    ```

    During data generation:

    ```
    yield {
            'en': 'the cat',
            'fr': ['le chat', 'la chatte,']
            'de': 'die katze'
    }
    ```

    Tensor returned by `.as_dataset()`:

    ```
    {
            'language': tf.Tensor(
                    shape=(4,), dtype=tf.string, numpy=array(['en', 'de', 'fr', 'fr']),
            'translation': tf.Tensor(
                    shape=(4,), dtype=tf.string,
                    numpy=array(['the cat', 'die katze', 'la chatte', 'le chat'])),
    }
    ```
    """

    def __init__(self, languages=None):
        """Constructs a Translation FeatureConnector.

        Args:
            languages: `list<string>` (optional), full list of language codes if known
                in advance.
        """
        # TODO(adarob): Add optional text encoders once `Sequence` adds support
        # for FixedVarLenFeatures.

        self._languages = set(languages) if languages else None
        super(TranslationVariableLanguages, self).__init__({
                "language": Text(),
                "translation": Text(),
        })

    @property
    def num_languages(self):
        """Number of languages or None, if not specified in advance."""
        return len(self._languages) if self._languages else None

    @property
    def languages(self):
        """List of languages or None, if not specified in advance."""
        return sorted(list(self._languages)) if self._languages else None

    def encode_example(self, translation_dict):
        if self.languages and set(translation_dict) - self._languages:
            raise ValueError(
                    "Some languages in example ({0}) are not in valid set ({1}).".format(
                            ", ".join(sorted(set(translation_dict) - self._languages)),
                            ", ".join(self.languages)))

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

        return super(TranslationVariableLanguages, self).encode_example(
                {"language": languages,
                 "translation": translations})

