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
"""This dataset is a new knowledge-base (KB) of hasPart relationships, extracted from a large corpus of generic statements. Complementary to other resources available, it is the first which is all three of: accurate (90% precision), salient (covers relationships a person may mention), and has high coverage of common terms (approximated as within a 10 year old’s vocabulary), as well as having several times more hasPart entries than in the popular ontologies ConceptNet and WordNet. In addition, it contains information about quantifiers, argument modifiers, and links the entities to appropriate concepts in Wikipedia and WordNet."""


import ast
from collections import defaultdict

import datasets


_CITATION = """\
@misc{bhakthavatsalam2020dogs,
      title={Do Dogs have Whiskers? A New Knowledge Base of hasPart Relations},
      author={Sumithra Bhakthavatsalam and Kyle Richardson and Niket Tandon and Peter Clark},
      year={2020},
      eprint={2006.07510},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
This dataset is a new knowledge-base (KB) of hasPart relationships, extracted from a large corpus of generic statements. Complementary to other resources available, it is the first which is all three of: accurate (90% precision), salient (covers relationships a person may mention), and has high coverage of common terms (approximated as within a 10 year old’s vocabulary), as well as having several times more hasPart entries than in the popular ontologies ConceptNet and WordNet. In addition, it contains information about quantifiers, argument modifiers, and links the entities to appropriate concepts in Wikipedia and WordNet.
"""

_HOMEPAGE = "https://allenai.org/data/haspartkb"

_LICENSE = ""


TSV_ID = "1Ev4RqWcPsLI9rgOGAKh-_dFKqcEZ1u-G"
FOLDER_ID = "1NzjXX46NnpxtgxBrkBWFiUbsXAMdd-lB"
ID = TSV_ID

_URL = f"https://drive.google.com/uc?export=download&id={ID}"


class HasPart(datasets.GeneratorBasedBuilder):
    def _info(self):
        features = datasets.Features(
            {
                "arg1": datasets.features.Value("string"),
                "arg2": datasets.features.Value("string"),
                "score": datasets.features.Value("float64"),
                "wikipedia_primary_page": datasets.features.Sequence(datasets.features.Value("string")),
                "synset": datasets.features.Sequence(datasets.features.Value("string")),
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

        dl_fp = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "input_file": dl_fp,
                    "split": "train",
                },
            ),
        ]

    def _parse_metadata(self, md):
        """metadata is a list of dicts in the tsv file, hence needs to be parsed using
        ast.literal_eval to convert to python objects.

        Note that metadata resulting in parsing error will be skipped
        """
        md = ast.literal_eval(md)
        dd = defaultdict(list)

        for entry in md:
            try:
                for k, v in entry.items():
                    dd[k].append(v)
            except AttributeError:
                continue
        return dd

    def _generate_examples(self, input_file, split):
        """Yields examples."""
        with open(input_file, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                _, arg1, arg2, score, metadata = line.split("\t")
                metadata = self._parse_metadata(metadata)
                example = {
                    "arg1": arg1,
                    "arg2": arg2,
                    "score": float(score),
                    "wikipedia_primary_page": metadata["wikipedia_primary_page"],
                    "synset": metadata["synset"],
                }
                yield id_, example
