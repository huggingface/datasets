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
"""HuggingFace datasets implementation of the json tasks in the BIG-Bench Dataset.
For the programatic tasks, please use the BIG-Bench API on github.com/google/BIG-bench.
"""


import csv
import json
import numpy as np
import os
from typing import Optional

import datasets

try:
  import bigbench.bbseqio.bigbench_bridge as bbb
  from bigbench.bbseqio import bigbench_json_paths as bb_json_paths
  import bigbench.api.util as bb_utils
  
except ModuleNotFoundError as error:
  print(f"Failed to import bigbench. Please see https://github.com/google/BIG-bench or install using 'pip install git+https://github.com/google/BIG-bench.git'")
  raise

_CITATION = """\
@InProceedings{bigbench,
title = {Beyond the Imitation Game: Quantifying and extrapolating the
capabilities of language models},
author={BIG-Bench Collaboration
},
year={2022}
}
"""

_DESCRIPTION = """\
The Beyond the Imitation Game Benchmark (BIG-bench) is a collaborative benchmark intended to 
probe large language models, and extrapolate their future capabilities.
"""

_HOMEPAGE = "https://github.com/google/BIG-bench"

_LICENSE = "Apache License 2.0"


def div_or_none(x, y):
  return x // y if x else x


def validate_task_name(task_name: str) -> None:
  """Check that the requested task name is a valid bigbench json task."""
  if task_name in bb_utils.get_all_json_task_names():
    pass
  elif task_name in bb_utils.get_all_programmatic_task_names():
    raise ValueError("BIG-Bench does not support programmatic tasks through HuggingFace datasets"
          			 f"Please see {_HOMEPAGE} for more information for how to interact with the programmatic tasks.")
  else:
    print("Invalid task_name. Please choose one from:")
    for name in bb_utils.get_all_json_task_names():
      print(f"-- {name}")
    raise ValueError(f"Unknown task name. Got {task_name}.")
    
def validate_subtask_name(task_name: str, subtask_name: str) -> None:
  """Check that the requested subtask name is a valid bigbench subtask."""
  subtasks = [name.split(":")[-1] for name in bb_utils.get_subtask_names_from_task(task_name)]
  if subtask_name not in subtasks:
    print(f"Invalid subtask_name {subtask_name} for task {task_name}. Please choose one from:")
    for name in subtasks:
      print(f"-- {name}")
    raise ValueError(f"Unknown subtask name. Got subtask {subtask_name} for task {task_name}.")
  

class BigBenchConfig(datasets.BuilderConfig):
    def __init__(self,
                 task_name: str,
                 *args, 
                 subtask_name: Optional[str] = None, 
                 num_shots: int = 0,
                 max_examples: Optional[int] = None,
                 **kwargs):
        super().__init__(
            *args,
            **kwargs,
        )
        self.task_name = task_name
        self.subtask_name = subtask_name
        self.num_shots = num_shots
        self.max_examples = max_examples
        
        validate_task_name(self.task_name)
        if self.subtask_name:
          # Subtasks are sometimes in bigbench written as task_name:subtask_name.
          # We want to remove the task_name from the subtask names:
          self.subtask_name = self.subtask_name.split(':')[-1]
          validate_subtask_name(self.task_name, self.subtask_name)


class BigBench(datasets.GeneratorBasedBuilder):
    """The Beyond the Imitation Game Benchmark (BIG-bench) is a collaborative benchmark
    intended to probe large language models, and extrapolate their future capabilities."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIG_CLASS = BigBenchConfig


    def _info(self):
        features = datasets.Features(
            {
              "idx": datasets.Value("int32"),
              "inputs": datasets.Value("string"),
              "targets": datasets.Sequence(datasets.Value("string")),
              "multiple_choice_targets": datasets.Sequence(datasets.Value("string")),
              "multiple_choice_scores": datasets.Sequence(datasets.Value("int32")),
            })
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
		
        return [
          	datasets.SplitGenerator(
              name=datasets.splits.NamedSplit('default'), # TODO(ajandreassen): Is there a way override and call this 'all'?
              # These kwargs will be passed to _generate_examples
              gen_kwargs={
                "split": "all",
              },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "split": "validation",
                },
            ),
        ]

    def _generate_examples(
        self, split # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """ Yields examples as (key, example) tuples. """
        if split == 'all':
          # not cutoff in number of examples for 'all' split
          MIN_VALIDATION_EXAMPLES = 0
        else:
          MIN_VALIDATION_EXAMPLES = 16

        try:
          task_path, json_util = bb_json_paths.get_task_path(self.config.task_name)

          has_subtasks = bb_json_paths.has_subtasks(self.config.task_name)
          if has_subtasks:
            subtask_names = bb_json_paths.get_subtask_names(self.config.task_name)
            num_subtasks = len(subtask_names)
            min_validation_examples_per_subtask = div_or_none(
              MIN_VALIDATION_EXAMPLES, num_subtasks)

          if not has_subtasks:
            ds_fn = bbb.get_dataset_fn(task_name = self.config.task_name,
                                       task_path = task_path,
                                       subtask_name = None,
                                       num_shots = self.config.num_shots,
                                       bigbench_task_type = bbb.BigBenchTaskType.HUGGINGFACE,
                                       max_examples = self.config.max_examples,
                                       json_util = json_util,
                                       min_validation_examples = MIN_VALIDATION_EXAMPLES
                                      )
            ds_list = [ds_fn(split)]
          elif self.config.subtask_name is not None:
            ds_fn = bbb.get_dataset_fn(task_name = self.config.task_name,
                                       task_path = task_path,
                                       subtask_name = self.config.subtask_name,
                                       num_shots = self.config.num_shots,
                                       bigbench_task_type = bbb.BigBenchTaskType.HUGGINGFACE,
                                       max_examples = self.config.max_examples,
                                       json_util = json_util,
                                       min_validation_examples = min_validation_examples_per_subtask)
            ds_list = [ds_fn(split)]
          else:
            # Create mixture of all subtasks
            ds_list = []
            for subtask_name in subtask_names:
              subtask_name = subtask_name.split(':')[-1]
              print(f"Loading subtask {split} split", subtask_name)
              ds_fn = bbb.get_dataset_fn(task_name = self.config.task_name,
                                       task_path = task_path,
                                       subtask_name = subtask_name,
                                       num_shots = self.config.num_shots,
                                       bigbench_task_type = bbb.BigBenchTaskType.HUGGINGFACE,
                                       max_examples = div_or_none(self.config.max_examples, num_subtasks),
                                       json_util = json_util,
                                       min_validation_examples = min_validation_examples_per_subtask
                                      )
              ds_list.append(ds_fn(split))
        except ValueError as value_error:
          # BIG-Bench requires at least 16 examples to use the train & validation splits, 
          # while using 'all'/'default' does not have such a requirement.
          if "has too few examples" in value_error.args[0] and split != 'all':
            print(f"-- WARNING: skipping split {split} because it has too few examples. Please use 'default' split.")
            print(value_error)
            return
          raise value_error
        
        unique_key_counter = 0
        for ds in ds_list:
          for example in ds:
            unique_key_counter +=1
            yield unique_key_counter, {
              "idx": example["idx"],
              "inputs": example["inputs"].numpy().decode().strip(),
              "targets": [target.numpy().decode().strip() for target in example["targets"]],
              "multiple_choice_targets": [targets.decode().strip() for targets in example["multiple_choice_targets"].numpy()],
              "multiple_choice_scores": [scores for scores in example["multiple_choice_scores"].numpy()],
              }
