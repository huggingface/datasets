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
"""Tests for tensorflow_datasets.core.download.download_manager."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import json
import os
import re
import tempfile
import threading

from absl.testing import absltest
import promise
import tensorflow.compat.v2 as tf
from tensorflow_datasets import testing
from tensorflow_datasets.core.download import checksums as checksums_lib
from tensorflow_datasets.core.download import download_manager as dm
from tensorflow_datasets.core.download import resource as resource_lib


ZIP = resource_lib.ExtractMethod.ZIP
TAR = resource_lib.ExtractMethod.TAR
NO_EXTRACT = resource_lib.ExtractMethod.NO_EXTRACT


def _get_promise_on_event(result=None, error=None):
  """Returns (event, Promise). Promise is fulfilled when `event.set()`."""
  event = threading.Event()
  def callback(resolve, reject):
    def inside():
      event.wait()
      if error is not None:
        reject(error)
      resolve(result)
    t = threading.Thread(target=inside)
    t.daemon = True
    t.start()
  return event, promise.Promise(callback)


def _sha256(str_):
  return hashlib.sha256(str_.encode('utf8')).hexdigest()


class Artifact(object):
  # For testing only.

  def __init__(self, name, url=None):
    url = url or 'http://foo-bar.ch/%s' % name
    content = 'content of %s' % name
    self.url = url
    self.content = content
    self.size = len(content)
    self.sha = _sha256(content)
    self.size_checksum = (self.size, self.sha)
    self.checksum_size = (self.sha, self.size)
    self.dl_fname = resource_lib.get_dl_fname(url, self.sha)
    self.dl_tmp_dirname = resource_lib.get_dl_dirname(url)


class DownloadManagerTest(testing.TestCase):

  def _add_file(self, path, content='', mode='w'):
    """Returns open file handle."""
    temp_f = tempfile.NamedTemporaryFile(mode=mode, delete=False)
    self.files_content[path] = temp_f.name
    temp_f.write(content)
    temp_f.close()
    self.existing_paths.append(path)
    return temp_f

  def setUp(self):
    self.addCleanup(absltest.mock.patch.stopall)
    self.existing_paths = []
    self.made_dirs = []
    self.dl_results = {}
    self.extract_results = {}
    self.file_names = {}  # resource fname -> original file name
    def list_directory(path):
      fname = os.path.basename(path).rsplit('.', 2)[0]  # suffix is '.tmp.$uuid'
      return [self.file_names.get(fname, 'file_with_no_ext')]
    self.files_content = {}
    def open_(path, mode='r'):
      if 'w' in mode:
        self._add_file(path)
      return open(self.files_content[path], mode)
    def rename(from_, to, overwrite=False):
      del overwrite
      if from_ in self.files_content:
        self.existing_paths.append(to)
        self.existing_paths.remove(from_)
        self.files_content[to] = self.files_content.pop(from_)

    self.gfile_patch = absltest.mock.patch.object(
        tf.io,
        'gfile',
        exists=lambda path: path in self.existing_paths,
        makedirs=self.made_dirs.append,
        # Used to get name of file as downloaded:
        listdir=list_directory,
        GFile=open_,
        rename=absltest.mock.Mock(side_effect=rename),
    )
    self.gfile = self.gfile_patch.start()
    absltest.mock.patch.object(checksums_lib, 'store_checksums').start()

  def tearDown(self):
    self.gfile_patch.stop()

  def _write_info(self, path, info):
    content = json.dumps(info, sort_keys=True)
    self._add_file(path, content)

  def _get_manager(self, force_download=False, force_extraction=False,
                   checksums=None, dl_dir='/dl_dir',
                   extract_dir='/extract_dir'):
    manager = dm.DownloadManager(
        dataset_name='mnist',
        download_dir=dl_dir,
        extract_dir=extract_dir,
        manual_dir='/manual_dir',
        force_download=force_download,
        force_extraction=force_extraction,
        )
    if checksums:
      manager._sizes_checksums = checksums
    download = absltest.mock.patch.object(
        manager._downloader,
        'download',
        side_effect=lambda url, tmpdir_path: self.dl_results[url])
    self.downloader_download = download.start()
    extract = absltest.mock.patch.object(
        manager._extractor,
        'extract',
        side_effect=lambda path, method, dest: self.extract_results[path])
    self.extractor_extract = extract.start()
    return manager

  def test_download(self):
    """One file in cache, one not."""
    a, b, c = [Artifact(i) for i in 'abc']
    urls = {
        'cached': a.url,
        'new': b.url,
        'info_deleted': c.url,
    }
    _ = [self._add_file(path, content) for path, content in [  # pylint: disable=g-complex-comprehension
        ('/dl_dir/%s' % a.dl_fname, a.content),
        ('/dl_dir/%s.INFO' % a.dl_fname, 'content of info file a'),
        # INFO file of c has been deleted:
        ('/dl_dir/%s' % c.dl_fname, c.content),
    ]]
    dl_b, self.dl_results[b.url] = _get_promise_on_event(b.checksum_size)
    dl_c, self.dl_results[c.url] = _get_promise_on_event(c.checksum_size)
    manager = self._get_manager(checksums=dict(
        (art.url, art.size_checksum) for art in (a, b, c)))
    dl_b.set()
    dl_c.set()
    downloads = manager.download(urls)
    expected = {
        'cached': '/dl_dir/%s' % a.dl_fname,
        'new': '/dl_dir/%s' % b.dl_fname,
        'info_deleted': '/dl_dir/%s' % c.dl_fname,
    }
    self.assertEqual(downloads, expected)

  def test_extract(self):
    """One file already extracted, one file with NO_EXTRACT, one to extract."""
    cached = resource_lib.Resource(path='/dl_dir/cached', extract_method=ZIP)
    new_ = resource_lib.Resource(path='/dl_dir/new', extract_method=TAR)
    no_extract = resource_lib.Resource(path='/dl_dir/noextract',
                                       extract_method=NO_EXTRACT)
    files = {
        'cached': cached,
        'new': new_,
        'noextract': no_extract,
    }
    self.existing_paths.append('/extract_dir/ZIP.cached')
    extracted_new, self.extract_results['/dl_dir/new'] = (
        _get_promise_on_event('/extract_dir/TAR.new'))
    manager = self._get_manager()
    extracted_new.set()
    res = manager.extract(files)
    expected = {
        'cached': '/extract_dir/ZIP.cached',
        'new': '/extract_dir/TAR.new',
        'noextract': '/dl_dir/noextract',
    }
    self.assertEqual(res, expected)

  def test_extract_twice_parallel(self):
    # Make sure calling extract twice on same resource actually does the
    # extraction once.
    extracted_new, self.extract_results['/dl_dir/foo.tar'] = (
        _get_promise_on_event('/extract_dir/TAR.foo'))
    manager = self._get_manager()
    extracted_new.set()
    out1 = manager.extract(['/dl_dir/foo.tar', '/dl_dir/foo.tar'])
    out2 = manager.extract('/dl_dir/foo.tar')
    expected = '/extract_dir/TAR.foo'
    self.assertEqual(out1[0], expected)
    self.assertEqual(out1[1], expected)
    expected = '/extract_dir/TAR.foo'
    self.assertEqual(out2, expected)
    # Result is memoize so extract has only been called once
    self.assertEqual(1, self.extractor_extract.call_count)

  def test_download_and_extract(self):
    a, b = Artifact('a.zip'), Artifact('b')
    self.file_names[a.dl_tmp_dirname] = 'a.zip'
    dl_a, self.dl_results[a.url] = _get_promise_on_event(a.checksum_size)
    dl_b, self.dl_results[b.url] = _get_promise_on_event(b.checksum_size)
    ext_a, self.extract_results['/dl_dir/%s' % a.dl_fname] = (
        _get_promise_on_event('/extract_dir/ZIP.%s' % a.dl_fname))
    # url_b doesn't need any extraction.
    for event in [dl_a, dl_b, ext_a]:
      event.set()
    # Result is the same after caching:
    manager = self._get_manager(checksums={
        a.url: a.size_checksum,
        b.url: b.size_checksum,
    })
    res = manager.download_and_extract({'a': a.url, 'b': b.url})
    expected = {
        'a': '/extract_dir/ZIP.%s' % a.dl_fname,
        'b': '/dl_dir/%s' % b.dl_fname,
    }
    self.assertEqual(res, expected)

  def test_download_and_extract_archive_ext_in_fname(self):
    # Make sure extraction method is properly deduced from original fname, and
    # not from URL.
    a = Artifact('a', url='http://a?key=1234')
    self.file_names[a.dl_tmp_dirname] = 'a.zip'
    dl, self.dl_results[a.url] = _get_promise_on_event(a.checksum_size)
    ext, self.extract_results['/dl_dir/%s' % a.dl_fname] = (
        _get_promise_on_event('/extract_dir/ZIP.%s' % a.dl_fname))
    dl.set()
    ext.set()
    manager = self._get_manager(checksums={
        a.url: a.size_checksum,
    })
    res = manager.download_and_extract({'a': a.url})
    expected = {
        'a': '/extract_dir/ZIP.%s' % a.dl_fname,
    }
    self.assertEqual(res, expected)


  def test_download_and_extract_already_downloaded(self):
    a = Artifact('a.zip')
    self.file_names[a.dl_tmp_dirname] = 'a.zip'
    # File was already downloaded:
    self._add_file('/dl_dir/%s' % a.dl_fname)
    self._write_info('/dl_dir/%s.INFO' % a.dl_fname,
                     {'original_fname': 'a.zip'})
    ext_a, self.extract_results['/dl_dir/%s' % a.dl_fname] = (
        _get_promise_on_event('/extract_dir/ZIP.%s' % a.dl_fname))
    ext_a.set()
    manager = self._get_manager(checksums={
        a.url: a.size_checksum,
    })
    res = manager.download_and_extract(a.url)
    expected = '/extract_dir/ZIP.%s' % a.dl_fname
    self.assertEqual(res, expected)

  def test_force_download_and_extract(self):
    a = Artifact('a.tar.gz')
    # resource was already downloaded / extracted:
    self.existing_paths = ['/dl_dir/%s' % a.dl_fname,
                           '/extract_dir/TAR_GZ.%s' % a.dl_fname]
    self.file_names[a.dl_tmp_dirname] = 'b.tar.gz'
    self._write_info('/dl_dir/%s.INFO' % a.dl_fname,
                     {'original_fname': 'b.tar.gz'})
    dl_a, self.dl_results[a.url] = _get_promise_on_event(a.checksum_size)
    ext_a, self.extract_results['/dl_dir/%s' % a.dl_fname] = (
        _get_promise_on_event('/extract_dir/TAR_GZ.%s' % a.dl_fname))
    dl_a.set()
    ext_a.set()
    manager = self._get_manager(
        force_download=True, force_extraction=True,
        checksums={
            a.url: a.size_checksum,
        })
    res = manager.download_and_extract(a.url)
    expected = '/extract_dir/TAR_GZ.%s' % a.dl_fname
    self.assertEqual(expected, res)
    # Rename after download:
    (from_, to), kwargs = self.gfile.rename.call_args
    self.assertTrue(re.match(
        r'/dl_dir/%s\.tmp\.[a-h0-9]{32}/b.tar.gz' % a.dl_tmp_dirname,
        from_))
    self.assertEqual('/dl_dir/%s' % a.dl_fname, to)
    self.assertEqual(kwargs, {'overwrite': True})
    self.assertEqual(1, self.downloader_download.call_count)
    self.assertEqual(1, self.extractor_extract.call_count)

  def test_wrong_checksum(self):
    a = Artifact('a.tar.gz')
    sha_b = _sha256('content of another file')
    dl_a, self.dl_results[a.url] = _get_promise_on_event(a.checksum_size)
    dl_a.set()
    manager = self._get_manager(checksums={
        a.url: (a.size, sha_b),
    })
    with self.assertRaises(dm.NonMatchingChecksumError):
      manager.download(a.url)
    self.assertEqual(0, self.extractor_extract.call_count)


if __name__ == '__main__':
  testing.test_main()
