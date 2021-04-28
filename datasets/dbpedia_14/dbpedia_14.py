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
"""The DBpedia dataset for text classification."""


import csv
import os

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{lehmann2015dbpedia,
  title={DBpedia--a large-scale, multilingual knowledge base extracted from Wikipedia},
  author={Lehmann, Jens and Isele, Robert and Jakob, Max and Jentzsch, Anja and Kontokostas,
  Dimitris and Mendes, Pablo N and Hellmann, Sebastian and Morsey, Mohamed and Van Kleef,
  Patrick and Auer, S{\"o}ren and others},
  journal={Semantic web},
  volume={6},
  number={2},
  pages={167--195},
  year={2015},
  publisher={IOS Press}
}
"""

_DESCRIPTION = """\
The DBpedia ontology classification dataset is constructed by picking 14 non-overlapping classes
from DBpedia 2014. They are listed in classes.txt. From each of thse 14 ontology classes, we
randomly choose 40,000 training samples and 5,000 testing samples. Therefore, the total size
of the training dataset is 560,000 and testing dataset 70,000.
There are 3 columns in the dataset (same for train and test splits), corresponding to class index
(1 to 14), title and content. The title and content are escaped using double quotes ("), and any
internal double quote is escaped by 2 double quotes (""). There are no new lines in title or content.
"""

_HOMEPAGE = "https://wiki.dbpedia.org/develop/datasets"

_LICENSE = "Creative Commons Attribution-ShareAlike 3.0 and the GNU Free Documentation License"

_URLs = {
    "dbpedia_14": "https://drive.google.com/uc?export=download&id=0Bz8a_Dbh9QhbQ2Vic1kxMmZZQ1k",
}


class DBpedia14Config(datasets.BuilderConfig):
    """BuilderConfig for DBpedia."""

    def __init__(self, **kwargs):
        """BuilderConfig for DBpedia.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DBpedia14Config, self).__init__(**kwargs)


class DBpedia14(datasets.GeneratorBasedBuilder):
    """DBpedia 2014 Ontology Classification Dataset."""

    VERSION = datasets.Version("2.0.0")

    BUILDER_CONFIGS = [
        DBpedia14Config(
            name="dbpedia_14", version=VERSION, description="DBpedia 2014 Ontology Classification Dataset."
        ),
    ]

    def _info(self):
        features = datasets.Features(
            {
                "label": datasets.features.ClassLabel(
                    names=[
                        "Company",
                        "EducationalInstitution",
                        "Artist",
                        "Athlete",
                        "OfficeHolder",
                        "MeanOfTransportation",
                        "Building",
                        "NaturalPlace",
                        "Village",
                        "Animal",
                        "Plant",
                        "Album",
                        "Film",
                        "WrittenWork",
                    ]
                ),
                "title": datasets.Value("string"),
                "content": datasets.Value("string"),
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
        my_urls = _URLs[self.config.name]
        data_dir = dl_manager.download_and_extract(my_urls)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dbpedia_csv/train.csv"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "dbpedia_csv/test.csv"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as f:
            data = csv.reader(f, delimiter=",", quoting=csv.QUOTE_NONNUMERIC)
            for id_, row in enumerate(data):
                yield id_, {
                    "title": row[1],
                    "content": row[2],
                    "label": int(row[0]) - 1,
                }
