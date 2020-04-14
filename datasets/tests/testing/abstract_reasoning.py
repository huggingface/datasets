# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
r"""Generate AbstractReasoning-like files, smaller and with random data.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile

from absl import app
from absl import flags
import numpy as np
import six
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.testing import test_utils

ENCODING_MAP = {
    "shape": 0,
    "line": 1,
    "color": 2,
    "number": 3,
    "position": 4,
    "size": 5,
    "type": 6,
    "progression": 7,
    "XOR": 8,
    "OR": 9,
    "AND": 10,
    "consistent_union": 11,
}

RELATIONS = ["progression", "XOR", "OR", "AND", "consistent_union"]
ATTRIBUTES = ["color", "number", "position", "size", "type"]
OBJECTS = ["shape", "line"]

SPLIT_TYPES = [
    "neutral",
    "interpolation",
    "extrapolation",
    "attr.rel.pairs",
    "attr.rels",
    "attrs.pairs",
    "attrs.shape.color",
    "attrs.line.type",
]

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")
FLAGS = flags.FLAGS


def _random_content(random_state):
  """Returns a dictionary with a data sample with random content."""
  # Randomly sample the number of relations.
  num_relations = random_state.randint(1, 5)
  # Randomly sample the relations.
  relation_structure = []
  for _ in range(num_relations):
    relation_structure.append(
        (random_state.choice(OBJECTS), random_state.choice(ATTRIBUTES),
         random_state.choice(RELATIONS)))
  # Encode the relations.
  relation_structure_encoded = np.zeros((4, 12), dtype=np.int64)
  for i, relation in enumerate(relation_structure):
    for name in relation:
      relation_structure_encoded[i, ENCODING_MAP[name]] = 1

  # Create the meta target which is the max across the relations.
  meta_target = np.max(relation_structure_encoded, axis=0)

  # Create the final object.
  return {
      "relation_structure_encoded": relation_structure_encoded,
      "relation_structure": np.array(relation_structure),
      "target": random_state.randint(8, dtype=np.int64),
      "image": random_state.randint(8, size=(160, 160, 16), dtype=np.int64),
      "meta_target": meta_target,
  }


def _create_fake_file(folder, split_type, random_state):
  """Creates a fake data file."""
  path = os.path.join(folder, "{}.tar.gz".format(split_type))
  with tf.io.gfile.GFile(path, "w") as fout:
    with tarfile.open(fileobj=fout, mode="w:gz") as tar:
      for i in range(5):
        for split in ["train", "test", "val"]:
          # Write serialized numpy to buffer.
          content = _random_content(random_state)
          buf = six.BytesIO()
          np.savez(buf, **content)
          buf.seek(0)
          # Create tarinfo for the file.
          filename = "{split_type}/PGM_{split_type}_{split}_{id}.npz".format(
              split_type=split_type, split=split, id=i)
          tarinfo = tarfile.TarInfo(filename)
          tarinfo.size = len(buf.getvalue())
          # Add the file to the archive.
          tar.addfile(tarinfo=tarinfo, fileobj=buf)


def _generate():
  """Generates a fake data set and writes it to the fake_examples directory."""
  output_dir = os.path.join(FLAGS.tfds_dir, "testing", "test_data",
                            "fake_examples", "abstract_reasoning")
  test_utils.remake_dir(output_dir)
  random_state = np.random.RandomState(0)
  for split_type in SPLIT_TYPES:
    _create_fake_file(output_dir, split_type, random_state)


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _generate()


if __name__ == "__main__":
  app.run(main)
