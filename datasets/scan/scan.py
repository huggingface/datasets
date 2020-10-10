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
"""SCAN tasks with various different splits."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """
@inproceedings{Lake2018GeneralizationWS,
  title={Generalization without Systematicity: On the Compositional Skills of
         Sequence-to-Sequence Recurrent Networks},
  author={Brenden M. Lake and Marco Baroni},
  booktitle={ICML},
  year={2018},
  url={https://arxiv.org/pdf/1711.00350.pdf},
}
"""

_DESCRIPTION = """SCAN tasks with various splits.

SCAN is a set of simple language-driven navigation tasks for studying
compositional learning and zero-shot generalization.

See https://github.com/brendenlake/SCAN for a description of the splits.

Example usage:
data = datasets.load_dataset('scan/length')
"""

_DATA_URL = "https://github.com/brendenlake/SCAN/archive/master.zip"


class ScanConfig(datasets.BuilderConfig):
    """BuilderConfig for SCAN."""

    def __init__(self, name, directory=None, **kwargs):
        """BuilderConfig for SCAN.

        Args:
          name: Unique name of the split.
          directory: Which subdirectory to read the split from.
          **kwargs: keyword arguments forwarded to super.
        """
        # Version history:
        super(ScanConfig, self).__init__(
            name=name, version=datasets.Version("1.0.0"), description=_DESCRIPTION, **kwargs
        )
        if directory is None:
            self.directory = name + "_split"
        else:
            self.directory = directory


_COMMANDS = "commands"
_ACTIONS = "actions"


class Scan(datasets.GeneratorBasedBuilder):
    """SCAN task / splits as proposed by Brenden M. Lake and Marco Baroni."""

    BUILDER_CONFIGS = [
        ScanConfig(name="simple"),
        ScanConfig(name="addprim_jump", directory="add_prim_split"),
        ScanConfig(name="addprim_turn_left", directory="add_prim_split"),
        ScanConfig(name="filler_num0", directory="filler_split"),
        ScanConfig(name="filler_num1", directory="filler_split"),
        ScanConfig(name="filler_num2", directory="filler_split"),
        ScanConfig(name="filler_num3", directory="filler_split"),
        ScanConfig(name="length"),
        ScanConfig(name="template_around_right", directory="template_split"),
        ScanConfig(name="template_jump_around_right", directory="template_split"),
        ScanConfig(name="template_opposite_right", directory="template_split"),
        ScanConfig(name="template_right", directory="template_split"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _COMMANDS: datasets.Value("string"),
                    _ACTIONS: datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/brendenlake/SCAN",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_DATA_URL)
        data_dir = os.path.join(data_dir, "SCAN-master", self.config.directory)
        split = self.config.name
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": os.path.join(data_dir, "tasks_train_" + split + ".txt")},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": os.path.join(data_dir, "tasks_test_" + split + ".txt")},
            ),
        ]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath, encoding="utf-8") as infile:
            for i, line in enumerate(infile):
                if not line.startswith("IN: "):
                    continue
                # Chop the prefix and split string between input and output
                commands, actions = line[len("IN: ") :].strip().split(" OUT: ", 1)
                yield i, {_COMMANDS: commands, _ACTIONS: actions}
