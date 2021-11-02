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
"""BIOSSES: A Benchmark Dataset for Biomedical Sentence Similarity Estimation"""


import pandas as pd

import datasets


_CITATION = """\
@article{souganciouglu2017biosses,
  title={BIOSSES: a semantic sentence similarity estimation system for the biomedical domain},
  author={So{\\u{g}}anc{\\i}o{\\u{g}}lu, Gizem and {\\"O}zt{\\"u}rk, Hakime and {\\"O}zg{\\"u}r, Arzucan},
  journal={Bioinformatics},
  volume={33},
  number={14},
  pages={i49--i58},
  year={2017},
  publisher={Oxford University Press}
}
"""


_DESCRIPTION = """\
BIOSSES is a benchmark dataset for biomedical sentence similarity estimation. The dataset comprises 100 sentence pairs, in which each sentence was selected from the TAC (Text Analysis Conference) Biomedical Summarization Track Training Dataset containing articles from the biomedical domain. The sentence pairs were evaluated by five different human experts that judged their similarity and gave scores ranging from 0 (no relation) to 4 (equivalent).
"""


_LICENSE = """\
BIOSSES is made available under the terms of The GNU Common Public License v.3.0.
"""


_URL = "https://tabilab.cmpe.boun.edu.tr/BIOSSES/DataSet.html"


_DATA_URL = "https://raw.githubusercontent.com/Markus-Zlabinger/ssts/fce78a649ab90269950aaf44ce20a36e94409392/data/biosses/all.tsv"


class BiossesConfig(datasets.BuilderConfig):
    """BuilderConfig for BIOSSES"""

    def __init__(self, **kwargs):
        """
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(BiossesConfig, self).__init__(**kwargs)


class Biosses(datasets.GeneratorBasedBuilder):
    """BIOSSES: A Benchmark Dataset for Biomedical Sentence Similarity Estimation"""

    def _info(self):
        features = datasets.Features(
            {
                "sentence1": datasets.Value("string"),
                "sentence2": datasets.Value("string"),
                "score": datasets.Value("float32"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_URL,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        downloaded_file = dl_manager.download_and_extract(_DATA_URL)
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_file})]

    def _generate_examples(self, filepath):
        """Yields examples as (key, example) tuples."""

        df = pd.read_csv(filepath, sep="\t", encoding="utf-8")
        for idx, row in df.iterrows():
            yield idx, {
                "sentence1": row["sentence1"],
                "sentence2": row["sentence2"],
                "score": row["score"],
            }
