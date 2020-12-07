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

from __future__ import absolute_import, division, print_function

import ast
import os
from collections import defaultdict

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
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

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This dataset is a new knowledge-base (KB) of hasPart relationships, extracted from a large corpus of generic statements. Complementary to other resources available, it is the first which is all three of: accurate (90% precision), salient (covers relationships a person may mention), and has high coverage of common terms (approximated as within a 10 year old’s vocabulary), as well as having several times more hasPart entries than in the popular ontologies ConceptNet and WordNet. In addition, it contains information about quantifiers, argument modifiers, and links the entities to appropriate concepts in Wikipedia and WordNet.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://allenai.org/data/haspartkb"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""


class HasPart(datasets.GeneratorBasedBuilder):
    @property
    def manual_download_instructions(self):
        return """\
  You should download the dataset from https://allenai.org/data/haspartkb
  Download hasPartKB.tsv to a dir of your choice,
  which will be used as a manual_dir, e.g. `~/.manual_dir/has_part`
  The data can then be loaded via:
  `datasets.load_dataset("has_part", data_dir="~/.manual_dir/has_part")`.
  """

    def _info(self):
        features = datasets.Features(
            {
                "arg1": datasets.features.Value("string"),
                "arg2": datasets.features.Value("string"),
                "score": datasets.features.Value("float64"),
                "wikipedia_primary_page": datasets.features.Sequence(
                    datasets.features.Value("string")
                ),
                "synset": datasets.features.Sequence(datasets.features.Value("string")),
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

        data_dir = os.path.abspath(os.path.expanduser(dl_manager.manual_dir))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                "{} does not exist. Make sure you insert a manual dir via `datasets.load_dataset('has_part', data_dir=...)` per the manual download instructions: {}".format(
                    data_dir, self.manual_download_instructions
                )
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "input_file": os.path.join(data_dir, "hasPartKB.tsv"),
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
        """ Yields examples. """
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
