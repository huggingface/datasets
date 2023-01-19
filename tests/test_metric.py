import os
import pickle
import tempfile
import time
from multiprocessing import Pool
from unittest import TestCase

import pytest

from datasets.features import Features, Sequence, Value
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
        return (
            {
                "accuracy": sum(i == j for i, j in zip(predictions, references)) / len(predictions),
                "set_equality": set(predictions) == set(references),
            }
            if predictions
            else {}
        )

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

    @classmethod
    def separate_predictions_and_references(cls):
        return ([1, 2, 3, 4], [1, 2, 3, 4]), ([1, 2, 4, 5], [1, 2, 3, 4])

    @classmethod
    def separate_expected_results(cls):
        return [{"accuracy": 1.0, "set_equality": True}, {"accuracy": 0.5, "set_equality": False}]


def properly_del_metric(metric):
    """properly delete a metric on windows if the process is killed during multiprocessing"""
    if metric is not None:
        if metric.filelock is not None:
            metric.filelock.release()
        if metric.rendez_vous_lock is not None:
            metric.rendez_vous_lock.release()
        del metric.writer
        del metric.data
        del metric


def metric_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    metric = None
    try:
        num_process, process_id, preds, refs, exp_id, cache_dir, wait = arg
        metric = DummyMetric(
            num_process=num_process, process_id=process_id, experiment_id=exp_id, cache_dir=cache_dir, timeout=5
        )
        time.sleep(wait)
        results = metric.compute(predictions=preds, references=refs)
        return results
    finally:
        properly_del_metric(metric)


def metric_add_batch_and_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    metric = None
    try:
        num_process, process_id, preds, refs, exp_id, cache_dir, wait = arg
        metric = DummyMetric(
            num_process=num_process, process_id=process_id, experiment_id=exp_id, cache_dir=cache_dir, timeout=5
        )
        metric.add_batch(predictions=preds, references=refs)
        time.sleep(wait)
        results = metric.compute()
        return results
    finally:
        properly_del_metric(metric)


def metric_add_and_compute(arg):
    """Thread worker function for distributed evaluation testing.
    On base level to be pickable.
    """
    metric = None
    try:
        num_process, process_id, preds, refs, exp_id, cache_dir, wait = arg
        metric = DummyMetric(
            num_process=num_process, process_id=process_id, experiment_id=exp_id, cache_dir=cache_dir, timeout=5
        )
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        time.sleep(wait)
        results = metric.compute()
        return results
    finally:
        properly_del_metric(metric)


class TestMetric(TestCase):
    def test_dummy_metric(self):
        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()

        metric = DummyMetric(experiment_id="test_dummy_metric")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        del metric

        metric = DummyMetric(experiment_id="test_dummy_metric")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(experiment_id="test_dummy_metric")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        # With keep_in_memory
        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        del metric

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        self.assertDictEqual({}, metric.compute(predictions=[], references=[]))
        del metric

        metric = DummyMetric(keep_in_memory=True, experiment_id="test_dummy_metric")
        with self.assertRaisesRegex(ValueError, "Mismatch in the number"):
            metric.add_batch(predictions=[1, 2, 3], references=[1, 2, 3, 4])
        del metric

    def test_metric_with_cache_dir(self):
        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()

        with tempfile.TemporaryDirectory() as tmp_dir:
            metric = DummyMetric(experiment_id="test_dummy_metric", cache_dir=tmp_dir)
            self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
            del metric

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
        del metric, other_metric

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
        del metric, other_metric

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
        del metric, other_metric

    def test_separate_experiments_in_parallel(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            (preds_0, refs_0), (preds_1, refs_1) = DummyMetric.separate_predictions_and_references()
            expected_results = DummyMetric.separate_expected_results()

            pool = Pool(processes=4)

            results = pool.map(
                metric_compute,
                [
                    (1, 0, preds_0, refs_0, None, tmp_dir, 0),
                    (1, 0, preds_1, refs_1, None, tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results[0], results[0])
            self.assertDictEqual(expected_results[1], results[1])
            del results

            # more than one sec of waiting so that the second metric has to sample a new hashing name
            results = pool.map(
                metric_compute,
                [
                    (1, 0, preds_0, refs_0, None, tmp_dir, 2),
                    (1, 0, preds_1, refs_1, None, tmp_dir, 2),
                ],
            )
            self.assertDictEqual(expected_results[0], results[0])
            self.assertDictEqual(expected_results[1], results[1])
            del results

            results = pool.map(
                metric_add_and_compute,
                [
                    (1, 0, preds_0, refs_0, None, tmp_dir, 0),
                    (1, 0, preds_1, refs_1, None, tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results[0], results[0])
            self.assertDictEqual(expected_results[1], results[1])
            del results

            results = pool.map(
                metric_add_batch_and_compute,
                [
                    (1, 0, preds_0, refs_0, None, tmp_dir, 0),
                    (1, 0, preds_1, refs_1, None, tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results[0], results[0])
            self.assertDictEqual(expected_results[1], results[1])
            del results

    def test_distributed_metrics(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            (preds_0, refs_0), (preds_1, refs_1) = DummyMetric.distributed_predictions_and_references()
            expected_results = DummyMetric.distributed_expected_results()

            pool = Pool(processes=4)

            results = pool.map(
                metric_compute,
                [
                    (2, 0, preds_0, refs_0, "test_distributed_metrics_0", tmp_dir, 0),
                    (2, 1, preds_1, refs_1, "test_distributed_metrics_0", tmp_dir, 0.5),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])
            del results

            results = pool.map(
                metric_compute,
                [
                    (2, 0, preds_0, refs_0, "test_distributed_metrics_0", tmp_dir, 0.5),
                    (2, 1, preds_1, refs_1, "test_distributed_metrics_0", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])
            del results

            results = pool.map(
                metric_add_and_compute,
                [
                    (2, 0, preds_0, refs_0, "test_distributed_metrics_1", tmp_dir, 0),
                    (2, 1, preds_1, refs_1, "test_distributed_metrics_1", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])
            del results

            results = pool.map(
                metric_add_batch_and_compute,
                [
                    (2, 0, preds_0, refs_0, "test_distributed_metrics_2", tmp_dir, 0),
                    (2, 1, preds_1, refs_1, "test_distributed_metrics_2", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertIsNone(results[1])
            del results

            # To use several distributed metrics on the same local file system, need to specify an experiment_id
            try:
                results = pool.map(
                    metric_add_and_compute,
                    [
                        (2, 0, preds_0, refs_0, "test_distributed_metrics_3", tmp_dir, 0),
                        (2, 1, preds_1, refs_1, "test_distributed_metrics_3", tmp_dir, 0),
                        (2, 0, preds_0, refs_0, "test_distributed_metrics_3", tmp_dir, 0),
                        (2, 1, preds_1, refs_1, "test_distributed_metrics_3", tmp_dir, 0),
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
                del results

            results = pool.map(
                metric_add_and_compute,
                [
                    (2, 0, preds_0, refs_0, "exp_0", tmp_dir, 0),
                    (2, 1, preds_1, refs_1, "exp_0", tmp_dir, 0),
                    (2, 0, preds_0, refs_0, "exp_1", tmp_dir, 0),
                    (2, 1, preds_1, refs_1, "exp_1", tmp_dir, 0),
                ],
            )
            self.assertDictEqual(expected_results, results[0])
            self.assertDictEqual(expected_results, results[2])
            self.assertIsNone(results[1])
            self.assertIsNone(results[3])
            del results

            # With keep_in_memory is not allowed
            with self.assertRaises(ValueError):
                DummyMetric(
                    experiment_id="test_distributed_metrics_4",
                    keep_in_memory=True,
                    num_process=2,
                    process_id=0,
                    cache_dir=tmp_dir,
                )

    def test_dummy_metric_pickle(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = os.path.join(tmp_dir, "metric.pt")
            preds, refs = DummyMetric.predictions_and_references()
            expected_results = DummyMetric.expected_results()

            metric = DummyMetric(experiment_id="test_dummy_metric_pickle")

            with open(tmp_file, "wb") as f:
                pickle.dump(metric, f)
            del metric

            with open(tmp_file, "rb") as f:
                metric = pickle.load(f)
            self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
            del metric

    def test_input_numpy(self):
        import numpy as np

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = np.array(preds), np.array(refs)

        metric = DummyMetric(experiment_id="test_input_numpy")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        del metric

        metric = DummyMetric(experiment_id="test_input_numpy")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(experiment_id="test_input_numpy")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

    @require_torch
    def test_input_torch(self):
        import torch

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = torch.tensor(preds), torch.tensor(refs)

        metric = DummyMetric(experiment_id="test_input_torch")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        del metric

        metric = DummyMetric(experiment_id="test_input_torch")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(experiment_id="test_input_torch")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

    @require_tf
    def test_input_tf(self):
        import tensorflow as tf

        preds, refs = DummyMetric.predictions_and_references()
        expected_results = DummyMetric.expected_results()
        preds, refs = tf.constant(preds), tf.constant(refs)

        metric = DummyMetric(experiment_id="test_input_tf")
        self.assertDictEqual(expected_results, metric.compute(predictions=preds, references=refs))
        del metric

        metric = DummyMetric(experiment_id="test_input_tf")
        metric.add_batch(predictions=preds, references=refs)
        self.assertDictEqual(expected_results, metric.compute())
        del metric

        metric = DummyMetric(experiment_id="test_input_tf")
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertDictEqual(expected_results, metric.compute())
        del metric


class MetricWithMultiLabel(Metric):
    def _info(self):
        return MetricInfo(
            description="dummy metric for tests",
            citation="insert citation here",
            features=Features(
                {"predictions": Sequence(Value("int64")), "references": Sequence(Value("int64"))}
                if self.config_name == "multilabel"
                else {"predictions": Value("int64"), "references": Value("int64")}
            ),
        )

    def _compute(self, predictions=None, references=None):
        return (
            {
                "accuracy": sum(i == j for i, j in zip(predictions, references)) / len(predictions),
            }
            if predictions
            else {}
        )


@pytest.mark.parametrize(
    "config_name, predictions, references, expected",
    [
        (None, [1, 2, 3, 4], [1, 2, 4, 3], 0.5),  # Multiclass: Value("int64")
        (
            "multilabel",
            [[1, 0], [1, 0], [1, 0], [1, 0]],
            [[1, 0], [0, 1], [1, 1], [0, 0]],
            0.25,
        ),  # Multilabel: Sequence(Value("int64"))
    ],
)
def test_metric_with_multilabel(config_name, predictions, references, expected, tmp_path):
    cache_dir = tmp_path / "cache"
    metric = MetricWithMultiLabel(config_name, cache_dir=cache_dir)
    results = metric.compute(predictions=predictions, references=references)
    assert results["accuracy"] == expected


def test_safety_checks_process_vars():
    with pytest.raises(ValueError):
        _ = DummyMetric(process_id=-2)

    with pytest.raises(ValueError):
        _ = DummyMetric(num_process=2, process_id=3)


class AccuracyWithNonStandardFeatureNames(Metric):
    def _info(self):
        return MetricInfo(
            description="dummy metric for tests",
            citation="insert citation here",
            features=Features({"inputs": Value("int64"), "targets": Value("int64")}),
        )

    def _compute(self, inputs, targets):
        return (
            {
                "accuracy": sum(i == j for i, j in zip(inputs, targets)) / len(targets),
            }
            if targets
            else {}
        )

    @classmethod
    def inputs_and_targets(cls):
        return ([1, 2, 3, 4], [1, 2, 4, 3])

    @classmethod
    def expected_results(cls):
        return {"accuracy": 0.5}


def test_metric_with_non_standard_feature_names_add(tmp_path):
    cache_dir = tmp_path / "cache"
    inputs, targets = AccuracyWithNonStandardFeatureNames.inputs_and_targets()
    metric = AccuracyWithNonStandardFeatureNames(cache_dir=cache_dir)
    for input, target in zip(inputs, targets):
        metric.add(inputs=input, targets=target)
    results = metric.compute()
    assert results == AccuracyWithNonStandardFeatureNames.expected_results()


def test_metric_with_non_standard_feature_names_add_batch(tmp_path):
    cache_dir = tmp_path / "cache"
    inputs, targets = AccuracyWithNonStandardFeatureNames.inputs_and_targets()
    metric = AccuracyWithNonStandardFeatureNames(cache_dir=cache_dir)
    metric.add_batch(inputs=inputs, targets=targets)
    results = metric.compute()
    assert results == AccuracyWithNonStandardFeatureNames.expected_results()


def test_metric_with_non_standard_feature_names_compute(tmp_path):
    cache_dir = tmp_path / "cache"
    inputs, targets = AccuracyWithNonStandardFeatureNames.inputs_and_targets()
    metric = AccuracyWithNonStandardFeatureNames(cache_dir=cache_dir)
    results = metric.compute(inputs=inputs, targets=targets)
    assert results == AccuracyWithNonStandardFeatureNames.expected_results()
