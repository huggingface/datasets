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
"""Tests for resource module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow_datasets import testing
from tensorflow_datasets.core.download import resource

NO_EXTRACT = resource.ExtractMethod.NO_EXTRACT
TAR = resource.ExtractMethod.TAR
TAR_GZ = resource.ExtractMethod.TAR_GZ
GZIP = resource.ExtractMethod.GZIP
ZIP = resource.ExtractMethod.ZIP
BZIP2 = resource.ExtractMethod.BZIP2


class GuessExtractMethodTest(testing.TestCase):

  def test_(self):
    for fname, expected_result in [
        ('bar.tar.gz', TAR_GZ),
        ('bar.gz', GZIP),
        ('bar.tar.zip', ZIP),
        ('bar.gz.strange', NO_EXTRACT),
        ('bar.tar', TAR),
        ('bar.tar.bz2', TAR),
        ('bar.bz2', BZIP2),
    ]:
      res = resource._guess_extract_method(fname)
      self.assertEqual(res, expected_result, '(%s)->%s instead of %s' % (
          fname, res, expected_result))


class DlDirNameTest(testing.TestCase):
  urls = '''\
http://data.statmt.org/wmt17/translation-task/dev.tgz
http://data.statmt.org/wmt18/translation-task/training-parallel-nc-v13.tgz
http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/train-images-idx3-ubyte.gz
http://ufldl.stanford.edu/housenumbers/test_32x32.mat
http://www.statmt.org/lm-benchmark/1-billion-word-language-modeling-benchmark-r13output.tar.gz
http://www.statmt.org/wmt13/training-parallel-europarl-v7.tgz
http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
https://drive.google.com/uc?export=download&id=0B7EVK8r0v71pd0FJY3Blby1HUTQ
https://github.com/brendenlake/omniglot/raw/master/python/images_background_small2.zip
https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json
https://storage.googleapis.com/scv_dataset/data/Brawl_64x64_png/valid-00000-of-00001.tfrecords
https://storage.googleapis.com/scv_dataset/data/CollectMineralShards_128x128_png/train-00005-of-00010.tfrecords
https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz\
'''.split('\n')
  expected = '''\
data.statmt.org_wmt17_translation-task_devDjZ11PU9sKPPvF2sZTAzTsV7Pi3IYHaPDMOoeEuby2E.tgz
data.stat.org_wmt1_tran-task_trai-para-nc-6LWgxBgzCHdv_LtotNmnXjpCH6OhzkF8D3v10aRrznA.tgz
fashion-mnist_train-images-idx3-ubytepR2BibiiUp2twRbpoktblvl2KbaPDel0VUV9KrXm91Y.gz
ufldl.stanford.edu_housenumbers_test_32x32kIzM03CdHZsHqtImuAxFCXPGHhEH4JT7Owsqi_QawO4.mat
stat.org_lm-benc_1-bill-word-lang-mode-fPxXes4bTZ_y2eAI2mGRqBKUvUJm1CS1Idm0DH98KN8.tar.gz
statmt.org_wmt13_traini-parall-europa-v71cKcs9sx8w9ctm8xHloEI83SJqzD7piDNK3xUXpQIB4.tgz
yann.lecu.com_exdb_mnis_trai-imag-idx3-ubyt5m0Lc_VeEzGZ1PUycLKoWNyYkH_vWEKNi0mu7m4Hmbk.gz
yann.lecu.com_exdb_mnis_trai-labe-idx1-ubyt7cc_IeM51G_ngIY2ORleKjMjLVCXd-TCUHlYvEiRiKI.gz
ucexport_download_id_0B7EVK8r0v71pd0FJY3Blby1HbdQ1eXJPJLYv0yq8hL1lCD5T2aOraaQwvj25ndmE7pg
bren_omni_raw_mast_pyth_imag_back_smalUSA8LkdUW89lgXr31txDoVFbI9BtQhxvtZWYTIdAJAg.zip
rajpurkar_SQuAD-explorer_train-v1.1uLsZc14btZFRCgHMAy9Mn5abwO6wga4bMozTBvOyQAg.json
scv_Brawl_64x64_png_valid-0_1Ez3yPwN0QDCxBd0xHeLb2DfUERJjkqFd2dyL5Z7-ULg.tfrecords
scv_CollectMi_128x128_png_train-5_10kiunW_2RTDhXuPrxCVkUZKCoWpADYBUWE8DpraC8zAA.tfrecords
cs.toronto.edu_kriz_cifar-100-pythonJDFhDchdt5UW8GUAkvf_-H_r_LnFs6sHlOrqTidrpSI.tar.gz\
'''.split('\n')

  def test_(self):
    for url, expected in zip(self.urls, self.expected):
      res = resource.get_dl_dirname(url)
      self.assertEqual(res, expected)


if __name__ == '__main__':
  testing.test_main()
