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
"""NorNE: Annotating Named Entities for Norwegian."""

import conllu

import datasets


_CITATION = """\
@inproceedings{johansen2019ner,
  title={NorNE: Annotating Named Entities for Norwegian},
  author={Fredrik Jørgensen, Tobias Aasmoe, Anne-Stine Ruud Husevåg,
          Lilja Øvrelid, and Erik Velldal},
  booktitle={LREC 2020},
  year={2020},
  url={https://arxiv.org/abs/1911.12146}
}
"""

_DESCRIPTION = """\
NorNE is a manually annotated
corpus of named entities which extends the annotation of the existing
Norwegian Dependency Treebank. Comprising both of the official standards of
written Norwegian (Bokmål and Nynorsk), the corpus contains around 600,000
tokens and annotates a rich set of entity types including persons,
organizations, locations, geo-political entities, products, and events,
in addition to a class corresponding to nominals derived from names.
"""

_HOMEPAGE = "https://github.com/ltgoslo/norne"

_URL = "https://raw.githubusercontent.com/ltgoslo/norne/master/ud/"
_BOKMAAL_TRAIN = "nob/no_bokmaal-ud-train.conllu"
_BOKMAAL_DEV = "nob/no_bokmaal-ud-dev.conllu"
_BOKMAAL_TEST = "nob/no_bokmaal-ud-test.conllu"
_NYNORSK_TRAIN = "nno/no_nynorsk-ud-train.conllu"
_NYNORSK_DEV = "nno/no_nynorsk-ud-dev.conllu"
_NYNORSK_TEST = "nno/no_nynorsk-ud-test.conllu"


class NorneConfig(datasets.BuilderConfig):
    """BuilderConfig for NorNE."""

    def __init__(self, **kwargs):
        """BuilderConfig for NorNE.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(NorneConfig, self).__init__(**kwargs)


class Norne(datasets.GeneratorBasedBuilder):
    """NorNE dataset."""

    BUILDER_CONFIGS = [
        NorneConfig(name="bokmaal", version=datasets.Version("1.0.0"), description="NorNE bokmaal dataset (full set)"),
        NorneConfig(name="nynorsk", version=datasets.Version("1.0.0"), description="NorNE nynorsk dataset (full set)"),
        NorneConfig(
            name="combined",
            version=datasets.Version("1.0.0"),
            description="NorNE bokmaal and nynorsk dataset (full set)",
        ),
        NorneConfig(
            name="bokmaal-7",
            version=datasets.Version("1.0.0"),
            description="NorNE bokmaal dataset (GPE_LOC/GPE_ORG as LOC/ORG)",
        ),
        NorneConfig(
            name="nynorsk-7",
            version=datasets.Version("1.0.0"),
            description="NorNE nynorsk dataset (GPE_LOC/GPE_ORG as LOC/ORG)",
        ),
        NorneConfig(
            name="combined-7",
            version=datasets.Version("1.0.0"),
            description="NorNE bokmaal and nynorsk dataset (GPE_LOC/GPE_ORG as LOC/ORG)",
        ),
        NorneConfig(
            name="bokmaal-8",
            version=datasets.Version("1.0.0"),
            description="NorNE bokmaal dataset (GPE_LOC/GPE_ORG as GPE)",
        ),
        NorneConfig(
            name="nynorsk-8",
            version=datasets.Version("1.0.0"),
            description="NorNE nynorsk dataset (GPE_LOC/GPE_ORG as GPE)",
        ),
        NorneConfig(
            name="combined-8",
            version=datasets.Version("1.0.0"),
            description="NorNE bokmaal and nynorsk dataset (GPE_LOC/GPE_ORG as GPE)",
        ),
    ]

    def _info(self):
        if self.config.name.endswith("-7"):
            ner_tags = datasets.Sequence(
                datasets.features.ClassLabel(
                    names=[
                        "O",
                        "B-PER",
                        "I-PER",
                        "B-ORG",
                        "I-ORG",
                        "B-PROD",
                        "I-PROD",
                        "B-LOC",
                        "I-LOC",
                        "B-DRV",
                        "I-DRV",
                        "B-EVT",
                        "I-EVT",
                        "B-MISC",
                        "I-MISC",
                    ]
                )
            )
        elif self.config.name.endswith("-8"):
            ner_tags = datasets.Sequence(
                datasets.features.ClassLabel(
                    names=[
                        "O",
                        "B-PER",
                        "I-PER",
                        "B-ORG",
                        "I-ORG",
                        "B-PROD",
                        "I-PROD",
                        "B-LOC",
                        "I-LOC",
                        "B-GPE",
                        "I-GPE",
                        "B-DRV",
                        "I-DRV",
                        "B-EVT",
                        "I-EVT",
                        "B-MISC",
                        "I-MISC",
                    ]
                )
            )
        else:
            ner_tags = datasets.Sequence(
                datasets.features.ClassLabel(
                    names=[
                        "O",
                        "B-PER",
                        "I-PER",
                        "B-ORG",
                        "I-ORG",
                        "B-GPE_LOC",
                        "I-GPE_LOC",
                        "B-PROD",
                        "I-PROD",
                        "B-LOC",
                        "I-LOC",
                        "B-GPE_ORG",
                        "I-GPE_ORG",
                        "B-DRV",
                        "I-DRV",
                        "B-EVT",
                        "I-EVT",
                        "B-MISC",
                        "I-MISC",
                    ]
                )
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "idx": datasets.Value("string"),
                    "lang": datasets.Value("string"),
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
                    "ner_tags": ner_tags,
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_filepaths = []
        dev_filepaths = []
        test_filepaths = []
        langs = []
        config_name = self.config.name.replace("-7", "").replace("-8", "")
        if config_name in ("bokmaal", "combined"):
            downloaded_files = dl_manager.download_and_extract(
                {
                    "train": f"{_URL}{_BOKMAAL_TRAIN}",
                    "dev": f"{_URL}{_BOKMAAL_DEV}",
                    "test": f"{_URL}{_BOKMAAL_TEST}",
                }
            )
            train_filepaths.append(downloaded_files["train"])
            dev_filepaths.append(downloaded_files["dev"])
            test_filepaths.append(downloaded_files["test"])
            langs.append("bokmaal")
        if config_name in ("nynorsk", "combined"):
            downloaded_files = dl_manager.download_and_extract(
                {
                    "train": f"{_URL}{_NYNORSK_TRAIN}",
                    "dev": f"{_URL}{_NYNORSK_DEV}",
                    "test": f"{_URL}{_NYNORSK_TEST}",
                }
            )
            train_filepaths.append(downloaded_files["train"])
            dev_filepaths.append(downloaded_files["dev"])
            test_filepaths.append(downloaded_files["test"])
            langs.append("nynorsk")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepaths": train_filepaths, "langs": langs}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepaths": dev_filepaths, "langs": langs}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepaths": test_filepaths, "langs": langs}
            ),
        ]

    def _generate_examples(self, filepaths, langs):
        idx = 0
        if self.config.name.endswith("-7"):

            def filter_tags(x):
                return x.replace("GPE_", "")

        elif self.config.name.endswith("-8"):

            def filter_tags(x):
                return x.replace("_LOC", "").replace("_ORG", "")

        else:

            def filter_tags(x):
                return x

        for filepath, lang in zip(filepaths, langs):
            with open(filepath, "r", encoding="utf-8") as data_file:
                tokens = list(conllu.parse_incr(data_file))
                for sent in tokens:
                    yield idx, {
                        "idx": sent.metadata["sent_id"],
                        "lang": lang,
                        "text": sent.metadata["text"],
                        "tokens": [token["form"] for token in sent],
                        "lemmas": [token["lemma"] for token in sent],
                        "pos_tags": [token["upos"] for token in sent],
                        "ner_tags": [filter_tags(token["misc"].get("name", "O")) for token in sent],
                    }
                    idx += 1
