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
"""Helper functions to generate fake Cityscapes-like data for testing."""

import os
import random
import re
import zipfile
from tensorflow_datasets.testing.fake_data_utils import get_random_png

CITY_IN_ID_RE = re.compile(r'(.+)_[0-9]+_[0-9]+')


def generate_ids(city, num=2):
  """Generates image ids following the format of the cityscapes dataset.

  Args:
    city (str): The city/scene the ids belong to, used as a prefix to the id.
    num (int): Number of random ids to generate.

  Yields:
    Generator for id strings.
  """
  for _ in range(num):
    yield '{}_{:06d}_{:06d}'.format(city, random.randint(0, 999999),
                                    random.randint(0, 999999))


def create_zipfile(zip_filepath, splits_with_ids, suffixes, maindir=None):
  """Generates a zipfile with a cityscapes-like file structure and random pngs.

  Args:
    zip_filepath (str): filepath to the zip archive that will be created
    splits_with_ids (Dict[str, List[str]]): data-splits like 'train' or 'val'
      that map to a list of image ids
    suffixes (List[str]): suffix per modality that should be created e.g.
      'leftImg8bit'
    maindir (str): name of the root directory of the zipfile, defaults to the
      name of the zipfile
  """
  with zipfile.ZipFile(zip_filepath, 'w') as z:
    for split, ids in splits_with_ids.items():
      if maindir is None:
        maindir = os.path.basename(zip_filepath).strip('.zip')
      split = os.path.join(maindir, split)
      for img_id in ids:
        city = CITY_IN_ID_RE.match(img_id).group(1)
        for suffix in suffixes:
          if 'Img' in suffix:
            img = get_random_png(height=1024, width=2048, channels=3)
          else:
            img = get_random_png(height=1024, width=2048, channels=1)
          z.write(img, os.path.join(split, city,
                                    '{}_{}.png'.format(img_id, suffix)))
