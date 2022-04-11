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
"""OPUS-100"""


import datasets


_CITATION = """\
@misc{zhang2020improving,
      title={Improving Massively Multilingual Neural Machine Translation and Zero-Shot Translation},
      author={Biao Zhang and Philip Williams and Ivan Titov and Rico Sennrich},
      year={2020},
      eprint={2004.11867},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
OPUS-100 is English-centric, meaning that all training pairs include English on either the source or target side.
The corpus covers 100 languages (including English).OPUS-100 contains approximately 55M sentence pairs.
Of the 99 language pairs, 44 have 1M sentence pairs of training data, 73 have at least 100k, and 95 have at least 10k.
"""

_URL = {
    "supervised": "https://object.pouta.csc.fi/OPUS-100/v1.0/opus-100-corpus-{}-v1.0.tar.gz",
    "zero-shot": "https://object.pouta.csc.fi/OPUS-100/v1.0/opus-100-corpus-zeroshot-v1.0.tar.gz",
}

_SupervisedLanguagePairs = [
    "af-en",
    "am-en",
    "an-en",
    "ar-en",
    "as-en",
    "az-en",
    "be-en",
    "bg-en",
    "bn-en",
    "br-en",
    "bs-en",
    "ca-en",
    "cs-en",
    "cy-en",
    "da-en",
    "de-en",
    "dz-en",
    "el-en",
    "en-eo",
    "en-es",
    "en-et",
    "en-eu",
    "en-fa",
    "en-fi",
    "en-fr",
    "en-fy",
    "en-ga",
    "en-gd",
    "en-gl",
    "en-gu",
    "en-ha",
    "en-he",
    "en-hi",
    "en-hr",
    "en-hu",
    "en-hy",
    "en-id",
    "en-ig",
    "en-is",
    "en-it",
    "en-ja",
    "en-ka",
    "en-kk",
    "en-km",
    "en-ko",
    "en-kn",
    "en-ku",
    "en-ky",
    "en-li",
    "en-lt",
    "en-lv",
    "en-mg",
    "en-mk",
    "en-ml",
    "en-mn",
    "en-mr",
    "en-ms",
    "en-mt",
    "en-my",
    "en-nb",
    "en-ne",
    "en-nl",
    "en-nn",
    "en-no",
    "en-oc",
    "en-or",
    "en-pa",
    "en-pl",
    "en-ps",
    "en-pt",
    "en-ro",
    "en-ru",
    "en-rw",
    "en-se",
    "en-sh",
    "en-si",
    "en-sk",
    "en-sl",
    "en-sq",
    "en-sr",
    "en-sv",
    "en-ta",
    "en-te",
    "en-tg",
    "en-th",
    "en-tk",
    "en-tr",
    "en-tt",
    "en-ug",
    "en-uk",
    "en-ur",
    "en-uz",
    "en-vi",
    "en-wa",
    "en-xh",
    "en-yi",
    "en-yo",
    "en-zh",
    "en-zu",
]

_0shotLanguagePairs = [
    "ar-de",
    "ar-fr",
    "ar-nl",
    "ar-ru",
    "ar-zh",
    "de-fr",
    "de-nl",
    "de-ru",
    "de-zh",
    "fr-nl",
    "fr-ru",
    "fr-zh",
    "nl-ru",
    "nl-zh",
    "ru-zh",
]


class Opus100Config(datasets.BuilderConfig):
    """BuilderConfig for Opus100"""

    def __init__(self, language_pair, **kwargs):
        super().__init__(**kwargs)
        """

        Args:
            language_pair: language pair, you want to load
            **kwargs: keyword arguments forwarded to super.
        """
        self.language_pair = language_pair


class Opus100(datasets.GeneratorBasedBuilder):
    """OPUS-100 is English-centric, meaning that all training pairs include English on either the source or target side."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIG_CLASS = Opus100Config
    BUILDER_CONFIGS = [
        Opus100Config(name=pair, description=_DESCRIPTION, language_pair=pair)
        for pair in _SupervisedLanguagePairs + _0shotLanguagePairs
    ]

    def _info(self):
        src_tag, tgt_tag = self.config.language_pair.split("-")
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features({"translation": datasets.features.Translation(languages=(src_tag, tgt_tag))}),
            supervised_keys=(src_tag, tgt_tag),
            homepage="http://opus.nlpl.eu/opus-100.php",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        lang_pair = self.config.language_pair
        src_tag, tgt_tag = lang_pair.split("-")

        domain = "supervised"
        if lang_pair in _0shotLanguagePairs:
            domain = "zero-shot"

        if domain == "supervised":
            archive = dl_manager.download(_URL["supervised"].format(lang_pair))
        elif domain == "zero-shot":
            archive = dl_manager.download(_URL["zero-shot"])

        data_dir = "/".join(["opus-100-corpus", "v1.0", domain, lang_pair])
        output = []

        test = datasets.SplitGenerator(
            name=datasets.Split.TEST,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={
                "filepath": f"{data_dir}/opus.{lang_pair}-test.{src_tag}",
                "labelpath": f"{data_dir}/opus.{lang_pair}-test.{tgt_tag}",
                "files": dl_manager.iter_archive(archive),
            },
        )

        available_files = [path for path, _ in dl_manager.iter_archive(archive)]
        if f"{data_dir}/opus.{lang_pair}-test.{src_tag}" in available_files:
            output.append(test)

        if domain == "supervised":

            train = datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": f"{data_dir}/opus.{lang_pair}-train.{src_tag}",
                    "labelpath": f"{data_dir}/opus.{lang_pair}-train.{tgt_tag}",
                    "files": dl_manager.iter_archive(archive),
                },
            )

            if f"{data_dir}/opus.{lang_pair}-train.{src_tag}" in available_files:
                output.append(train)

            valid = datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": f"{data_dir}/opus.{lang_pair}-dev.{src_tag}",
                    "labelpath": f"{data_dir}/opus.{lang_pair}-dev.{tgt_tag}",
                    "files": dl_manager.iter_archive(archive),
                },
            )

            if f"{data_dir}/opus.{lang_pair}-dev.{src_tag}" in available_files:
                output.append(valid)

        return output

    def _generate_examples(self, filepath, labelpath, files):
        """Yields examples."""
        src_tag, tgt_tag = self.config.language_pair.split("-")
        src, tgt = None, None
        for path, f in files:
            if path == filepath:
                src = f.read().decode("utf-8").split("\n")[:-1]
            elif path == labelpath:
                tgt = f.read().decode("utf-8").split("\n")[:-1]
            if src is not None and tgt is not None:
                for idx, (s, t) in enumerate(zip(src, tgt)):
                    yield idx, {"translation": {src_tag: s, tgt_tag: t}}
                break
