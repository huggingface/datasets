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
"""Introduction to the CoNLL-2002 Shared Task: Language-Independent Named Entity Recognition"""

import logging

import datasets


_CITATION = """\
@inproceedings{tjong-kim-sang-2002-introduction,
    title = "Introduction to the {C}o{NLL}-2002 Shared Task: Language-Independent Named Entity Recognition",
    author = "Tjong Kim Sang, Erik F.",
    booktitle = "{COLING}-02: The 6th Conference on Natural Language Learning 2002 ({C}o{NLL}-2002)",
    year = "2002",
    url = "https://www.aclweb.org/anthology/W02-2024",
}
"""

_DESCRIPTION = """\
Named entities are phrases that contain the names of persons, organizations, locations, times and quantities.

Example:
[PER Wolff] , currently a journalist in [LOC Argentina] , played with [PER Del Bosque] in the final years of the seventies in [ORG Real Madrid] .

The shared task of CoNLL-2002 concerns language-independent named entity recognition.
We will concentrate on four types of named entities: persons, locations, organizations and names of miscellaneous entities that do not belong to the previous three groups.
The participants of the shared task will be offered training and test data for at least two languages.
They will use the data for developing a named-entity recognition system that includes a machine learning component.
Information sources other than the training data may be used in this shared task.
We are especially interested in methods that can use additional unannotated data for improving their performance (for example co-training).

The train/validation/test sets are available in Spanish and Dutch.

For more details see https://www.clips.uantwerpen.be/conll2002/ner/ and https://www.aclweb.org/anthology/W02-2024/
"""

_URL = "https://raw.githubusercontent.com/teropa/nlp/master/resources/corpora/conll2002/"
_ES_TRAINING_FILE = "esp.train"
_ES_DEV_FILE = "esp.testa"
_ES_TEST_FILE = "esp.testb"
_NL_TRAINING_FILE = "ned.train"
_NL_DEV_FILE = "ned.testa"
_NL_TEST_FILE = "ned.testb"


class Conll2002Config(datasets.BuilderConfig):
    """BuilderConfig for Conll2002"""

    def __init__(self, **kwargs):
        """BuilderConfig forConll2002.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Conll2002Config, self).__init__(**kwargs)


class Conll2002(datasets.GeneratorBasedBuilder):
    """Conll2002 dataset."""

    BUILDER_CONFIGS = [
        Conll2002Config(name="es", version=datasets.Version("1.0.0"), description="Conll2002 Spanish dataset"),
        Conll2002Config(name="nl", version=datasets.Version("1.0.0"), description="Conll2002 Dutch dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "pos_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "AO",
                                "AQ",
                                "CC",
                                "CS",
                                "DA",
                                "DE",
                                "DD",
                                "DI",
                                "DN",
                                "DP",
                                "DT",
                                "Faa",
                                "Fat",
                                "Fc",
                                "Fd",
                                "Fe",
                                "Fg",
                                "Fh",
                                "Fia",
                                "Fit",
                                "Fp",
                                "Fpa",
                                "Fpt",
                                "Fs",
                                "Ft",
                                "Fx",
                                "Fz",
                                "I",
                                "NC",
                                "NP",
                                "P0",
                                "PD",
                                "PI",
                                "PN",
                                "PP",
                                "PR",
                                "PT",
                                "PX",
                                "RG",
                                "RN",
                                "SP",
                                "VAI",
                                "VAM",
                                "VAN",
                                "VAP",
                                "VAS",
                                "VMG",
                                "VMI",
                                "VMM",
                                "VMN",
                                "VMP",
                                "VMS",
                                "VSG",
                                "VSI",
                                "VSM",
                                "VSN",
                                "VSP",
                                "VSS",
                                "Y",
                                "Z",
                            ]
                        )
                        if self.config.name == "es"
                        else datasets.features.ClassLabel(
                            names=["Adj", "Adv", "Art", "Conj", "Int", "Misc", "N", "Num", "Prep", "Pron", "Punc", "V"]
                        )
                    ),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PER",
                                "I-PER",
                                "B-ORG",
                                "I-ORG",
                                "B-LOC",
                                "I-LOC",
                                "B-MISC",
                                "I-MISC",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://www.aclweb.org/anthology/W02-2024/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "train": f"{_URL}{_ES_TRAINING_FILE if self.config.name == 'es' else _NL_TRAINING_FILE}",
            "dev": f"{_URL}{_ES_DEV_FILE if self.config.name == 'es' else _NL_DEV_FILE}",
            "test": f"{_URL}{_ES_TEST_FILE if self.config.name == 'es' else _NL_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            pos_tags = []
            ner_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "pos_tags": pos_tags,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        pos_tags = []
                        ner_tags = []
                else:
                    # conll2002 tokens are space separated
                    splits = line.split(" ")
                    tokens.append(splits[0])
                    pos_tags.append(splits[1])
                    ner_tags.append(splits[2].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "pos_tags": pos_tags,
                "ner_tags": ner_tags,
            }
