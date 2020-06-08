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
"""IMDB movie reviews dataset."""

from __future__ import absolute_import, division, print_function

import os

import nlp


_DESCRIPTION = """\
Large Movie Review Dataset.
This is a dataset for binary sentiment classification containing substantially \
more data than previous benchmark datasets. We provide a set of 25,000 highly \
polar movie reviews for training, and 25,000 for testing. There is additional \
unlabeled data for use as well.\
"""

_CITATION = """\
@InProceedings{maas-EtAl:2011:ACL-HLT2011,
  author    = {Maas, Andrew L.  and  Daly, Raymond E.  and  Pham, Peter T.  and  Huang, Dan  and  Ng, Andrew Y.  and  Potts, Christopher},
  title     = {Learning Word Vectors for Sentiment Analysis},
  booktitle = {Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies},
  month     = {June},
  year      = {2011},
  address   = {Portland, Oregon, USA},
  publisher = {Association for Computational Linguistics},
  pages     = {142--150},
  url       = {http://www.aclweb.org/anthology/P11-1015}
}
"""

_DOWNLOAD_URL = "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz"


class IMDBReviewsConfig(nlp.BuilderConfig):
    """BuilderConfig for IMDBReviews."""

    def __init__(self, **kwargs):
        """BuilderConfig for IMDBReviews.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(IMDBReviewsConfig, self).__init__(
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"), **kwargs
        )


class Imdb(nlp.GeneratorBasedBuilder):
    """IMDB movie reviews dataset."""

    BUILDER_CONFIGS = [IMDBReviewsConfig(name="plain_text", description="Plain text",)]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {"text": nlp.Value("string"), "label": nlp.features.ClassLabel(names=["neg", "pos"])}
            ),
            supervised_keys=None,
            homepage="http://ai.stanford.edu/~amaas/data/sentiment/",
            citation=_CITATION,
        )

    def _vocab_text_gen(self, archive):
        for _, ex in self._generate_examples(archive, os.path.join("aclImdb", "train")):
            yield ex["text"]

    def _split_generators(self, dl_manager):
        arch_path = dl_manager.download_and_extract(_DOWNLOAD_URL)
        data_dir = os.path.join(arch_path, "aclImdb")
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"directory": os.path.join(data_dir, "train")}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"directory": os.path.join(data_dir, "test")}),
            nlp.SplitGenerator(
                name=nlp.Split("unsupervised"),
                gen_kwargs={"directory": os.path.join(data_dir, "train"), "labeled": False},
            ),
        ]

    def _generate_examples(self, directory, labeled=True):
        """Generate IMDB examples."""
        # For labeled examples, extract the label from the path.
        if labeled:
            files = {
                "pos": sorted(os.listdir(os.path.join(directory, "pos"))),
                "neg": sorted(os.listdir(os.path.join(directory, "neg"))),
            }
            for key in files:
                for id_, file in enumerate(files[key]):
                    filepath = os.path.join(directory, key, file)
                    with open(filepath) as f:
                        yield key + "_" + str(id_), {"text": f.read(), "label": key}
        else:
            unsup_files = sorted(os.listdir(os.path.join(directory, "unsup")))
            for id_, file in enumerate(unsup_files):
                filepath = os.path.join(directory, "unsup", file)
                with open(filepath) as f:
                    yield id_, {"text": f.read(), "label": -1}
