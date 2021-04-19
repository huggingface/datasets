# coding=utf-8
# Copyright 2020 HuggingFace Datasets Authors.
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
"""CrossWeigh: Training Named Entity Tagger from Imperfect Annotations"""

import logging

import datasets


_CITATION = """\
@inproceedings{wang2019crossweigh,
  title={CrossWeigh: Training Named Entity Tagger from Imperfect Annotations},
  author={Wang, Zihan and Shang, Jingbo and Liu, Liyuan and Lu, Lihao and Liu, Jiacheng and Han, Jiawei},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)},
  pages={5157--5166},
  year={2019}
}
"""

_DESCRIPTION = """\
CoNLLpp is a corrected version of the CoNLL2003 NER dataset where labels of 5.38% of the sentences in the test set
have been manually corrected. The training set and development set are included for completeness.
For more details see https://www.aclweb.org/anthology/D19-1519/ and https://github.com/ZihanWangKi/CrossWeigh
"""

_URL = "https://github.com/ZihanWangKi/CrossWeigh/raw/master/data/"
_TRAINING_FILE = "conllpp_train.txt"
_DEV_FILE = "conllpp_dev.txt"
_TEST_FILE = "conllpp_test.txt"


class ConllppConfig(datasets.BuilderConfig):
    """BuilderConfig for Conll2003"""

    def __init__(self, **kwargs):
        """BuilderConfig forConll2003.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ConllppConfig, self).__init__(**kwargs)


class Conllpp(datasets.GeneratorBasedBuilder):
    """Conllpp dataset."""

    BUILDER_CONFIGS = [
        ConllppConfig(name="conllpp", version=datasets.Version("1.0.0"), description="Conllpp dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
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
                    "chunk_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-ADJP",
                                "I-ADJP",
                                "B-ADVP",
                                "I-ADVP",
                                "B-CONJP",
                                "I-CONJP",
                                "B-INTJ",
                                "I-INTJ",
                                "B-LST",
                                "I-LST",
                                "B-NP",
                                "I-NP",
                                "B-PP",
                                "I-PP",
                                "B-PRT",
                                "I-PRT",
                                "B-SBAR",
                                "I-SBAR",
                                "B-UCP",
                                "I-UCP",
                                "B-VP",
                                "I-VP",
                            ]
                        )
                    ),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-MISC",
                                "I-MISC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/ZihanWangKi/CrossWeigh",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            pos_tags = []
            chunk_tags = []
            ner_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "pos_tags": pos_tags,
                            "chunk_tags": chunk_tags,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        pos_tags = []
                        chunk_tags = []
                        ner_tags = []
                else:
                    # conll2003 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    pos_tags.append(splits[1])
                    chunk_tags.append(splits[2])
                    ner_tags.append(splits[3].rstrip())
            # last example
            if tokens:
                yield guid, {
                    "id": str(guid),
                    "tokens": tokens,
                    "pos_tags": pos_tags,
                    "chunk_tags": chunk_tags,
                    "ner_tags": ner_tags,
                }
