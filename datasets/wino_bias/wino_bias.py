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
"""WinoBias: Winograd-schema dataset for detecting gender bias"""

from __future__ import absolute_import, division, print_function

import csv
import json
import os

import datasets


_CITATION = """\
@article{DBLP:journals/corr/abs-1804-06876,
  author    = {Jieyu Zhao and
               Tianlu Wang and
               Mark Yatskar and
               Vicente Ordonez and
               Kai{-}Wei Chang},
  title     = {Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods},
  journal   = {CoRR},
  volume    = {abs/1804.06876},
  year      = {2018},
  url       = {http://arxiv.org/abs/1804.06876},
  archivePrefix = {arXiv},
  eprint    = {1804.06876},
  timestamp = {Mon, 13 Aug 2018 16:47:01 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-1804-06876.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

_DESCRIPTION = """\
WinoBias, a Winograd-schema dataset for coreference resolution focused on gender bias. 
The corpus contains Winograd-schema style sentences with entities corresponding to people
referred by their occupation (e.g. the nurse, the doctor, the carpenter).
"""

_HOMEPAGE = "https://uclanlp.github.io/corefBias/overview"

_LICENSE = "MIT License (https://github.com/uclanlp/corefBias/blob/master/LICENSE)"

_URLs = {
    "https://drive.google.com/uc?export=download&confirm=yLNb&id=14Im3BnNl-d2fYETYmiH5yq6eFGLVC3g0"
}


class WinoBias(datasets.GeneratorBasedBuilder):
    """WinoBias: Winograd-schema dataset for detecting gender bias"""

    VERSION = datasets.Version("4.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="wino_bias", version=VERSION, description="WinoBias: Winograd-schema dataset for detecting gender bias"),
    ]


    def _info(self):
        
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            # Info about features for this: http://cemantix.org/data/ontonotes.html
            features= datasets.Features(
                {
                    "document_id": datasets.Value("string"),
                    "part_number": datasets.Value("int64"),
                    "word_number": datasets.Value("int64"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                '"',
                                "''",
                                "#",
                                "$",
                                "(",
                                ")",
                                ",",
                                ".",
                                ":",
                                "``",
                                "CC",
                                "CD",
                                "DT",
                                "EX",
                                "FW",
                                "IN",
                                "JJ",
                                "JJR",
                                "JJS",
                                "LS",
                                "MD",
                                "NN",
                                "NNP",
                                "NNPS",
                                "NNS",
                                "NN|SYM",
                                "PDT",
                                "POS",
                                "PRP",
                                "PRP$",
                                "RB",
                                "RBR",
                                "RBS",
                                "RP",
                                "SYM",
                                "TO",
                                "UH",
                                "VB",
                                "VBD",
                                "VBG",
                                "VBN",
                                "VBP",
                                "VBZ",
                                "WDT",
                                "WP",
                                "WP$",
                                "WRB",
                            ]
                        )
                    ),
                    "parse_bit": datasets.Sequence(datasets.Value("string")),
                    "predicate_lemma": datasets.Sequence(datasets.Value("string")),
                    "predicate_framenet_id": datasets.Value("int32"),
                    "word_sense": datasets.Value("float32"),
                    "speaker": datasets.Value("string"),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "PERSON",
                                "NORP",
                                "FAC",
                                "ORG",
                                "GPE",
                                "LOC",
                                "PRODUCT",
                                "EVENT",
                                "WORK_OF_ART",
                                "LAW",
                                "LANGUAGE",
                                "DATE",
                                "TIME",
                                "PERCENT",
                                "MONEY",
                                "QUANTITY",
                                "ORDINAL",
                                "CARDINAL"
                            ]
                        )
                    ),
                    "verbal_predicates": datasets.Sequence(datasets.Value("string"))
                }
            )
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive 
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test"
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """
        # TODO: This method will receive as arguments the `gen_kwargs` defined in the previous `_split_generators` method.
        # It is in charge of opening the given file and yielding (key, example) tuples from the dataset
        # The key is not important, it's more here for legacy reason (legacy from tfds)

        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                data = json.loads(row)
                if self.config.name == "first_domain":
                    yield id_, {
                        "sentence": data["sentence"],
                        "option1": data["option1"],
                        "answer": "" if split == "test" else data["answer"],
                    }
                else:
                    yield id_, {
                        "sentence": data["sentence"],
                        "option2": data["option2"],
                        "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
                    }
