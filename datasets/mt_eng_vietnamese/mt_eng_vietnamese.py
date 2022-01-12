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


import collections

import datasets


_DESCRIPTION = """\
Preprocessed Dataset from IWSLT'15 English-Vietnamese machine translation: English-Vietnamese.
"""

_CITATION = """\
@inproceedings{Luong-Manning:iwslt15,
        Address = {Da Nang, Vietnam}
        Author = {Luong, Minh-Thang  and Manning, Christopher D.},
        Booktitle = {International Workshop on Spoken Language Translation},
        Title = {Stanford Neural Machine Translation Systems for Spoken Language Domain},
        Year = {2015}}
"""

_DATA_URL = "https://nlp.stanford.edu/projects/nmt/data/iwslt15.en-vi/{}.{}"

# Tuple that describes a single pair of files with matching translations.
# language_to_file is the map from language (2 letter string: example 'en')
# to the file path in the extracted directory.
TranslateData = collections.namedtuple("TranslateData", ["url", "language_to_file"])


class MT_Eng_ViConfig(datasets.BuilderConfig):
    """BuilderConfig for MT_Eng_Vietnamese."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for MT_Eng_Vi.
        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
          language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings. First will be used at source and second
            as target in supervised mode. For example: ("vi", "en").
          **kwargs: keyword arguments forwarded to super.
        """

        description = ("Translation dataset from %s to %s") % (language_pair[0], language_pair[1])
        super(MT_Eng_ViConfig, self).__init__(
            description=description,
            version=datasets.Version("1.0.0"),
            **kwargs,
        )
        self.language_pair = language_pair


class MTEngVietnamese(datasets.GeneratorBasedBuilder):
    """English Vietnamese machine translation dataset from IWSLT2015."""

    BUILDER_CONFIGS = [
        MT_Eng_ViConfig(
            name="iwslt2015-vi-en",
            language_pair=("vi", "en"),
        ),
        MT_Eng_ViConfig(
            name="iwslt2015-en-vi",
            language_pair=("en", "vi"),
        ),
    ]
    BUILDER_CONFIG_CLASS = MT_Eng_ViConfig

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(source, target),
            homepage="https://nlp.stanford.edu/projects/nmt/data/iwslt15.en-vi/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        source, target = self.config.language_pair

        files = {}
        for split in ("train", "dev", "test"):
            if split == "dev":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format("tst2012", source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format("tst2012", target))
            if split == "dev":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format("tst2013", source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format("tst2013", target))
            if split == "train":
                dl_dir_src = dl_manager.download_and_extract(_DATA_URL.format(split, source))
                dl_dir_tar = dl_manager.download_and_extract(_DATA_URL.format(split, target))

            files[split] = {"source_file": dl_dir_src, "target_file": dl_dir_tar}

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=files["train"]),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=files["dev"]),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=files["test"]),
        ]

    def _generate_examples(self, source_file, target_file):
        """This function returns the examples in the raw (text) form."""
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
        with open(target_file, encoding="utf-8") as f:
            target_sentences = f.read().split("\n")

        source, target = self.config.language_pair
        for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
            result = {"translation": {source: l1, target: l2}}
            # Make sure that both translations are non-empty.
            yield idx, result
