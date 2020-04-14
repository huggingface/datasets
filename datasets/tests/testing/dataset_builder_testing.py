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
"""Base DatasetBuilderTestCase to test a DatasetBuilder base class."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import itertools
import numbers
import os

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
import tensorflow.compat.v2 as tf

from tensorflow_datasets.core import builder
from tensorflow_datasets.core import dataset_info
from tensorflow_datasets.core import dataset_utils
from tensorflow_datasets.core import download
from tensorflow_datasets.core import load
from tensorflow_datasets.core import utils
from tensorflow_datasets.core.download import checksums
from tensorflow_datasets.core.utils import tf_utils
from tensorflow_datasets.testing import test_utils


# `os` module Functions for which tf.io.gfile equivalent should be preferred.
FORBIDDEN_OS_FUNCTIONS = (
        "chmod",
        "chown",
        "link",
        "listdir",
        "lstat",
        "makedirs",
        "mkdir",
        "mknod",
        "open",
        "pathconf",
        "readlink",
        "remove",
        "removedirs",
        "rename",
        "renames",
        "rmdir",
        "stat",
        "statvfs",
        "symlink",
        "unlink",
        "walk",
)
FORBIDDEN_OS_PATH_FUNCTIONS = (
        "exists",
        "isdir",
        "isfile",
)


_ORGINAL_NP_LOAD = np.load


def _np_load(file_, mmap_mode=None, allow_pickle=False, **kwargs):
    if not hasattr(file_, "read"):
        raise AssertionError(
                "You MUST pass a `tf.io.gfile.GFile` or file-like object to `np.load`.")
    if allow_pickle:
        raise AssertionError("Unpicling files is forbidden for security reasons.")
    return _ORGINAL_NP_LOAD(file_, mmap_mode, allow_pickle, **kwargs)


class DatasetBuilderTestCase(parameterized.TestCase, test_utils.SubTestCase):
    """Inherit this class to test your DatasetBuilder class.

    You must set the following class attributes:

        * DATASET_CLASS: class object of DatasetBuilder you want to test.

    You may set the following class attributes:

        * VERSION: `str`. The version used to run the test. eg: '1.2.*'.
            Defaults to None (canonical version).
        * BUILDER_CONFIG_NAMES_TO_TEST: `list[str]`, the list of builder configs
            that should be tested. If None, all the BUILDER_CONFIGS from the class
            will be tested.
        * DL_EXTRACT_RESULT: `dict[str]`, the returned result of mocked
            `download_and_extract` method. The values should be the path of files
            present in the `fake_examples` directory, relative to that directory.
            If not specified, path to `fake_examples` will always be returned.
        * DL_DOWNLOAD_RESULT: `dict[str]`, the returned result of mocked
            `download_and_extract` method. The values should be the path of files
            present in the `fake_examples` directory, relative to that directory.
            If not specified: will use DL_EXTRACT_RESULT (this is due to backwards
            compatibility and will be removed in the future).
        * EXAMPLE_DIR: `str`, the base directory in in which fake examples are
            contained. Optional; defaults to
            tensorflow_datasets/testing/test_data/fake_examples/<dataset name>.
        * OVERLAPPING_SPLITS: `list[str]`, splits containing examples from other
            splits (e.g. a "example" split containing pictures from other splits).
        * MOCK_OUT_FORBIDDEN_OS_FUNCTIONS: `bool`, defaults to True. Set to False to
            disable checks preventing usage of `os` or builtin functions instead of
            recommended `tf.io.gfile` API.

    This test case will check for the following:

     - the dataset builder can read the fake examples stored in
             testing/test_data/fake_examples/{dataset_name};
     - the dataset builder can produce serialized data;
     - the dataset builder produces a valid Dataset object from serialized data
         - in eager mode;
         - in graph mode.
     - the produced Dataset examples have the expected dimensions and types;
     - the produced Dataset has and the expected number of examples;
     - a example is not part of two splits, or one of these splits is whitelisted
             in OVERLAPPING_SPLITS.
    """

    DATASET_CLASS = None
    VERSION = None
    BUILDER_CONFIG_NAMES_TO_TEST = None
    DL_EXTRACT_RESULT = None
    DL_DOWNLOAD_RESULT = None
    EXAMPLE_DIR = None
    OVERLAPPING_SPLITS = []
    MOCK_OUT_FORBIDDEN_OS_FUNCTIONS = True

    @classmethod
    def setUpClass(cls):
        tf.enable_v2_behavior()
        super(DatasetBuilderTestCase, cls).setUpClass()
        name = cls.__name__
        # Check class has the right attributes
        if cls.DATASET_CLASS is None or not callable(cls.DATASET_CLASS):
            raise AssertionError(
                    "Assign your DatasetBuilder class to %s.DATASET_CLASS." % name)

    def setUp(self):
        super(DatasetBuilderTestCase, self).setUp()
        self.patchers = []
        self.builder = self._make_builder()

        # Determine the fake_examples directory.
        self.example_dir = os.path.join(
                test_utils.fake_examples_dir(), self.builder.name)
        if self.EXAMPLE_DIR is not None:
            self.example_dir = self.EXAMPLE_DIR

        if not tf.io.gfile.exists(self.example_dir):
            err_msg = "fake_examples dir %s not found." % self.example_dir
            raise ValueError(err_msg)
        if self.MOCK_OUT_FORBIDDEN_OS_FUNCTIONS:
            self._mock_out_forbidden_os_functions()

        # Track the urls which are downloaded to validate the checksums
        # The `dl_manager.download` and `dl_manager.download_and_extract` are
        # patched to record the urls in `_download_urls`.
        # Calling `dl_manager.download_checksums` stop the url
        # registration (as checksums are stored remotelly)
        # `_test_checksums` validates the recorded urls.
        self._download_urls = set()
        self._stop_record_download = False

    def tearDown(self):
        super(DatasetBuilderTestCase, self).tearDown()
        for patcher in self.patchers:
            patcher.stop()

    def _mock_out_forbidden_os_functions(self):
        """Raises error if forbidden os functions are called instead of gfile."""
        err = AssertionError("Do not use `os`, but `tf.io.gfile` module instead. "
                                                 "This makes code compatible with more filesystems.")
        mock_os_path = absltest.mock.Mock(os.path, wraps=os.path)
        for fop in FORBIDDEN_OS_PATH_FUNCTIONS:
            getattr(mock_os_path, fop).side_effect = err
        mock_os = absltest.mock.Mock(os, path=mock_os_path)
        for fop in FORBIDDEN_OS_FUNCTIONS:
            getattr(mock_os, fop).side_effect = err
        os_patcher = absltest.mock.patch(
                self.DATASET_CLASS.__module__ + ".os", mock_os, create=True)
        os_patcher.start()
        self.patchers.append(os_patcher)

        mock_builtins = __builtins__.copy()
        mock_builtins["open"] = absltest.mock.Mock(side_effect=err)
        open_patcher = absltest.mock.patch(
                self.DATASET_CLASS.__module__ + ".__builtins__", mock_builtins)
        open_patcher.start()
        self.patchers.append(open_patcher)

        # It's hard to mock open within numpy, so mock np.load.
        np_load_patcher = absltest.mock.patch("numpy.load", _np_load)
        np_load_patcher.start()
        self.patchers.append(np_load_patcher)

    def test_baseclass(self):
        self.assertIsInstance(
                self.builder, builder.DatasetBuilder,
                "Dataset class must inherit from `builder.DatasetBuilder`.")
        # Since class was instantiated and base class is ABCMeta, then we know
        # all needed methods were implemented.

    def test_info(self):
        info = self.builder.info
        self.assertIsInstance(info, dataset_info.DatasetInfo)
        self.assertEqual(self.builder.name, info.name)

    def _add_url(self, url_or_urls):
        if self._stop_record_download:
            # Stop record the checksums if dl_manager.download_checksums has been
            # called (as checksums may be stored remotelly)
            return
        if isinstance(url_or_urls, download.resource.Resource):
            self._download_urls.add(url_or_urls.url)
        else:
            self._download_urls.add(url_or_urls)

    def _get_dl_extract_result(self, url):
        tf.nest.map_structure(self._add_url, url)
        del url
        if self.DL_EXTRACT_RESULT is None:
            return self.example_dir
        return utils.map_nested(lambda fname: os.path.join(self.example_dir, fname),
                                                        self.DL_EXTRACT_RESULT)

    def _get_dl_download_result(self, url):
        tf.nest.map_structure(self._add_url, url)
        if self.DL_DOWNLOAD_RESULT is None:
            # This is only to be backwards compatible with old approach.
            # In the future it will be replaced with using self.example_dir.
            return self._get_dl_extract_result(url)
        return utils.map_nested(lambda fname: os.path.join(self.example_dir, fname),
                                                        self.DL_DOWNLOAD_RESULT)

    def _download_checksums(self, url):
        self._stop_record_download = True

    def _make_builder(self, config=None):
        return self.DATASET_CLASS(  # pylint: disable=not-callable
                data_dir=self.tmp_dir,
                config=config,
                version=self.VERSION)

    @test_utils.run_in_graph_and_eager_modes()
    def test_download_and_prepare_as_dataset(self):
        # If configs specified, ensure they are all valid
        if self.BUILDER_CONFIG_NAMES_TO_TEST:
            for config in self.BUILDER_CONFIG_NAMES_TO_TEST:  # pylint: disable=not-an-iterable
                assert config in self.builder.builder_configs, (
                        "Config %s specified in test does not exist. Available:\n%s" % (
                                config, list(self.builder.builder_configs)))

        configs = self.builder.BUILDER_CONFIGS
        print("Total configs: %d" % len(configs))
        if configs:
            for config in configs:
                # Skip the configs that are not in the list.
                if (self.BUILDER_CONFIG_NAMES_TO_TEST is not None and
                        (config.name not in self.BUILDER_CONFIG_NAMES_TO_TEST)):  # pylint: disable=unsupported-membership-test
                    print("Skipping config %s" % config.name)
                    continue
                with self._subTest(config.name):
                    print("Testing config %s" % config.name)
                    builder = self._make_builder(config=config)
                    self._download_and_prepare_as_dataset(builder)
        else:
            self._download_and_prepare_as_dataset(self.builder)

    def _download_and_prepare_as_dataset(self, builder):
        # Provide the manual dir only if builder has MANUAL_DOWNLOAD_INSTRUCTIONS
        # set.

        missing_dir_mock = absltest.mock.PropertyMock(
                side_effect=Exception("Missing MANUAL_DOWNLOAD_INSTRUCTIONS"))

        manual_dir = (
                self.example_dir
                if builder.MANUAL_DOWNLOAD_INSTRUCTIONS else missing_dir_mock)
        with absltest.mock.patch.multiple(
                "tensorflow_datasets.core.download.DownloadManager",
                download_and_extract=self._get_dl_extract_result,
                download=self._get_dl_download_result,
                download_checksums=self._download_checksums,
                manual_dir=manual_dir,
        ):
            if isinstance(builder, builder.BeamBasedBuilder):
                import apache_beam as beam   # pylint: disable=import-outside-toplevel,g-import-not-at-top
                # For Beam datasets, set-up the runner config
                beam_runner = None
                beam_options = beam.options.pipeline_options.PipelineOptions()
            else:
                beam_runner = None
                beam_options = None

            download_config = download.DownloadConfig(
                    compute_stats=download.ComputeStatsMode.FORCE,
                    beam_runner=beam_runner,
                    beam_options=beam_options,
            )
            builder.download_and_prepare(download_config=download_config)

        with self._subTest("as_dataset"):
            self._assertAsDataset(builder)

        with self._subTest("num_examples"):
            self._assertNumSamples(builder)

        with self._subTest("reload"):
            # When reloading the dataset, metadata should been reloaded too.

            builder_reloaded = self._make_builder(config=builder.builder_config)
            self._assertNumSamples(builder_reloaded)

            # After reloading, as_dataset should still be working
            with self._subTest("as_dataset"):
                self._assertAsDataset(builder_reloaded)

    def _assertAsDataset(self, builder):
        split_to_checksums = {}  # {"split": set(examples_checksums)}
        for split_name, expected_examples_number in self.SPLITS.items():
            ds = builder.as_dataset(split=split_name)
            compare_shapes_and_types(
                    builder.info.features.get_tensor_info(),
                    tf.compat.v1.data.get_output_types(ds),
                    tf.compat.v1.data.get_output_shapes(ds),
            )
            examples = list(dataset_utils.as_numpy(
                    builder.as_dataset(split=split_name)))
            split_to_checksums[split_name] = set(checksum(rec) for rec in examples)
            if not builder.version.implements(utils.Experiment.S3):
                self.assertLen(examples, expected_examples_number)
        for (split1, hashes1), (split2, hashes2) in itertools.combinations(
                split_to_checksums.items(), 2):
            if (split1 in self.OVERLAPPING_SPLITS or
                    split2 in self.OVERLAPPING_SPLITS):
                continue
            self.assertFalse(
                    hashes1.intersection(hashes2),
                    ("Splits '%s' and '%s' are overlapping. Are you sure you want to "
                     "have the same objects in those splits? If yes, add one one of "
                     "them to OVERLAPPING_SPLITS class attribute.") % (split1, split2))

    def _assertNumSamples(self, builder):
        for split_name, expected_num_examples in self.SPLITS.items():
            self.assertEqual(
                    builder.info.splits[split_name].num_examples,
                    expected_num_examples,
            )
        self.assertEqual(
                builder.info.splits.total_num_examples,
                sum(self.SPLITS.values()),
        )


def checksum(example):
    """Computes the md5 for a given example."""

    def _bytes_flatten(flat_str, element):
        """Recursively flatten an element to its byte representation."""
        if isinstance(element, numbers.Number):
            # In python3, bytes(-3) is not allowed (or large numbers),
            # so convert to str to avoid problems.
            element = str(element)
        if isinstance(element, dict):
            for k, v in sorted(element.items()):
                flat_str.append(k)
                _bytes_flatten(flat_str, v)
        elif isinstance(element, str):
            if hasattr(element, "decode"):
                # Python2 considers bytes to be str, but are almost always latin-1
                # encoded bytes here. Extra step needed to avoid DecodeError.
                element = element.decode("latin-1")
            flat_str.append(element)
        elif isinstance(element,
                                        (tf.RaggedTensor, tf.compat.v1.ragged.RaggedTensorValue)):
            flat_str.append(str(element.to_list()))
        elif isinstance(element, np.ndarray):
            # tf.Tensor() returns np.array of dtype object, which don't work
            # with x.to_bytes(). So instead convert numpy into list.
            if element.dtype.type is np.object_:
                flat_str.append(str(tuple(element.shape)))
                flat_str.append(str(list(element.ravel())))
            else:
                flat_str.append(element.tobytes())
        else:
            flat_str.append(bytes(element))
        return flat_str

    flat_str = _bytes_flatten([], example)
    flat_bytes = [
            s.encode("utf-8") if not isinstance(s, bytes) else s
            for s in flat_str
    ]
    flat_bytes = b"".join(flat_bytes)

    hash_ = hashlib.md5()
    hash_.update(flat_bytes)
    return hash_.hexdigest()


def compare_shapes_and_types(tensor_info, output_types, output_shapes):
    """Compare shapes and types between TensorInfo and Dataset types/shapes."""
    for feature_name, feature_info in tensor_info.items():
        if isinstance(feature_info, dict):
            compare_shapes_and_types(feature_info, output_types[feature_name],
                                                             output_shapes[feature_name])
        else:
            expected_type = feature_info.dtype
            output_type = output_types[feature_name]
            if expected_type != output_type:
                raise TypeError("Feature %s has type %s but expected %s" %
                                                (feature_name, output_type, expected_type))

            expected_shape = feature_info.shape
            output_shape = output_shapes[feature_name]
            tf_utils.assert_shape_match(expected_shape, output_shape)
