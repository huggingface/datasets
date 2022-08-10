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
"""The LAMA Dataset"""


import json
from fnmatch import fnmatch

import datasets


_CITATION = """@inproceedings{petroni2019language,
  title={Language Models as Knowledge Bases?},
  author={F. Petroni, T. Rockt{\"{a}}schel, A. H. Miller, P. Lewis, A. Bakhtin, Y. Wu and S. Riedel},
  booktitle={In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP), 2019},
  year={2019}
}
@inproceedings{petroni2020how,
  title={How Context Affects Language Models' Factual Predictions},
  author={Fabio Petroni and Patrick Lewis and Aleksandra Piktus and Tim Rockt{\"a}schel and Yuxiang Wu and Alexander H. Miller and Sebastian Riedel},
  booktitle={Automated Knowledge Base Construction},
  year={2020},
  url={https://openreview.net/forum?id=025X0zPfn}
}
"""


_DESCRIPTION = """LAMA is a dataset used to probe and analyze the factual and commonsense knowledge contained in pretrained language models. See https://github.com/facebookresearch/LAMA.
"""

_HOMEPAGE = "https://github.com/facebookresearch/LAMA"

_LICENSE = "The Creative Commons Attribution-Noncommercial 4.0 International License. see https://github.com/facebookresearch/LAMA/blob/master/LICENSE"

_RELATIONS_URL = "https://s3.amazonaws.com/datasets.huggingface.co/lama/relations.jsonl"

_DATA_URL = "https://dl.fbaipublicfiles.com/LAMA/negated_data.tar.gz"


class Lama(datasets.GeneratorBasedBuilder):
    """Lama Dataset"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="trex", version=VERSION, description="The TRex part of the Lama dataset"),
        datasets.BuilderConfig(name="squad", version=VERSION, description="The Squad part of the Lama dataset"),
        datasets.BuilderConfig(
            name="google_re", version=VERSION, description="The Google_re part of the Lama dataset"
        ),
        datasets.BuilderConfig(
            name="conceptnet", version=VERSION, description="The Conceptnet part of the Lama dataset"
        ),
    ]

    DEFAULT_CONFIG_NAME = "trex"

    def _info(self):
        if self.config.name == "trex":
            features = datasets.Features(
                {
                    "uuid": datasets.Value("string"),
                    "obj_uri": datasets.Value("string"),
                    "obj_label": datasets.Value("string"),
                    "sub_uri": datasets.Value("string"),
                    "sub_label": datasets.Value("string"),
                    "predicate_id": datasets.Value("string"),
                    "sub_surface": datasets.Value("string"),
                    "obj_surface": datasets.Value("string"),
                    "masked_sentence": datasets.Value("string"),
                    "template": datasets.Value("string"),
                    "template_negated": datasets.Value("string"),
                    "label": datasets.Value("string"),
                    "description": datasets.Value("string"),
                    "type": datasets.Value("string"),
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
        elif self.config.name == "conceptnet":
            features = datasets.Features(
                {
                    "uuid": datasets.Value("string"),
                    "sub": datasets.Value("string"),
                    "obj": datasets.Value("string"),
                    "pred": datasets.Value("string"),
                    "obj_label": datasets.Value("string"),
                    "masked_sentence": datasets.Value("string"),
                    "negated": datasets.Value("string"),
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
        elif self.config.name == "squad":
            features = datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "sub_label": datasets.Value("string"),
                    "obj_label": datasets.Value("string"),
                    "negated": datasets.Value("string"),
                    "masked_sentence": datasets.Value("string"),
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
        elif self.config.name == "google_re":
            features = datasets.Features(
                {
                    "pred": datasets.Value("string"),
                    "sub": datasets.Value("string"),
                    "obj": datasets.Value("string"),
                    "evidences": datasets.Value("string"),
                    "judgments": datasets.Value("string"),
                    "sub_w": datasets.Value("string"),
                    "sub_label": datasets.Value("string"),
                    "sub_aliases": datasets.Value("string"),
                    "obj_w": datasets.Value("string"),
                    "obj_label": datasets.Value("string"),
                    "obj_aliases": datasets.Value("string"),
                    "uuid": datasets.Value("string"),
                    "masked_sentence": datasets.Value("string"),
                    "template": datasets.Value("string"),
                    "template_negated": datasets.Value("string"),
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
        archive = dl_manager.download(_DATA_URL)
        if self.config.name == "trex":
            relations_path = dl_manager.download(_RELATIONS_URL)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepaths": ["TREx/*"],
                        "files": dl_manager.iter_archive(archive),
                        "relations_path": relations_path,
                    },
                ),
            ]
        elif self.config.name == "google_re":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepaths": [
                            "Google_RE/date_of_birth_test.jsonl",
                            "Google_RE/place_of_birth_test.jsonl",
                            "Google_RE/place_of_death_test.jsonl",
                        ],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        elif self.config.name == "conceptnet":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepaths": ["ConceptNet/test.jsonl"],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]
        elif self.config.name == "squad":
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepaths": ["Squad/test.jsonl"],
                        "files": dl_manager.iter_archive(archive),
                    },
                ),
            ]

    def _generate_examples(self, filepaths, files, relations_path=None):
        """Yields examples from the LAMA dataset."""
        filepaths = list(filepaths)
        if self.config.name == "trex":
            all_rels = {}
            with open(relations_path, encoding="utf-8") as f:
                for row in f:
                    data = json.loads(row)
                    all_rels[data["relation"]] = data
            id_ = -1
            inside_trec_directory = False
            for path, f in files:
                if any(fnmatch(path, pattern) for pattern in filepaths):
                    inside_trec_directory = True
                    for row in f:
                        data = json.loads(row)
                        pred = all_rels.get(data["predicate_id"], {})
                        for evidences in data["evidences"]:
                            id_ += 1
                            yield id_, {
                                "uuid": str(data["uuid"]),
                                "obj_uri": str(data["obj_uri"]),
                                "obj_label": str(data["obj_label"]),
                                "sub_uri": str(data["sub_uri"]),
                                "sub_label": str(data["sub_label"]),
                                "predicate_id": str(data["predicate_id"]),
                                "sub_surface": str(evidences["sub_surface"]),
                                "obj_surface": str(evidences["obj_surface"]),
                                "masked_sentence": str(evidences["masked_sentence"]),
                                "template": str(pred.get("template", "")),
                                "template_negated": str(pred.get("template_negated", "")),
                                "label": str(pred.get("label", "")),
                                "description": str(pred.get("description", "")),
                                "type": str(pred.get("type", "")),
                            }
                elif inside_trec_directory:
                    break
        elif self.config.name == "conceptnet":
            id_ = -1
            for path, f in files:
                if not filepaths:
                    break
                if path in list(filepaths):
                    for row in f:
                        data = json.loads(row)
                        if data.get("negated") is not None:
                            for masked_sentence, negated in zip(data["masked_sentences"], data["negated"]):
                                id_ += 1
                                yield id_, {
                                    "uuid": str(data["uuid"]),
                                    "sub": str(data.get("sub", "")),
                                    "obj": str(data.get("obj", "")),
                                    "pred": str(data["pred"]),
                                    "obj_label": str(data["obj_label"]),
                                    "masked_sentence": str(masked_sentence),
                                    "negated": str(negated),
                                }
                        else:
                            for masked_sentence in data["masked_sentences"]:
                                id_ += 1
                                yield id_, {
                                    "uuid": str(data["uuid"]),
                                    "sub": str(data.get("sub", "")),
                                    "obj": str(data.get("obj", "")),
                                    "pred": str(data["pred"]),
                                    "obj_label": str(data["obj_label"]),
                                    "masked_sentence": str(masked_sentence),
                                    "negated": str(""),
                                }
                    filepaths.remove(path)
        elif self.config.name == "squad":
            id_ = -1
            for path, f in files:
                if not filepaths:
                    break
                if path in filepaths:
                    for row in f:
                        data = json.loads(row)
                        for masked_sentence in data["masked_sentences"]:
                            id_ += 1
                            yield id_, {
                                "id": str(data["id"]),
                                "sub_label": str(data["sub_label"]),
                                "obj_label": str(data["obj_label"]),
                                "negated": str(data.get("negated", "")),
                                "masked_sentence": str(masked_sentence),
                            }
                    filepaths.remove(path)
        elif self.config.name == "google_re":
            id_ = -1
            for path, f in files:
                if path in filepaths:
                    if not filepaths:
                        break
                    if path in filepaths:
                        # from https://github.com/facebookresearch/LAMA/blob/master/scripts/run_experiments.py
                        if "place_of_birth" in path:
                            pred = {
                                "relation": "place_of_birth",
                                "template": "[X] was born in [Y] .",
                                "template_negated": "[X] was not born in [Y] .",
                            }
                        elif "date_of_birth" in path:
                            pred = {
                                "relation": "date_of_birth",
                                "template": "[X] (born [Y]).",
                                "template_negated": "[X] (not born [Y]).",
                            }
                        else:
                            pred = {
                                "relation": "place_of_death",
                                "template": "[X] died in [Y] .",
                                "template_negated": "[X] did not die in [Y] .",
                            }
                        for row in f:
                            data = json.loads(row)
                            for masked_sentence in data["masked_sentences"]:
                                id_ += 1
                                yield id_, {
                                    "pred": str(data["pred"]),
                                    "sub": str(data["sub"]),
                                    "obj": str(data["obj"]),
                                    "evidences": str(data["evidences"]),
                                    "judgments": str(data["judgments"]),
                                    "sub_w": str(data["sub_w"]),
                                    "sub_label": str(data["sub_label"]),
                                    "sub_aliases": str(data["sub_aliases"]),
                                    "obj_w": str(data["obj_w"]),
                                    "obj_label": str(data["obj_label"]),
                                    "obj_aliases": str(data["obj_aliases"]),
                                    "uuid": str(data["uuid"]),
                                    "masked_sentence": str(masked_sentence),
                                    "template": str(pred["template"]),
                                    "template_negated": str(pred["template_negated"]),
                                }
                        filepaths.remove(path)
