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
"""Scientific Papers Dataset."""

from __future__ import absolute_import, division, print_function

import json
import os

import nlp


_CITATION = """
@article{Cohan_2018,
   title={A Discourse-Aware Attention Model for Abstractive Summarization of
            Long Documents},
   url={http://dx.doi.org/10.18653/v1/n18-2097},
   DOI={10.18653/v1/n18-2097},
   journal={Proceedings of the 2018 Conference of the North American Chapter of
          the Association for Computational Linguistics: Human Language
          Technologies, Volume 2 (Short Papers)},
   publisher={Association for Computational Linguistics},
   author={Cohan, Arman and Dernoncourt, Franck and Kim, Doo Soon and Bui, Trung and Kim, Seokhwan and Chang, Walter and Goharian, Nazli},
   year={2018}
}
"""

_DESCRIPTION = """
Scientific papers datasets contains two sets of long and structured documents.
The datasets are obtained from ArXiv and PubMed OpenAccess repositories.

Both "arxiv" and "pubmed" have two features:
  - article: the body of the document, pagragraphs seperated by "/n".
  - abstract: the abstract of the document, pagragraphs seperated by "/n".
  - section_names: titles of sections, seperated by "/n".

"""

_DOCUMENT = "article"
_SUMMARY = "abstract"

_URLS = {
    "arxiv": "https://drive.google.com/uc?id=1b3rmCSIoh6VhD4HKWjI4HOW-cSwcwbeC&export=download",
    "pubmed": "https://drive.google.com/uc?id=1lvsqvsFi3W-pE1SqNZI0s8NR9rC1tsja&export=download",
}


class ScientificPapersConfig(nlp.BuilderConfig):
    """BuilderConfig for Scientific Papers."""

    def __init__(self, filename=None, **kwargs):
        """BuilderConfig for Wikihow.

    Args:
      filename: filename of different configs for the dataset.
      **kwargs: keyword arguments forwarded to super.
    """
        # 1.1.0 remove sentence breaker <S> and </S> in summary.
        super(ScientificPapersConfig, self).__init__(version=nlp.Version("1.1.1"), **kwargs)
        self.filename = filename


class ScientificPapers(nlp.GeneratorBasedBuilder):
    """Scientific Papers."""

    BUILDER_CONFIGS = [
        ScientificPapersConfig(name="pubmed", description="Documents from PubMed repository."),
        ScientificPapersConfig(name="arxiv", description="Documents from ArXiv repository."),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {_DOCUMENT: nlp.Value("string"), _SUMMARY: nlp.Value("string"), "section_names": nlp.Value("string"),}
            ),
            supervised_keys=None,
            homepage="https://github.com/armancohan/long-summarization",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        dl_paths = dl_manager.download_and_extract(_URLS)
        path = os.path.join(dl_paths[self.config.name], self.config.name + "-dataset")
        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"path": os.path.join(path, "train.txt")},),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"path": os.path.join(path, "val.txt")},),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"path": os.path.join(path, "test.txt")},),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path) as f:
            for line in f:
                # Possible keys are:
                # "article_id": str
                # "article_text": list[str] article (list of paragraphs).
                # "abstract_text": list[str], abstract (list of paragraphs).
                # "section_names": list[str], list of section names.
                # "sections": list[list[str]], list of sections (list of paragraphs)
                d = json.loads(line)
                summary = "\n".join(d["abstract_text"])
                # In original paper, <S> and </S> are not used in vocab during training
                # or during decoding.
                # https://github.com/armancohan/long-summarization/blob/master/data.py#L27
                summary = summary.replace("<S>", "").replace("</S>", "")
                yield d["article_id"], {
                    _DOCUMENT: "\n".join(d["article_text"]),
                    _SUMMARY: summary,
                    "section_names": "\n".join(d["section_names"]),
                }
