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
"""Introduction to the CoNLL-2000 Shared Task: Chunking"""

import logging

import datasets


_CITATION = """\
@inproceedings{tksbuchholz2000conll,
   author     = "Tjong Kim Sang, Erik F. and Sabine Buchholz",
   title      = "Introduction to the CoNLL-2000 Shared Task: Chunking",
   editor     = "Claire Cardie and Walter Daelemans and Claire
                 Nedellec and Tjong Kim Sang, Erik",
   booktitle  = "Proceedings of CoNLL-2000 and LLL-2000",
   publisher  = "Lisbon, Portugal",
   pages      = "127--132",
   year       = "2000"
}
"""

_DESCRIPTION = """\
 Text chunking consists of dividing a text in syntactically correlated parts of words. For example, the sentence
 He reckons the current account deficit will narrow to only # 1.8 billion in September . can be divided as follows:
[NP He ] [VP reckons ] [NP the current account deficit ] [VP will narrow ] [PP to ] [NP only # 1.8 billion ]
[PP in ] [NP September ] .

Text chunking is an intermediate step towards full parsing. It was the shared task for CoNLL-2000. Training and test
data for this task is available. This data consists of the same partitions of the Wall Street Journal corpus (WSJ)
as the widely used data for noun phrase chunking: sections 15-18 as training data (211727 tokens) and section 20 as
test data (47377 tokens). The annotation of the data has been derived from the WSJ corpus by a program written by
Sabine Buchholz from Tilburg University, The Netherlands.
"""

_URL = "https://github.com/teropa/nlp/raw/master/resources/corpora/conll2000/"
_TRAINING_FILE = "train.txt"
_TEST_FILE = "test.txt"


class Conll2000Config(datasets.BuilderConfig):
    """BuilderConfig for Conll2000"""

    def __init__(self, **kwargs):
        """BuilderConfig forConll2000.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Conll2000Config, self).__init__(**kwargs)


class Conll2000(datasets.GeneratorBasedBuilder):
    """Conll2000 dataset."""

    BUILDER_CONFIGS = [
        Conll2000Config(name="conll2000", version=datasets.Version("1.0.0"), description="Conll2000 dataset"),
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
                                "MD",
                                "NN",
                                "NNP",
                                "NNPS",
                                "NNS",
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
                }
            ),
            supervised_keys=None,
            homepage="https://www.clips.uantwerpen.be/conll2000/chunking/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_TRAINING_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            pos_tags = []
            chunk_tags = []
            for line in f:
                if line == "" or line == "\n":
                    if tokens:
                        yield guid, {"id": str(guid), "tokens": tokens, "pos_tags": pos_tags, "chunk_tags": chunk_tags}
                        guid += 1
                        tokens = []
                        pos_tags = []
                        chunk_tags = []
                else:
                    # conll2000 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    pos_tags.append(splits[1])
                    chunk_tags.append(splits[2].rstrip())
            # last example
            yield guid, {"id": str(guid), "tokens": tokens, "pos_tags": pos_tags, "chunk_tags": chunk_tags}
