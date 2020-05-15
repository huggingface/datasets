# coding=utf-8
# Copyright 2020 HuggingFace NLP Authors.
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
"""The GermEval 2014 NER Shared Task dataset."""

from __future__ import absolute_import, division, print_function

import csv
import glob
import logging
import os
from pathlib import Path

import nlp


_CITATION = """\
@inproceedings{benikova-etal-2014-nosta,
    title = "{N}o{S}ta-D Named Entity Annotation for {G}erman: Guidelines and Dataset",
    author = "Benikova, Darina  and
      Biemann, Chris  and
      Reznicek, Marc",
    booktitle = "Proceedings of the Ninth International Conference on Language Resources and Evaluation ({LREC}'14)",
    month = may,
    year = "2014",
    address = "Reykjavik, Iceland",
    publisher = "European Language Resources Association (ELRA)",
    url = "http://www.lrec-conf.org/proceedings/lrec2014/pdf/276_Paper.pdf",
    pages = "2524--2531",
}
"""

_DESCRIPTION = """\
The GermEval 2014 NER Shared Task builds on a new dataset with German Named Entity annotation with the following properties:\
    - The data was sampled from German Wikipedia and News Corpora as a collection of citations.\
    - The dataset covers over 31,000 sentences corresponding to over 590,000 tokens.\
    - The NER annotation uses the NoSta-D guidelines, which extend the Tübingen Treebank guidelines,\
      using four main NER categories with sub-structure, and annotating embeddings among NEs\
      such as [ORG FC Kickers [LOC Darmstadt]].
"""

_URL = "https://sites.google.com/site/germeval2014ner/data/"
_TRAINING_FILE = "NER-de-train.tsv"
_DEV_FILE = "NER-de-dev.tsv"
_TEST_FILE = "NER-de-test.tsv"


class GermEval14Config(nlp.BuilderConfig):
    """BuilderConfig for GermEval 2014."""

    def __init__(self, **kwargs):
        """BuilderConfig for GermEval 2014.

    Args:
      **kwargs: keyword arguments forwarded to super.
    """
        super(GermEval14Config, self).__init__(**kwargs)


class GermEval14(nlp.GeneratorBasedBuilder):
    """GermEval 2014 NER Shared Task dataset."""

    BUILDER_CONFIGS = [
        GermEval14Config(
            name="germeval_14", version=nlp.Version("1.0.0"), description="GermEval 2014 NER Shared Task dataset"
        ),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "id": nlp.Value("string"),
                    "source": nlp.Value("string"),
                    "tokens": nlp.Sequence(nlp.Value("string")),
                    "labels": nlp.Sequence(nlp.Value("string")),
                    "nested-labels": nlp.Sequence(nlp.Value("string")),
                }
            ),
            supervised_keys=None,
            homepage="https://sites.google.com/site/germeval2014ner/",
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
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            nlp.SplitGenerator(name=nlp.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            nlp.SplitGenerator(name=nlp.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath) as f:
            data = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            current_source = ""
            current_tokens = []
            current_labels = []
            current_nested_labels = []
            sentence_counter = 0
            for row in data:
                if row:
                    if row[0] == "#":
                        current_source = " ".join(row[1:])
                        continue
                    id_, token, label, nested_label = row[:4]
                    current_tokens.append(token)
                    current_labels.append(label)
                    current_nested_labels.append(nested_label)
                else:
                    # New sentence
                    if not current_tokens:
                        # Consecutive empty lines will cause empty sentences
                        continue
                    assert len(current_tokens) == len(current_labels), "💔 between len of tokens & labels"
                    assert len(current_labels) == len(current_nested_labels), "💔 between len of labels & nested labels"
                    assert current_source, "💥 Source for new sentence was not set"
                    sentence = (
                        sentence_counter,
                        {
                            "id": str(sentence_counter),
                            "tokens": current_tokens,
                            "labels": current_labels,
                            "nested-labels": current_nested_labels,
                            "source": current_source,
                        },
                    )
                    sentence_counter += 1
                    current_tokens = []
                    current_labels = []
                    current_nested_labels = []
                    current_source = ""
                    yield sentence
            # Don't forget last sentence in dataset 🧐
            yield sentence_counter, {
                "id": str(sentence_counter),
                "tokens": current_tokens,
                "labels": current_labels,
                "nested-labels": current_nested_labels,
                "source": current_source,
            }
