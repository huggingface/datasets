# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""CFQ (Compositional Freebase Question) dataset."""

from __future__ import absolute_import, division, print_function

import json
import logging
import os
import re

import nlp


_CITATION = """
@inproceedings{Keysers2020,
  title={Measuring Compositional Generalization: A Comprehensive Method on
         Realistic Data},
  author={Daniel Keysers and Nathanael Sch\"{a}rli and Nathan Scales and
          Hylke Buisman and Daniel Furrer and Sergii Kashubin and
          Nikola Momchev and Danila Sinopalnikov and Lukasz Stafiniak and
          Tibor Tihon and Dmitry Tsarkov and Xiao Wang and Marc van Zee and
          Olivier Bousquet},
  booktitle={ICLR},
  year={2020},
  url={https://arxiv.org/abs/1912.09713.pdf},
}
"""

_DESCRIPTION = """
The CFQ dataset (and it's splits) for measuring compositional generalization.

See https://arxiv.org/abs/1912.09713.pdf for background.

Example usage:
data = nlp.load_dataset('cfq/mcd1')
"""

_DATA_URL = "https://storage.googleapis.com/cfq_dataset/cfq.tar.gz"


class CfqConfig(nlp.BuilderConfig):
    """BuilderConfig for CFQ splits."""

    def __init__(self, name, directory="splits", **kwargs):
        """BuilderConfig for CFQ.

    Args:
      name: Unique name of the split.
      directory: Which subdirectory to read the split from.
      **kwargs: keyword arguments forwarded to super.
    """
        # Version history:
        super(CfqConfig, self).__init__(name=name, version=nlp.Version("1.0.1"), description=_DESCRIPTION, **kwargs)
        self.split_file = os.path.join(directory, name + ".json")


_QUESTION = "question"
_QUERY = "query"
_QUESTION_FIELD = "questionPatternModEntities"
_QUERY_FIELD = "sparqlPatternModEntities"


class Cfq(nlp.GeneratorBasedBuilder):
    """CFQ task / splits."""

    BUILDER_CONFIGS = [
        CfqConfig(name="mcd1"),
        CfqConfig(name="mcd2"),
        CfqConfig(name="mcd3"),
        CfqConfig(name="question_complexity_split"),
        CfqConfig(name="question_pattern_split"),
        CfqConfig(name="query_complexity_split"),
        CfqConfig(name="query_pattern_split"),
        CfqConfig(name="random_split"),
    ]

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features({_QUESTION: nlp.Value("string"), _QUERY: nlp.Value("string"),}),
            supervised_keys=(_QUESTION, _QUERY),
            homepage="https://github.com/google-research/google-research/tree/master/cfq",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = dl_manager.download_and_extract(_DATA_URL)
        data_dir = os.path.join(data_dir, "cfq")
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN,
                gen_kwargs={
                    "base_directory": data_dir,
                    "splits_file": self.config.split_file,
                    "split_id": "trainIdxs",
                },
            ),
            nlp.SplitGenerator(
                name=nlp.Split.TEST,
                gen_kwargs={"base_directory": data_dir, "splits_file": self.config.split_file, "split_id": "testIdxs"},
            ),
        ]

    def _scrub_json(self, content):
        """Reduce JSON by filtering out only the fields of interest."""
        # Loading of json data with the standard Python library is very inefficient:
        # For the 4GB dataset file it requires more than 40GB of RAM and takes 3min.
        # There are more efficient libraries but in order to avoid additional
        # dependencies we use a simple (perhaps somewhat brittle) regexp to reduce
        # the content to only what is needed. This takes 1min to execute but
        # afterwards loading requires only 500MB or RAM and is done in 2s.
        regex = re.compile(r'("%s":\s*"[^"]*").*?("%s":\s*"[^"]*")' % (_QUESTION_FIELD, _QUERY_FIELD), re.DOTALL)
        return "[" + ",".join(["{" + m.group(1) + "," + m.group(2) + "}" for m in regex.finditer(content)]) + "]"

    def _generate_examples(self, base_directory, splits_file, split_id):
        """Yields examples."""
        samples_path = os.path.join(base_directory, "dataset.json")
        splits_path = os.path.join(base_directory, splits_file)
        with open(samples_path) as samples_file:
            with open(splits_path) as splits_file:
                logging.info("Reading json from %s into memory...", samples_path)
                samples = json.loads(self._scrub_json(samples_file.read()))
                logging.info("%d samples loaded", len(samples))
                logging.info("Loaded json data from %s.", samples_path)
                splits = json.load(splits_file)
                for idx in splits[split_id]:
                    sample = samples[idx]
                    yield idx, {_QUESTION: sample[_QUESTION_FIELD], _QUERY: sample[_QUERY_FIELD]}
