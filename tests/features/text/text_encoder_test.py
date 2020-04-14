# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
# coding=utf-8
"""Tests for tensorflow_datasets.core.features.text.text_encoder."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from absl.testing import parameterized
import numpy as np
from tensorflow_datasets import testing
from tensorflow_datasets.core.features.text import text_encoder

ZH_HELLO = '你好 '
EN_HELLO = 'hello '


class TextEncoderTest(testing.TestCase):

  def test_pad_decr(self):
    self.assertEqual([2, 1, 0], text_encoder.pad_decr([3, 2, 1]))
    self.assertEqual([2, 1, 0], text_encoder.pad_decr([3, 2, 1, 0, 0, 0]))
    self.assertEqual([-1, 2, 1, 0], text_encoder.pad_decr([0, 3, 2, 1, 0, 0]))
    self.assertEqual([], text_encoder.pad_decr([]))
    self.assertEqual([], text_encoder.pad_decr(np.array([])))

  def test_pad_incr(self):
    self.assertEqual([4, 3, 2], text_encoder.pad_incr([3, 2, 1]))
    self.assertEqual([4, 3, 2, 1], text_encoder.pad_incr([3, 2, 1, 0]))

  def test_is_mixed_alphanum(self):
    self.assertFalse(text_encoder.is_mixed_alphanum('hi'))
    self.assertFalse(text_encoder.is_mixed_alphanum(ZH_HELLO[:-1]))
    self.assertTrue(text_encoder.is_mixed_alphanum('hi.'))
    self.assertTrue(text_encoder.is_mixed_alphanum('hi.bye'))
    self.assertTrue(text_encoder.is_mixed_alphanum('hi '))
    self.assertTrue(text_encoder.is_mixed_alphanum(ZH_HELLO))


class ByteTextEncoderTest(parameterized.TestCase, testing.TestCase):
  # Incremented for pad
  ZH_HELLO_IDS = [i + 1 for i in [228, 189, 160, 229, 165, 189, 32]]
  EN_HELLO_IDS = [i + 1 for i in [104, 101, 108, 108, 111, 32]]

  def test_encode_decode(self):
    encoder = text_encoder.ByteTextEncoder()
    self.assertEqual(self.ZH_HELLO_IDS, encoder.encode(ZH_HELLO))
    self.assertEqual(self.EN_HELLO_IDS, encoder.encode(EN_HELLO))
    self.assertEqual(self.EN_HELLO_IDS, encoder.encode('hello '))
    self.assertEqual(EN_HELLO, encoder.decode(self.EN_HELLO_IDS))
    self.assertEqual(ZH_HELLO, encoder.decode(self.ZH_HELLO_IDS))
    self.assertEqual(text_encoder.NUM_BYTES + 1, encoder.vocab_size)

  def test_additional_tokens(self):
    # One with non-alphanumeric chars, one uppercase, one lowercase
    additional_tokens = ['<EOS>', 'FOO', 'bar']
    encoder = text_encoder.ByteTextEncoder(additional_tokens=additional_tokens)
    # Without additional tokens
    hello_ids = [i + len(additional_tokens) for i in self.ZH_HELLO_IDS]
    self.assertEqual(hello_ids, encoder.encode(ZH_HELLO))
    # With additional tokens
    text_additional = '%s %s%s%s' % (additional_tokens[0], ZH_HELLO,
                                     additional_tokens[1], additional_tokens[2])
    expected_ids = [1, 32 + 1 + len(additional_tokens)] + hello_ids + [2, 3]
    self.assertEqual(expected_ids,
                     encoder.encode(text_additional))
    self.assertEqual(text_additional, encoder.decode(expected_ids))
    self.assertEqual(text_encoder.NUM_BYTES + 1 + len(additional_tokens),
                     encoder.vocab_size)

  @parameterized.parameters(
      (['<EOS>', 'FOO', 'bar'],),
      ([],),
  )
  def test_file_backed(self, additional_tokens):
    encoder = text_encoder.ByteTextEncoder(additional_tokens=additional_tokens)
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      vocab_fname = os.path.join(tmp_dir, 'vocab')
      encoder.save_to_file(vocab_fname)

      file_backed_encoder = text_encoder.ByteTextEncoder.load_from_file(
          vocab_fname)
      self.assertEqual(encoder.vocab_size, file_backed_encoder.vocab_size)
      self.assertEqual(encoder.additional_tokens,
                       file_backed_encoder.additional_tokens)


class TokenTextEncoderTest(testing.TestCase):

  def test_encode_decode(self):
    encoder = text_encoder.TokenTextEncoder(
        vocab_list=['hi', 'bye', ZH_HELLO])
    ids = [i + 1 for i in [0, 1, 2, 0]]
    self.assertEqual(ids, encoder.encode('hi  bye %s hi' % ZH_HELLO))
    self.assertEqual('hi bye %shi' % ZH_HELLO, encoder.decode(ids))

  def test_oov(self):
    encoder = text_encoder.TokenTextEncoder(
        vocab_list=['hi', 'bye', ZH_HELLO],
        oov_buckets=1,
        oov_token='UNK')
    ids = [i + 1 for i in [0, 3, 3, 1]]
    self.assertEqual(ids, encoder.encode('hi boo foo bye'))
    self.assertEqual('hi UNK UNK bye', encoder.decode(ids))
    self.assertEqual(5, encoder.vocab_size)

  def test_multiple_oov(self):
    encoder = text_encoder.TokenTextEncoder(
        vocab_list=['hi', 'bye', ZH_HELLO],
        oov_buckets=2,
        oov_token='UNK')
    encoded = encoder.encode('hi boo zoo too foo bye')
    self.assertEqual(1, encoded[0])
    self.assertEqual(2, encoded[-1])
    self.assertIn(4, encoded)
    self.assertIn(5, encoded)
    self.assertEqual(6, encoder.vocab_size)
    self.assertEqual('hi UNK UNK bye', encoder.decode([1, 4, 5, 2]))

  def test_tokenization(self):
    encoder = text_encoder.TokenTextEncoder(vocab_list=['hi', 'bye', ZH_HELLO])
    text = 'hi<<>><<>foo!^* bar && bye (%s hi)' % ZH_HELLO
    self.assertEqual(['hi', 'foo', 'bar', 'bye',
                      ZH_HELLO.strip(), 'hi'],
                     text_encoder.Tokenizer().tokenize(text))
    self.assertEqual([i + 1 for i in [0, 3, 3, 1, 2, 0]], encoder.encode(text))

  def test_file_backed(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      vocab_fname = os.path.join(tmp_dir, 'vocab')
      encoder = text_encoder.TokenTextEncoder(
          vocab_list=['hi', 'bye', ZH_HELLO])
      encoder.save_to_file(vocab_fname)
      file_backed_encoder = text_encoder.TokenTextEncoder.load_from_file(
          vocab_fname)
      self.assertEqual(encoder.tokens, file_backed_encoder.tokens)

  def test_file_backed_with_args(self):
    with testing.tmp_dir(self.get_temp_dir()) as tmp_dir:
      # Set all the args to non-default values, including Tokenizer
      tokenizer = text_encoder.Tokenizer(
          reserved_tokens=['<FOOBAR>'], alphanum_only=False)
      encoder = text_encoder.TokenTextEncoder(
          vocab_list=['hi', 'bye', ZH_HELLO],
          lowercase=True,
          oov_buckets=2,
          oov_token='ZOO',
          tokenizer=tokenizer)

      vocab_fname = os.path.join(tmp_dir, 'vocab')
      encoder.save_to_file(vocab_fname)

      file_backed_encoder = text_encoder.TokenTextEncoder.load_from_file(
          vocab_fname)
      self.assertEqual(encoder.tokens, file_backed_encoder.tokens)
      self.assertEqual(encoder.vocab_size, file_backed_encoder.vocab_size)
      self.assertEqual(encoder.lowercase, file_backed_encoder.lowercase)
      self.assertEqual(encoder.oov_token, file_backed_encoder.oov_token)
      self.assertEqual(encoder.tokenizer.alphanum_only,
                       file_backed_encoder.tokenizer.alphanum_only)
      self.assertEqual(encoder.tokenizer.reserved_tokens,
                       file_backed_encoder.tokenizer.reserved_tokens)

  def test_mixedalphanum_tokens(self):
    mixed_tokens = ['<EOS>', 'zoo!', '!foo']
    vocab_list = mixed_tokens + ['hi', 'bye', ZH_HELLO]

    encoder = text_encoder.TokenTextEncoder(vocab_list=vocab_list)

    # No mixed tokens
    text = 'hi<<>><<>foo!^* bar && bye (%s hi)' % ZH_HELLO
    # hi=3, foo=OOV, bar=OOV, bye=4, ZH_HELLO=5, hi=3
    text_ids = [i + 1 for i in [3, 6, 6, 4, 5, 3]]
    self.assertEqual(text_ids, encoder.encode(text))

    # With mixed tokens
    text = 'hi<<>><<>foo!<EOS>^* barzoo! FOO && bye (%s hi)' % ZH_HELLO
    # hi=3, foo=OOV, <EOS>=0, bar=OOV, zoo!=1, FOO=OOV, bye=4, ZH_HELLO=5, hi=3
    text_ids = [i + 1 for i in [3, 6, 0, 6, 1, 6, 4, 5, 3]]
    self.assertEqual(text_ids, encoder.encode(text))

  def test_lowercase(self):
    mixed_tokens = ['<EOS>', 'zoo!']
    vocab_list = mixed_tokens + ['hi', 'bye', ZH_HELLO]
    encoder = text_encoder.TokenTextEncoder(
        vocab_list=vocab_list, lowercase=True)
    # No mixed tokens
    self.assertEqual([3, 4, 3], encoder.encode('hi byE HI!'))
    # With mixed tokens
    self.assertEqual([3, 1, 4, 2, 3], encoder.encode('hi<EOS>byE Zoo! HI!'))

  def test_with_tokenizer(self):

    class DummyTokenizer(object):

      def tokenize(self, s):
        del s
        return ['hi', 'bye']

    tokenizer = DummyTokenizer()
    vocab_list = ['hi', 'bye', ZH_HELLO]
    encoder = text_encoder.TokenTextEncoder(
        vocab_list=vocab_list, tokenizer=tokenizer)
    # Ensure it uses the passed tokenizer and not the default
    self.assertEqual([1, 2], encoder.encode('zoo foo'))


class TokenizeTest(parameterized.TestCase, testing.TestCase):

  def test_default(self):
    text = 'hi<<>><<>foo!^* bar &&  bye (%s hi)' % ZH_HELLO
    self.assertEqual(['hi', 'foo', 'bar', 'bye', ZH_HELLO.strip(), 'hi'],
                     text_encoder.Tokenizer().tokenize(text))

  def test_with_nonalphanum(self):
    text = 'hi world<<>><<>foo!^* bar &&  bye (%s hi)' % ZH_HELLO
    tokens = [
        'hi', ' ', 'world', '<<>><<>', 'foo', '!^* ', 'bar', ' &&  ', 'bye',
        ' (', ZH_HELLO.strip(), '  ', 'hi', ')'
    ]
    tokenizer = text_encoder.Tokenizer(alphanum_only=False)
    self.assertEqual(
        tokens, tokenizer.tokenize(text))
    self.assertEqual(
        text, tokenizer.join(tokenizer.tokenize(text)))

  @parameterized.parameters(
      # Single Space at at beginning
      (' hello world', [' ', 'hello', ' ', 'world']),
      (' !hello world', [' !', 'hello', ' ', 'world']),
      # Single space at end
      ('hello world ', ['hello', ' ', 'world', ' ']),
      ('hello world! ', ['hello', ' ', 'world', '! ']),
      # Double space at beginning
      ('  hello world', ['  ', 'hello', ' ', 'world']),
      ('  !hello world', ['  !', 'hello', ' ', 'world']),
      # Double space in middle
      ('hello  world', ['hello', '  ', 'world']),
      ('hello!  world', ['hello', '!  ', 'world']),
      ('hello  !world', ['hello', '  !', 'world']),
  )
  def test_whitespace(self, s, exp):
    tokenizer = text_encoder.Tokenizer(alphanum_only=False)
    self.assertEqual(exp, tokenizer.tokenize(s))
    self.assertEqual(s, tokenizer.join(tokenizer.tokenize(s)))

  def test_reserved_tokens(self):
    text = 'hello worldbar bar foozoo zoo FOO<EOS>'
    tokens = ['hello', ' ', 'world', 'bar', ' ', 'bar', ' ', 'foozoo',
              ' ', 'zoo', ' ', 'FOO', '<EOS>']
    tokenizer = text_encoder.Tokenizer(alphanum_only=False,
                                       reserved_tokens=['<EOS>', 'FOO', 'bar'])
    self.assertEqual(tokens, tokenizer.tokenize(text))
    self.assertEqual(text, tokenizer.join(tokenizer.tokenize(text)))

  def test_reserved_tokens_with_regex_chars(self):
    text = r'hello worldba\)r bar foozoo zoo FOO|<EOS>'
    tokens = ['hello', ' ', 'world', r'ba\)r', ' ', 'bar', ' ', 'foozoo',
              ' ', 'zoo', ' ', 'FOO|', '<EOS>']
    tokenizer = text_encoder.Tokenizer(
        alphanum_only=False,
        reserved_tokens=['<EOS>', 'FOO|', r'ba\)r'])
    self.assertEqual(tokens, tokenizer.tokenize(text))
    self.assertEqual(text, tokenizer.join(tokenizer.tokenize(text)))


if __name__ == '__main__':
  testing.test_main()
