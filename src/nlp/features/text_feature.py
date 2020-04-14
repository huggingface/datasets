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
"""Text feature.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import pyarrow as pa

from .feature import Tensor
# from .text import SubwordTextEncoder, TextEncoderConfig


class Text(Tensor):
    """`FeatureConnector` for text, encoding to integers with a `TextEncoder`."""

    def __init__(self, encoder=None, encoder_config=None):
        """Constructs a Text FeatureConnector.

        Args:
            encoder: `nlp.features.text.TextEncoder`, an encoder that can convert
                text to integers. If None, the text will be utf-8 byte-encoded.
            encoder_config: `nlp.features.text.TextEncoderConfig`, needed if
                restoring from a file with `load_metadata`.
        """
        if encoder and encoder_config:
            raise ValueError("If encoder is provided, encoder_config must be None.")
        # if encoder:
        #     encoder_config = TextEncoderConfig(
        #             encoder_cls=type(encoder),
        #             vocab_size=encoder.vocab_size)
        # elif encoder_config:
        #     encoder = encoder_config.encoder

        self._encoder = encoder
        self._encoder_config = encoder_config

        has_encoder = bool(encoder or self._encoder_cls)
        super(Text, self).__init__(
                shape=(None,) if has_encoder else (),
                dtype=pa.int64 if has_encoder else pa.string,
        )

    @property
    def encoder(self):
        return self._encoder

    @encoder.setter
    def encoder(self, new_encoder):
        if self.encoder:
            raise ValueError("Cannot override encoder")
        self._encoder = new_encoder
        encoder_cls = self._encoder_cls or type(None)
        if not isinstance(new_encoder, encoder_cls):
            raise ValueError(
                    "Changing type of encoder. Got %s but must be %s" %
                    (type(new_encoder).__name__,
                     self._encoder_cls.__name__))

    def maybe_set_encoder(self, new_encoder):
        """Set encoder, but no-op if encoder is already set."""
        if self.encoder:
            return
        self.encoder = new_encoder

    @property
    def vocab_size(self):
        return self.encoder and self.encoder.vocab_size

    def str2ints(self, str_value):
        """Conversion string => encoded list[int]."""
        if not self._encoder:
            raise ValueError(
                    "Text.str2ints is not available because encoder hasn't been defined.")
        return self._encoder.encode(str_value)

    def ints2str(self, int_values):
        """Conversion list[int] => decoded string."""
        if not self._encoder:
            raise ValueError(
                    "Text.ints2str is not available because encoder hasn't been defined.")
        return self._encoder.decode(int_values)

    def encode_example(self, example_data):
        if self.encoder:
            example_data = self.encoder.encode(example_data)
        else:
            example_data = example_data
        return super(Text, self).encode_example(example_data)

    def save_metadata(self, data_dir, feature_name):
        fname_prefix = os.path.join(data_dir, "%s.text" % feature_name)
        if not self.encoder:
            return
        self.encoder.save_to_file(fname_prefix)

    def load_metadata(self, data_dir, feature_name):
        fname_prefix = os.path.join(data_dir, "%s.text" % feature_name)
        encoder_cls = self._encoder_cls
        if encoder_cls:
            self._encoder = encoder_cls.load_from_file(fname_prefix)
            return

        # Error checking: ensure there are no metadata files
        feature_files = [
                f for f in os.listdir(data_dir) if f.startswith(fname_prefix)
        ]
        if feature_files:
            raise ValueError(
                    "Text feature files found for feature %s but encoder_cls=None. "
                    "Make sure to set encoder_cls in the TextEncoderConfig. "
                    "Files: %s" % (feature_name, feature_files))

    def maybe_build_from_corpus(self, corpus_generator, **kwargs):
        """Call SubwordTextEncoder.build_from_corpus is encoder_cls is such.

        If `self.encoder` is `None` and `self._encoder_cls` is of type
        `SubwordTextEncoder`, the method instantiates `self.encoder` as returned
        by `SubwordTextEncoder.build_from_corpus()`.

        Args:
            corpus_generator: generator yielding `str`, from which
                subwords will be constructed.
            **kwargs: kwargs forwarded to `SubwordTextEncoder.build_from_corpus()`
        """
        pass
        # if self._encoder_cls is not SubwordTextEncoder:
        #     return
        # if self.encoder:
        #     return

        # vocab_size = self._encoder_config.vocab_size
        # self.encoder = SubwordTextEncoder.build_from_corpus(
        #         corpus_generator=corpus_generator,
        #         target_vocab_size=vocab_size,
        #         **kwargs)

    @property
    def _encoder_cls(self):
        return self._encoder_config and self._encoder_config.encoder_cls

    def _additional_repr_info(self):
        if self.encoder is None:
            return {}
        return {"encoder": repr(self.encoder)}
