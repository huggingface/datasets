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
"""TODO: Add a description here."""


import os

import datasets


logger = datasets.logging.get_logger(__name__)


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings@article{DBLP:journals/corr/SahinTYES17,
  author    = {H. Bahadir Sahin and
               Caglar Tirkaz and
               Eray Yildiz and
               Mustafa Tolga Eren and
               Omer Ozan Sonmez},
  title     = {Automatically Annotated Turkish Corpus for Named Entity Recognition
               and Text Categorization using Large-Scale Gazetteers},
  journal   = {CoRR},
  volume    = {abs/1702.02363},
  year      = {2017},
  url       = {http://arxiv.org/abs/1702.02363},
  archivePrefix = {arXiv},
  eprint    = {1702.02363},
  timestamp = {Mon, 13 Aug 2018 16:46:36 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/SahinTYES17.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
Turkish Wikipedia Named-Entity Recognition and Text Categorization
(TWNERTC) dataset is a collection of automatically categorized and annotated
sentences obtained from Wikipedia. The authors constructed large-scale
gazetteers by using a graph crawler algorithm to extract
relevant entity and domain information
from a semantic knowledge base, Freebase.
The constructed gazetteers contains approximately
300K entities with thousands of fine-grained entity types
under 77 different domains.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://data.mendeley.com/datasets/cdcztymf4k/1"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = "Creative Commons Attribution 4.0 International"

_URL = "https://data.mendeley.com/public-files/datasets/cdcztymf4k/files/5557ef78-7d53-4a01-8241-3173c47bbe10/file_downloaded"


_FILE_NAME_ZIP = "TWNERTC_TC_Coarse Grained NER_DomainIndependent_NoiseReduction.zip"
_FILE_NAME = "TWNERTC_TC_Coarse Grained NER_DomainIndependent_NoiseReduction.DUMP"


class TurkishNER(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "domain": datasets.ClassLabel(
                        names=[
                            "architecture",
                            "basketball",
                            "book",
                            "business",
                            "education",
                            "fictional_universe",
                            "film",
                            "food",
                            "geography",
                            "government",
                            "law",
                            "location",
                            "military",
                            "music",
                            "opera",
                            "organization",
                            "people",
                            "religion",
                            "royalty",
                            "soccer",
                            "sports",
                            "theater",
                            "time",
                            "travel",
                            "tv",
                        ]
                    ),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "O",
                                "B-PERSON",
                                "I-PERSON",
                                "B-ORGANIZATION",
                                "I-ORGANIZATION",
                                "B-LOCATION",
                                "I-LOCATION",
                                "B-MISC",
                                "I-MISC",
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
        data_dir = dl_manager.extract(os.path.join(dl_manager.download_and_extract(_URL), _FILE_NAME_ZIP))
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": (os.path.join(data_dir, _FILE_NAME)),
                    "split": "train",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        logger.info("⏳ Generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as f:
            id_ = -1
            for line in f:
                if line == "" or line == "\n":
                    continue
                else:
                    splits = line.split("\t")
                    id_ += 1
                    yield id_, {
                        "id": str(id_),
                        "domain": splits[0],
                        "tokens": splits[2].split(" "),
                        "ner_tags": splits[1].split(" "),
                    }
