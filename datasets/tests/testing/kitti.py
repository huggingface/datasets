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
r"""Script to generate fake Kitti files with random data for testing.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tempfile
import zipfile

from absl import app
from absl import flags

import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import utils
from tensorflow_datasets.core.utils import py_utils
from tensorflow_datasets.object_detection import kitti
from tensorflow_datasets.testing import fake_data_utils

flags.DEFINE_string("tfds_dir", py_utils.tfds_dir(),
                    "Path to tensorflow_datasets directory")

FLAGS = flags.FLAGS
NUM_IMAGES = 10
NUM_VIDEOS = 5
HEIGHT = 375
WIDTH = 1242
OBJECTS = [
    "Car",
    "Van",
    "Truck",
    "Pedestrian",
    "Person_sitting",
    "Cyclist",
    "Tram",
    "Misc",
]


def _get_png():
  """Returns a random png image."""
  image = fake_data_utils.get_random_picture(HEIGHT, WIDTH)
  png = tf.image.encode_png(image)
  with utils.nogpu_session() as sess:
    res = sess.run(png)
  return res


def _list_f2s(float_list):
  """Converts a list of floats to strings."""
  return ["{:0.2f}".format(x) for x in float_list]


def _list_d2s(int_list):
  """Converts a list of ints to strings."""
  return ["{:d}".format(x) for x in int_list]


def _get_object_annotation():
  """Returns a annotation for a random object."""
  objects = kitti._OBJECT_LABELS  # pylint: disable=protected-access
  obj_type = list(np.random.choice(objects, size=1))
  truncated = _list_f2s(np.random.rand(1))
  occluded = _list_d2s(np.random.choice(range(4), size=1))
  alpha = _list_f2s(np.random.uniform(low=-np.pi, high=np.pi, size=1))
  lr = np.random.uniform(low=0, high=WIDTH, size=2)
  tb = np.random.uniform(low=0, high=HEIGHT, size=2)
  # Left, top, right, bottom. Origin is the top-left pixel.
  bbox = _list_f2s([min(lr), HEIGHT - max(tb), max(lr), HEIGHT - min(tb)])
  # Height, width, length.
  dimensions = _list_f2s(np.random.uniform(low=0, high=5, size=3))
  location = _list_f2s(np.random.uniform(low=0, high=30, size=3))
  rotation = _list_f2s(np.random.uniform(low=-np.pi, high=np.pi, size=1))
  return " ".join(obj_type + truncated + occluded + alpha + bbox + dimensions +
                  location + rotation)


def _get_dontcare_object_annotation():
  """Returns a annotation for a random object in class `DontCare`."""
  obj_type = ["DontCare"]
  truncated = _list_f2s([-1])
  occluded = _list_d2s([-1])
  alpha = _list_f2s([-10])
  lr = np.random.uniform(low=0, high=WIDTH, size=2)
  tb = np.random.uniform(low=0, high=HEIGHT, size=2)
  # Left, top, right, bottom. Origin is the top-left pixel.
  bbox = _list_f2s([min(lr), HEIGHT - max(tb), max(lr), HEIGHT - min(tb)])
  # Height, width, length.
  dimensions = _list_f2s([-1] * 3)
  location = _list_f2s([-1000] * 3)
  rotation = _list_f2s([-10])
  return " ".join(obj_type + truncated + occluded + alpha + bbox + dimensions +
                  location + rotation)


def _get_annotations():
  """Generates annotations for a random number of objects in the image."""
  annotation = []
  for _ in range(np.random.choice(range(1, 10))):
    annotation.append(_get_object_annotation())

  # Add some DontCare objects.
  for _ in range(np.random.choice(range(1, 3))):
    annotation.append(_get_dontcare_object_annotation())

  return annotation


def _output_dir():
  """Returns output directory."""
  return os.path.join(FLAGS.tfds_dir, "testing", "test_data", "fake_examples",
                      "kitti")


def _get_label_file(annotation):
  """Returns path to label files."""
  fobj = tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=".txt")
  for row in annotation:
    fobj.write(row + "\n")
  fobj.close()
  return fobj.name


def _get_mapping_files():
  """Returns dummy image to video mapping files."""
  # Random indices file.
  train_rand = np.random.permutation(range(1, NUM_IMAGES + 1))  # 1-based index
  fobj_rand = tempfile.NamedTemporaryFile(
      delete=False, mode="wb", suffix=".txt")
  fobj_rand.write(",".join([str(x) for x in train_rand]))
  fobj_rand.close()

  # Mapping file.
  fobj_map = tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=".txt")
  assert NUM_IMAGES > NUM_VIDEOS
  assert NUM_IMAGES % NUM_VIDEOS == 0
  vid_ids = list(range(NUM_VIDEOS)) * (NUM_IMAGES // NUM_VIDEOS)
  for vid in vid_ids:
    row = "2011_09_26 2011_09_26_drive_00{:02d}_sync 0000000123".format(vid)
    fobj_map.write(row + "\n")
  fobj_map.close()

  return fobj_rand.name, fobj_map.name


def _create_zip_files():
  """Saves png and label using name index."""
  if not os.path.exists(_output_dir()):
    os.makedirs(_output_dir())

  images_out_path = os.path.join(_output_dir(), "data_object_image_2.zip")
  with zipfile.ZipFile(images_out_path, "w") as image_zip:
    for i in range(NUM_IMAGES):
      png = fake_data_utils.get_random_png(HEIGHT, WIDTH)
      image_zip.write(
          png, os.path.join("training", "image_2",
                            "image_{:06d}.png".format(i)))

  label_out_path = os.path.join(_output_dir(), "data_object_label_2.zip")
  with zipfile.ZipFile(label_out_path, "w") as label_zip:
    for i in range(NUM_IMAGES):
      annotation = _get_annotations()
      label = _get_label_file(annotation)
      label_zip.write(
          label,
          os.path.join("training", "label_2", "label_{:06d}.txt".format(i)))

  devkit_out_path = os.path.join(_output_dir(), "devkit_object.zip")
  with zipfile.ZipFile(devkit_out_path, "w") as devkit_zip:
    train_rand, train_mapping = _get_mapping_files()
    devkit_zip.write(train_rand, os.path.join("mapping", "train_rand.txt"))
    devkit_zip.write(train_mapping, os.path.join("mapping",
                                                 "train_mapping.txt"))


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  _create_zip_files()


if __name__ == "__main__":
  app.run(main)
