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
"""NLI-TR: The Turkish translation of SNLI and MultiNLI datasets using Amazon Translate."""

from __future__ import absolute_import, division, print_function

import codecs
import json
import os

import datasets


_CITATION = """\
@inproceedings{budur-etal-2020-data,
    title = "Data and Representation for Turkish Natural Language Inference",
    author = "Budur, Emrah and
      \"{O}zçelik, Rıza and
      G\"{u}ng\"{o}r, Tunga",
    booktitle = "Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    month = nov,
    year = "2020",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    abstract = "Large annotated datasets in NLP are overwhelmingly in English. This is an obstacle to progress in other languages. Unfortunately, obtaining new annotated resources for each task in each language would be prohibitively expensive. At the same time, commercial machine translation systems are now robust. Can we leverage these systems to translate English-language datasets automatically? In this paper, we offer a positive response for natural language inference (NLI) in Turkish. We translated two large English NLI datasets into Turkish and had a team of experts validate their translation quality and fidelity to the original labels. Using these datasets, we address core issues of representation for Turkish NLI. We find that in-language embeddings are essential and that morphological parsing can be avoided where the training set is large. Finally, we show that models trained on our machine-translated datasets are successful on human-translated evaluation sets. We share all code, models, and data publicly.",
}
"""

_DESCRIPTION = """\
The Natural Language Inference in Turkish (NLI-TR) is a set of two large scale datasets that were obtained by translating the foundational NLI corpora (SNLI and MNLI) using Amazon Translate.
"""

_HOMEPAGE = "https://github.com/boun-tabi/NLI-TR"


class NLITRConfig(datasets.BuilderConfig):
    """ BuilderConfig for NLI-TR"""

    def __init__(self, version=None, data_url=None, **kwargs):
        super(NLITRConfig, self).__init__(version=datasets.Version(version, ""), **kwargs)
        self.data_url = data_url


class NliTr(datasets.GeneratorBasedBuilder):
    """NLI-TR: The Turkish translation of SNLI and MultiNLI datasets using Amazon Translate."""

    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIG_CLASS = NLITRConfig
    BUILDER_CONFIGS = [
        NLITRConfig(
            name="snli_tr",
            version="1.0.0",
            data_url="https://tabilab.cmpe.boun.edu.tr/datasets/nli_datasets/snli_tr_1.0.zip",
        ),
        NLITRConfig(
            name="multinli_tr",
            version="1.0.0",
            data_url="https://tabilab.cmpe.boun.edu.tr/datasets/nli_datasets/multinli_tr_1.0.zip",
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "idx": datasets.Value("int32"),
                "premise": datasets.Value("string"),
                "hypothesis": datasets.Value("string"),
                "label": datasets.features.ClassLabel(names=["entailment", "neutral", "contradiction"]),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(features),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        dl_dir = dl_manager.download_and_extract(self.config.data_url)
        data_dir = os.path.join(dl_dir)

        if self.config.name == "multinli_tr":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multinli_tr_1.0_train.jsonl"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name="validation_matched",
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multinli_tr_1.0_dev_matched.jsonl"),
                        "split": "dev",
                    },
                ),
                datasets.SplitGenerator(
                    name="validation_mismatched",
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "multinli_tr_1.0_dev_mismatched.jsonl"),
                        "split": "dev",
                    },
                ),
            ]

        if self.config.name == "snli_tr":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "snli_tr_1.0_train.jsonl"),
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "snli_tr_1.0_dev.jsonl"),
                        "split": "validation",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "snli_tr_1.0_test.jsonl"),
                        "split": "test",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with codecs.open(filepath, encoding="utf-8") as f:
            for idx, row in enumerate(f):
                data = json.loads(row)
                example = {"idx": idx, "premise": data["sentence1"], "hypothesis": data["sentence2"]}

                if "gold_label" in data:
                    if data["gold_label"] != "-":
                        example["label"] = data["gold_label"]
                    else:
                        example["label"] = -1

                yield idx, example
