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
"""TNE: Text-based NP Enrichment"""

import json

import datasets


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@article{tne,
    author = {Elazar, Yanai and Basmov, Victoria and Goldberg, Yoav and Tsarfaty, Reut},
    title = "{Text-based NP Enrichment}",
    journal = {Transactions of the Association for Computational Linguistics},
    year = {2022},
}
"""

# You can copy an official description
_DESCRIPTION = """\
TNE is an NLU task, which focus on relations between noun phrases (NPs) that can be mediated via prepositions.
The dataset contains 5,497 documents, annotated exhaustively with all possible links between the NPs in each document.
"""

_HOMEPAGE = "https://yanaiela.github.io/TNE/"

_LICENSE = "MIT"

_VERSION = "v1.1"

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/yanaiela/TNE/raw/main/data/"
_URLS = {
    "train": _URL + f"train-{_VERSION}.jsonl.gz",
    "dev": _URL + f"dev-{_VERSION}.jsonl.gz",
    "test_unlabeled": _URL + f"test_unlabeled-{_VERSION}.jsonl.gz",
    "ood_unlabeled": _URL + f"ood_unlabeled-{_VERSION}.jsonl.gz",
}


class TNEDataset(datasets.GeneratorBasedBuilder):
    """TNE: Text-based NP Enrichment"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "tokens": datasets.Sequence(datasets.Value("string")),
                "nps": [
                    {
                        "text": datasets.Value("string"),
                        "first_char": datasets.Value("int32"),
                        "last_char": datasets.Value("int32"),
                        "first_token": datasets.Value("int32"),
                        "last_token": datasets.Value("int32"),
                        "id": datasets.Value("string"),
                    }
                ],
                "np_relations": [
                    {
                        "anchor": datasets.Value("string"),
                        "complement": datasets.Value("string"),
                        "preposition": datasets.features.ClassLabel(
                            names=[
                                "about",
                                "for",
                                "with",
                                "from",
                                "among",
                                "by",
                                "on",
                                "at",
                                "during",
                                "of",
                                "member(s) of",
                                "in",
                                "after",
                                "under",
                                "to",
                                "into",
                                "before",
                                "near",
                                "outside",
                                "around",
                                "between",
                                "against",
                                "over",
                                "inside",
                            ]
                        ),
                        "complement_coref_cluster_id": datasets.Value("string"),
                    }
                ],
                "coref": [
                    {
                        "id": datasets.Value("string"),
                        "members": datasets.Sequence(datasets.Value("string")),
                        "np_type": datasets.features.ClassLabel(
                            names=[
                                "standard",
                                "time/date/measurement",
                                "idiomatic",
                            ]
                        ),
                    }
                ],
                "metadata": {
                    "annotators": {
                        "coref_worker": datasets.Value("int32"),
                        "consolidator_worker": datasets.Value("int32"),
                        "np-relations_worker": datasets.Sequence(datasets.Value("int32")),
                    },
                    "url": datasets.Value("string"),
                    "source": datasets.Value("string"),
                },
            }
        )

        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls = _URLS
        data_dir = dl_manager.download_and_extract(urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["train"],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": data_dir["dev"],
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["test_unlabeled"], "split": "test_unlabeled"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split("test_ood"),
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": data_dir["ood_unlabeled"], "split": "ood_unlabeled"},
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, "r", encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)

                ex_id = data["id"]
                text = data["text"]
                tokens = data["tokens"]
                nps = data["nps"]
                if split in ["test_unlabeled", "ood_unlabeled"]:
                    np_relations = []
                else:
                    np_relations = data["np_relations"]
                coref = data["coref"]
                metadata = data["metadata"]

                yield key, {
                    "id": ex_id,
                    "text": text,
                    "tokens": tokens,
                    "nps": nps,
                    "np_relations": np_relations,
                    "coref": coref,
                    "metadata": metadata,
                }
