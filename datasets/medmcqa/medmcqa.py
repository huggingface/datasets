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
"""MedMCQA : A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering"""


import json
import os

import datasets


_DESCRIPTION = """\
MedMCQA is a large-scale, Multiple-Choice Question Answering (MCQA) dataset designed to address real-world medical entrance exam questions. 
MedMCQA has more than 194k high-quality AIIMS & NEET PG entrance exam MCQs covering 2.4k healthcare topics and 21 medical subjects are collected with an average token length of 12.77 and high topical diversity.
The dataset contains questions about the following topics: Anesthesia, Anatomy, Biochemistry, Dental, ENT, Forensic Medicine (FM)
Obstetrics and Gynecology (O&G), Medicine, Microbiology, Ophthalmology, Orthopedics Pathology, Pediatrics, Pharmacology, Physiology, 
Psychiatry, Radiology Skin, Preventive & Social Medicine (PSM) and Surgery
"""


_HOMEPAGE = "https://medmcqa.github.io"

_LICENSE = "Apache License 2.0"
_URL = "https://drive.google.com/uc?export=download&id=15VkJdq5eyWIkfb_aoD3oS8i4tScbHYky"
_CITATION = "CHILL'2022"


class MedMCQA(datasets.GeneratorBasedBuilder):
    """MedMCQA : A Large-scale Multi-Subject Multi-Choice Dataset for Medical domain Question Answering"""

    VERSION = datasets.Version("1.1.0")

    def _info(self):

        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "question": datasets.Value("string"),
                "opa": datasets.Value("string"),
                "opb": datasets.Value("string"),
                "opc": datasets.Value("string"),
                "opd": datasets.Value("string"),
                "cop": datasets.Value("string"),
                "choice_type": datasets.Value("string"),
                "exp": datasets.Value("string"),
                "subject_name": datasets.Value("string"),
                "topic_name": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_URL)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.json"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.json"),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):

        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                key = data["id"]
                yield key, {
                    "id": key,
                    "question": data["question"],
                    "opa": data["opa"],
                    "opb": data["opb"],
                    "opc": data["opc"],
                    "opd": data["opd"],
                    "cop": "" if split == "test" else int(data["cop"]),
                    "choice_type": data["choice_type"],
                    "exp": "" if split == "test" else data["exp"],
                    "subject_name": data["subject_name"],
                    "topic_name": data["topic_name"],
                }
