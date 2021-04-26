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
"""Semantic Scholar's records for research papers published in all fields"""


import json
import re

import datasets


_CITATION = """\
@misc{lo2020s2orc,
      title={S2ORC: The Semantic Scholar Open Research Corpus},
      author={Kyle Lo and Lucy Lu Wang and Mark Neumann and Rodney Kinney and Dan S. Weld},
      year={2020},
      eprint={1911.02782},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
A large corpus of 81.1M English-language academic papers spanning many academic disciplines.
Rich metadata, paper abstracts, resolved bibliographic references, as well as structured full
text for 8.1M open access papers. Full text annotated with automatically-detected inline mentions of
citations, figures, and tables, each linked to their corresponding paper objects. Aggregated papers
from hundreds of academic publishers and digital archives into a unified source, and create the largest
publicly-available collection of machine-readable academic text to date.
"""

_HOMEPAGE = "http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/"

_LICENSE = "Semantic Scholar Open Research Corpus is licensed under ODC-BY."

_ROOT_URL = "https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-12-01/"


class S2orc(datasets.GeneratorBasedBuilder):
    """Semantic Scholar's records for research papers published in all fields"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "title": datasets.Value("string"),
                "paperAbstract": datasets.Value("string"),
                "entities": datasets.Sequence(datasets.Value("string")),
                "s2Url": datasets.Value("string"),
                "pdfUrls": datasets.Sequence(datasets.Value("string")),
                "s2PdfUrl": datasets.Value("string"),
                "authors": [
                    {
                        "name": datasets.Value("string"),
                        "ids": datasets.Sequence(datasets.Value("string")),
                    },
                ],
                "inCitations": datasets.Sequence(datasets.Value("string")),
                "outCitations": datasets.Sequence(datasets.Value("string")),
                "fieldsOfStudy": datasets.Sequence(datasets.Value("string")),
                "year": datasets.Value("int32"),
                "venue": datasets.Value("string"),
                "journalName": datasets.Value("string"),
                "journalVolume": datasets.Value("string"),
                "journalPages": datasets.Value("string"),
                "sources": datasets.Sequence(datasets.Value("string")),
                "doi": datasets.Value("string"),
                "doiUrl": datasets.Value("string"),
                "pmid": datasets.Value("string"),
                "magId": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
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
        _MANIFEST_URL = _ROOT_URL + "manifest.txt"
        manifest_file = dl_manager.download_and_extract(_MANIFEST_URL)

        file = open(manifest_file, "r", encoding="utf-8")
        train_names = file.read().splitlines()

        r = re.compile("(?s:s2\\-corpus\\-.*\\.gz)\\Z")  # files are of the form 's2-corpus-*.gz'
        train_names = list(filter(r.match, train_names))

        train_filepaths = dl_manager.download_and_extract([_ROOT_URL + x for x in train_names])

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepaths": train_filepaths,
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepaths, split):
        """Yields examples."""
        for train_files in filepaths:
            with open(train_files, encoding="utf-8") as f:
                for id_, row in enumerate(f):
                    data = json.loads(row)
                    if type(data["year"]) != int:
                        data["year"] = -1
                    yield id_, data
