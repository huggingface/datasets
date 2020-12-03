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
"""ChrEn: Cherokee-English Machine Translation data"""

from __future__ import absolute_import, division, print_function

import pandas as pd

import datasets


_CITATION = """\
@inproceedings{zhang2020chren,
  title={ChrEn: Cherokee-English Machine Translation for Endangered Language Revitalization},
  author={Zhang, Shiyue and Frey, Benjamin and Bansal, Mohit},
  booktitle={EMNLP2020},
  year={2020}
}
"""

_DESCRIPTION = """\
ChrEn is a Cherokee-English parallel dataset to facilitate machine translation research between Cherokee and English.
ChrEn is extremely low-resource contains 14k sentence pairs in total, split in ways that facilitate both in-domain and out-of-domain evaluation.
ChrEn also contains 5k Cherokee monolingual data to enable semi-supervised learning.
"""

_HOMEPAGE = "https://github.com/ZhangShiyue/ChrEn"

_LICENSE = ""

_URLs = {
    "monolingual_raw": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/raw/monolingual_data.xlsx",
    "parallel_raw": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/raw/parallel_data.xlsx",
    "monolingual_chr": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/chr",
    "monolingual_en5000": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/en5000",
    "monolingual_en10000": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/en10000",
    "monolingual_en20000": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/en20000",
    "monolingual_en50000": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/en50000",
    "monolingual_en100000": "https://raw.githubusercontent.com/ZhangShiyue/ChrEn/main/data/monolingual/en100000",
    "parallel_train.chr": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/train.chr",
    "parallel_train.en": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/train.en",
    "parallel_dev.chr": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/dev.chr",
    "parallel_dev.en": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/dev.en",
    "parallel_out_dev.chr": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/out_dev.chr",
    "parallel_out_dev.en": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/out_dev.en",
    "parallel_test.chr": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/test.chr",
    "parallel_test.en": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/test.en",
    "parallel_out_test.chr": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/out_test.chr",
    "parallel_out_test.en": "https://github.com/ZhangShiyue/ChrEn/raw/main/data/parallel/out_test.en",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class ChrEn(datasets.GeneratorBasedBuilder):
    """ChrEn: Cherokee-English Machine Translation data."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="monolingual_raw", version=VERSION, description="Monolingual data with metadata"),
        datasets.BuilderConfig(name="parallel_raw", version=VERSION, description="Parallel data with metadata"),
        datasets.BuilderConfig(name="monolingual", version=VERSION, description="Monolingual data text only"),
        datasets.BuilderConfig(
            name="parallel", version=VERSION, description="Parallel data text pairs only with default split"
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "parallel"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        if (
            self.config.name == "monolingual_raw"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "text_sentence": datasets.Value("string"),
                    "text_title": datasets.Value("string"),
                    "speaker": datasets.Value("string"),
                    "date": datasets.Value("int32"),
                    "type": datasets.Value("string"),
                    "dialect": datasets.Value("string"),
                }
            )
        elif (
            self.config.name == "parallel_raw"
        ):  # This is the name of the configuration selected in BUILDER_CONFIGS above
            features = datasets.Features(
                {
                    "line_number": datasets.Value("string"),  # doesn't always map to a number
                    "sentence_pair": datasets.Translation(languages=["en", "chr"]),
                    "text_title": datasets.Value("string"),
                    "speaker": datasets.Value("string"),
                    "date": datasets.Value("int32"),
                    "type": datasets.Value("string"),
                    "dialect": datasets.Value("string"),
                }
            )
        elif (
            self.config.name == "parallel"
        ):  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "sentence_pair": datasets.Translation(languages=["en", "chr"]),
                }
            )
        elif (
            self.config.name == "monolingual"
        ):  # This is an example to show how to have different features for "first_domain" and "second_domain"
            features = datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,  # Here we define them above because they are different between the two configurations
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download(_URLs)
        if self.config.name in [
            "monolingual_raw",
            "parallel_raw",
        ]:  # This is the name of the configuration selected in BUILDER_CONFIGS above
            return [
                datasets.SplitGenerator(
                    name="full",
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": "full",
                    },
                )
            ]
        elif self.config.name == "monolingual":
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": spl,
                    },
                )
                for spl in ["chr", "en5000", "en10000", "en20000", "en50000", "en100000"]
            ]
        else:
            return [
                datasets.SplitGenerator(
                    name=spl,
                    gen_kwargs={
                        "filepaths": data_dir,
                        "split": spl,
                    },
                )
                for spl in ["train", "dev", "out_dev", "test", "out_test"]
            ]

    def _generate_examples(self, filepaths, split):
        if self.config.name == "monolingual_raw":
            keys = ["text_sentence", "text_title", "speaker", "date", "type", "dialect"]
            monolingual = pd.read_excel(filepaths["monolingual_raw"])
            for id_, row in enumerate(monolingual.itertuples()):
                yield id_, dict(zip(keys, row[1:]))
        elif self.config.name == "parallel_raw":
            keys = ["line_number", "en_sent", "chr_sent", "text_title", "speaker", "date", "type", "dialect"]
            parallel = pd.read_excel(filepaths["parallel_raw"])
            for id_, row in enumerate(parallel.itertuples()):
                res = dict(zip(keys, row[1:]))
                res["sentence_pair"] = {"en": res["en_sent"], "chr": res["chr_sent"]}
                res["line_number"] = str(res["line_number"])
                del res["en_sent"]
                del res["chr_sent"]
                yield id_, res
        elif self.config.name == "monolingual":
            f = open(filepaths[f"monolingual_{split}"], encoding="utf-8")
            for id_, line in enumerate(f):
                yield id_, {"sentence": line.strip()}
        elif self.config.name == "parallel":
            fi = open(filepaths[f"parallel_{split}.en"], encoding="utf-8")
            fo = open(filepaths[f"parallel_{split}.chr"], encoding="utf-8")
            for id_, (line_en, line_chr) in enumerate(zip(fi, fo)):
                yield id_, {"sentence_pair": {"en": line_en.strip(), "chr": line_chr.strip()}}
