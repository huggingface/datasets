# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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


import csv

import datasets


_CITATION = """\
    @inproceedings{uppal-etal-2020-two,
    title = "Two-Step Classification using Recasted Data for Low Resource Settings",
    author = "Uppal, Shagun  and
      Gupta, Vivek  and
      Swaminathan, Avinash  and
      Zhang, Haimin  and
      Mahata, Debanjan  and
      Gosangi, Rakesh  and
      Shah, Rajiv Ratn  and
      Stent, Amanda",
    booktitle = "Proceedings of the 1st Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 10th International Joint Conference on Natural Language Processing",
    month = dec,
    year = "2020",
    address = "Suzhou, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/2020.aacl-main.71",
    pages = "706--719",
    abstract = "An NLP model{'}s ability to reason should be independent of language. Previous works utilize Natural Language Inference (NLI) to understand the reasoning ability of models, mostly focusing on high resource languages like English. To address scarcity of data in low-resource languages such as Hindi, we use data recasting to create NLI datasets for four existing text classification datasets. Through experiments, we show that our recasted dataset is devoid of statistical irregularities and spurious patterns. We further study the consistency in predictions of the textual entailment models and propose a consistency regulariser to remove pairwise-inconsistencies in predictions. We propose a novel two-step classification method which uses textual-entailment predictions for classification task. We further improve the performance by using a joint-objective for classification and textual entailment. We therefore highlight the benefits of data recasting and improvements on classification performance using our approach with supporting experimental results.",
}
"""

_DESCRIPTION = """\
This dataset is a recasted version of the Hindi Discourse Analysis Dataset used to train models for Natural Language Inference Tasks in Low-Resource Languages like Hindi.
"""

_HOMEPAGE = "https://github.com/midas-research/hindi-nli-data"

_LICENSE = """
MIT License

Copyright (c) 2019 MIDAS, IIIT Delhi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

_TRAIN_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/avinsit123/hindi-nli-data/master/Textual_Entailment/HDA/HDA_recasted_train.tsv"
)
_VALID_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/avinsit123/hindi-nli-data/master/Textual_Entailment/HDA/HDA_recasted_dev.tsv"
)
_TEST_DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/avinsit123/hindi-nli-data/master/Textual_Entailment/HDA/HDA_recasted_test.tsv"
)


class HdaNliHindiConfig(datasets.BuilderConfig):
    """BuilderConfig for HDA NLI Hindi Config"""

    def __init__(self, **kwargs):
        """BuilderConfig for HDA NLI Hindi Config
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(HdaNliHindiConfig, self).__init__(**kwargs)


class HdaNliHindi(datasets.GeneratorBasedBuilder):
    """HDA NLI Hindi dataset -- Dataset providing textual-entailment pairs for NLI tasks in Hindi"""

    BUILDER_CONFIGS = [
        HdaNliHindiConfig(
            name="HDA nli hindi",
            version=datasets.Version("1.1.0"),
            description="HDA Hindi NLI: Natural Language Inference Dataset for Hindi Discourse Analysis in Hindi",
        ),
    ]

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["not-entailment", "entailment"]),
                    "topic": datasets.ClassLabel(
                        names=["Argumentative", "Descriptive", "Dialogic", "Informative", "Narrative"]
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        test_path = dl_manager.download_and_extract(_TEST_DOWNLOAD_URL)
        valid_path = dl_manager.download_and_extract(_VALID_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": test_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as tsv_file:
            tsv_reader = csv.reader(tsv_file, delimiter="\t")
            for id_, row in enumerate(tsv_reader):
                if id_ == 0:
                    continue
                (premise, hypothesis, label, topic) = row
                yield id_, {
                    "premise": premise,
                    "hypothesis": hypothesis,
                    "label": 1 if label == "entailed" else 0,
                    "topic": int(topic),
                }
