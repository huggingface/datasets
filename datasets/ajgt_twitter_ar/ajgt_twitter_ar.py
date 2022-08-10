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
"""Arabic Jordanian General Tweets."""


import os

import openpyxl  # noqa: requires this pandas optional dependency for reading xlsx files
import pandas as pd

import datasets
from datasets.tasks import TextClassification


_DESCRIPTION = """\
Arabic Jordanian General Tweets (AJGT) Corpus consisted of 1,800 tweets \
annotated as positive and negative. Modern Standard Arabic (MSA) or Jordanian dialect.
"""

_CITATION = """\
@inproceedings{alomari2017arabic,
  title={Arabic tweets sentimental analysis using machine learning},
  author={Alomari, Khaled Mohammad and ElSherif, Hatem M and Shaalan, Khaled},
  booktitle={International Conference on Industrial, Engineering and Other Applications of Applied Intelligent Systems},
  pages={602--610},
  year={2017},
  organization={Springer}
}
"""

_URL = "https://raw.githubusercontent.com/komari6/Arabic-twitter-corpus-AJGT/master/"


class AjgtConfig(datasets.BuilderConfig):
    """BuilderConfig for Ajgt."""

    def __init__(self, **kwargs):
        """BuilderConfig for Ajgt.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AjgtConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)


class AjgtTwitterAr(datasets.GeneratorBasedBuilder):
    """Ajgt dataset."""

    BUILDER_CONFIGS = [
        AjgtConfig(
            name="plain_text",
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                            "Negative",
                            "Positive",
                        ]
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/komari6/Arabic-twitter-corpus-AJGT",
            citation=_CITATION,
            task_templates=[TextClassification(text_column="text", label_column="label")],
        )

    def _split_generators(self, dl_manager):
        urls_to_download = {
            "train": os.path.join(_URL, "AJGT.xlsx"),
        }
        downloaded_files = dl_manager.download(urls_to_download)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
        ]

    def _generate_examples(self, filepath):
        """Generate examples."""
        with open(filepath, "rb") as f:
            df = pd.read_excel(f, engine="openpyxl")
            for id_, record in df.iterrows():
                tweet, sentiment = record["Feed"], record["Sentiment"]
                yield str(id_), {"text": tweet, "label": sentiment}
