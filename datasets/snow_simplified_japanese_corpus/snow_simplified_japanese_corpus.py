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
"""SNOW T15 and T23: "Japanese Simplified Corpus with Core Vocabulary" and ''Crowdsourced Corpus of Sentence Simplification with Core Vocabulary"."""


import openpyxl  # noqa: requires this pandas optional dependency for reading xlsx files
import pandas as pd

import datasets


_CITATION = """\
@inproceedings{maruyama-yamamoto-2018-simplified,
    title = "Simplified Corpus with Core Vocabulary",
    author = "Maruyama, Takumi  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L18-1185",
}

@inproceedings{yamamoto-2017-simplified-japanese,
    title = "やさしい⽇本語対訳コーパスの構築",
    author = "⼭本 和英  and
      丸⼭ 拓海  and
      ⾓張 ⻯晴  and
      稲岡 夢⼈  and
      ⼩川 耀⼀朗  and
      勝⽥ 哲弘  and
      髙橋 寛治",
    booktitle = "言語処理学会第23回年次大会",
    month = 3月,
    year = "2017",
    address = "茨城, 日本",
    publisher = "言語処理学会",
    url = "https://www.anlp.jp/proceedings/annual_meeting/2017/pdf_dir/B5-1.pdf",
}

@inproceedings{katsuta-yamamoto-2018-crowdsourced,
    title = "Crowdsourced Corpus of Sentence Simplification with Core Vocabulary",
    author = "Katsuta, Akihiro  and
      Yamamoto, Kazuhide",
    booktitle = "Proceedings of the Eleventh International Conference on Language Resources and Evaluation ({LREC} 2018)",
    month = may,
    year = "2018",
    address = "Miyazaki, Japan",
    publisher = "European Language Resources Association (ELRA)",
    url = "https://www.aclweb.org/anthology/L18-1072",
}
"""

_DESCRIPTION = """\
About SNOW T15: \
The simplified corpus for the Japanese language. The corpus has 50,000 manually simplified and aligned sentences. \
This corpus contains the original sentences, simplified sentences and English translation of the original sentences. \
It can be used for automatic text simplification as well as translating simple Japanese into English and vice-versa. \
The core vocabulary is restricted to 2,000 words where it is selected by accounting for several factors such as meaning preservation, variation, simplicity and the UniDic word segmentation criterion.
For details, refer to the explanation page of Japanese simplification (http://www.jnlp.org/research/Japanese_simplification). \
The original texts are from "small_parallel_enja: 50k En/Ja Parallel Corpus for Testing SMT Methods", which is a bilingual corpus for machine translation. \
\
About SNOW T23: \
An expansion corpus of 35,000 sentences rewritten in easy Japanese (simple Japanese vocabulary) based on SNOW T15. \
The original texts are from "Tanaka Corpus" (http://www.edrdg.org/wiki/index.php/Tanaka_Corpus).
"""

_HOMEPAGE = "http://www.jnlp.org/SNOW/T15, http://www.jnlp.org/SNOW/T23"

_LICENSE = "CC BY 4.0"

# The HuggingFace dataset library don't host the datasets but only point to the original files
_URLs = {
    "snow_t15": "https://filedn.com/lit4DCIlHwxfS1gj9zcYuDJ/SNOW/T15-2020.1.7.xlsx",
    "snow_t23": "https://filedn.com/lit4DCIlHwxfS1gj9zcYuDJ/SNOW/T23-2020.1.7.xlsx",
}


class SnowSimplifiedJapaneseCorpus(datasets.GeneratorBasedBuilder):
    """SNOW T15 and T23: "Japanese Simplified Corpus with Core Vocabulary" and ''Crowdsourced Corpus of Sentence Simplification with Core Vocabulary"."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="snow_t15", version=VERSION, description="SNOW T15 dataset"),
        datasets.BuilderConfig(name="snow_t23", version=VERSION, description="SNOW T23 dataset (extension)"),
    ]

    DEFAULT_CONFIG_NAME = "snow_t15"

    def _info(self):
        if self.config.name == "snow_t15":
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "original_ja": datasets.Value("string"),
                    "simplified_ja": datasets.Value("string"),
                    "original_en": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "ID": datasets.Value("string"),
                    "original_ja": datasets.Value("string"),
                    "simplified_ja": datasets.Value("string"),
                    "original_en": datasets.Value("string"),
                    "proper_noun": datasets.Value("string"),
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
        """Returns SplitGenerators."""

        my_urls = _URLs[self.config.name]
        data_url = dl_manager.download(my_urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": data_url, "split": "train"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, "rb") as f:
            df = pd.read_excel(f, engine="openpyxl").astype("str")

            if self.config.name == "snow_t15":
                for id_, row in df.iterrows():
                    yield id_, {
                        "ID": row["ID"],
                        "original_ja": row["#日本語(原文)"],
                        "simplified_ja": row["#やさしい日本語"],
                        "original_en": row["#英語(原文)"],
                    }
            else:
                for id_, row in df.iterrows():
                    yield id_, {
                        "ID": row["ID"],
                        "original_ja": row["#日本語(原文)"],
                        "simplified_ja": row["#やさしい日本語"],
                        "original_en": row["#英語(原文)"],
                        "proper_noun": row["#固有名詞"],
                    }
