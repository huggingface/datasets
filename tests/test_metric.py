from unittest import TestCase

from nlp.features import Features, Value
from nlp.metric import Metric, MetricInfo

from .utils import require_tf, require_torch


class DummyMetric(Metric):
    def _info(self):
        return MetricInfo(
            description="dummy metric for tests",
            citation="insert citation here",
            features=Features({"predictions": Value("int64"), "references": Value("int64")}),
        )

    def _compute(self, predictions, references):
        return sum(i == j for i, j in zip(predictions, references)) / len(predictions)


class TestMetric(TestCase):
    def test_dummy_metric(self):
        preds, refs = [1, 2, 3, 4], [1, 2, 4, 3]

        metric = DummyMetric()
        self.assertEqual(0.5, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric()
        metric.add_batch(predictions=preds, references=refs)
        self.assertEqual(0.5, metric.compute())

        metric = DummyMetric()
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertEqual(0.5, metric.compute())

    def test_input_numpy(self):
        import numpy as np

        preds, refs = np.array([1, 2, 3, 4]), np.array([1, 2, 4, 3])

        metric = DummyMetric()
        self.assertEqual(0.5, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric()
        metric.add_batch(predictions=preds, references=refs)
        self.assertEqual(0.5, metric.compute())

        metric = DummyMetric()
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertEqual(0.5, metric.compute())

    @require_torch
    def test_input_torch(self):
        import torch

        preds, refs = torch.Tensor([1, 2, 3, 4]), torch.Tensor([1, 2, 4, 3])

        metric = DummyMetric()
        self.assertEqual(0.5, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric()
        metric.add_batch(predictions=preds, references=refs)
        self.assertEqual(0.5, metric.compute())

        metric = DummyMetric()
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertEqual(0.5, metric.compute())

    @require_tf
    def test_input_tf(self):
        import tensorflow as tf

        preds, refs = tf.constant([1, 2, 3, 4]), tf.constant([1, 2, 4, 3])

        metric = DummyMetric()
        self.assertEqual(0.5, metric.compute(predictions=preds, references=refs))

        metric = DummyMetric()
        metric.add_batch(predictions=preds, references=refs)
        self.assertEqual(0.5, metric.compute())

        metric = DummyMetric()
        for pred, ref in zip(preds, refs):
            metric.add(prediction=pred, reference=ref)
        self.assertEqual(0.5, metric.compute())
