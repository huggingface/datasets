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
"""Korean named entity recognition dataset"""


import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@InProceedings{Kim:2016,
  title     = "Korean Named Entity Recognition Dataset",
  authors   = "Jae-Hoon Kim",
  publisher = "GitHub",
  year      = "2016"
}
"""


_DESCRIPTION = """\
Korean named entity recognition dataset
"""

_HOMEPAGE = "https://github.com/kmounlp/NER"

_LICENSE = "NER License, MIT License for non-commercial use"

_URL = "https://raw.githubusercontent.com/kmounlp/NER/master/2016klp/ner."
_URLs = {key: _URL + key for key in ("train", "test", "dev")}


class KorNER(datasets.GeneratorBasedBuilder):
    """Korean Named entity recognition dataset"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "annot_text": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "SO",
                                "SS",
                                "VV",
                                "XR",
                                "VCP",
                                "JC",
                                "VCN",
                                "JKB",
                                "MM",
                                "SP",
                                "XSN",
                                "SL",
                                "NNP",
                                "NP",
                                "EP",
                                "JKQ",
                                "IC",
                                "XSA",
                                "EC",
                                "EF",
                                "SE",
                                "XPN",
                                "ETN",
                                "SH",
                                "XSV",
                                "MAG",
                                "SW",
                                "ETM",
                                "JKO",
                                "NNB",
                                "MAJ",
                                "NNG",
                                "JKV",
                                "JKC",
                                "VA",
                                "NR",
                                "JKG",
                                "VX",
                                "SF",
                                "JX",
                                "JKS",
                                "SN",
                            ]
                        )
                    ),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(names=["I", "O", "B_OG", "B_TI", "B_LC", "B_DT", "B_PS"])
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": downloaded_files["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": downloaded_files["test"],
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_files["dev"],
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            text = ""
            annot_text = ""
            tokens = []
            pos_tags = []
            ner_tags = []
            for id_, row in enumerate(f):
                row = row.strip()
                if not row:
                    yield id_, {
                        "text": text,
                        "annot_text": annot_text,
                        "tokens": tokens,
                        "pos_tags": pos_tags,
                        "ner_tags": ner_tags,
                    }
                    tokens.clear()
                    pos_tags.clear()
                    ner_tags.clear()
                    continue
                if row[0] == ";":
                    text = row[2:]
                elif row[0] == "$":
                    annot_text = row[1:]
                else:
                    _, token, pos_tag, ner_tag = row.split("\t")
                    tokens.append(token)
                    pos_tags.append(pos_tag)
                    ner_tags.append(ner_tag)
