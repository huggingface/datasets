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
"""The SPECIES and ORGANISMS Resources for Fast and Accurate Identification of Taxonomic Names in Text"""

import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{pafilis2013species,
         title={The SPECIES and ORGANISMS resources for fast and accurate identification of taxonomic names in text},
         author={Pafilis, Evangelos and Frankild, Sune P and Fanini, Lucia and Faulwetter, Sarah and Pavloudi, Christina and Vasileiadou, Aikaterini and Arvanitidis, Christos and Jensen, Lars Juhl},
         journal={PloS one},
         volume={8},
         number={6},
         pages={e65390},
         year={2013},
         publisher={Public Library of Science}
}
"""

_DESCRIPTION = """\
We have developed an efficient algorithm and implementation of a dictionary-based approach to named entity recognition,
which we here use to identifynames of species and other taxa in text. The tool, SPECIES, is more than an order of
magnitude faster and as accurate as existing tools. The precision and recall was assessed both on an existing gold-standard
corpus and on a new corpus of 800 abstracts, which were manually annotated after the development of the tool. The corpus
comprises abstracts from journals selected to represent many taxonomic groups, which gives insights into which types of
organism names are hard to detect and which are easy. Finally, we have tagged organism names in the entire Medline database
and developed a web resource, ORGANISMS, that makes the results accessible to the broad community of biologists.
"""

_HOMEPAGE = "https://species.jensenlab.org/"
_URL = "https://drive.google.com/u/0/uc?id=1OletxmPYNkz2ltOr9pyT0b0iBtUWxslh&export=download/"
_BIOBERT_NER_DATASET_DIRECTORY = "s800"
_TRAINING_FILE = "train.tsv"
_DEV_FILE = "devel.tsv"
_TEST_FILE = "test.tsv"


class Species800Config(datasets.BuilderConfig):
    """BuilderConfig for Species800"""

    def __init__(self, **kwargs):
        """BuilderConfig for Species800.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(Species800Config, self).__init__(**kwargs)


class Species800(datasets.GeneratorBasedBuilder):
    """Species800 dataset."""

    BUILDER_CONFIGS = [
        Species800Config(name="species_800", version=datasets.Version("1.0.0"), description="Species800 dataset"),
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
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line == "" or line == "\n":
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
