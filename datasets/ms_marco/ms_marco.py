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
"""MS MARCO dataset."""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """
@article{DBLP:journals/corr/NguyenRSGTMD16,
  author    = {Tri Nguyen and
               Mir Rosenberg and
               Xia Song and
               Jianfeng Gao and
               Saurabh Tiwary and
               Rangan Majumder and
               Li Deng},
  title     = {{MS} {MARCO:} {A} Human Generated MAchine Reading COmprehension Dataset},
  journal   = {CoRR},
  volume    = {abs/1611.09268},
  year      = {2016},
  url       = {http://arxiv.org/abs/1611.09268},
  archivePrefix = {arXiv},
  eprint    = {1611.09268},
  timestamp = {Mon, 13 Aug 2018 16:49:03 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/NguyenRSGTMD16.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
}
"""

_DESCRIPTION = """
Starting with a paper released at NIPS 2016, MS MARCO is a collection of datasets focused on deep learning in search.

The first dataset was a question answering dataset featuring 100,000 real Bing questions and a human generated answer.
Since then we released a 1,000,000 question dataset, a natural langauge generation dataset, a passage ranking dataset,
keyphrase extraction dataset, crawling dataset, and a conversational search.

There have been 277 submissions. 20 KeyPhrase Extraction submissions, 87 passage ranking submissions, 0 document ranking
submissions, 73 QnA V2 submissions, 82 NLGEN submisions, and 15 QnA V1 submissions

This data comes in three tasks/forms: Original QnA dataset(v1.1), Question Answering(v2.1), Natural Language Generation(v2.1).

The original question answering datset featured 100,000 examples and was released in 2016. Leaderboard is now closed but data is availible below.

The current competitive tasks are Question Answering and Natural Language Generation. Question Answering features over 1,000,000 queries and
is much like the original QnA dataset but bigger and with higher quality. The Natural Language Generation dataset features 180,000 examples and
builds upon the QnA dataset to deliver answers that could be spoken by a smart speaker.

"""
_V2_URLS = {
    "train": "https://msmarco.blob.core.windows.net/msmarco/train_v2.1.json.gz",
    "dev": "https://msmarco.blob.core.windows.net/msmarco/dev_v2.1.json.gz",
    "test": "https://msmarco.blob.core.windows.net/msmarco/eval_v2.1_public.json.gz",
}

_V1_URLS = {
    "train": "https://msmarco.blob.core.windows.net/msmsarcov1/train_v1.1.json.gz",
    "dev": "https://msmarco.blob.core.windows.net/msmsarcov1/dev_v1.1.json.gz",
    "test": "https://msmarco.blob.core.windows.net/msmsarcov1/test_hidden_v1.1.json",
}


class MsMarcoConfig(datasets.BuilderConfig):
    """BuilderConfig for MS MARCO."""

    def __init__(self, **kwargs):
        """BuilderConfig for MS MARCO

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(MsMarcoConfig, self).__init__(**kwargs)


class MsMarco(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        MsMarcoConfig(
            name="v1.1",
            description="""version v1.1""",
            version=datasets.Version("1.1.0", ""),
        ),
        MsMarcoConfig(
            name="v2.1",
            description="""version v2.1""",
            version=datasets.Version("2.1.0", ""),
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(
                {
                    "answers": datasets.features.Sequence(datasets.Value("string")),
                    "passages": datasets.features.Sequence(
                        {
                            "is_selected": datasets.Value("int32"),
                            "passage_text": datasets.Value("string"),
                            "url": datasets.Value("string"),
                        }
                    ),
                    "query": datasets.Value("string"),
                    "query_id": datasets.Value("int32"),
                    "query_type": datasets.Value("string"),
                    "wellFormedAnswers": datasets.features.Sequence(datasets.Value("string")),
                }
            ),
            homepage="https://microsoft.github.io/msmarco/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "v2.1":
            dl_path = dl_manager.download_and_extract(_V2_URLS)
        else:
            dl_path = dl_manager.download_and_extract(_V1_URLS)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": dl_path["dev"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": dl_path["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": dl_path["test"]},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            if self.config.name == "v2.1":
                data = json.load(f)
                questions = data["query"]
                answers = data.get("answers", {})
                passages = data["passages"]
                query_ids = data["query_id"]
                query_types = data["query_type"]
                wellFormedAnswers = data.get("wellFormedAnswers", {})
                for key in questions:

                    is_selected = [passage.get("is_selected", -1) for passage in passages[key]]
                    passage_text = [passage["passage_text"] for passage in passages[key]]
                    urls = [passage["url"] for passage in passages[key]]
                    question = questions[key]
                    answer = answers.get(key, [])
                    query_id = query_ids[key]
                    query_type = query_types[key]
                    wellFormedAnswer = wellFormedAnswers.get(key, [])
                    if wellFormedAnswer == "[]":
                        wellFormedAnswer = []
                    yield query_id, {
                        "answers": answer,
                        "passages": {"is_selected": is_selected, "passage_text": passage_text, "url": urls},
                        "query": question,
                        "query_id": query_id,
                        "query_type": query_type,
                        "wellFormedAnswers": wellFormedAnswer,
                    }
            if self.config.name == "v1.1":
                for row in f:
                    data = json.loads(row)
                    question = data["query"]
                    answer = data.get("answers", [])
                    passages = data["passages"]
                    query_id = data["query_id"]
                    query_type = data["query_type"]
                    wellFormedAnswer = data.get("wellFormedAnswers", [])

                    is_selected = [passage.get("is_selected", -1) for passage in passages]
                    passage_text = [passage["passage_text"] for passage in passages]
                    urls = [passage["url"] for passage in passages]
                    if wellFormedAnswer == "[]":
                        wellFormedAnswer = []
                    yield query_id, {
                        "answers": answer,
                        "passages": {"is_selected": is_selected, "passage_text": passage_text, "url": urls},
                        "query": question,
                        "query_id": query_id,
                        "query_type": query_type,
                        "wellFormedAnswers": wellFormedAnswer,
                    }
