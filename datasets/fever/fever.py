# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace Datasets Authors.
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

# Lint as: python3
"""FEVER dataset."""


import json
import os

import datasets


_CITATION = """
@inproceedings{Thorne18Fever,
    author = {Thorne, James and Vlachos, Andreas and Christodoulopoulos, Christos and Mittal, Arpit},
    title = {{FEVER}: a Large-scale Dataset for Fact Extraction and VERification},
    booktitle = {NAACL-HLT},
    year = {2018}
}
}
"""

_DESCRIPTION = """
With billions of individual pages on the web providing information on almost every conceivable topic, we should have the ability to collect facts that answer almost every conceivable question. However, only a small fraction of this information is contained in structured sources (Wikidata, Freebase, etc.) – we are therefore limited by our ability to transform free-form text to structured knowledge. There is, however, another problem that has become the focus of a lot of recent research and media coverage: false information coming from unreliable sources. [1] [2]

The FEVER workshops are a venue for work in verifiable knowledge extraction and to stimulate progress in this direction.
"""


class FeverConfig(datasets.BuilderConfig):
    """BuilderConfig for FEVER."""

    def __init__(self, **kwargs):
        """BuilderConfig for FEVER

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(FeverConfig, self).__init__(**kwargs)


class Fever(datasets.GeneratorBasedBuilder):
    """Fact Extraction and VERification Dataset."""

    BUILDER_CONFIGS = [
        FeverConfig(
            name="v1.0",
            description="FEVER  V1.0",
            version=datasets.Version("1.0.0", ""),
        ),
        FeverConfig(
            name="v2.0",
            description="FEVER  V2.0",
            version=datasets.Version("2.0.0", ""),
        ),
        FeverConfig(
            name="wiki_pages",
            description="Wikipedia pages",
            version=datasets.Version("1.0.0", ""),
        ),
    ]

    def _info(self):

        if self.config.name == "wiki_pages":
            features = {
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
                "lines": datasets.Value("string"),
            }
        else:
            features = {
                "id": datasets.Value("int32"),
                "label": datasets.Value("string"),
                "claim": datasets.Value("string"),
                "evidence_annotation_id": datasets.Value("int32"),
                "evidence_id": datasets.Value("int32"),
                "evidence_wiki_url": datasets.Value("string"),
                "evidence_sentence_id": datasets.Value("int32"),
            }
        return datasets.DatasetInfo(
            description=_DESCRIPTION + "\n" + self.config.description,
            features=datasets.Features(features),
            homepage="https://fever.ai/",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        if self.config.name == "v2.0":
            urls = "https://s3-eu-west-1.amazonaws.com/fever.public/fever2-fixers-dev.jsonl"
            dl_path = dl_manager.download_and_extract(urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": dl_path,
                    },
                )
            ]
        elif self.config.name == "v1.0":
            urls = {
                "train": "https://s3-eu-west-1.amazonaws.com/fever.public/train.jsonl",
                "labelled_dev": "https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_dev.jsonl",
                "unlabelled_dev": "https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_dev_public.jsonl",
                "unlabelled_test": "https://s3-eu-west-1.amazonaws.com/fever.public/shared_task_test.jsonl",
                "paper_dev": "https://s3-eu-west-1.amazonaws.com/fever.public/paper_dev.jsonl",
                "paper_test": "https://s3-eu-west-1.amazonaws.com/fever.public/paper_test.jsonl",
            }
            dl_path = dl_manager.download_and_extract(urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": dl_path["train"],
                    },
                ),
                datasets.SplitGenerator(
                    name="unlabelled_test",
                    gen_kwargs={
                        "filepath": dl_path["unlabelled_test"],
                    },
                ),
                datasets.SplitGenerator(
                    name="unlabelled_dev",
                    gen_kwargs={
                        "filepath": dl_path["unlabelled_dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name="labelled_dev",
                    gen_kwargs={
                        "filepath": dl_path["labelled_dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name="paper_dev",
                    gen_kwargs={
                        "filepath": dl_path["paper_dev"],
                    },
                ),
                datasets.SplitGenerator(
                    name="paper_test",
                    gen_kwargs={
                        "filepath": dl_path["paper_test"],
                    },
                ),
            ]
        elif self.config.name == "wiki_pages":
            urls = "https://s3-eu-west-1.amazonaws.com/fever.public/wiki-pages.zip"
            dl_path = dl_manager.download_and_extract(urls)
            files = sorted(os.listdir(os.path.join(dl_path, "wiki-pages")))
            file_paths = [os.path.join(dl_path, "wiki-pages", file) for file in files]
            return [
                datasets.SplitGenerator(
                    name="wikipedia_pages",
                    gen_kwargs={
                        "filepath": file_paths,
                    },
                ),
            ]
        else:
            raise ValueError("config name not found")

    def _generate_examples(self, filepath):
        """Yields examples."""
        if self.config.name == "v1.0" or self.config.name == "v2.0":
            with open(filepath, encoding="utf-8") as f:
                for row_id, row in enumerate(f):
                    data = json.loads(row)
                    id_ = data["id"]
                    label = data.get("label", "")
                    claim = data["claim"]
                    evidences = data.get("evidence", [])
                    if len(evidences) > 0:
                        for i in range(len(evidences)):
                            for j in range(len(evidences[i])):
                                annot_id = evidences[i][j][0] if evidences[i][j][0] else -1
                                evidence_id = evidences[i][j][1] if evidences[i][j][1] else -1
                                wiki_url = evidences[i][j][2] if evidences[i][j][2] else ""
                                sent_id = evidences[i][j][3] if evidences[i][j][3] else -1
                                yield str(row_id) + "_" + str(i) + "_" + str(j), {
                                    "id": id_,
                                    "label": label,
                                    "claim": claim,
                                    "evidence_annotation_id": annot_id,
                                    "evidence_id": evidence_id,
                                    "evidence_wiki_url": wiki_url,
                                    "evidence_sentence_id": sent_id,
                                }
                    else:
                        yield row_id, {
                            "id": id_,
                            "label": label,
                            "claim": claim,
                            "evidence_annotation_id": -1,
                            "evidence_id": -1,
                            "evidence_wiki_url": "",
                            "evidence_sentence_id": -1,
                        }
        elif self.config.name == "wiki_pages":
            for file_id, file in enumerate(filepath):
                with open(file, encoding="utf-8") as f:
                    for row_id, row in enumerate(f):
                        data = json.loads(row)
                        yield f"{file_id}_{row_id}", data
