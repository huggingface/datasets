# coding=utf-8
# Copyright 2020 HuggingFace Inc.
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

import doctest
import glob
import importlib
import inspect
import os
import re
from contextlib import contextmanager
from functools import wraps
from unittest.mock import patch

import numpy as np
import pytest
from absl.testing import parameterized

import datasets
from datasets import load_metric

from .utils import for_all_test_methods, local, slow


REQUIRE_FAIRSEQ = {"comet"}
_has_fairseq = importlib.util.find_spec("fairseq") is not None


def skip_if_dataset_requires_fairseq(test_case):
    @wraps(test_case)
    def wrapper(self, metric_name):
        if not _has_fairseq and metric_name in REQUIRE_FAIRSEQ:
            self.skipTest('"test requires Fairseq"')
        else:
            test_case(self, metric_name)

    return wrapper


def get_local_metric_names():
    metrics = [metric_dir.split(os.sep)[-2] for metric_dir in glob.glob("./metrics/*/")]
    return [{"testcase_name": x, "metric_name": x} for x in metrics if x != "gleu"]  # gleu is unfinished


@parameterized.named_parameters(get_local_metric_names())
@for_all_test_methods(skip_if_dataset_requires_fairseq)
@local
class LocalMetricTest(parameterized.TestCase):
    INTENSIVE_CALLS_PATCHER = {}
    metric_name = None

    def test_load_metric(self, metric_name):
        doctest.ELLIPSIS_MARKER = "[...]"
        metric_module = importlib.import_module(datasets.load.prepare_module(os.path.join("metrics", metric_name))[0])
        metric = datasets.load.import_main_class(metric_module.__name__, dataset=False)
        # check parameters
        parameters = inspect.signature(metric._compute).parameters
        self.assertTrue("predictions" in parameters)
        self.assertTrue("references" in parameters)
        self.assertTrue(all([p.kind != p.VAR_KEYWORD for p in parameters.values()]))  # no **kwargs
        # run doctest
        with self.patch_intensive_calls(metric_name, metric_module.__name__):
            with self.use_local_metrics():
                results = doctest.testmod(metric_module, verbose=True, raise_on_error=True)
        self.assertEqual(results.failed, 0)
        self.assertGreater(results.attempted, 1)

    @slow
    def test_load_real_metric(self, metric_name):
        doctest.ELLIPSIS_MARKER = "[...]"
        metric_module = importlib.import_module(datasets.load.prepare_module(os.path.join("metrics", metric_name))[0])
        # run doctest
        with self.use_local_metrics():
            results = doctest.testmod(metric_module, verbose=True, raise_on_error=True)
        self.assertEqual(results.failed, 0)
        self.assertGreater(results.attempted, 1)

    @contextmanager
    def patch_intensive_calls(self, metric_name, module_name):
        if metric_name in self.INTENSIVE_CALLS_PATCHER:
            with self.INTENSIVE_CALLS_PATCHER[metric_name](module_name):
                yield
        else:
            yield

    @contextmanager
    def use_local_metrics(self):
        def load_local_metric(metric_name, *args, **kwargs):
            return load_metric(os.path.join("metrics", metric_name), *args, **kwargs)

        with patch("datasets.load_metric") as mock_load_metric:
            mock_load_metric.side_effect = load_local_metric
            yield

    @classmethod
    def register_intensive_calls_patcher(cls, metric_name):
        def wrapper(patcher):
            patcher = contextmanager(patcher)
            cls.INTENSIVE_CALLS_PATCHER[metric_name] = patcher
            return patcher

        return wrapper


# Metrics intensive calls patchers
# --------------------------------


@LocalMetricTest.register_intensive_calls_patcher("bleurt")
def patch_bleurt(module_name):
    import tensorflow.compat.v1 as tf
    from bleurt.score import Predictor

    tf.flags.DEFINE_string("sv", "", "")  # handle pytest cli flags

    class MockedPredictor(Predictor):
        def predict(self, input_dict):
            assert len(input_dict["input_ids"]) == 2
            return np.array([1.03, 1.04])

    # mock predict_fn which is supposed to do a forward pass with a bleurt model
    with patch("bleurt.score._create_predictor") as mock_create_predictor:
        mock_create_predictor.return_value = MockedPredictor()
        yield


@LocalMetricTest.register_intensive_calls_patcher("bertscore")
def patch_bertscore(module_name):
    import torch

    def bert_cos_score_idf(model, refs, *args, **kwargs):
        return torch.tensor([[1.0, 1.0, 1.0]] * len(refs))

    # mock get_model which is supposed to do download a bert model
    # mock bert_cos_score_idf which is supposed to do a forward pass with a bert model
    with patch("bert_score.scorer.get_model"), patch(
        "bert_score.scorer.bert_cos_score_idf"
    ) as mock_bert_cos_score_idf:
        mock_bert_cos_score_idf.side_effect = bert_cos_score_idf
        yield


@LocalMetricTest.register_intensive_calls_patcher("comet")
def patch_comet(module_name):
    def download_model(model):
        class Model:
            def predict(self, data, *args, **kwargs):
                assert len(data) == 2
                scores = [0.19, 0.92]
                data[0]["predicted_score"] = scores[0]
                data[1]["predicted_score"] = scores[1]
                return data, scores

        print("Download succeeded. Loading model...")
        return Model()

    # mock download_model which is supposed to do download a bert model
    with patch("comet.models.download_model") as mock_download_model:
        mock_download_model.side_effect = download_model
        yield


def test_seqeval_raises_when_incorrect_scheme():
    metric = load_metric(os.path.join("metrics", "seqeval"))
    wrong_scheme = "ERROR"
    error_message = f"Scheme should be one of [IOB1, IOB2, IOE1, IOE2, IOBES, BILOU], got {wrong_scheme}"
    with pytest.raises(ValueError, match=re.escape(error_message)):
        metric.compute(predictions=[], references=[], scheme=wrong_scheme)
