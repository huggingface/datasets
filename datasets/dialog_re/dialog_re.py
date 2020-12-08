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

"""DialogRE: the first human-annotated dialogue-based relation extraction dataset"""

from __future__ import absolute_import, division, print_function

import json
import os

import datasets


_CITATION = """\
@inproceedings{yu2020dialogue,
  title={Dialogue-Based Relation Extraction},
  author={Yu, Dian and Sun, Kai and Cardie, Claire and Yu, Dong},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
  year={2020},
  url={https://arxiv.org/abs/2004.08056v1}
}
"""

_DESCRIPTION = """\
DialogRE is the first human-annotated dialogue based relation extraction (RE) dataset aiming
to support the prediction of relation(s) between two arguments that appear in a dialogue.
The dataset annotates all occurrences of 36 possible relation types that exist between pairs
of arguments in the 1,788 dialogues originating from the complete transcripts of Friends.
"""

_HOMEPAGE = "https://github.com/nlpdata/dialogre"

_LICENSE = "https://github.com/nlpdata/dialogre/blob/master/license.txt"

_URL = "https://raw.githubusercontent.com/nlpdata/dialogre/master/data_v2/en/data/"
_URLs = {
    "train": _URL + "train.json",
    "dev": _URL + "dev.json",
    "test": _URL + "test.json",
}


class DialogREConfig(datasets.BuilderConfig):
    """BuilderConfig for DialogRE"""

    def __init__(self, **kwargs):
        """BuilderConfig for DialogRE.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(DialogREConfig, self).__init__(**kwargs)


class DialogRE(datasets.GeneratorBasedBuilder):
    """DialogRE: Human-annotated dialogue-based relation extraction dataset Version 2"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        DialogREConfig(
            name="dialog_re",
            version=datasets.Version("1.1.0"),
            description="DialogRE: Human-annotated dialogue-based relation extraction dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "dialog": datasets.Sequence(datasets.Value("string")),
                    "relation_data": datasets.Sequence(
                        {
                            "x": datasets.Value("string"),
                            "y": datasets.Value("string"),
                            "x_type": datasets.Value("string"),
                            "y_type": datasets.Value("string"),
                            "r": datasets.Sequence(datasets.Value("string")),
                            "rid": datasets.Sequence(datasets.Value("int32")),
                            "t": datasets.Sequence(datasets.Value("string")),
                        }
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""

        data_dir = dl_manager.download_and_extract(_URLs)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["train"]),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir["test"]), "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "filepath": os.path.join(data_dir["dev"]),
                    "split": "dev",
                },
            ),
        ]

    def _generate_examples(self, filepath, split):
        """ Yields examples. """

        with open(filepath, encoding="utf-8") as f:
            dataset = json.load(f)

            for id_, data in enumerate(dataset):
                dialog = data[0]
                relation_data = data[1]

                yield id_, {
                    "dialog": dialog,
                    "relation_data": relation_data,
                }
