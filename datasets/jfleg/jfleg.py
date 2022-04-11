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
"""JFLEG dataset."""


import datasets


_CITATION = """\
@InProceedings{napoles-sakaguchi-tetreault:2017:EACLshort,
  author    = {Napoles, Courtney
               and  Sakaguchi, Keisuke
               and  Tetreault, Joel},
  title     = {JFLEG: A Fluency Corpus and Benchmark for Grammatical Error Correction},
  booktitle = {Proceedings of the 15th Conference of the European Chapter of the
               Association for Computational Linguistics: Volume 2, Short Papers},
  month     = {April},
  year      = {2017},
  address   = {Valencia, Spain},
  publisher = {Association for Computational Linguistics},
  pages     = {229--234},
  url       = {http://www.aclweb.org/anthology/E17-2037}
}
@InProceedings{heilman-EtAl:2014:P14-2,
  author    = {Heilman, Michael
               and  Cahill, Aoife
               and  Madnani, Nitin
               and  Lopez, Melissa
               and  Mulholland, Matthew
               and  Tetreault, Joel},
  title     = {Predicting Grammaticality on an Ordinal Scale},
  booktitle = {Proceedings of the 52nd Annual Meeting of the
               Association for Computational Linguistics (Volume 2: Short Papers)},
  month     = {June},
  year      = {2014},
  address   = {Baltimore, Maryland},
  publisher = {Association for Computational Linguistics},
  pages     = {174--180},
  url       = {http://www.aclweb.org/anthology/P14-2029}
}
"""

_DESCRIPTION = """\
JFLEG (JHU FLuency-Extended GUG) is an English grammatical error correction (GEC) corpus.
It is a gold standard benchmark for developing and evaluating GEC systems with respect to
fluency (extent to which a text is native-sounding) as well as grammaticality.

For each source document, there are four human-written corrections (ref0 to ref3).
"""

_HOMEPAGE = "https://github.com/keisks/jfleg"

_LICENSE = "CC BY-NC-SA 4.0"

_URLs = {
    "dev": {
        "src": "https://raw.githubusercontent.com/keisks/jfleg/master/dev/dev.src",
        "ref0": "https://raw.githubusercontent.com/keisks/jfleg/master/dev/dev.ref0",
        "ref1": "https://raw.githubusercontent.com/keisks/jfleg/master/dev/dev.ref1",
        "ref2": "https://raw.githubusercontent.com/keisks/jfleg/master/dev/dev.ref2",
        "ref3": "https://raw.githubusercontent.com/keisks/jfleg/master/dev/dev.ref3",
    },
    "test": {
        "src": "https://raw.githubusercontent.com/keisks/jfleg/master/test/test.src",
        "ref0": "https://raw.githubusercontent.com/keisks/jfleg/master/test/test.ref0",
        "ref1": "https://raw.githubusercontent.com/keisks/jfleg/master/test/test.ref1",
        "ref2": "https://raw.githubusercontent.com/keisks/jfleg/master/test/test.ref2",
        "ref3": "https://raw.githubusercontent.com/keisks/jfleg/master/test/test.ref3",
    },
}


class Jfleg(datasets.GeneratorBasedBuilder):
    """JFLEG (JHU FLuency-Extended GUG) grammatical error correction dataset."""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {"sentence": datasets.Value("string"), "corrections": datasets.Sequence(datasets.Value("string"))}
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        downloaded_dev = dl_manager.download_and_extract(_URLs["dev"])
        downloaded_test = dl_manager.download_and_extract(_URLs["test"])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": downloaded_dev,
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": downloaded_test, "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        source_file = filepath["src"]
        with open(source_file, encoding="utf-8") as f:
            source_sentences = f.read().split("\n")
            num_source = len(source_sentences)

        corrections = []
        for n in range(0, 4):
            correction_file = filepath[f"ref{n}"]
            with open(correction_file, encoding="utf-8") as f:
                correction_sentences = f.read().split("\n")
                num_correction = len(correction_sentences)

                assert len(correction_sentences) == len(
                    source_sentences
                ), f"Sizes do not match: {num_source} vs {num_correction} for {source_file} vs {correction_file}."
                corrections.append(correction_sentences)

        corrected_sentences = list(zip(*corrections))
        for id_, source_sentence in enumerate(source_sentences):
            yield id_, {"sentence": source_sentence, "corrections": corrected_sentences[id_]}
