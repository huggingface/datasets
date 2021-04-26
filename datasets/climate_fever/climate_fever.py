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
"""A dataset adopting the FEVER methodology that consists of 1,535 real-world claims regarding climate-change collected on the internet."""


import json
import os

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@misc{diggelmann2020climatefever,
      title={CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims},
      author={Thomas Diggelmann and Jordan Boyd-Graber and Jannis Bulian and Massimiliano Ciaramita and Markus Leippold},
      year={2020},
      eprint={2012.00614},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

# You can copy an official description
_DESCRIPTION = """\
A dataset adopting the FEVER methodology that consists of 1,535 real-world claims regarding climate-change collected on the internet. Each claim is accompanied by five manually annotated evidence sentences retrieved from the English Wikipedia that support, refute or do not give enough information to validate the claim totalling in 7,675 claim-evidence pairs. The dataset features challenging claims that relate multiple facets and disputed cases of claims where both supporting and refuting evidence are present.
"""

# dataset version (corresponds to release on GitHub)
_VERSION = "1.0.1"

# link to an official homepage
_HOMEPAGE = "http://climatefever.ai"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# url to dataset release on GitHub
_URL = f"https://github.com/tdiggelm/climate-fever-dataset/archive/{_VERSION}.zip"


class ClimateFever(datasets.GeneratorBasedBuilder):
    """CLIMATE-FEVER: A dataset adopting the FEVER methodology that consists of 1,535 real-world claims regarding climate-change collected on the internet. Each claim is accompanied by five manually annotated evidence sentences retrieved from the English Wikipedia that support, refute or do not give enough information to validate the claim totalling in 7,675 claim-evidence pairs. The dataset features challenging claims that relate multiple facets and disputed cases of claims where both supporting and refuting evidence are present."""

    VERSION = datasets.Version(_VERSION)

    def _info(self):

        features = datasets.Features(
            {
                "claim_id": datasets.Value("string"),
                "claim": datasets.Value("string"),
                "claim_label": datasets.ClassLabel(names=["SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO", "DISPUTED"]),
                "evidences": [
                    {
                        "evidence_id": datasets.Value("string"),
                        "evidence_label": datasets.ClassLabel(names=["SUPPORTS", "REFUTES", "NOT_ENOUGH_INFO"]),
                        "article": datasets.Value("string"),
                        "evidence": datasets.Value("string"),
                        "entropy": datasets.Value("float32"),
                        "votes": [datasets.Value("string")],
                    },
                ],
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
        data_dir = dl_manager.download_and_extract(_URL)
        data_dir = os.path.join(data_dir, f"climate-fever-dataset-{_VERSION}", "dataset")
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": os.path.join(data_dir, "climate-fever.jsonl"), "split": "test"},
            ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                doc = json.loads(row)
                yield id_, doc
