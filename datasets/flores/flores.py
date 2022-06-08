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
"""Facebook Low Resource (FLoRes) machine translation benchmark dataset."""


import collections

import datasets


_DESCRIPTION = """\
Evaluation datasets for low-resource machine translation: Nepali-English and Sinhala-English.
"""

_CITATION = """\
@misc{guzmn2019new,
    title={Two New Evaluation Datasets for Low-Resource Machine Translation: Nepali-English and Sinhala-English},
    author={Francisco Guzman and Peng-Jen Chen and Myle Ott and Juan Pino and Guillaume Lample and Philipp Koehn and Vishrav Chaudhary and Marc'Aurelio Ranzato},
    year={2019},
    eprint={1902.01382},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
"""

_DATA_URL = "https://github.com/facebookresearch/flores/raw/main/floresv1/data/wikipedia_en_ne_si_test_sets.tgz"

# Tuple that describes a single pair of files with matching translations.
# language_to_file is the map from language (2 letter string: example 'en')
# to the file path in the extracted directory.
TranslateData = collections.namedtuple("TranslateData", ["url", "language_to_file"])


class FloresConfig(datasets.BuilderConfig):
    """BuilderConfig for FLoRes."""

    def __init__(self, language_pair=(None, None), **kwargs):
        """BuilderConfig for FLoRes.

        Args:
            for the `datasets.features.text.TextEncoder` used for the features feature.
          language_pair: pair of languages that will be used for translation. Should
            contain 2-letter coded strings. First will be used at source and second
            as target in supervised mode. For example: ("se", "en").
          **kwargs: keyword arguments forwarded to super.
        """
        name = "%s%s" % (language_pair[0], language_pair[1])

        description = ("Translation dataset from %s to %s") % (language_pair[0], language_pair[1])
        super(FloresConfig, self).__init__(
            name=name,
            description=description,
            version=datasets.Version("1.1.0", ""),
            **kwargs,
        )

        # Validate language pair.
        assert "en" in language_pair, ("Config language pair must contain `en`, got: %s", language_pair)
        source, target = language_pair
        non_en = source if target == "en" else target
        assert non_en in ["ne", "si"], ("Invalid non-en language in pair: %s", non_en)

        self.language_pair = language_pair


class Flores(datasets.GeneratorBasedBuilder):
    """FLoRes machine translation dataset."""

    BUILDER_CONFIGS = [
        FloresConfig(
            language_pair=("ne", "en"),
        ),
        FloresConfig(
            language_pair=("si", "en"),
        ),
    ]

    def _info(self):
        source, target = self.config.language_pair
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"translation": datasets.features.Translation(languages=self.config.language_pair)}
            ),
            supervised_keys=(source, target),
            homepage="https://github.com/facebookresearch/flores/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive = dl_manager.download(_DATA_URL)

        source, target = self.config.language_pair
        non_en = source if target == "en" else target
        path_tmpl = "wikipedia_en_ne_si_test_sets/wikipedia.{split}.{non_en}-en." "{lang}"

        files = {}
        for split in ("dev", "devtest"):
            files[split] = {
                "source_file": path_tmpl.format(split=split, non_en=non_en, lang=source),
                "target_file": path_tmpl.format(split=split, non_en=non_en, lang=target),
                "files": dl_manager.iter_archive(archive),
            }

        return [
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs=files["dev"]),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs=files["devtest"]),
        ]

    def _generate_examples(self, files, source_file, target_file):
        """This function returns the examples in the raw (text) form."""
        source_sentences, target_sentences = None, None
        for path, f in files:
            if path == source_file:
                source_sentences = f.read().decode("utf-8").split("\n")
            elif path == target_file:
                target_sentences = f.read().decode("utf-8").split("\n")
            if source_sentences is not None and target_sentences is not None:
                break

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
