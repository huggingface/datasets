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
"""CFQ (Compositional Freebase Questions) dataset."""


import json
import re

import datasets


logger = datasets.logging.get_logger(__name__)


_HOMEPAGE = "https://github.com/google-research/google-research/tree/master/cfq"

_LICENSE = "CC BY 4.0"

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
data = datasets.load_dataset('cfq/mcd1')
"""

_DATA_URL = "https://storage.googleapis.com/cfq_dataset/cfq.tar.gz"


class CfqConfig(datasets.BuilderConfig):
    """BuilderConfig for CFQ splits."""

    def __init__(self, name, directory="splits", **kwargs):
        """BuilderConfig for CFQ.

        Args:
          name: Unique name of the split.
          directory: Which subdirectory to read the split from.
          **kwargs: keyword arguments forwarded to super.
        """
        # Version history:
        super(CfqConfig, self).__init__(
            name=name, version=datasets.Version("1.0.1"), description=_DESCRIPTION, **kwargs
        )
        self.splits_path = f"cfq/{directory}/{name}.json"


_QUESTION = "question"
_QUERY = "query"
_QUESTION_FIELD = "questionPatternModEntities"
_QUERY_FIELD = "sparqlPatternModEntities"


class Cfq(datasets.GeneratorBasedBuilder):
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
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    _QUESTION: datasets.Value("string"),
                    _QUERY: datasets.Value("string"),
                }
            ),
            supervised_keys=(_QUESTION, _QUERY),
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive_path = dl_manager.download(_DATA_URL)
        return [
            datasets.SplitGenerator(
                name=split,
                gen_kwargs={
                    "data_files": dl_manager.iter_archive(archive_path),
                    "split_id": f"{split}Idxs",
                },
            )
            for split in [datasets.Split.TRAIN, datasets.Split.TEST]
        ]

    def _scrub_json(self, content):
        """Reduce JSON by filtering out only the fields of interest."""
        # Loading of json data with the standard Python library is very inefficient:
        # For the 4GB dataset file it requires more than 40GB of RAM and takes 3min.
        # There are more efficient libraries but in order to avoid additional
        # dependencies we use a simple (perhaps somewhat brittle) regexp to reduce
        # the content to only what is needed.
        question_regex = re.compile(r'("%s":\s*"[^"]*")' % _QUESTION_FIELD)
        query_regex = re.compile(r'("%s":\s*"[^"]*")' % _QUERY_FIELD)
        question_match = None
        for line in content:
            line = line.decode("utf-8")
            if not question_match:
                question_match = question_regex.match(line)
            else:
                query_match = query_regex.match(line)
                if query_match:
                    yield json.loads("{" + question_match.group(1) + "," + query_match.group(1) + "}")
                    question_match = None

    def _generate_examples(self, data_files, split_id):
        """Yields examples."""
        samples_path = "cfq/dataset.json"
        for path, file in data_files:
            if path == self.config.splits_path:
                splits = json.load(file)[split_id]
            elif path == samples_path:
                # The samples_path is the last path inside the archive
                generator = enumerate(self._scrub_json(file))
                samples = {}
                splits_set = set(splits)
                for split_idx in splits:
                    if split_idx in samples:
                        sample = samples.pop(split_idx)
                    else:
                        for sample_idx, sample in generator:
                            if sample_idx == split_idx:
                                break
                            elif sample_idx in splits_set:
                                samples[sample_idx] = sample
                    yield split_idx, {_QUESTION: sample[_QUESTION_FIELD], _QUERY: sample[_QUERY_FIELD]}
