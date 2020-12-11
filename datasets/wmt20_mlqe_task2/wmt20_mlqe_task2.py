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
"""WMT20 MLQE Shared task 2."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """
Not available.
"""

_DESCRIPTION = """\
This shared task (part of WMT20) will build on its previous editions
to further examine automatic methods for estimating the quality
of neural machine translation output at run-time, without relying
on reference translations. As in previous years, we cover estimation
at various levels. Important elements introduced this year include: a new
task where sentences are annotated with Direct Assessment (DA)
scores instead of labels based on post-editing; a new multilingual
sentence-level dataset mainly from Wikipedia articles, where the
source articles can be retrieved for document-wide context; the
availability of NMT models to explore system-internal information for the task.

Task 2 evaluates the application of QE for post-editing purposes. It consists of predicting:
- A/ Word-level tags. This is done both on source side (to detect which words caused errors)
and target side (to detect mistranslated or missing words).
  - A1/ Each token is tagged as either `OK` or `BAD`. Additionally,
  each gap between two words is tagged as `BAD` if one or more
  missing words should have been there, and `OK` otherwise. Note
  that number of tags for each target sentence is 2*N+1, where
  N is the number of tokens in the sentence.
  - A2/ Tokens are tagged as `OK` if they were correctly
  translated, and `BAD` otherwise. Gaps are not tagged.
- B/ Sentence-level HTER scores. HTER (Human Translation Error Rate)
is the ratio between the number of edits (insertions/deletions/replacements)
needed and the reference translation length.
"""

_HOMEPAGE = "http://www.statmt.org/wmt20/quality-estimation-task.html"

_LICENSE = "Unknown"

_LANGUAGE_PAIRS = [
    ("en", "de"),
    ("en", "zh"),
]
_MAIN_URL = "https://github.com/deep-spin/deep-spin.github.io/raw/master/docs/data/wmt2020_qe"


def inject_to_link(src_lg, tgt_lg):
    links = {
        "train+dev": f"{_MAIN_URL}/qe-{src_lg}{tgt_lg}-traindev.tar.gz",
        "test": f"{_MAIN_URL}/qe-{src_lg}{tgt_lg}-blindtest.tar.gz",
    }
    return links


_URLs = {f"{src_lg}-{tgt_lg}": inject_to_link(src_lg, tgt_lg) for (src_lg, tgt_lg) in _LANGUAGE_PAIRS}


class WmtMlqeConfig(datasets.BuilderConfig):
    def __init__(self, src_lg, tgt_lg, **kwargs):
        super(WmtMlqeConfig, self).__init__(**kwargs)
        self.src_lg = src_lg
        self.tgt_lg = tgt_lg


class Wmt20MlqeTask2(datasets.GeneratorBasedBuilder):
    """WMT MLQE Shared task 2."""

    BUILDER_CONFIGS = [
        WmtMlqeConfig(
            name=f"{src_lg}-{tgt_lg}",
            version=datasets.Version("1.1.0"),
            description=f"Task 2: {src_lg} - {tgt_lg}",
            src_lg=src_lg,
            tgt_lg=tgt_lg,
        )
        for (src_lg, tgt_lg) in _LANGUAGE_PAIRS
    ]
    BUILDER_CONFIG_CLASS = WmtMlqeConfig

    def _info(self):
        features = datasets.Features(
            {
                "translation": datasets.Translation(languages=(self.config.src_lg, self.config.tgt_lg)),
                "src_tags": datasets.Sequence(datasets.ClassLabel(names=["BAD", "OK"])),
                "mt_tags": datasets.Sequence(datasets.ClassLabel(names=["BAD", "OK"])),
                "pe": datasets.Value("string"),
                "hter": datasets.Value("float32"),
                "alignments": datasets.Sequence(datasets.Sequence(datasets.Value("int32"))),
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
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir["train+dev"], f"{self.config.src_lg}-{self.config.tgt_lg}", "train"
                    ),
                    "split": "train",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir["test"], f"{self.config.src_lg}-{self.config.tgt_lg}", "test-blind"
                    ),
                    "split": "test",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(
                        data_dir["train+dev"], f"{self.config.src_lg}-{self.config.tgt_lg}", "dev"
                    ),
                    "split": "dev",
                    "source_lg": self.config.src_lg,
                    "target_lg": self.config.tgt_lg,
                },
            ),
        ]

    def _generate_examples(self, filepath, split, source_lg, target_lg):
        """ Yields examples. """

        def open_and_read(fp):
            with open(fp, encoding="utf-8") as f:
                return f.read().splitlines()

        srcs = open_and_read(os.path.join(filepath, f"{split}.src"))
        mts = open_and_read(os.path.join(filepath, f"{split}.mt"))
        alignments = [
            [idx_.split("-") for idx_ in t.split(" ")]
            for t in open_and_read(os.path.join(filepath, f"{split}.src-mt.alignments"))
        ]

        if split != "test":
            src_tags = [t.split(" ") for t in open_and_read(os.path.join(filepath, f"{split}.source_tags"))]
            mt_tags = [t.split(" ") for t in open_and_read(os.path.join(filepath, f"{split}.tags"))]
            pes = open_and_read(os.path.join(filepath, f"{split}.pe"))
            hters = open_and_read(os.path.join(filepath, f"{split}.hter"))
        else:
            src_tags = [[]] * len(srcs)
            mt_tags = [[]] * len(srcs)
            pes = [""] * len(srcs)
            hters = [-10_000] * len(srcs)

        for id_, (src_, src_tags_, mt_, mt_tags_, pe_, hter_, alignments_) in enumerate(
            zip(srcs, src_tags, mts, mt_tags, pes, hters, alignments)
        ):
            yield id_, {
                "translation": {source_lg: src_, target_lg: mt_},
                "src_tags": src_tags_,
                "mt_tags": mt_tags_,
                "pe": pe_,
                "hter": hter_,
                "alignments": alignments_,
            }
