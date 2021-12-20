# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors. Licensed under the Apache License, Version 2.0 (the "License");
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
"""AmericasNLI: A NLI Corpus of 10 Indigenous Low-Resource Languages."""


import csv

import datasets
from datasets.utils.download_manager import DownloadManager


_CITATION = """
@article{DBLP:journals/corr/abs-2104-08726,
  author    = {Abteen Ebrahimi and
               Manuel Mager and
               Arturo Oncevay and
               Vishrav Chaudhary and
               Luis Chiruzzo and
               Angela Fan and
               John Ortega and
               Ricardo Ramos and
               Annette Rios and
               Ivan Vladimir and
               Gustavo A. Gim{\'{e}}nez{-}Lugo and
               Elisabeth Mager and
               Graham Neubig and
               Alexis Palmer and
               Rolando A. Coto Solano and
               Ngoc Thang Vu and
               Katharina Kann},
  title     = {AmericasNLI: Evaluating Zero-shot Natural Language Understanding of
               Pretrained Multilingual Models in Truly Low-resource Languages},
  journal   = {CoRR},
  volume    = {abs/2104.08726},
  year      = {2021},
  url       = {https://arxiv.org/abs/2104.08726},
  eprinttype = {arXiv},
  eprint    = {2104.08726},
  timestamp = {Mon, 26 Apr 2021 17:25:10 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2104-08726.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
AmericasNLI is an extension of XNLI (Conneau et al., 2018) – a natural language inference (NLI) dataset covering 15 high-resource languages – to 10 low-resource indigenous languages spoken in the Americas: Ashaninka, Aymara, Bribri, Guarani, Nahuatl, Otomi, Quechua, Raramuri, Shipibo-Konibo, and Wixarika. As with MNLI, the goal is to predict textual entailment (does sentence A imply/contradict/neither sentence B) and is a classification task (given two sentences, predict one of three labels).
"""

VERSION = datasets.Version("1.0.0", "")
_DEV_DATA_URL = "https://raw.githubusercontent.com/nala-cub/AmericasNLI/main/dev.tsv"
_TEST_DATA_URL = "https://raw.githubusercontent.com/nala-cub/AmericasNLI/main/test.tsv"

_LANGUAGES = ("aym", "bzd", "cni", "gn", "hch", "nah", "oto", "quy", "shp", "tar")


class AmericasNLIConfig(datasets.BuilderConfig):
    """BuilderConfig for AmericasNLI."""

    def __init__(self, language: str, languages=None, **kwargs):
        """BuilderConfig for AmericasNLI.

        Args:
        language: One of aym, bzd, cni, gn, hch, nah, oto, quy, shp, tar or all_languages
          **kwargs: keyword arguments forwarded to super.
        """
        super(AmericasNLIConfig, self).__init__(**kwargs)
        self.language = language
        if language != "all_languages":
            self.languages = [language]
        else:
            self.languages = languages if languages is not None else _LANGUAGES


class AmericasNLI(datasets.GeneratorBasedBuilder):
    """TODO"""

    VERSION = VERSION
    BUILDER_CONFIG_CLASS = AmericasNLIConfig
    BUILDER_CONFIGS = [
        AmericasNLIConfig(
            name=lang,
            language=lang,
            version=VERSION,
            description=f"Plain text import of AmericasNLI for the {lang} language",
        )
        for lang in _LANGUAGES
    ] + [
        AmericasNLIConfig(
            name="all_languages",
            language="all_languages",
            version=VERSION,
            description="Plain text import of AmericasNLI for all languages",
        )
    ]

    def _info(self):
        if self.config.language == "all_languages":
            features = datasets.Features(
                {
                    "language": datasets.Value("string"),
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                }
            )
        else:
            features = datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://github.com/nala-cub/AmericasNLI",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: DownloadManager):
        dl_paths = dl_manager.download(
            {
                "dev_data": _DEV_DATA_URL,
                "test_data": _TEST_DATA_URL,
            }
        )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": dl_paths["dev_data"],
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": dl_paths["test_data"],
                },
            ),
        ]

    def _generate_examples(self, filepath: str):
        """This function returns the examples in the raw (text) form."""
        idx = 0
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in reader:
                if row["language"] == self.config.language:
                    yield idx, {
                        "premise": row["premise"],
                        "hypothesis": row["hypothesis"],
                        "label": row["label"],
                    }
                    idx += 1
                elif self.config.language == "all_languages":
                    yield idx, {
                        "language": row["language"],
                        "premise": row["premise"],
                        "hypothesis": row["hypothesis"],
                        "label": row["label"],
                    }
                    idx += 1
