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
"""TED talk multilingual data set."""
from __future__ import absolute_import, division, print_function

import csv
import os

import six

import datasets


_DESCRIPTION = """\
Massively multilingual (60 language) data set derived from TED Talk transcripts.
Each record consists of parallel arrays of language and text. Missing and
incomplete translations will be filtered out.
"""

_CITATION = """\
@InProceedings{qi-EtAl:2018:N18-2,
  author    = {Qi, Ye  and  Sachan, Devendra  and  Felix, Matthieu  and  Padmanabhan, Sarguna  and  Neubig, Graham},
  title     = {When and Why Are Pre-Trained Word Embeddings Useful for Neural Machine Translation?},
  booktitle = {Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)},
  month     = {June},
  year      = {2018},
  address   = {New Orleans, Louisiana},
  publisher = {Association for Computational Linguistics},
  pages     = {529--535},
  abstract  = {The performance of Neural Machine Translation (NMT) systems often suffers in low-resource scenarios where sufficiently large-scale parallel corpora cannot be obtained. Pre-trained word embeddings have proven to be invaluable for improving performance in natural language analysis tasks, which often suffer from paucity of data. However, their utility for NMT has not been extensively explored. In this work, we perform five sets of experiments that analyze when we can expect pre-trained word embeddings to help in NMT tasks. We show that such embeddings can be surprisingly effective in some cases -- providing gains of up to 20 BLEU points in the most favorable setting.},
  url       = {http://www.aclweb.org/anthology/N18-2084}
}
"""

_DATA_URL = "http://phontron.com/data/ted_talks.tar.gz"

_LANGUAGES = (
    "en",
    "es",
    "pt-br",
    "fr",
    "ru",
    "he",
    "ar",
    "ko",
    "zh-cn",
    "it",
    "ja",
    "zh-tw",
    "nl",
    "ro",
    "tr",
    "de",
    "vi",
    "pl",
    "pt",
    "bg",
    "el",
    "fa",
    "sr",
    "hu",
    "hr",
    "uk",
    "cs",
    "id",
    "th",
    "sv",
    "sk",
    "sq",
    "lt",
    "da",
    "calv",
    "my",
    "sl",
    "mk",
    "fr-ca",
    "fi",
    "hy",
    "hi",
    "nb",
    "ka",
    "mn",
    "et",
    "ku",
    "gl",
    "mr",
    "zh",
    "ur",
    "eo",
    "ms",
    "az",
    "ta",
    "bn",
    "kk",
    "be",
    "eu",
    "bs",
)


class TedMultiTranslate(datasets.GeneratorBasedBuilder):
    """TED talk multilingual data set."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text import of multilingual TED talk translations",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "translations": datasets.features.TranslationVariableLanguages(languages=_LANGUAGES),
                    "talk_name": datasets.Value("string"),
                }
            ),
            homepage="https://github.com/neulab/word-embeddings-for-nmt",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"data_file": os.path.join(dl_dir, "all_talks_train.tsv")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"data_file": os.path.join(dl_dir, "all_talks_dev.tsv")}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"data_file": os.path.join(dl_dir, "all_talks_test.tsv")}
            ),
        ]

    def _generate_examples(self, data_file):
        """This function returns the examples in the raw (text) form."""
        with open(data_file, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
            for idx, row in enumerate(reader):
                # Everything in the row except for 'talk_name' will be a translation.
                # Missing/incomplete translations will contain the string "__NULL__" or
                # "_ _ NULL _ _".
                yield idx, {
                    "translations": {
                        lang: text
                        for lang, text in six.iteritems(row)
                        if lang != "talk_name" and _is_translation_complete(text)
                    },
                    "talk_name": row["talk_name"],
                }


def _is_translation_complete(text):
    return text and "__NULL__" not in text and "_ _ NULL _ _" not in text
