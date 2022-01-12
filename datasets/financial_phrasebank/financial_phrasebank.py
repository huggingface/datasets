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

"""Financial Phrase Bank v1.0: Polar sentiment dataset of sentences from
financial news. The dataset consists of 4840 sentences from English language
financial news categorised by sentiment. The dataset is divided by agreement
rate of 5-8 annotators."""


import os

import datasets


_CITATION = """\
@article{Malo2014GoodDO,
  title={Good debt or bad debt: Detecting semantic orientations in economic texts},
  author={P. Malo and A. Sinha and P. Korhonen and J. Wallenius and P. Takala},
  journal={Journal of the Association for Information Science and Technology},
  year={2014},
  volume={65}
}
"""

_DESCRIPTION = """\
The key arguments for the low utilization of statistical techniques in
financial sentiment analysis have been the difficulty of implementation for
practical applications and the lack of high quality training data for building
such models. Especially in the case of finance and economic texts, annotated
collections are a scarce resource and many are reserved for proprietary use
only. To resolve the missing training data problem, we present a collection of
∼ 5000 sentences to establish human-annotated standards for benchmarking
alternative modeling techniques.

The objective of the phrase level annotation task was to classify each example
sentence into a positive, negative or neutral category by considering only the
information explicitly available in the given sentence. Since the study is
focused only on financial and economic domains, the annotators were asked to
consider the sentences from the view point of an investor only; i.e. whether
the news may have positive, negative or neutral influence on the stock price.
As a result, sentences which have a sentiment that is not relevant from an
economic or financial perspective are considered neutral.

This release of the financial phrase bank covers a collection of 4840
sentences. The selected collection of phrases was annotated by 16 people with
adequate background knowledge on financial markets. Three of the annotators
were researchers and the remaining 13 annotators were master’s students at
Aalto University School of Business with majors primarily in finance,
accounting, and economics.

Given the large number of overlapping annotations (5 to 8 annotations per
sentence), there are several ways to define a majority vote based gold
standard. To provide an objective comparison, we have formed 4 alternative
reference datasets based on the strength of majority agreement: all annotators
agree, >=75% of annotators agree, >=66% of annotators agree and >=50% of
annotators agree.
"""

_HOMEPAGE = "https://www.kaggle.com/ankurzing/sentiment-analysis-for-financial-news"

_LICENSE = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License"

_URL = "https://www.researchgate.net/profile/Pekka_Malo/publication/251231364_FinancialPhraseBank-v10/data/0c96051eee4fb1d56e000000/FinancialPhraseBank-v10.zip"


_VERSION = datasets.Version("1.0.0")


class FinancialPhraseBankConfig(datasets.BuilderConfig):
    """BuilderConfig for FinancialPhraseBank."""

    def __init__(
        self,
        split,
        **kwargs,
    ):
        """BuilderConfig for Discovery.
        Args:
          filename_bit: `string`, the changing part of the filename.
        """

        super(FinancialPhraseBankConfig, self).__init__(name=f"sentences_{split}agree", version=_VERSION, **kwargs)

        self.path = os.path.join("FinancialPhraseBank-v1.0", f"Sentences_{split.title()}Agree.txt")


class FinancialPhrasebank(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        FinancialPhraseBankConfig(
            split="all",
            description="Sentences where all annotators agreed",
        ),
        FinancialPhraseBankConfig(split="75", description="Sentences where at least 75% of annotators agreed"),
        FinancialPhraseBankConfig(split="66", description="Sentences where at least 66% of annotators agreed"),
        FinancialPhraseBankConfig(split="50", description="Sentences where at least 50% of annotators agreed"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "negative",
                            "neutral",
                            "positive",
                        ]
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
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, self.config.path)},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="iso-8859-1") as f:
            for id_, line in enumerate(f):
                sentence, label = line.rsplit("@", 1)
                yield id_, {"sentence": sentence, "label": label}
