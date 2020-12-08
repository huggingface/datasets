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
"""Deal or no deal negotiator"""

from __future__ import absolute_import, division, print_function

import datasets


_CITATION = """\
@article{lewis2017deal,
  title={Deal or no deal? end-to-end learning for negotiation dialogues},
  author={Lewis, Mike and Yarats, Denis and Dauphin, Yann N and Parikh, Devi and Batra, Dhruv},
  journal={arXiv preprint arXiv:1706.05125},
  year={2017}
}
"""

_DESCRIPTION = """\
A large dataset of human-human negotiations on a multi-issue bargaining task, where agents who cannot observe each other’s reward functions must reach anagreement (o a deal) via natural language dialogue.
"""

_HOMEPAGE = "https://github.com/facebookresearch/end-to-end-negotiator"

_LICENSE = "The project is licenced under CC-by-NC"

_URLs = {
    "train": "https://raw.githubusercontent.com/facebookresearch/end-to-end-negotiator/master/src/data/negotiate/train.txt",
    "test": "https://raw.githubusercontent.com/facebookresearch/end-to-end-negotiator/master/src/data/negotiate/test.txt",
    "val": "https://raw.githubusercontent.com/facebookresearch/end-to-end-negotiator/master/src/data/negotiate/val.txt",
    "selfplay": "https://raw.githubusercontent.com/facebookresearch/end-to-end-negotiator/master/src/data/negotiate/selfplay.txt",
}


class DealOrNoDialog(datasets.GeneratorBasedBuilder):
    """Deal or no deal negotiator"""

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="dialogues",
            description="Consists of 5808 dialogues, based on 2236 unique scenarios.",
            version=VERSION,
        ),
        datasets.BuilderConfig(
            name="self_play", description="Count and values with no dialogues. Used for self playing.", version=VERSION
        ),
    ]

    DEFAULT_CONFIG_NAME = "dialogues"

    def _info(self):
        if self.config.name == "dialogues":
            features = datasets.Features(
                {
                    "input": datasets.Sequence({"count": datasets.Value("int32"), "value": datasets.Value("int32")}),
                    "dialogue": datasets.Value("string"),
                    "output": datasets.Value("string"),
                    "partner_input": datasets.Sequence(
                        {"count": datasets.Value("int32"), "value": datasets.Value("int32")}
                    ),
                }
            )
        else:  # self_play
            features = datasets.Features(
                {
                    "input": datasets.Sequence({"count": datasets.Value("int32"), "value": datasets.Value("int32")}),
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
        if self.config.name == "dialogues":
            path_train = dl_manager.download_and_extract(_URLs["train"])
            path_test = dl_manager.download_and_extract(_URLs["test"])
            path_val = dl_manager.download_and_extract(_URLs["val"])

            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": path_train,
                        "split": "train",
                    },
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.TEST,
                    gen_kwargs={"filepath": path_test, "split": "test"},
                ),
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    gen_kwargs={
                        "filepath": path_val,
                        "split": "val",
                    },
                ),
            ]

        else:
            path = dl_manager.download_and_extract(_URLs["selfplay"])
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={
                        "filepath": path,
                        "split": "train",
                    },
                ),
            ]

    def _generate_examples(self, filepath, split="train"):
        """ Yields examples. """
        if self.config.name == "dialogues":
            with open(filepath, encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    tokens = line.split()

                    yield idx, {
                        "input": {
                            "count": get_count_value(get_tag(tokens, "input"))[0],
                            "value": get_count_value(get_tag(tokens, "input"))[1],
                        },
                        "dialogue": get_tag(tokens, "dialogue"),
                        "output": get_tag(tokens, "output"),
                        "partner_input": {
                            "count": get_count_value(get_tag(tokens, "partner_input"))[0],
                            "value": get_count_value(get_tag(tokens, "partner_input"))[1],
                        },
                    }

        else:
            with open(filepath, encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    yield idx, {"input": {"count": get_count_value(line)[0], "value": get_count_value(line)[1]}}


def get_tag(tokens, tag):
    return " ".join(tokens[tokens.index("<" + tag + ">") + 1 : tokens.index("</" + tag + ">")])


def get_count_value(sequence):
    seq_list = [int(el) for el in sequence.split()]
    assert len(seq_list) == 6
    return [seq_list[idx] for idx in [0, 2, 4]], [seq_list[idx] for idx in [1, 3, 5]]
