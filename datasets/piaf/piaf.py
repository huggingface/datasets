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
"""PIAF Question Answering Dataset"""

from __future__ import absolute_import, division, print_function

import json
import logging
import os

import nlp


_CITATION = """\
@InProceedings{keraron-EtAl:2020:LREC,
  author    = {Keraron, Rachel  and  Lancrenon, Guillaume  and  Bras, Mathilde  and  Allary, Frédéric  and  Moyse, Gilles  and  Scialom, Thomas  and  Soriano-Morales, Edmundo-Pavel  and  Staiano, Jacopo},
  title     = {Project PIAF: Building a Native French Question-Answering Dataset},
  booktitle      = {Proceedings of The 12th Language Resources and Evaluation Conference},
  month          = {May},
  year           = {2020},
  address        = {Marseille, France},
  publisher      = {European Language Resources Association},
  pages     = {5483--5492},
  abstract  = {Motivated by the lack of data for non-English languages, in particular for the evaluation of downstream tasks such as Question Answering, we present a participatory effort to collect a native French Question Answering Dataset. Furthermore, we describe and publicly release the annotation tool developed for our collection effort, along with the data obtained and preliminary baselines.},
  url       = {https://www.aclweb.org/anthology/2020.lrec-1.673}
}
"""

_DESCRIPTION = """\
Piaf is a reading comprehension \
dataset. This version, published in February 2020, contains 3835 questions on French Wikipedia.
"""


class PiafConfig(nlp.BuilderConfig):
    """BuilderConfig for PIAF."""

    def __init__(self, **kwargs):
        """BuilderConfig for PIAF.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(PiafConfig, self).__init__(**kwargs)


class Piaf(nlp.GeneratorBasedBuilder):
    """The Piaf Question Answering Dataset. Version 1.0."""

    _URL = "https://github.com/etalab-ia/piaf-code/raw/master/"
    _TRAINING_FILE = "piaf-v1.0.json"

    BUILDER_CONFIGS = [
        PiafConfig(
            name="plain_text",
            version=nlp.Version("1.0.0", "New split API (https://tensorflow.org/datasets/splits)"),
            description="Plain text",
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "title": nlp.Value("string"),
                    "context": nlp.Value("string"),
                    "question": nlp.Value("string"),
                    "answers": nlp.features.Sequence(
                        {"text": nlp.Value("string"), "answer_start": nlp.Value("int32"),}
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://piaf.etalab.studio",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = {"train": os.path.join(self._URL, self._TRAINING_FILE)}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        with open(filepath) as f:
            dataset = json.load(f)
            for article in dataset["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers,},
                        }
