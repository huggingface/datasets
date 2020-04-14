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
"""Gigaword summarization dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
@article{graff2003english,
  title={English gigaword},
  author={Graff, David and Kong, Junbo and Chen, Ke and Maeda, Kazuaki},
  journal={Linguistic Data Consortium, Philadelphia},
  volume={4},
  number={1},
  pages={34},
  year={2003}
}

@article{Rush_2015,
   title={A Neural Attention Model for Abstractive Sentence Summarization},
   url={http://dx.doi.org/10.18653/v1/D15-1044},
   DOI={10.18653/v1/d15-1044},
   journal={Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing},
   publisher={Association for Computational Linguistics},
   author={Rush, Alexander M. and Chopra, Sumit and Weston, Jason},
   year={2015}
}
"""

_DESCRIPTION = """
Headline-generation on a corpus of article pairs from Gigaword consisting of
around 4 million articles. Use the 'org_data' provided by
https://github.com/microsoft/unilm/ which is identical to
https://github.com/harvardnlp/sent-summary but with better format.

There are two features:
  - document: article.
  - summary: headline.

"""

_URL = "https://drive.google.com/uc?export=download&id=1USoQ8lJgN8kAWnUnRrupMGrPMLlDVqlV"

_DOCUMENT = "document"
_SUMMARY = "summary"


class Gigaword(tfds.core.GeneratorBasedBuilder):
  """Gigaword summarization dataset."""

  # 1.0.0 contains a bug that uses validation data as training data.
  # 1.1.0 Update to the correct train, validation and test data.
  # 1.2.0 Replace <unk> with <UNK> in train/val to be consistent with test.
  VERSION = tfds.core.Version("1.2.0")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            _DOCUMENT: tfds.features.Text(),
            _SUMMARY: tfds.features.Text()
        }),
        supervised_keys=(_DOCUMENT, _SUMMARY),
        homepage="https://github.com/harvardnlp/sent-summary",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    dl_path = dl_manager.download_and_extract(_URL)
    pattern = os.path.join(dl_path, "org_data", "%s.%s.txt")
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "src_path": pattern % ("train", "src"),
                "tgt_path": pattern % ("train", "tgt"),
                "replace_unk": True,
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={
                "src_path": pattern % ("dev", "src"),
                "tgt_path": pattern % ("dev", "tgt"),
                "replace_unk": True,
            },
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={
                "src_path": pattern % ("test", "src"),
                "tgt_path": pattern % ("test", "tgt"),
                "replace_unk": False,
            },
        ),
    ]

  def _generate_examples(self, src_path=None, tgt_path=None, replace_unk=None):
    """Yields examples."""
    with tf.io.gfile.GFile(src_path) as f_d, tf.io.gfile.GFile(tgt_path) as f_s:
      for i, (doc_text, sum_text) in enumerate(zip(f_d, f_s)):
        if replace_unk:
          yield i, {
              _DOCUMENT: doc_text.strip().replace("<unk>", "UNK"),
              _SUMMARY: sum_text.strip().replace("<unk>", "UNK")
          }
        else:
          yield i, {_DOCUMENT: doc_text.strip(), _SUMMARY: sum_text.strip()}
