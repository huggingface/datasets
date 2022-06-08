# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
import json

import datasets


_DESCRIPTION = """\
The NQ-Open task, introduced by Lee et.al. 2019,
is an open domain question answering benchmark that is derived from Natural Questions.
The goal is to predict an English answer string for an input English question.
All questions can be answered using the contents of English Wikipedia.
"""

_HOMEPAGE_URL = "https://efficientqa.github.io/"

_CITATION = """\
@article{doi:10.1162/tacl_a_00276,
    author = {Kwiatkowski, Tom and Palomaki, Jennimaria and Redfield, Olivia and Collins, Michael and Parikh, Ankur and Alberti, Chris and Epstein, Danielle and Polosukhin, Illia and Devlin, Jacob and Lee, Kenton and Toutanova, Kristina and Jones, Llion and Kelcey, Matthew and Chang, Ming-Wei and Dai, Andrew                         M. and Uszkoreit, Jakob and Le, Quoc and Petrov, Slav},
    title = {Natural Questions: A Benchmark for Question Answering Research},
    journal = {Transactions of the Association for Computational Linguistics},
    volume = {7},
    number = {},
    pages = {453-466},
    year = {2019},
    doi = {10.1162/tacl_a_00276},
    URL = {
            https://doi.org/10.1162/tacl_a_00276
        },
    eprint = {
            https://doi.org/10.1162/tacl_a_00276
        },
    abstract = { We present the Natural Questions corpus, a question answering data set. Questions consist of real anonymized, aggregated queries issued to the Google search engine. An annotator is presented with a question along with a Wikipedia page from the top 5 search results, and annotates a long answer (typically a paragraph) and a short answer (one or more entities) if present on the page, or marks null if no long/short answer is present. The public release consists of 307,373 training examples with single annotations; 7,830 examples with 5-way annotations for development data; and a further 7,842 examples with 5-way annotated sequestered as test data. We present experiments validating quality of the data. We also describe analysis of 25-way annotations on 302 examples, giving insights into human variability on the annotation task. We introduce robust metrics for the purposes of evaluating question answering systems; demonstrate high human upper bounds on these metrics; and establish baseline results using competitive methods drawn from related literature. }
}

@inproceedings{lee-etal-2019-latent,
    title = "Latent Retrieval for Weakly Supervised Open Domain Question Answering",
    author = "Lee, Kenton  and
      Chang, Ming-Wei  and
      Toutanova, Kristina",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1612",
    doi = "10.18653/v1/P19-1612",
    pages = "6086--6096",
    abstract = "Recent work on open domain question answering (QA) assumes strong supervision of the supporting evidence and/or assumes a blackbox information retrieval (IR) system to retrieve evidence candidates. We argue that both are suboptimal, since gold evidence is not always available, and QA is fundamentally different from IR. We show for the first time that it is possible to jointly learn the retriever and reader from question-answer string pairs and without any IR system. In this setting, evidence retrieval from all of Wikipedia is treated as a latent variable. Since this is impractical to learn from scratch, we pre-train the retriever with an Inverse Cloze Task. We evaluate on open versions of five QA datasets. On datasets where the questioner already knows the answer, a traditional IR system such as BM25 is sufficient. On datasets where a user is genuinely seeking an answer, we show that learned retrieval is crucial, outperforming BM25 by up to 19 points in exact match.",
}
"""

_URLS = {
    "dev": "https://raw.githubusercontent.com/google-research-datasets/natural-questions/master/nq_open/NQ-open.dev.jsonl",
    "train": "https://raw.githubusercontent.com/google-research-datasets/natural-questions/master/nq_open/NQ-open.train.jsonl",
}


class NQOpenConfig(datasets.BuilderConfig):
    """BuilderConfig for NQ_Open."""

    def __init__(self, **kwargs):
        """BuilderConfig for NQ_Open.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(NQOpenConfig, self).__init__(**kwargs)


class NQOpen(datasets.GeneratorBasedBuilder):
    """NQ_Open open domain question answering dataset."""

    BUILDER_CONFIGS = [
        NQOpenConfig(
            name="nq_open",
            version=datasets.Version("2.0.0", ""),
            description="NQ_Open open domain question answering dataset.",
        ),
    ]
    BUILDER_CONFIG_CLASS = NQOpenConfig

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "question": datasets.Value("string"),
                    "answer": datasets.Sequence(datasets.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        paths = dl_manager.download_and_extract(_URLS)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"datapath": paths["train"]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"datapath": paths["dev"]},
            ),
        ]

    def _generate_examples(self, datapath):
        """Generate NQ_Open examples."""

        with open(datapath, encoding="utf-8") as json_file:
            for i, json_str in enumerate(json_file):
                result = json.loads(json_str)
                yield i, result
