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
"""Named entities Recognition dataset for Norwegian."""

import conllu

import datasets


_CITATION = """\
@inproceedings{johansen2019ner,
  title={Named-Entity Recognition for Norwegian},
  author={Johansen, Bjarte},
  booktitle={Proceedings of the 22nd Nordic Conference on Computational Linguistics, NoDaLiDa},
  year={2019}
}
"""

_DESCRIPTION = """\
Named entities Recognition dataset for Norwegian. It is
a version of the Universal Dependency (UD) Treebank for both Bokmål and Nynorsk (UDN) where
all proper nouns have been tagged with their type according to the NER tagging scheme. UDN is a converted
version of the Norwegian Dependency Treebank into the UD scheme.
"""

# Files are stored with Git LFS then we add raw=true at the end
_URL = "https://github.com/ljos/navnkjenner/blob/master/data/"
_BOKMAAL_TRAIN = "bokmaal/no_bokmaal-ud-train.bioes?raw=true"
_BOKMAAL_DEV = "bokmaal/no_bokmaal-ud-dev.bioes?raw=true"
_BOKMAAL_TEST = "bokmaal/no_bokmaal-ud-test.bioes?raw=true"
_NYNORSK_TRAIN = "nynorsk/no_nynorsk-ud-train.bioes?raw=true"
_NYNORSK_DEV = "nynorsk/no_nynorsk-ud-dev.bioes?raw=true"
_NYNORSK_TEST = "nynorsk/no_nynorsk-ud-test.bioes?raw=true"
_SAMNORSK_TRAIN = "samnorsk/no_samnorsk-ud-train.bioes?raw=true"
_SAMNORSK_DEV = "samnorsk/no_samnorsk-ud-dev.bioes?raw=true"
_SAMNORSK_TEST = "samnorsk/no_samnorsk-ud-test.bioes?raw=true"


class NorwegiannerConfig(datasets.BuilderConfig):
    """BuilderConfig for NorwegianNER."""

    def __init__(self, **kwargs):
        """BuilderConfig for Norwegianner.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(NorwegiannerConfig, self).__init__(**kwargs)


class Norwegianner(datasets.GeneratorBasedBuilder):
    """Norwegianner dataset."""

    BUILDER_CONFIGS = [
        NorwegiannerConfig(
            name="bokmaal", version=datasets.Version("1.0.0"), description="Norwegianner bokmaal dataset"
        ),
        NorwegiannerConfig(
            name="nynorsk", version=datasets.Version("1.0.0"), description="Norwegianner nynorsk dataset"
        ),
        NorwegiannerConfig(
            name="samnorsk", version=datasets.Version("1.0.0"), description="Norwegianner samnorsk dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "idx": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "lemmas": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "NOUN",
                                "PUNCT",
                                "ADP",
                                "NUM",
                                "SYM",
                                "SCONJ",
                                "ADJ",
                                "PART",
                                "DET",
                                "CCONJ",
                                "PROPN",
                                "PRON",
                                "X",
                                "ADV",
                                "INTJ",
                                "VERB",
                                "AUX",
                            ]
                        )
                    ),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-OTH",
                                "I-OTH",
                                "E-OTH",
                                "S-OTH",
                                "B-ORG",
                                "I-ORG",
                                "E-ORG",
                                "S-ORG",
                                "B-PRS",
                                "I-PRS",
                                "E-PRS",
                                "S-PRS",
                                "B-GEO",
                                "I-GEO",
                                "E-GEO",
                                "S-GEO",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/ljos/navnkjenner",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "bokmaal":
            urls_to_download = {
                "train": f"{_URL}{_BOKMAAL_TRAIN}",
                "dev": f"{_URL}{_BOKMAAL_DEV}",
                "test": f"{_URL}{_BOKMAAL_TEST}",
            }
        elif self.config.name == "nynorsk":
            urls_to_download = {
                "train": f"{_URL}{_NYNORSK_TRAIN}",
                "dev": f"{_URL}{_NYNORSK_DEV}",
                "test": f"{_URL}{_NYNORSK_TEST}",
            }
        elif self.config.name == "samnorsk":
            urls_to_download = {
                "train": f"{_URL}{_SAMNORSK_TRAIN}",
                "dev": f"{_URL}{_SAMNORSK_DEV}",
                "test": f"{_URL}{_SAMNORSK_TEST}",
            }

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, "r", encoding="utf-8") as data_file:
            tokenlist = list(conllu.parse_incr(data_file))
            id = 0
            for sent in tokenlist:
                yield id, {
                    "idx": sent.metadata["sent_id"],
                    "text": sent.metadata["text"],
                    "tokens": [token["form"] for token in sent],
                    "lemmas": [token["lemma"] for token in sent],
                    "pos_tags": [token["upos"] for token in sent],
                    "ner_tags": [token["xpos"] for token in sent],
                }
                id += 1
