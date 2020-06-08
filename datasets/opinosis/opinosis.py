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
"""Opinosis Opinion Dataset."""

from __future__ import absolute_import, division, print_function

import os

import nlp


_CITATION = """
@inproceedings{ganesan2010opinosis,
  title={Opinosis: a graph-based approach to abstractive summarization of highly redundant opinions},
  author={Ganesan, Kavita and Zhai, ChengXiang and Han, Jiawei},
  booktitle={Proceedings of the 23rd International Conference on Computational Linguistics},
  pages={340--348},
  year={2010},
  organization={Association for Computational Linguistics}
}
"""

_DESCRIPTION = """
The Opinosis Opinion Dataset consists of sentences extracted from reviews for 51 topics.
Topics and opinions are obtained from Tripadvisor, Edmunds.com and Amazon.com.
"""

_URL = "https://github.com/kavgan/opinosis-summarization/raw/master/OpinosisDataset1.0_0.zip"

_REVIEW_SENTS = "review_sents"
_SUMMARIES = "summaries"


class Opinosis(nlp.GeneratorBasedBuilder):
    """Opinosis Opinion Dataset."""

    VERSION = nlp.Version("1.0.0")

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {_REVIEW_SENTS: nlp.Value("string"), _SUMMARIES: nlp.features.Sequence(nlp.Value("string"))}
            ),
            supervised_keys=(_REVIEW_SENTS, _SUMMARIES),
            homepage="http://kavita-ganesan.com/opinosis/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        extract_path = dl_manager.download_and_extract(_URL)
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"path": extract_path},),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        topics_path = os.path.join(path, "topics")
        filenames = sorted(os.listdir(topics_path))
        for filename in filenames:
            file_path = os.path.join(topics_path, filename)
            topic_name = filename.split(".txt")[0]
            with open(file_path, "rb") as src_f:
                input_data = src_f.read().decode("latin-1")
            summaries_path = os.path.join(path, "summaries-gold", topic_name)
            summary_lst = []
            for summ_filename in sorted(os.listdir(summaries_path)):
                file_path = os.path.join(summaries_path, summ_filename)
                with open(file_path, "rb") as tgt_f:
                    data = tgt_f.read().strip().decode("latin-1")
                    summary_lst.append(data)
            summary_data = summary_lst
            yield filename, {_REVIEW_SENTS: input_data, _SUMMARIES: summary_data}
