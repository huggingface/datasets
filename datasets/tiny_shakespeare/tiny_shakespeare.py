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
"""Tiny Shakespeare dataset."""

from __future__ import absolute_import, division, print_function

import os

import nlp


_CITATION = """\
@misc{
  author={Karpathy, Andrej},
  title={char-rnn},
  year={2015},
  howpublished={\\url{https://github.com/karpathy/char-rnn}}
}"""

_DESCRIPTION = """\
40,000 lines of Shakespeare from a variety of Shakespeare's plays. \
Featured in Andrej Karpathy's blog post 'The Unreasonable Effectiveness of \
Recurrent Neural Networks': \
http://karpathy.github.io/2015/05/21/rnn-effectiveness/.

To use for e.g. character modelling:

```
d = nlp.load_dataset(name='tiny_shakespeare')['train']
d = d.map(lambda x: nlp.Value('strings').unicode_split(x['text'], 'UTF-8'))
# train split includes vocabulary for other splits
vocabulary = sorted(set(next(iter(d)).numpy()))
d = d.map(lambda x: {'cur_char': x[:-1], 'next_char': x[1:]})
d = d.unbatch()
seq_len = 100
batch_size = 2
d = d.batch(seq_len)
d = d.batch(batch_size)
```
"""


class TinyShakespeare(nlp.GeneratorBasedBuilder):
    """Tiny Shakespeare dataset builder."""

    VERSION = nlp.Version("1.0.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({"text": nlp.Value("string")}),
            supervised_keys=None,
            homepage="https://github.com/karpathy/char-rnn/blob/master/data/tinyshakespeare/input.txt",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        download_path = dl_manager.download_and_extract(
            "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
        )
        if os.path.isdir(download_path):
            # During testing the download manager mock gives us a directory
            txt_path = os.path.join(download_path, "input.txt")
        else:
            txt_path = download_path
        with open(txt_path, "r") as f:
            text = f.read()

        # 90/5/5 split
        i = int(len(text) * 0.9)
        train_text, text = text[:i], text[i:]
        i = int(len(text) * 0.5)
        validation_text, text = text[:i], text[i:]
        test_text = text

        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"split_key": "train", "split_text": train_text},
            ),
            nlp.SplitGenerator(
                name=nlp.Split.VALIDATION, gen_kwargs={"split_key": "validation", "split_text": validation_text},
            ),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"split_key": "test", "split_text": test_text},),
        ]

    def _generate_examples(self, split_key, split_text):
        """Yields examples."""
        data_key = split_key  # Should uniquely identify the thing yielded
        feature_dict = {"text": split_text}
        yield data_key, feature_dict
