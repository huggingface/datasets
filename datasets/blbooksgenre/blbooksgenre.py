# coding=utf-8
# Copyright 2021 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""British Library Books Genre Dataset"""

import ast
import csv
from datetime import datetime
from typing import Dict, List

import datasets


_CITATION = """\
@misc{british library_genre,
title={ 19th Century Books - metadata with additional crowdsourced annotations},
url={https://doi.org/10.23636/BKHQ-0312},
author={{British Library} and  Morris, Victoria and van Strien, Daniel and Tolfo, Giorgia and Afric, Lora and Robertson, Stewart and Tiney, Patricia and Dogterom, Annelies and Wollner, Ildi},
year={2021}}
"""

_DESCRIPTION = """\
This dataset contains metadata for resources belonging to the British Library’s digitised printed books (18th-19th century) collection (bl.uk/collection-guides/digitised-printed-books).
This metadata has been extracted from British Library catalogue records.
The metadata held within our main catalogue is updated regularly.
This metadata dataset should be considered a snapshot of this metadata.
"""

_HOMEPAGE = "doi.org/10.23636/BKHQ-0312"

_LICENSE = "CC0 1.0 Universal Public Domain"


_URL = "https://bl.iro.bl.uk/downloads/36c7cd20-c8a7-4495-acbe-469b9132c6b1?locale=en"

common_features = {
    "BL record ID": datasets.Value("string"),
    "Name": datasets.Value("string"),
    "Dates associated with name": datasets.Value("string"),
    "Type of name": datasets.Value("string"),
    "Role": datasets.Value("string"),
    "All names": datasets.features.Sequence(datasets.Value("string")),
    "Title": datasets.Value("string"),
    "Variant titles": datasets.Value("string"),
    "Series title": datasets.Value("string"),
    "Number within series": datasets.Value("string"),
    "Country of publication": datasets.Sequence(datasets.Value("string")),
    "Place of publication": datasets.Sequence(datasets.Value("string")),
    "Publisher": datasets.Value("string"),
    "Date of publication": datasets.Value("string"),
    "Edition": datasets.Value("string"),
    "Physical description": datasets.Value("string"),
    "Dewey classification": datasets.Value("string"),
    "BL shelfmark": datasets.Value("string"),
    "Topics": datasets.Value("string"),
    "Genre": datasets.Value("string"),
    "Languages": datasets.features.Sequence(datasets.Value("string")),
    "Notes": datasets.Value("string"),
    "BL record ID for physical resource": datasets.Value("string"),
    "classification_id": datasets.Value("string"),
    "user_id": datasets.Value("string"),
    "subject_ids": datasets.Value("string"),
    "annotator_date_pub": datasets.Value("string"),
    "annotator_normalised_date_pub": datasets.Value("string"),
    "annotator_edition_statement": datasets.Value("string"),
    "annotator_FAST_genre_terms": datasets.Value("string"),
    "annotator_FAST_subject_terms": datasets.Value("string"),
    "annotator_comments": datasets.Value("string"),
    "annotator_main_language": datasets.Value("string"),
    "annotator_other_languages_summaries": datasets.Value("string"),
    "annotator_summaries_language": datasets.Value("string"),
    "annotator_translation": datasets.Value("string"),
    "annotator_original_language": datasets.Value("string"),
    "annotator_publisher": datasets.Value("string"),
    "annotator_place_pub": datasets.Value("string"),
    "annotator_country": datasets.Value("string"),
    "annotator_title": datasets.Value("string"),
    "Link to digitised book": datasets.Value("string"),
    "annotated": datasets.Value("bool"),
}

raw_features = datasets.Features(
    {
        **common_features,
        **{
            "Type of resource": datasets.features.ClassLabel(
                names=["Monograph", "Serial", "Monographic component part"]
            ),
            "created_at": datasets.Value("string"),
            "annotator_genre": datasets.Value("string"),
        },
    }
)

annotated_raw_features = datasets.Features(
    {
        **common_features,
        **{
            "Type of resource": datasets.features.ClassLabel(
                names=[
                    "Monograph",
                    "Serial",
                ]
            ),
            "created_at": datasets.Value("timestamp[s]"),
            "annotator_genre": datasets.features.ClassLabel(
                names=[
                    "Fiction",
                    "Can't tell",
                    "Non-fiction",
                    "The book contains both Fiction and Non-Fiction",
                ]
            ),
        },
    }
)


class BlBooksGenre(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="title_genre_classifiction",
            version=VERSION,
            description="This part of my dataset covers a first domain",
        ),
        datasets.BuilderConfig(
            name="annotated_raw",
            version=VERSION,
            description="""\
                This version of the dataset includes all fields from the original dataset which are annotated.
                This includes duplication from different annotators""",
        ),
        datasets.BuilderConfig(
            name="raw",
            version=VERSION,
            description="""\
            This version of the dataset includes all the fields from the original dataset including rows without annotation.
            It includes duplications from different annotators""",
        ),
    ]

    DEFAULT_CONFIG_NAME = "title_genre_classifiction"

    def _info(self):
        if self.config.name == "title_genre_classifiction":
            features = datasets.Features(
                {
                    "BL record ID": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(names=["Fiction", "Non-fiction"]),
                }
            )
        if self.config.name == "annotated_raw":
            features = annotated_raw_features
        if self.config.name == "raw":
            features = raw_features

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_file = dl_manager.download(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_file,
                    "split": "train",
                },
            ),
        ]

    def _parse_language(self, row: Dict) -> List[str]:
        languages = row["Languages"]
        if not languages:
            return []
        return languages.split(";")

    def _parse_country(self, row: Dict) -> List[str]:
        return row["Country of publication"].split(";") if row["Country of publication"] else []

    def _parse_place_of_publication(self, row: Dict) -> List[str]:
        return row["Place of publication"].split(";") if row["Place of publication"] else []

    def _parse_all_names(self, row: Dict) -> List[str]:
        return row["All names"].split(";") if row["All names"] else []

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""
        with open(filepath, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if self.config.name == "title_genre_classifiction":
                unique = set()
                id_ = 0
                for row in reader:
                    annotated = ast.literal_eval(row["annotated"])
                    if not annotated:
                        continue
                    label = row["annotator_genre"]
                    if label not in {"Fiction", "Non-fiction"}:
                        continue
                    title = row["Title"]
                    if title in unique:
                        continue
                    unique.add(title)
                    id_ += 1
                    yield id_, {
                        "BL record ID": row["BL record ID"],
                        "title": title,
                        "label": label,
                    }
            if self.config.name == "annotated_raw":
                id_ = 0
                for row in reader:
                    annotated = ast.literal_eval(row["annotated"])
                    if not annotated:
                        continue
                    created_at = datetime.strptime(row["created_at"], "%Y-%m-%d %H:%M:%S %Z")
                    id_ += 1
                    yield id_, {
                        "BL record ID": row["BL record ID"],
                        "Type of resource": row["Type of resource"],
                        "Name": row["Name"],
                        "Dates associated with name": row["Dates associated with name"],
                        "Type of name": row["Type of name"],
                        "Role": row["Role"],
                        "All names": self._parse_all_names(row),
                        "Title": row["Title"],
                        "Variant titles": row["Variant titles"],
                        "Series title": row["Series title"],
                        "Number within series": row["Number within series"],
                        "Country of publication": self._parse_country(row),
                        "Place of publication": self._parse_place_of_publication(row),
                        "Publisher": row["Publisher"],
                        "Date of publication": row["Date of publication"],
                        "Edition": row["Edition"],
                        "Physical description": row["Physical description"],
                        "Dewey classification": row["Dewey classification"],
                        "BL shelfmark": row["BL shelfmark"],
                        "Topics": row["Topics"],
                        "Genre": row["Genre"],
                        "Languages": self._parse_language(row),
                        "Notes": row["Notes"],
                        "BL record ID for physical resource": row["BL record ID for physical resource"],
                        "classification_id": row["classification_id"],
                        "user_id": row["user_id"],
                        "created_at": created_at,
                        "subject_ids": row["subject_ids"],
                        "annotator_date_pub": row["annotator_date_pub"],
                        "annotator_normalised_date_pub": row["annotator_normalised_date_pub"],
                        "annotator_edition_statement": row["annotator_edition_statement"],
                        "annotator_genre": row["annotator_genre"],
                        "annotator_FAST_genre_terms": row["annotator_FAST_genre_terms"],
                        "annotator_FAST_subject_terms": row["annotator_FAST_subject_terms"],
                        "annotator_comments": row["annotator_comments"],
                        "annotator_main_language": row["annotator_main_language"],
                        "annotator_other_languages_summaries": row["annotator_other_languages_summaries"],
                        "annotator_summaries_language": row["annotator_summaries_language"],
                        "annotator_translation": row["annotator_translation"],
                        "annotator_original_language": row["annotator_original_language"],
                        "annotator_publisher": row["annotator_publisher"],
                        "annotator_place_pub": row["annotator_place_pub"],
                        "annotator_country": row["annotator_country"],
                        "annotator_title": row["annotator_title"],
                        "Link to digitised book": row["Link to digitised book"],
                        "annotated": annotated,
                    }
            if self.config.name == "raw":
                for id_, row in enumerate(reader):

                    yield id_, {
                        "BL record ID": row["BL record ID"],
                        "Type of resource": row["Type of resource"],
                        "Name": row["Name"],
                        "Dates associated with name": row["Dates associated with name"],
                        "Type of name": row["Type of name"],
                        "Role": row["Role"],
                        "All names": self._parse_all_names(row),
                        "Title": row["Title"],
                        "Variant titles": row["Variant titles"],
                        "Series title": row["Series title"],
                        "Number within series": row["Number within series"],
                        "Country of publication": self._parse_country(row),
                        "Place of publication": self._parse_place_of_publication(row),
                        "Publisher": row["Publisher"],
                        "Date of publication": row["Date of publication"],
                        "Edition": row["Edition"],
                        "Physical description": row["Physical description"],
                        "Dewey classification": row["Dewey classification"],
                        "BL shelfmark": row["BL shelfmark"],
                        "Topics": row["Topics"],
                        "Genre": row["Genre"],
                        "Languages": self._parse_language(row),
                        "Notes": row["Notes"],
                        "BL record ID for physical resource": row["BL record ID for physical resource"],
                        "classification_id": row["classification_id"],
                        "user_id": row["user_id"],
                        "created_at": row["created_at"],
                        "subject_ids": row["subject_ids"],
                        "annotator_date_pub": row["annotator_date_pub"],
                        "annotator_normalised_date_pub": row["annotator_normalised_date_pub"],
                        "annotator_edition_statement": row["annotator_edition_statement"],
                        "annotator_genre": row["annotator_genre"],
                        "annotator_FAST_genre_terms": row["annotator_FAST_genre_terms"],
                        "annotator_FAST_subject_terms": row["annotator_FAST_subject_terms"],
                        "annotator_comments": row["annotator_comments"],
                        "annotator_main_language": row["annotator_main_language"],
                        "annotator_other_languages_summaries": row["annotator_other_languages_summaries"],
                        "annotator_summaries_language": row["annotator_summaries_language"],
                        "annotator_translation": row["annotator_translation"],
                        "annotator_original_language": row["annotator_original_language"],
                        "annotator_publisher": row["annotator_publisher"],
                        "annotator_place_pub": row["annotator_place_pub"],
                        "annotator_country": row["annotator_country"],
                        "annotator_title": row["annotator_title"],
                        "Link to digitised book": row["Link to digitised book"],
                        "annotated": ast.literal_eval(row["annotated"]),
                    }
