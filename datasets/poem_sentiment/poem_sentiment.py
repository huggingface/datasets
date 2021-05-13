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
"""Poem Sentiment: A sentiment dataset of poem verses"""


import datasets


_CITATION = """\
@misc{sheng2020investigating,
      title={Investigating Societal Biases in a Poetry Composition System},
      author={Emily Sheng and David Uthus},
      year={2020},
      eprint={2011.02686},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
Poem Sentiment is a sentiment dataset of poem verses from Project Gutenberg. \
This dataset can be used for tasks such as sentiment classification or style transfer for poems.
"""


_HOMEPAGE = "https://github.com/google-research-datasets/poem-sentiment"

_BASE_URL = "https://raw.githubusercontent.com/google-research-datasets/poem-sentiment/master/data/"
_URLS = {
    "train": f"{_BASE_URL}/train.tsv",
    "dev": f"{_BASE_URL}/dev.tsv",
    "test": f"{_BASE_URL}/test.tsv",
}
_LABEL_MAPPING = {-1: 0, 0: 2, 1: 1, 2: 3}


class PoemSentiment(datasets.GeneratorBasedBuilder):
    """Poem Sentiment: A sentiment dataset of poem verses"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("int32"),
                    "verse_text": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["negative", "positive", "no_impact", "mixed"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        downloaded_files = dl_manager.download(_URLS)
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                fields = line.strip().split("\t")
                idx, verse_text, label = fields
                label = _LABEL_MAPPING[int(label)]
                yield int(idx), {"id": int(idx), "verse_text": verse_text, "label": label}
