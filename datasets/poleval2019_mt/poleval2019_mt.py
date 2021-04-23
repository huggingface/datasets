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
"""Poleval 2019 dataset for Polish Translation"""


import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = ""


_DESCRIPTION = """\
PolEval is a SemEval-inspired evaluation campaign for natural language processing tools for Polish.\
Submitted solutions compete against one another within certain tasks selected by organizers, using available data and are evaluated according to\
pre-established procedures. One of the tasks in PolEval-2019 was Machine Translation (Task-4).\

The task is to train as good as possible machine translation system, using any technology,with limited textual resources.\
The competition will be done for 2 language pairs, more popular English-Polish (into Polish direction) and pair that can be called low resourced\
Russian-Polish (in both directions).

Here, Polish-English is also made available to allow for training in both directions. However, the test data is ONLY available for English-Polish.
"""

# Official homepage for the dataset
_HOMEPAGE = "http://2019.poleval.pl/"

# Licence
_LICENSE = ""

# All the urls for train data download
_TRAIN_URL = {
    "ru-pl": {
        "dev.pl": "https://drive.google.com/u/0/uc?id=1mwx_zyQeTZzkXEWMPoj4yghcbFq4ETWx&export=download",
        "dev.ru": "https://drive.google.com/u/0/uc?id=1-z09ntfDYo6j3TBTpxqu6htE_a7IAWte&export=download",
        "train.pl": "https://drive.google.com/u/0/uc?id=11EBGHMAswT5JDO60xh7gnZfYjpMQs7h7&export=download",
        "train.ru": "https://drive.google.com/u/0/uc?id=1H7FphKVVCYoH49sUXl79CuztEfJLaKoF&export=download",
    },
    "en-pl": {
        "dev.en": "https://drive.google.com/u/0/uc?id=1L6qQiO6kPLFj8BUK9XFNUH7bNyJVA7FC&export=download",
        "dev.pl": "https://drive.google.com/u/0/uc?id=1CP3oHL04qE1nfu3h_zmaxz5fmEtlwzLs&export=download",
        "train.en": "https://drive.google.com/u/0/uc?id=1NAeuWLgYBzLwU5jCdkrtj4_PRUocuvlb&export=download",
        "train.pl": "https://drive.google.com/u/0/uc?id=13ZyFc2qepAYSg9WIFaeJ9y402gblsl2e&export=download",
    },
}


# All the tsv files are present in the below link.
_TEST_URL = "http://2019.poleval.pl/task4/task4_test.zip"

# These are the supported languages in the parallel corpora in the PolEval-2019 MT task
_SUPPORTED_LANGUAGES = {
    "ru": "Russian",
    "en": "English",
}


class PolevalMTConfig(datasets.BuilderConfig):
    """BuilderConfig for PolEval-2019 MT corpus."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for PolEval-2019.
        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
            language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings. First will be used at source and second
            as target in supervised mode. For example: ("pl", "en").
          **kwargs: keyword arguments forwarded to super.
        """
        # Validate language pair.
        name = "%s-%s" % (language_pair[0], language_pair[1])
        assert "pl" in language_pair, ("Config language pair must contain `pl` (Polish), got: %s", language_pair)
        source, target = language_pair
        non_pl = source if target == "pl" else target
        assert non_pl in _SUPPORTED_LANGUAGES.keys(), ("Invalid non-polish language in pair: %s", non_pl)

        description = ("Translation dataset between Polish and %s") % (_SUPPORTED_LANGUAGES[non_pl])
        super(PolevalMTConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.0.0", ""),
            **kwargs,
        )

        self.language_pair = language_pair


class Poleval2019Mt(datasets.GeneratorBasedBuilder):
    """Polish Translation Dataset"""

    BUILDER_CONFIGS = [PolevalMTConfig(language_pair=(key, "pl")) for key, val in _SUPPORTED_LANGUAGES.items()] + [
        PolevalMTConfig(language_pair=("pl", key)) for key, val in _SUPPORTED_LANGUAGES.items()
    ]

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(source, target),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        source, target = self.config.language_pair

        if "en" in self.config.language_pair:
            urls = _TRAIN_URL["en-pl"]
        else:
            urls = _TRAIN_URL["ru-pl"]

        # Test path templates
        test_tmpl = "tst_to_{target}.{source}"  # Hardcode alert

        files = {}
        for split in ("train", "dev"):
            dl_file_src = dl_manager.download_and_extract(urls[split + "." + source])
            dl_file_dst = dl_manager.download_and_extract(urls[split + "." + target])

            files[split] = {
                "source_file": dl_file_src,
                "target_file": dl_file_dst,
                "split": split,
            }

        # To handle test split when english is the target language.
        # This is because there is no Polish to English test file that is available in the default set
        if "en" == source:
            dl_dir_test = dl_manager.download_and_extract(_TEST_URL)
            test_file = os.path.join(dl_dir_test, "task4_test", "tst.en")
        elif "en" == target:
            test_file = ""
        else:
            dl_dir_test = dl_manager.download_and_extract(_TEST_URL)
            test_file = os.path.join(dl_dir_test, "task4_test", test_tmpl.format(target=target.upper(), source=source))

        files["test"] = {"source_file": test_file, "target_file": "", "split": "test"}

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs=files["train"]),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=files["dev"]),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=files["test"]),
        ]

    def _generate_examples(self, source_file, target_file, split):
        """This function returns the examples in the raw (text) form."""
        source, target = self.config.language_pair

        # Returning an empty source and target just to handle the test file absence when English is the target
        if split == "test":
            if target == "en":
                # Returning dummy info
                result = {"translation": {source: "", target: ""}}
                yield 0, result
            else:  # Handling cases for Polish and Russian languages
                with open(source_file, encoding="utf-8") as f:
                    source_sentences = f.read().split("\n")

                for idx, sent in enumerate(source_sentences):
                    if sent.strip() != "":
                        result = {"translation": {source: sent, target: ""}}
                        yield idx, result
        else:
            # Training and Dev sets examples
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

            for idx, (l1, l2) in enumerate(zip(source_sentences, target_sentences)):
                result = {"translation": {source: l1, target: l2}}
                # Make sure that both translations are non-empty.
                yield idx, result
