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
"""Multi-XScience Dataset."""

from __future__ import absolute_import, division, print_function

import json

import datasets


_CITATION = """
@article{lu2020multi,
  title={Multi-XScience: A Large-scale Dataset for Extreme Multi-document Summarization of Scientific Articles},
  author={Lu, Yao and Dong, Yue and Charlin, Laurent},
  journal={arXiv preprint arXiv:2010.14235},
  year={2020}
}
"""

_DESCRIPTION = """
Multi-XScience, a large-scale multi-document summarization dataset created from scientific articles. Multi-XScience introduces a challenging multi-document summarization task: writing the related-work section of a paper based on its abstract and the articles it references.
"""

_URL_TRAIN = "https://raw.githubusercontent.com/yaolu/Multi-XScience/master/data/train.json.gz"
_URL_TEST = "https://raw.githubusercontent.com/yaolu/Multi-XScience/master/data/test.json.gz"
_URL_VAL = "https://raw.githubusercontent.com/yaolu/Multi-XScience/master/data/val.json.gz"


class MultiXScienceSum(datasets.GeneratorBasedBuilder):
    """"Multi-XScience Dataset."""

    VERSION = datasets.Version("1.1.0")

    def _info(selif):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "aid": datasets.Value("string"),
                    "mid": datasets.Value("string"),
                    "abstract": datasets.Value("string"),
                    "related_work": datasets.Value("string"),
                    "ref_abstract": datasets.Sequence(
                        {
                            "cite_N": datasets.Value("string"),
                            "mid": datasets.Value("string"),
                            "abstract": datasets.Value("string"),
                        },
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/yaolu/Multi-XScience",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_URL_TRAIN)
        test_path = dl_manager.download_and_extract(_URL_TEST)
        val_path = dl_manager.download_and_extract(_URL_VAL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"path": train_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"path": test_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"path": val_path},
            ),
        ]

    def _generate_examples(self, path=None):
        """Yields examples."""
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            f.close()

        for idx, el in enumerate(data):
            cite_n = list(el["ref_abstract"].keys())
            cite_n_mid = [el["ref_abstract"][cite]["mid"] for cite in cite_n]
            cite_n_abstract = [el["ref_abstract"][cite]["abstract"] for cite in cite_n]
            tmp = {"cite_N": cite_n, "mid": cite_n_mid, "abstract": cite_n_abstract}
            d = el.copy()
            d["ref_abstract"] = tmp
            yield idx, d
