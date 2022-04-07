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
""" Shrinked Turkish NER """


import os

import datasets


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
"""

_DESCRIPTION = """\
Shrinked version (48 entity type) of the turkish_ner.

Original turkish_ner dataset: Automatically annotated Turkish corpus for named entity recognition and text categorization using large-scale gazetteers. The constructed gazetteers contains approximately 300K entities with thousands of fine-grained entity types under 25 different domains.

Shrinked entity types are: academic, academic_person, aircraft, album_person, anatomy, animal, architect_person, capital, chemical, clothes, country, culture, currency, date, food, genre, government, government_person, language, location, material, measure, medical, military, military_person, nation, newspaper, organization, organization_person, person, production_art_music, production_art_music_person, quantity, religion, science, shape, ship, software, space, space_person, sport, sport_name, sport_person, structure, subject, tech, train, vehicle
"""

_HOMEPAGE = "https://www.kaggle.com/behcetsenturk/shrinked-twnertc-turkish-ner-data-by-kuzgunlar"

_LICENSE = "Attribution 4.0 International (CC BY 4.0)"

_FILENAME = "train.txt"


class TurkishShrinkedNER(datasets.GeneratorBasedBuilder):
    @property
    def manual_download_instructions(self):
        return """\
    You need to go to https://www.kaggle.com/behcetsenturk/shrinked-twnertc-turkish-ner-data-by-kuzgunlar,
    and manually download the turkish_shrinked_ner. Once it is completed,
    a file named archive.zip will be appeared in your Downloads folder
    or whichever folder your browser chooses to save files to. You then have
    to unzip the file and move train.txt under <path/to/folder>.
    The <path/to/folder> can e.g. be "~/manual_data".
    turkish_shrinked_ner can then be loaded using the following command `datasets.load_dataset("turkish_shrinked_ner", data_dir="<path/to/folder>")`.
    """

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
                                "B-academic",
                                "I-academic",
                                "B-academic_person",
                                "I-academic_person",
                                "B-aircraft",
                                "I-aircraft",
                                "B-album_person",
                                "I-album_person",
                                "B-anatomy",
                                "I-anatomy",
                                "B-animal",
                                "I-animal",
                                "B-architect_person",
                                "I-architect_person",
                                "B-capital",
                                "I-capital",
                                "B-chemical",
                                "I-chemical",
                                "B-clothes",
                                "I-clothes",
                                "B-country",
                                "I-country",
                                "B-culture",
                                "I-culture",
                                "B-currency",
                                "I-currency",
                                "B-date",
                                "I-date",
                                "B-food",
                                "I-food",
                                "B-genre",
                                "I-genre",
                                "B-government",
                                "I-government",
                                "B-government_person",
                                "I-government_person",
                                "B-language",
                                "I-language",
                                "B-location",
                                "I-location",
                                "B-material",
                                "I-material",
                                "B-measure",
                                "I-measure",
                                "B-medical",
                                "I-medical",
                                "B-military",
                                "I-military",
                                "B-military_person",
                                "I-military_person",
                                "B-nation",
                                "I-nation",
                                "B-newspaper",
                                "I-newspaper",
                                "B-organization",
                                "I-organization",
                                "B-organization_person",
                                "I-organization_person",
                                "B-person",
                                "I-person",
                                "B-production_art_music",
                                "I-production_art_music",
                                "B-production_art_music_person",
                                "I-production_art_music_person",
                                "B-quantity",
                                "I-quantity",
                                "B-religion",
                                "I-religion",
                                "B-science",
                                "I-science",
                                "B-shape",
                                "I-shape",
                                "B-ship",
                                "I-ship",
                                "B-software",
                                "I-software",
                                "B-space",
                                "I-space",
                                "B-space_person",
                                "I-space_person",
                                "B-sport",
                                "I-sport",
                                "B-sport_name",
                                "I-sport_name",
                                "B-sport_person",
                                "I-sport_person",
                                "B-structure",
                                "I-structure",
                                "B-subject",
                                "I-subject",
                                "B-tech",
                                "I-tech",
                                "B-train",
                                "I-train",
                                "B-vehicle",
                                "I-vehicle",
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        path_to_manual_file = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))
        if not os.path.exists(path_to_manual_file):
            raise FileNotFoundError(
                "{path_to_manual_file} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('turkish_shrinked_ner', data_dir=...)` that includes file name {_FILENAME}. Manual download instructions: {self.manual_download_instructions}"
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(path_to_manual_file, "train.txt"),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        logger.info("⏳ Generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as f:
            id_ = 0
            tokens = []
            ner_tags = []
            for row in f:
                if row == "":
                    continue
                elif row == "\n":
                    yield id_, {
                        "id": str(id_),
                        "tokens": tokens,
                        "ner_tags": ner_tags,
                    }
                    tokens = []
                    ner_tags = []
                    id_ += 1
                else:
                    token, tag = row.split(" ")
                    tokens.append(token)
                    ner_tags.append(tag)

            if len(tokens) > 0:
                yield id_, {
                    "id": str(id_),
                    "tokens": tokens,
                    "ner_tags": ner_tags,
                }
