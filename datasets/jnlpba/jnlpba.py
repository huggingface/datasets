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
"""Introduction to the Bio-Entity Recognition Task at JNLPBA"""

import logging
import os

import datasets


_CITATION = """\
@inproceedings{kim2004introduction,
               title={Introduction to the bio-entity recognition task at JNLPBA},
               author={Kim, Jin-Dong and Ohta, Tomoko and Tsuruoka, Yoshimasa and Tateisi, Yuka and Collier, Nigel},
               booktitle={Proceedings of the international joint workshop on natural language processing in biomedicine and its applications},
               pages={70--75},
               year={2004},
               organization={Citeseer}
}
"""

_DESCRIPTION = """\
The data came from the GENIA version 3.02 corpus (Kim et al., 2003). This was formed from a controlled search
on MEDLINE using the MeSH terms human, blood cells and transcription factors. From this search 2,000 abstracts
were selected and hand annotated according to a small taxonomy of 48 classes based on a chemical classification.
Among the classes, 36 terminal classes were used to annotate the GENIA corpus.
"""

_HOMEPAGE = "http://www.geniaproject.org/shared-tasks/bionlp-jnlpba-shared-task-2004"
_URL = "https://drive.google.com/u/0/uc?id=1OletxmPYNkz2ltOr9pyT0b0iBtUWxslh&export=download/"
_BIOBERT_NER_DATASET_DIRECTORY = "JNLPBA"
_TRAINING_FILE = "train.tsv"
_DEV_FILE = "devel.tsv"
_TEST_FILE = "test.tsv"


class JNLPBAConfig(datasets.BuilderConfig):
    """BuilderConfig for JNLPBA"""

    def __init__(self, **kwargs):
        """BuilderConfig for JNLPBA.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(JNLPBAConfig, self).__init__(**kwargs)


class JNLPBA(datasets.GeneratorBasedBuilder):
    """JNLPBA dataset."""

    BUILDER_CONFIGS = [
        JNLPBAConfig(name="jnlpba", version=datasets.Version("1.0.0"), description="JNLPBA dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B",
                                "I",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "biobert_ner_datasets": _URL,
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)
        dataset_directory = os.path.join(downloaded_files["biobert_ner_datasets"], _BIOBERT_NER_DATASET_DIRECTORY)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN, gen_kwargs={"filepath": os.path.join(dataset_directory, _TRAINING_FILE)}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": os.path.join(dataset_directory, _DEV_FILE)}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST, gen_kwargs={"filepath": os.path.join(dataset_directory, _TEST_FILE)}
            ),
        ]

    def _generate_examples(self, filepath):
        logging.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # tokens are tab separated
                    splits = line.split("\t")
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }
