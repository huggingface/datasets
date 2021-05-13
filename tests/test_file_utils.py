import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pytest

from datasets.utils.file_utils import (
    DownloadConfig,
    OfflineModeIsEnabled,
    cached_path,
    ftp_get,
    ftp_head,
    http_get,
    http_head,
    temp_seed,
)

from .utils import require_tf, require_torch


class TempSeedTest(TestCase):
    @require_tf
    def test_tensorflow(self):
        import tensorflow as tf
        from tensorflow.keras import layers

        def gen_random_output():
            model = layers.Dense(2)
            x = tf.random.uniform((1, 3))
            return model(x).numpy()

        with temp_seed(42, set_tensorflow=True):
            out1 = gen_random_output()
        with temp_seed(42, set_tensorflow=True):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)

    @require_torch
    def test_torch(self):
        import torch

        def gen_random_output():
            model = torch.nn.Linear(3, 2)
            x = torch.rand(1, 3)
            return model(x).detach().numpy()

        with temp_seed(42, set_pytorch=True):
            out1 = gen_random_output()
        with temp_seed(42, set_pytorch=True):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)

    def test_numpy(self):
        def gen_random_output():
            return np.random.rand(1, 3)

        with temp_seed(42):
            out1 = gen_random_output()
        with temp_seed(42):
            out2 = gen_random_output()
        out3 = gen_random_output()

        np.testing.assert_equal(out1, out2)
        self.assertGreater(np.abs(out1 - out3).sum(), 0)


def test_cached_path_extract(xz_file, tmp_path, text_file):
    filename = xz_file
    cache_dir = tmp_path / "cache"
    download_config = DownloadConfig(cache_dir=cache_dir, extract_compressed_file=True)
    extracted_filename = cached_path(filename, download_config=download_config)
    with open(extracted_filename) as f:
        extracted_file_content = f.read()
    with open(text_file) as f:
        expected_file_content = f.read()
    assert extracted_file_content == expected_file_content


def test_cached_path_local(text_file):
    # absolute path
    text_file = str(Path(text_file).resolve())
    assert cached_path(text_file) == text_file
    # relative path
    text_file = str(Path(__file__).resolve().relative_to(Path(os.getcwd())))
    assert cached_path(text_file) == text_file


def test_cached_path_missing_local(tmp_path):
    # absolute path
    missing_file = str(tmp_path.resolve() / "__missing_file__.txt")
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)
    # relative path
    missing_file = "./__missing_file__.txt"
    with pytest.raises(FileNotFoundError):
        cached_path(missing_file)


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_cached_path_offline():
    with pytest.raises(OfflineModeIsEnabled):
        cached_path("https://huggingface.co")


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_http_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        http_get("https://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        http_head("https://huggingface.co")


@patch("datasets.config.HF_DATASETS_OFFLINE", True)
def test_ftp_offline(tmp_path_factory):
    filename = tmp_path_factory.mktemp("data") / "file.html"
    with pytest.raises(OfflineModeIsEnabled):
        ftp_get("ftp://huggingface.co", temp_file=filename)
    with pytest.raises(OfflineModeIsEnabled):
        ftp_head("ftp://huggingface.co")
