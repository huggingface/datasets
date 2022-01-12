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


import glob
import json
import os
import re
from pathlib import Path

import datasets


logger = datasets.logging.get_logger(__name__)


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


class IdLiputan6Config(datasets.BuilderConfig):
    """BuilderConfig for IdLiputan6"""

    def __init__(self, **kwargs):
        """BuilderConfig for IdLiputan6.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IdLiputan6Config, self).__init__(**kwargs)


class IdLiputan6(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        IdLiputan6Config(
            name="canonical",
            version=VERSION,
            description="Canonical Liputan6 dataset",
        ),
        IdLiputan6Config(
            name="xtreme",
            version=VERSION,
            description="Xtreme Liputan6 dataset",
        ),
    ]

    @property
    def manual_download_instructions(self):
        return """\
            You need to manually request the liputan6 dataset using the form in https://github.com/fajri91/sum_liputan6/
            and uncompress it.  The liputan6 dataset can then be loaded using the following command
            `datasets.load_dataset("id_liputan6", 'canonical', data_dir="<path/to/uncompressed_folder>")` or
            `datasets.load_dataset("id_liputan6", 'xtreme', data_dir="<path/to/uncompressed_folder>")`.
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
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('id_liputan6', "
                "'canonical', data_dir=...)`. Manual download instructions:\n{self.manual_download_instructions}"
            )
        split_generators = [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, f"{self.config.name}/dev"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "article_dir": os.path.join(data_dir, f"{self.config.name}/test"),
                    "split": "test",
                },
            ),
        ]
        if self.config.name == "canonical":
            split_generators.append(
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "article_dir": os.path.join(data_dir, f"{self.config.name}/train"),
                        "split": "train",
                    },
                )
            )
        return split_generators

    def _generate_examples(self, article_dir, split):
        detokenizers = [
            [re.compile(r"([Ll])iputan6 . com "), r"\1iputan6.com"],
            [re.compile(r" ([.,:])"), r"\1"],
            [re.compile(r"\( ([^)]+) \)"), r"(\1)"],
            [re.compile(r"\" ([^\"]+) \""), r'"\1"'],
            [re.compile(r"\[ ([^]]+) ]"), r"[\1]"],
        ]
        logger.info("⏳ Generating %s examples from = %s", split, article_dir)
        guid = 0
        for path in sorted(
            glob.glob(os.path.join(article_dir, "**/*.json"), recursive=True), key=lambda p: int(Path(p).stem)
        ):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                clean_article = " ".join([" ".join(i) for i in data["clean_article"]])
                for d in detokenizers:
                    clean_article = d[0].sub(d[1], clean_article)
                clean_summary = " ".join([" ".join(i) for i in data["clean_summary"]])
                for d in detokenizers:
                    clean_summary = d[0].sub(d[1], clean_summary)
                extractive_summary = " ".join([" ".join(data["clean_article"][i]) for i in data["extractive_summary"]])
                for d in detokenizers:
                    extractive_summary = d[0].sub(d[1], extractive_summary)
                yield guid, {
                    "id": str(data["id"]),
                    "url": data["url"],
                    "clean_article": clean_article,
                    "clean_summary": clean_summary,
                    "extractive_summary": extractive_summary,
                }
            guid += 1
