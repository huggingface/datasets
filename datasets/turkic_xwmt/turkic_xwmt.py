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
"""A Large-Scale Study of Machine Translation in Turkic Languages."""
import os

import datasets


_LANGUAGES = ["az", "ba", "en", "kaa", "kk", "ky", "ru", "sah", "tr", "uz"]

_DESCRIPTION = """\
A Large-Scale Study of Machine Translation in Turkic Languages
"""

_CITATION = """\
@inproceedings{mirzakhalov2021large,
  title={A Large-Scale Study of Machine Translation in Turkic Languages},
  author={Mirzakhalov, Jamshidbek and Babu, Anoop and Ataman, Duygu and Kariev, Sherzod and Tyers, Francis and Abduraufov, Otabek and Hajili, Mammad and Ivanova, Sardana and Khaytbaev, Abror and Laverghetta Jr, Antonio and others},
  booktitle={Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing},
  pages={5876--5890},
  year={2021}
}
"""

_DATA_URL = (
    "https://github.com/turkic-interlingua/til-mt/blob/6ac179350448895a63cc06fcfd1135882c8cc49b/xwmt/test.zip?raw=true"
)


class XWMTConfig(datasets.BuilderConfig):
    """BuilderConfig for XWMT."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for XWMT.

        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
          language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings.
          **kwargs: keyword arguments forwarded to super.
        """
        name = "%s-%s" % (language_pair[0], language_pair[1])

        description = ("Translation dataset from %s to %s") % (language_pair[0], language_pair[1])
        super(XWMTConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.1.0", ""),
            **kwargs,
        )

        # Validate language pair.
        source, target = language_pair

        assert source in _LANGUAGES, ("Config language pair must be one of the supported languages, got: %s", source)
        assert target in _LANGUAGES, ("Config language pair must be one of the supported languages, got: %s", source)

        self.language_pair = language_pair


class TurkicXWMT(datasets.GeneratorBasedBuilder):
    """XWMT machine translation dataset."""

    BUILDER_CONFIGS = [
        XWMTConfig(
            language_pair=(lang1, lang2),
        )
        for lang1 in _LANGUAGES
        for lang2 in _LANGUAGES
        if lang1 != lang2
    ]

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(source, target),
            homepage="https://github.com/turkicinterlingua/til-mt",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        path = dl_manager.download_and_extract(_DATA_URL)

        source, target = self.config.language_pair
        source_path = os.path.join(path, "test", f"{source}-{target}", f"{source}-{target}.{source}.txt")
        target_path = os.path.join(path, "test", f"{source}-{target}", f"{source}-{target}.{target}.txt")

        files = {}
        files["test"] = {
            "source_file": source_path,
            "target_file": target_path,
        }

        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=files["test"]),
        ]

    def _generate_examples(self, source_file, target_file):
        """This function returns the examples in the raw (text) form."""
        source_sentences, target_sentences = None, None
        source_sentences = open(source_file, encoding="utf-8").read().strip().split("\n")
        target_sentences = open(target_file, encoding="utf-8").read().strip().split("\n")

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
