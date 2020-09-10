import os
import pickle
import tempfile
import time
from multiprocessing import Pool
from unittest import TestCase

from datasets.features import Features, Value
from datasets.metric import Metric, MetricInfo

from .utils import require_tf, require_torch


class DummyMetric(Metric):
    def _info(self):
        return MetricInfo(
            description="dummy metric for tests",
            citation="insert citation here",
            features=Features({"predictions": Value("int64"), "references": Value("int64")}),
        )

    def _compute(self, predictions, references):
        return {
            "accuracy": sum(i == j for i, j in zip(predictions, references)) / len(predictions),
            "set_equality": set(predictions) == set(references),
        }

    @classmethod
    def predictions_and_references(cls):
        return ([1, 2, 3, 4], [1, 2, 4, 3])

    @classmethod
    def expected_results(cls):
        return {"accuracy": 0.5, "set_equality": True}

    @classmethod
    def other_predictions_and_references(cls):
        return ([1, 3, 4, 5], [1, 2, 3, 4])

    @classmethod
    def other_expected_results(cls):
        return {"accuracy": 0.25, "set_equality": False}

    @classmethod
    def distributed_predictions_and_references(cls):
        return ([1, 2, 3, 4], [1, 2, 3, 4]), ([1, 2, 4, 5], [1, 2, 3, 4])

    @classmethod
    def distributed_expected_results(cls):
        return {"accuracy": 0.75, "set_equality": False}


def metric_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    process_id, preds, refs, exp_id, data_dir, wait = arg
    metric = DummyMetric(num_process=2, process_id=process_id, experiment_id=exp_id, data_dir=data_dir, timeout=5)
    time.sleep(wait)
    return metric.compute(predictions=preds, references=refs)


def metric_add_batch_and_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    process_id, preds, refs, exp_id, data_dir, wait = arg
    metric = DummyMetric(num_process=2, process_id=process_id, experiment_id=exp_id, data_dir=data_dir, timeout=5)
    time.sleep(wait)
    metric.add_batch(predictions=preds, references=refs)
    return metric.compute()


def metric_add_and_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    process_id, preds, refs, exp_id, data_dir, wait = arg
    metric = DummyMetric(num_process=2, process_id=process_id, experiment_id=exp_id, data_dir=data_dir, timeout=5)
    time.sleep(wait)
    for pred, ref in zip(preds, refs):
        metric.add(prediction=pred, reference=ref)
    return metric.compute()


def metric_add_and_compute_exp_id(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    process_id, preds, refs, exp_id, data_dir, wait = arg
    metric = DummyMetric(num_process=2, process_id=process_id, experiment_id=exp_id, data_dir=data_dir, timeout=5)
    time.sleep(wait)
    for pred, ref in zip(preds, refs):
        metric.add(prediction=pred, reference=ref)
    return metric.compute()


class TestMetric(TestCase):
    def test_dummy_metric(self):
        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()

        metric = DummyMetric(experiment_id="test_dummy_metric")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric(experiment_id="test_dummy_metric")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())

        metric = DummyMetric(experiment_id="test_dummy_metric")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())

        # With keep_in_memory
        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())

    def test_concurrent_metrics(self):
        preds, refs = DummyMetric.predictions_and_references()
        other_preds, other_refs = DummyMetric.other_predictions_and_references()
        expected_results = DummyMetric.expected_results()
        other_expected_results = DummyMetric.other_expected_results()

        metric = DummyMetric(experiment_id="test_concurrent_metrics")
        other_metric = DummyMetric(
            experiment_id="test_concurrent_metrics",
        )

        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        self.assertDictEqual(
            other_expected_results, other_metric.compute(predictions=other_preds, references=other_refs)
        )

        metric = DummyMetric(
            experiment_id="test_concurrent_metrics",
        )
        other_metric = DummyMetric(
            experiment_id="test_concurrent_metrics",
        )
        metric.add_batch(predictions=preds, references=refs)
        other_metric.add_batch(predictions=other_preds, references=other_refs)
        self.assertDictEqual(expected_results, metric.compute())
        self.assertDictEqual(other_expected_results, other_metric.compute())

        for pred, ref, other_pred, other_ref in zip(preds, refs, other_preds, other_refs):
            metric.add(prediction=pred, reference=ref)
            other_metric.add(prediction=other_pred, reference=other_ref)
        self.assertDictEqual(expected_results, metric.compute())
        self.assertDictEqual(other_expected_results, other_metric.compute())

        # With keep_in_memory
        metric = DummyMetric(experiment_id="test_concurrent_metrics", keep_in_memory=True)
        other_metric = DummyMetric(experiment_id="test_concurrent_metrics", keep_in_memory=True)

        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        self.assertDictEqual(
            other_expected_results, other_metric.compute(predictions=other_preds, references=other_refs)
        )

        metric = DummyMetric(experiment_id="test_concurrent_metrics", keep_in_memory=True)
        other_metric = DummyMetric(experiment_id="test_concurrent_metrics", keep_in_memory=True)
        metric.add_batch(predictions=preds, references=refs)
        other_metric.add_batch(predictions=other_preds, references=other_refs)
        self.assertDictEqual(expected_results, metric.compute())
        self.assertDictEqual(other_expected_results, other_metric.compute())

        for pred, ref, other_pred, other_ref in zip(preds, refs, other_preds, other_refs):
            metric.add(prediction=pred, reference=ref)
            other_metric.add(prediction=other_pred, reference=other_ref)
        self.assertDictEqual(expected_results, metric.compute())
        self.assertDictEqual(other_expected_results, other_metric.compute())

    def test_distributed_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            (preds_0, refs_0), (preds_1, refs_1) = DummyMetric.distributed_predictions_and_references()
            expected_results = DummyMetric.distributed_expected_results()

            pool = Pool()

            results = pool.map(
                metric_compute,
                [
                    (0, preds_0, refs_0, "test_distributed_metrics_0", tmp_dir, 0),
                    (1, preds_1, refs_1, "test_distributed_metrics_0", tmp_dir, 0.5),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])

            results = pool.map(
                metric_compute,
                [
                    (0, preds_0, refs_0, "test_distributed_metrics_0", tmp_dir, 0.5),
                    (1, preds_1, refs_1, "test_distributed_metrics_0", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])

            results = pool.map(
                metric_add_and_compute,
                [
                    (0, preds_0, refs_0, "test_distributed_metrics_1", tmp_dir, 0),
                    (1, preds_1, refs_1, "test_distributed_metrics_1", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])

            results = pool.map(
                metric_add_batch_and_compute,
                [
                    (0, preds_0, refs_0, "test_distributed_metrics_2", tmp_dir, 0),
                    (1, preds_1, refs_1, "test_distributed_metrics_2", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])

            # To use several distributed metrics on the same local file system, need to specify an experiment_id
            try:
                results = pool.map(
                    metric_add_and_compute,
                    [
                        (0, preds_0, refs_0, "test_distributed_metrics_3", tmp_dir, 0),
                        (1, preds_1, refs_1, "test_distributed_metrics_3", tmp_dir, 0),
                        (0, preds_0, refs_0, "test_distributed_metrics_3", tmp_dir, 0),
                        (1, preds_1, refs_1, "test_distributed_metrics_3", tmp_dir, 0),
                    ],
                )
            except ValueError:
                # We are fine with either raising a ValueError or computing well the metric
                # Being sure we raise the error would means making the dummy dataset bigger
                # and the test longer...
                pass
            else:
                self.assertDictEqual(expected_results, results[0])
                self.assertDictEqual(expected_results, results[2])
                self.assertIsNone(results[1])
                self.assertIsNone(results[3])

            results = pool.map(
                metric_add_and_compute_exp_id,
                [
                    (0, preds_0, refs_0, "exp_0", tmp_dir, 0),
                    (1, preds_1, refs_1, "exp_0", tmp_dir, 0),
                    (0, preds_0, refs_0, "exp_1", tmp_dir, 0),
                    (1, preds_1, refs_1, "exp_1", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertDictEqual(expected_results, results[2])
            self.assertIsNone(results[1])
            self.assertIsNone(results[3])

            # With keep_in_memory is not allowed
            with self.assertRaises(AssertionError):
                DummyMetric(
                    experiment_id="test_distributed_metrics_4",
                    keep_in_memory=True,
                    num_process=2,
                    process_id=0,
                    data_dir=tmp_dir,
                )

    def test_dummy_metric_pickle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "metric.pt")
            preds, refs = DummyMetric.predictions_and_references()
            expected_results = DummyMetric.expected_results()

            metric = DummyMetric(experiment_id="test_dummy_metric_pickle")

            with open(tmp_file, "wb") as f:
                pickle.dump(metric, f)

            with open(tmp_file, "rb") as f:
                metric = pickle.load(f)
            self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

    def test_input_numpy(self):
        import numpy as np

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = np.array(preds), np.array(refs)

        metric = DummyMetric(experiment_id="test_input_numpy")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric(experiment_id="test_input_numpy")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())

        metric = DummyMetric(experiment_id="test_input_numpy")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())

    @require_torch
    def test_input_torch(self):
        import torch

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = torch.Tensor(preds), torch.Tensor(refs)

        metric = DummyMetric(experiment_id="test_input_torch")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric(experiment_id="test_input_torch")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())

        metric = DummyMetric(experiment_id="test_input_torch")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())

    @require_tf
    def test_input_tf(self):
        import tensorflow as tf

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = tf.constant(preds), tf.constant(refs)

        metric = DummyMetric(experiment_id="test_input_tf")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric(experiment_id="test_input_tf")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())

        metric = DummyMetric(experiment_id="test_input_tf")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
