# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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
"""SQUAD: The Stanford Question Answering Dataset."""

from __future__ import absolute_import, division, print_function

import json
import logging

import datasets


_CITATION = """\
@inproceedings{miller2020effect,
  author = {J. Miller and K. Krauth and B. Recht and L. Schmidt},
  booktitle = {International Conference on Machine Learning (ICML)},
  title = {The Effect of Natural Distribution Shift on Question Answering Models},
  year = {2020},
}
"""

_DESCRIPTION = r"""\
SquadShifts consists of four new test sets for the Stanford Question Answering \
Dataset (SQuAD) from four different domains: Wikipedia articles, New York \
Times articles, Reddit comments, and Amazon product reviews. Each dataset \
was generated using the same data generating pipeline, Amazon Mechanical \
Turk interface, and data cleaning code as the original SQuAD v1.1 dataset. \
The "new-wikipedia" dataset measures overfitting on the original SQuAD v1.1 \
dataset.  The "new-york-times", "reddit", and "amazon" datasets measure \
robustness to natural distribution shifts. We encourage SQuAD model developers \
to also evaluate their methods on these new datasets! \
"""

_URL = "https://raw.githubusercontent.com/modestyachts/squadshifts-website/master/datasets/"
_URLS = {
    "new_wiki": _URL + "new_wiki_v1.0.json",
    "nyt": _URL + "nyt_v1.0.json",
    "reddit": _URL + "reddit_v1.0.json",
    "amazon": _URL + "amazon_reviews_v1.0.json",
}


class SquadShiftsConfig(datasets.BuilderConfig):
    """BuilderConfig for SquadShifts."""

    def __init__(self, **kwargs):
        """BuilderConfig for SQUAD.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(SquadShiftsConfig, self).__init__(**kwargs)


class SquadShifts(datasets.GeneratorBasedBuilder):
    """SquadShifts consists of four new test sets for the SQUAD dataset."""

    BUILDER_CONFIGS = [
        SquadShiftsConfig(
            name="new_wiki",
            version=datasets.Version("1.0.0", ""),
            description="SQuADShifts New Wikipedia article dataset",
        ),
        SquadShiftsConfig(
            name="nyt",
            version=datasets.Version("1.0.0", ""),
            description="SQuADShifts New York Times article dataset.",
        ),
        SquadShiftsConfig(
            name="reddit",
            version=datasets.Version("1.0.0", ""),
            description="SQuADShifts Reddit comment dataset.",
        ),
        SquadShiftsConfig(
            name="amazon",
            version=datasets.Version("1.0.0", ""),
            description="SQuADShifts Amazon product review dataset.",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {
                            "text": datasets.Value("string"),
                            "answer_start": datasets.Value("int32"),
                        }
                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage="https://modestyachts.github.io/squadshifts-website/index.html",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = _URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        if self.config.name == "new_wiki" or self.config.name == "default":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["new_wiki"]}
                ),
            ]
        elif self.config.name == "nyt":
            return [
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["nyt"]}),
            ]
        elif self.config.name == "reddit":
            return [
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["reddit"]}),
            ]
        elif self.config.name == "amazon":
            return [
                datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["amazon"]}),
            ]
        else:
            raise ValueError("SQuADShifts dataset name {} not found!".format(self.config.name))

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logging.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            squad = json.load(f)
            for article in squad["data"]:
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
                            "answers": {
                                "answer_start": answer_starts,
                                "text": answers,
                            },
                        }
