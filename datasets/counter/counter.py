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


import xml.etree.ElementTree as ET
from pathlib import Path

import datasets


_CITATION = """\
@Article{Sharjeel2016,
author="Sharjeel, Muhammad
and Nawab, Rao Muhammad Adeel
and Rayson, Paul",
title="COUNTER: corpus of Urdu news text reuse",
journal="Language Resources and Evaluation",
year="2016",
pages="1--27",
issn="1574-0218",
doi="10.1007/s10579-016-9367-2",
url="http://dx.doi.org/10.1007/s10579-016-9367-2"
}
"""

_DESCRIPTION = """\
 The COrpus of Urdu News TExt Reuse (COUNTER) corpus contains 1200 documents with real examples of text reuse from the field of journalism. It has been manually annotated at document level with three levels of reuse: wholly derived, partially derived and non derived.
"""

_HOMEPAGE = "http://ucrel.lancs.ac.uk/textreuse/counter.php"

_LICENSE = (
    "The corpus is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. "
)

_DOWNLOAD_URL = "http://ucrel.lancs.ac.uk/textreuse/COUNTER.zip"

_NUM_EXAMPLES = 600

_CLASS_NAME_MAP = {"WD": "wholly_derived", "PD": "partially_derived", "ND": "not_derived"}


class Counter(datasets.GeneratorBasedBuilder):
    """Corpus of Urdu News Text Reuse"""

    VERSION = datasets.Version("1.0.0")

    def _info(self):
        features = datasets.Features(
            {
                "source": {
                    "filename": datasets.Value("string"),
                    "headline": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "total_number_of_words": datasets.Value("int64"),
                    "total_number_of_sentences": datasets.Value("int64"),
                    "number_of_words_with_swr": datasets.Value("int64"),
                    "newspaper": datasets.Value("string"),
                    "newsdate": datasets.Value("string"),
                    "domain": datasets.ClassLabel(
                        names=[
                            "business",
                            "sports",
                            "national",
                            "foreign",
                            "showbiz",
                        ]
                    ),
                    "classification": datasets.ClassLabel(
                        names=["wholly_derived", "partially_derived", "not_derived"]
                    ),
                },
                "derived": {
                    "filename": datasets.Value("string"),
                    "headline": datasets.Value("string"),
                    "body": datasets.Value("string"),
                    "total_number_of_words": datasets.Value("int64"),
                    "total_number_of_sentences": datasets.Value("int64"),
                    "number_of_words_with_swr": datasets.Value("int64"),
                    "newspaper": datasets.Value("string"),
                    "newsdate": datasets.Value("string"),
                    "domain": datasets.ClassLabel(
                        names=[
                            "business",
                            "sports",
                            "national",
                            "foreign",
                            "showbiz",
                        ]
                    ),
                    "classification": datasets.ClassLabel(
                        names=["wholly_derived", "partially_derived", "not_derived"]
                    ),
                },
            }
        )
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
        data_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"data_dir": data_dir},
            )
        ]

    def _generate_examples(self, data_dir):
        """Yields examples."""

        def parse_file(file):
            tree = ET.parse(file)
            root = tree.getroot()
            attributes = root.attrib
            headline = root.find("headline").text
            body = root.find("body").text
            parsed = {
                "filename": attributes["filename"],
                "headline": headline,
                "body": body,
                "total_number_of_words": int(attributes["totalnoofwords"]),
                "total_number_of_sentences": int(attributes["totalnoofsentences"]),
                "number_of_words_with_swr": int(attributes["noofwordswithSWR"]),
                "newspaper": attributes["newspaper"],
                "newsdate": attributes["newsdate"],
                "domain": attributes["domain"],
                "classification": _CLASS_NAME_MAP[attributes["classification"]],
            }
            return parsed

        base_path = Path(data_dir)
        base_path = base_path / "COUNTER"
        files = sorted(base_path.glob(r"[0-9][0-9][0-9][0-9].xml"))
        for _id, file in enumerate(files):
            example = {}
            with file.open(encoding="utf-8") as f:
                source = parse_file(f)
                example["source"] = source

            if file.stem == "0032":
                derived_file = base_path / (file.stem + "P" + file.suffix)
            else:
                derived_file = base_path / (file.stem + "p" + file.suffix)
            with derived_file.open(encoding="utf-8") as f:
                derived = parse_file(f)
                example["derived"] = derived
            yield _id, example
