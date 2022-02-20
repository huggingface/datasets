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


import json

import datasets


# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
  @inproceedings{mahendra-etal-2021-indonli,
    title = "{I}ndo{NLI}: A Natural Language Inference Dataset for {I}ndonesian",
    author = "Mahendra, Rahmad and Aji, Alham Fikri and Louvan, Samuel and Rahman, Fahrurrozi and Vania, Clara",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.821",
    pages = "10511--10527",
  }
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
  IndoNLI is the first human-elicited Natural Language Inference (NLI) dataset for Indonesian.
  IndoNLI is annotated by both crowd workers and experts. The expert-annotated data is used exclusively as a test set.
  It is designed to provide a challenging test-bed for Indonesian NLI by explicitly incorporating various linguistic phenomena such as numerical reasoning, structural changes, idioms, or temporal and spatial reasoning.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "https://github.com/ir-nlp-csui/indonli"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = """
  CC BY-SA 4.0

  Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

  ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

  No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

"""

_TRAIN_DOWNLOAD_URL = "https://raw.githubusercontent.com/ir-nlp-csui/indonli/main/data/indonli/train.jsonl"

_VALID_DOWNLOAD_URL = "https://raw.githubusercontent.com/ir-nlp-csui/indonli/main/data/indonli/val.jsonl"

_TEST_LAY_DOWNLOAD_URL = "https://raw.githubusercontent.com/ir-nlp-csui/indonli/main/data/indonli/test_lay.jsonl"

_TEST_EXPERT_DOWNLOAD_URL = "https://raw.githubusercontent.com/ir-nlp-csui/indonli/main/data/indonli/test_expert.jsonl"


class IndoNLIConfig(datasets.BuilderConfig):
    """BuilderConfig for IndoNLI Config"""

    def __init__(self, **kwargs):
        """BuilderConfig for IndoNLI Config.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(IndoNLIConfig, self).__init__(**kwargs)


class IndoNLI(datasets.GeneratorBasedBuilder):
    """IndoNLI dataset -- Dataset providing natural language inference for Indonesian"""

    BUILDER_CONFIGS = [
        IndoNLIConfig(
            name="indonli",
            version=datasets.Version("1.1.0"),
            description="IndoNLI: A Natural Language Inference Dataset for Indonesian",
        ),
    ]

    def _info(self):

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "premise": datasets.Value("string"),
                    "hypothesis": datasets.Value("string"),
                    "label": datasets.ClassLabel(names=["entailment", "neutral", "contradiction"]),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        train_path = dl_manager.download_and_extract(_TRAIN_DOWNLOAD_URL)
        valid_path = dl_manager.download_and_extract(_VALID_DOWNLOAD_URL)
        test_lay_path = dl_manager.download_and_extract(_TEST_LAY_DOWNLOAD_URL)
        test_expert_path = dl_manager.download_and_extract(_TEST_EXPERT_DOWNLOAD_URL)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": train_path}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": valid_path}),
            datasets.SplitGenerator(name=datasets.Split("test_lay"), gen_kwargs={"filepath": test_lay_path}),
            datasets.SplitGenerator(name=datasets.Split("test_expert"), gen_kwargs={"filepath": test_expert_path}),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""

        with open(filepath, encoding="utf-8") as jsonl_file:
            for id_, row in enumerate(jsonl_file):
                row_jsonl = json.loads(row)
                yield id_, {
                    "premise": row_jsonl["premise"],
                    "hypothesis": row_jsonl["hypothesis"],
                    "label": {"e": "entailment", "n": "neutral", "c": "contradiction"}[row_jsonl["label"]],
                }
