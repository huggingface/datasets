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
"""TED talk high/low-resource paired language data set from Qi, et al. 2018."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_DESCRIPTION = """\
Data sets derived from TED talk transcripts for comparing similar language pairs
where one is high resource and the other is low resource.
"""

_CITATION = """\
@inproceedings{Ye2018WordEmbeddings,
  author  = {Ye, Qi and Devendra, Sachan and Matthieu, Felix and Sarguna, Padmanabhan and Graham, Neubig},
  title   = {When and Why are pre-trained word embeddings useful for Neural Machine Translation},
  booktitle = {HLT-NAACL},
  year    = {2018},
  }
"""

_DATA_URL = "http://www.phontron.com/data/qi18naacl-dataset.tar.gz"

_VALID_LANGUAGE_PAIRS = (
    ("az", "en"),
    ("az_tr", "en"),
    ("be", "en"),
    ("be_ru", "en"),
    ("es", "pt"),
    ("fr", "pt"),
    ("gl", "en"),
    ("gl_pt", "en"),
    ("he", "pt"),
    ("it", "pt"),
    ("pt", "en"),
    ("ru", "en"),
    ("ru", "pt"),
    ("tr", "en"),
)


class TedHrlrConfig(datasets.BuilderConfig):
    """BuilderConfig for TED talk data comparing high/low resource languages."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for TED talk data comparing high/low resource languages.

        The first language in `language_pair` should either be a 2-letter coded
        string or two such strings joined by an underscore (e.g., "az" or "az_tr").
        In cases where it contains two languages, the train data set will contain an
        (unlabelled) mix of the two languages and the validation and test sets
        will contain only the first language. This dataset will refer to the
        source language by the 5-letter string with the underscore. The second
        language in `language_pair` must be a 2-letter coded string.

        For example, to get pairings between Russian and English, specify
        `("ru", "en")` as `language_pair`. To get a mix of Belarusian and Russian in
        the training set and purely Belarusian in the validation and test sets,
        specify `("be_ru", "en")`.

        Args:
          language_pair: pair of languages that will be used for translation. The
            first will be used as source and second as target in supervised mode.
          **kwargs: keyword arguments forwarded to super.
        """
        name = "%s_to_%s" % (language_pair[0].replace("_", ""), language_pair[1])

        description = ("Translation dataset from %s to %s in plain text.") % (language_pair[0], language_pair[1])
        super(TedHrlrConfig, self).__init__(name=name, description=description, **kwargs)

        # Validate language pair.
        assert language_pair in _VALID_LANGUAGE_PAIRS, (
            "Config language pair (%s, " "%s) not supported"
        ) % language_pair

        self.language_pair = language_pair


class TedHrlr(datasets.GeneratorBasedBuilder):
    """TED talk data set for comparing high and low resource languages."""

    BUILDER_CONFIGS = [
        TedHrlrConfig(  # pylint: disable=g-complex-comprehension
            language_pair=pair,
            version=datasets.Version("1.0.0", ""),
        )
        for pair in _VALID_LANGUAGE_PAIRS
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            homepage="https://github.com/neulab/word-embeddings-for-nmt",
            supervised_keys=self.config.language_pair,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        source, target = self.config.language_pair

        data_dir = os.path.join(dl_dir, "datasets", "%s_to_%s" % (source, target))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, "{}.train".format(source.replace("_", "-"))),
                    "target_file": os.path.join(data_dir, "{}.train".format(target)),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, "{}.dev".format(source.split("_")[0])),
                    "target_file": os.path.join(data_dir, "{}.dev".format(target)),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "source_file": os.path.join(data_dir, "{}.test".format(source.split("_")[0])),
                    "target_file": os.path.join(data_dir, "{}.test".format(target)),
                },
            ),
        ]

    def _generate_examples(self, source_file, target_file):
        """This function returns the examples in the raw (text) form."""
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
        with open(target_file, encoding="utf-8") as f:
            target_sentences = f.read().split("\n")

        assert len(target_sentences) == len(source_sentences), "Sizes do not match: %d vs %d for %s vs %s." % (
            len(source_sentences),
            len(target_sentences),
            source_file,
            target_file,
        )

        source, target = self.config.language_pair
        for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
            result = {"translation": {source: l1, target: l2}}
            # Make sure that both translations are non-empty.
            if all(result.values()):
                yield idx, result
