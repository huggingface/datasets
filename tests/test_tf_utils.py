import os
from types import SimpleNamespace
from unittest.mock import Mock

import numpy as np
import pytest

from datasets import Dataset
from datasets.utils import tf_utils

from .utils import require_tf


@require_tf
@pytest.mark.parametrize("cuda_devices", [None, "0"])
@pytest.mark.parametrize("num_workers", [1, 2])
def test_tf_workers_hide_gpus_before_importing_collator(monkeypatch, cuda_devices, num_workers):
    import tensorflow as tf

    from .fixtures.tf_initialized_collate import collate_with_initialized_tensorflow

    parent_gpus = tf.config.get_visible_devices("GPU")
    if cuda_devices is None:
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    else:
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", cuda_devices)
    dataset = Dataset.from_dict({"x": list(range(6))})
    tf_dataset = dataset.to_tf_dataset(
        collate_fn=collate_with_initialized_tensorflow, batch_size=2, num_workers=num_workers, prefetch=False
    )
    batches = list(tf_dataset.as_numpy_iterator())
    np.testing.assert_array_equal(np.concatenate([batch["x"] for batch in batches]), np.arange(6))
    assert np.concatenate([batch["gpus_hidden_at_import"] for batch in batches]).all()
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == cuda_devices
    assert tf.config.get_visible_devices("GPU") == parent_gpus


@pytest.mark.parametrize("cuda_devices", [None, "0"])
def test_tf_worker_start_failure_restores_cuda_environment(monkeypatch, cuda_devices):
    if cuda_devices is None:
        monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    else:
        monkeypatch.setenv("CUDA_VISIBLE_DEVICES", cuda_devices)
    context = tf_utils.get_context("spawn")
    failure = RuntimeError("worker start failed")
    worker = Mock()
    worker.start.side_effect = failure
    monkeypatch.setattr(context, "Process", lambda **kwargs: worker)
    generator = tf_utils.NumpyMultiprocessingGenerator(
        dataset=Dataset.from_dict({"x": [0, 1]}),
        cols_to_retain=["x"],
        collate_fn=None,
        collate_fn_args={},
        columns_to_np_types={"x": np.int64},
        output_signature={"x": SimpleNamespace(shape=SimpleNamespace(rank=1))},
        shuffle=False,
        batch_size=1,
        drop_remainder=False,
        num_workers=1,
    )
    with pytest.raises(RuntimeError) as exc_info:
        next(iter(generator))
    assert exc_info.value is failure
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == cuda_devices
