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
"""Large-scale Indonesian Summarization Dataset"""

from __future__ import absolute_import, division, print_function

import glob
import json
import logging
import os
from pathlib import Path

import datasets


_CITATION = """\
@inproceedings{id_liputan6,
  author    = {Fajri Koto, Jey Han Lau, Timothy Baldwin},
  title     = {Liputan6: A Large-scale Indonesian Dataset for Text Summarization},
  year      = {2020},
  url       = {https://arxiv.org/abs/2011.00679},
}
"""

_DESCRIPTION = """\
In this paper, we introduce a large-scale Indonesian summarization dataset. We harvest articles from this http URL,
an online news portal, and obtain 215,827 document-summary pairs. We leverage pre-trained language models to develop
benchmark extractive and abstractive summarization methods over the dataset with multilingual and monolingual
BERT-based models. We include a thorough error analysis by examining machine-generated summaries that have
low ROUGE scores, and expose both issues with ROUGE it-self, as well as with extractive and abstractive
summarization models.
"""

_HOMEPAGE = "https://arxiv.org/abs/2011.00679"

_LICENSE = ""

_URLs = []

_FILENAME = "liputan6_data.tar.gz"


class IdLiputan6Config(datasets.BuilderConfig):
    """BuilderConfig for IdLiputan6"""

    def __init__(self, filename=None, **kwargs):
        """BuilderConfig for IdLiputan6.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdLiputan6Config, self).__init__(**kwargs)
        self.filename = filename


class IdLiputan6(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdLiputan6Config(
            name="canonical",
            version=VERSION,
            description="Canonical Liputan6 dataset",
            filename=_FILENAME,
        ),
        IdLiputan6Config(
            name="xtreme",
            version=VERSION,
            description="Xtreme Liputan6 dataset",
            filename=_FILENAME,
        )
    ]

    @property
    def manual_download_instructions(self):
        return """\
  You need to manually request the liputan6 dataset from https://github.com/fajri91/sum_liputan6/
  and save it in a directory <path/to/folder>. The name of downloaded file is "liputan6_data.tar.gz".
  The liputan6 dataset can then be loaded using the following command 
  `datasets.load_dataset("id_liputan6", 'canonical', data_dir="<path/to/folder>")`.
  """

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "url": datasets.Value("string"),
                "clean_article": datasets.Value("string"),
                "clean_summary": datasets.Value("string"),
                "extractive_summary": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path_to_manual_file = os.path.join(
            os.path.abspath(os.path.expanduser(dl_manager.manual_dir)), self.config.filename
        )
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('id_liputan6', "
                "data_dir=...)` that includes a file name {}. Manual download instructions: {})".format(
                    path_to_manual_file, self.config.filename, self.manual_download_instructions
                )
            )
        data_dir = dl_manager.download_and_extract(path_to_manual_file)
        split_generators = [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, "liputan6_data/{}/dev".format(self.config.name)),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, "liputan6_data/{}/test".format(self.config.name)),
                    "split": "test",
                },
            )
        ]
        if self.config.name == "canonical":
            split_generators.append(datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, "liputan6_data/{}/train".format(self.config.name)),
                    "split": "train",
                },
            ))
        return split_generators

    def _generate_examples(self, article_dir, split):
        logging.info("⏳ Generating %s examples from = %s", split, article_dir)
        guid = 0
        for path in sorted(glob.glob(os.path.join(article_dir, "**/*.json"), recursive=True),
                           key=lambda p: int(Path(p).stem)):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                yield guid, {
                    "id": str(data["id"]),
                    "url": data["url"],
                    "clean_article": " ".join([" ".join(i) for i in data["clean_article"]]),
                    "clean_summary": " ".join([" ".join(i) for i in data["clean_summary"]]),
                    "extractive_summary": " ".join([" ".join(data["clean_article"][i])
                                                    for i in data["extractive_summary"]]),
                }
            guid += 1
