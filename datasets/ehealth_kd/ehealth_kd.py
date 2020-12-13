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
"""The eHealth-KD 2020 Corpus."""

from __future__ import absolute_import, division, print_function

import datasets


_CITATION = """\
@inproceedings{overview_ehealthkd2020,
  author    = {Piad{-}Morffis, Alejandro and
               Guti{\'{e}}rrez, Yoan and
               Cañizares-Diaz, Hian and
               Estevez{-}Velarde, Suilan and
               Almeida{-}Cruz, Yudivi{\'{a}}n and
               Muñoz, Rafael and
               Montoyo, Andr{\'{e}}s},
  title     = {Overview of the eHealth Knowledge Discovery Challenge at IberLEF 2020},
  booktitle = ,
  year      = {2020},
}
"""

_DESCRIPTION = """\
This is the dataset of the eHealth-KD Challenge at IberLEF 2020. It is designed for 
the identification of semantic entities and relations in Spanish health documents.
"""

_HOMEPAGE = "https://knowledge-learning.github.io/ehealthkd-2020/"

_LICENSE = "https://creativecommons.org/licenses/by-nc-sa/4.0/"

_URL = "https://raw.githubusercontent.com/knowledge-learning/ehealthkd-2020/master/data/"
_TRAIN_DIR = "training/"
_DEV_DIR = "development/main/"
_TEST_DIR = "testing/scenario1-main/"
_TEXT_FILE = "scenario.txt"
_ANNOTATIONS_FILE = "scenario.ann"


class EHealthKD(datasets.GeneratorBasedBuilder):
    """The eHealth-KD 2020 dataset."""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="ehealth_kd", version=VERSION, description="eHealth-KD dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence": datasets.Value("string"),
                    "entities": [
                        {
                            "ent_id": datasets.Value("string"),
                            "ent_text": datasets.Value("string"),
                            "ent_tag": datasets.Value("string"),
                            "start_character": datasets.Value("int32"),
                            "end_character": datasets.Value("int32"),
                        }
                    ],
                    "relations": [
                        {
                            "rel_id": datasets.Value("string"),
                            "rel_tag": datasets.Value("string"),
                            "arg1": datasets.Value("string"),
                            "arg2": datasets.Value("string"),
                        }
                    ],
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            k: [f"{_URL}{v}{_TEXT_FILE}", f"{_URL}{v}{_ANNOTATIONS_FILE}"]
            for k, v in zip(["train", "dev", "test"], [_TRAIN_DIR, _DEV_DIR, _TEST_DIR])
        }

        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"text_dir": downloaded_files["train"][0], "ann_dir": downloaded_files["train"][1]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"text_dir": downloaded_files["dev"][0], "ann_dir": downloaded_files["dev"][1]},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"text_dir": downloaded_files["test"][0], "ann_dir": downloaded_files["test"][1]},
            ),
        ]

    def _generate_examples(self, text_dir, ann_dir):
        """ Yields examples. """
        with open(text_dir, encoding="utf-8") as txt_file, open(ann_dir, encoding="utf-8") as ann_file:
            _id = 0
            entities = []
            relations = []

            # Create a variable to keep track of the last annotation (entity or relation) to know when a sentence is fully annotated
            # In the annotations file, the entities are before the relations
            last_annotation = ""

            for annotation in ann_file:
                if annotation.startswith("T"):
                    if last_annotation == "relation":
                        sentence = txt_file.readline().strip()
                        yield _id, {"sentence": sentence, "entities": entities, "relations": relations}
                        _id += 1
                        entities = []
                        relations = []

                    ent_id, mid, ent_text = annotation.strip().split("\t")
                    ent_tag, spans = mid.split(" ", 1)
                    start_character = spans.split(" ")[0]
                    end_character = spans.split(" ")[-1]

                    entities.append(
                        {
                            "ent_id": ent_id,
                            "ent_text": ent_text,
                            "ent_tag": ent_tag,
                            "start_character": start_character,
                            "end_character": end_character,
                        }
                    )

                    last_annotation = "entity"

                if annotation.startswith("R"):
                    rel_id, rel_tag, arg1, arg2 = annotation.strip().split()
                    arg1 = arg1.split(":")[1]
                    arg2 = arg2.split(":")[1]

                    relations.append({"rel_id": rel_id, "rel_tag": rel_tag, "arg1": arg1, "arg2": arg2})

                    last_annotation = "relation"
