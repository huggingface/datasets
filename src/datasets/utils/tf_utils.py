# Copyright 2022 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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

"""TF-specific utils import."""

from math import ceil
from multiprocessing import get_context

import numpy as np
import pyarrow as pa

from .. import config


def minimal_tf_collate_fn(features):
    if config.TF_AVAILABLE:
        import tensorflow as tf
    else:
        raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")

    first = features[0]
    batch = {}
    for k, v in first.items():
        if isinstance(v, np.ndarray):
            batch[k] = np.stack([f[k] for f in features])
        elif isinstance(v, tf.Tensor):
            batch[k] = tf.stack([f[k] for f in features])
        else:
            batch[k] = np.array([f[k] for f in features])
    return batch


def minimal_tf_collate_fn_with_renaming(features):
    batch = minimal_tf_collate_fn(features)
    if "label" in batch:
        batch["labels"] = batch["label"]
        del batch["label"]
    return batch


def is_numeric_pa_type(pa_type):
    if pa.types.is_list(pa_type):
        return is_numeric_pa_type(pa_type.value_type)
    return pa.types.is_integer(pa_type) or pa.types.is_floating(pa_type) or pa.types.is_decimal(pa_type)


def is_numeric_feature(feature):
    from .. import ClassLabel, Sequence, Value
    from ..features.features import _ArrayXD

    if isinstance(feature, Sequence):
        return is_numeric_feature(feature.feature)
    elif isinstance(feature, list):
        return is_numeric_feature(feature[0])
    elif isinstance(feature, _ArrayXD):
        return is_numeric_pa_type(feature().storage_dtype)
    elif isinstance(feature, Value):
        return is_numeric_pa_type(feature())
    elif isinstance(feature, ClassLabel):
        return True
    else:
        return False


def dataset_to_tf(
    dataset,
    cols_to_retain,
    collate_fn,
    collate_fn_args,
    columns_to_np_types,
    output_signature,
    shuffle,
    batch_size,
    drop_remainder,
):
    if config.TF_AVAILABLE:
        import tensorflow as tf
    else:
        raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")

    def np_get_batch(indices):
        # Optimization - if we're loading a sequential batch, do it with slicing instead of a list of indices
        if np.all(np.diff(indices) == 1):
            batch = dataset[indices[0] : indices[-1] + 1]
        else:
            batch = dataset[indices]

        if cols_to_retain is not None:
            batch = {
                key: value
                for key, value in batch.items()
                if key in cols_to_retain or key in ("label", "label_ids", "labels")
            }
        elif cols_to_retain is not None:
            batch = {key: value for key, value in batch.items() if key in cols_to_retain}

        actual_size = len(list(batch.values())[0])  # Get the length of one of the arrays, assume all same
        # Our collators expect a list of dicts, not a dict of lists/arrays, so we invert
        batch = [{key: value[i] for key, value in batch.items()} for i in range(actual_size)]
        batch = collate_fn(batch, **collate_fn_args)
        out_batch = []
        for col, cast_dtype in columns_to_np_types.items():
            # In case the collate_fn returns something strange
            array = np.array(batch[col])
            array = array.astype(cast_dtype)
            out_batch.append(array)
        return out_batch

    @tf.function(input_signature=[tf.TensorSpec(None, tf.int64)])
    def fetch_function(indices):
        output = tf.numpy_function(
            np_get_batch,
            inp=[indices],
            # This works because dictionaries always output in the same order
            Tout=[tf.dtypes.as_dtype(dtype) for dtype in columns_to_np_types.values()],
        )
        return {key: output[i] for i, key in enumerate(columns_to_np_types.keys())}

    tf_dataset = tf.data.Dataset.from_tensor_slices(np.arange(len(dataset), dtype=np.int64))

    if shuffle:
        tf_dataset = tf_dataset.shuffle(len(dataset))

    tf_dataset = tf_dataset.batch(batch_size, drop_remainder=drop_remainder).map(fetch_function)

    def ensure_shapes(input_dict):
        return {key: tf.ensure_shape(val, output_signature[key].shape) for key, val in input_dict.items()}

    return tf_dataset.map(ensure_shapes)


class NumpyMultiprocessingGenerator:
    def __init__(
        self,
        dataset,
        cols_to_retain,
        collate_fn,
        collate_fn_args,
        columns_to_np_types,
        shuffle,
        batch_size,
        drop_remainder,
        num_workers,
    ):
        self.dataset = dataset
        self.cols_to_retain = cols_to_retain
        self.collate_fn = collate_fn
        self.collate_fn_args = collate_fn_args
        self.columns_to_np_types = columns_to_np_types
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.drop_remainder = drop_remainder
        self.num_workers = num_workers

    def __iter__(self):
        # Make sure we only spawn workers if they have work to do
        num_workers = min(self.num_workers, ceil(len(self.dataset) / self.batch_size))
        # Do the shuffling in iter so that it's done at the start of each epoch
        per_worker_batches, final_batch, final_batch_worker = self.distribute_batches(
            self.dataset, self.batch_size, self.drop_remainder, num_workers, self.shuffle
        )
        ctx = get_context("spawn")
        worker_queues = [ctx.Queue(maxsize=5) for _ in range(num_workers)]
        workers = []
        base_args = [
            self.dataset,
            self.cols_to_retain,
            self.collate_fn,
            self.collate_fn_args,
            self.columns_to_np_types,
        ]

        for i in range(num_workers):
            worker_args = [*base_args, worker_queues[i], per_worker_batches[i]]
            if i == final_batch_worker:
                worker_args.append(final_batch)
            else:
                worker_args.append(None)
            worker_args = tuple(worker_args)
            worker = ctx.Process(target=self.worker_loop, args=worker_args, daemon=True)
            worker.start()
            workers.append(worker)
        while True:
            for i in range(num_workers):
                batch = worker_queues[i].get()
                if isinstance(batch, str) and batch == "DONE":
                    raise StopIteration
                yield batch

    def __call__(self):
        return self

    @staticmethod
    def worker_loop(
        dataset, cols_to_retain, collate_fn, collate_fn_args, columns_to_np_types, queue, indices, extra_batch
    ):
        if config.TF_AVAILABLE:
            import tensorflow as tf
        else:
            raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")  #

        def get_batch(indices):
            # Optimization - if we're loading a sequential batch, do it with slicing instead of a list of indices
            if np.all(np.diff(indices) == 1):
                batch = dataset[indices[0] : indices[-1] + 1]
            else:
                batch = dataset[indices]

            if cols_to_retain is not None:
                batch = {
                    key: value
                    for key, value in batch.items()
                    if key in cols_to_retain or key in ("label", "label_ids", "labels")
                }
            elif cols_to_retain is not None:
                batch = {key: value for key, value in batch.items() if key in cols_to_retain}

            actual_size = len(list(batch.values())[0])  # Get the length of one of the arrays, assume all same
            # Our collators expect a list of dicts, not a dict of lists/arrays, so we invert
            batch = [{key: value[i] for key, value in batch.items()} for i in range(actual_size)]
            batch = collate_fn(batch, **collate_fn_args)
            out_batch = dict()
            for col, cast_dtype in columns_to_np_types.items():
                # In case the collate_fn returns something strange
                array = np.array(batch[col])
                array = array.astype(cast_dtype)
                out_batch[col] = array
            return out_batch

        with tf.device("/cpu:0"):
            for batch in indices:
                queue.put(get_batch(batch))
            if extra_batch is not None:
                queue.put(get_batch(extra_batch))
        queue.put("DONE")

    @staticmethod
    def distribute_batches(dataset, batch_size, drop_remainder, num_workers, shuffle):
        indices = np.arange(len(dataset))
        if shuffle:
            np.random.shuffle(indices)
        # We distribute the batches so that reading from the workers in round-robin order yields the exact
        # order specified in indices. This is only important when shuffle is False, but we do it regardless.
        if drop_remainder or len(indices) % batch_size == 0:
            last_incomplete_batch = None
        else:
            last_incomplete_batch = [indices[len(indices) // batch_size * batch_size :]]
        indices = indices[: len(indices) // batch_size * batch_size]
        indices = indices.reshape(-1, batch_size)
        if len(indices) % num_workers != 0:
            final_batches = indices[-(len(indices) % num_workers) :]
        else:
            final_batches = []
        indices = indices.reshape(-1, num_workers, batch_size)
        per_worker_indices = np.split(indices, indices.shape[1], axis=1)
        per_worker_indices = [np.squeeze(worker_indices, 1) for worker_indices in per_worker_indices]
        # Distribute the final batches to the first workers
        for i in range(len(final_batches)):
            per_worker_indices[i] = np.concatenate([per_worker_indices[i], final_batches[i].reshape(1, -1)], axis=0)
        # Add the last incomplete batch to the next worker, which might be the first worker
        if last_incomplete_batch is not None:
            incomplete_batch_worker_idx = len(final_batches)
        else:
            incomplete_batch_worker_idx = None
        return per_worker_indices, last_incomplete_batch, incomplete_batch_worker_idx


def multiprocess_dataset_to_tf(
    dataset,
    cols_to_retain,
    collate_fn,
    collate_fn_args,
    columns_to_np_types,
    output_signature,
    shuffle,
    batch_size,
    drop_remainder,
    num_workers,
):
    if config.TF_AVAILABLE:
        import tensorflow as tf
    else:
        raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")

    data_generator = NumpyMultiprocessingGenerator(
        dataset,
        cols_to_retain,
        collate_fn,
        collate_fn_args,
        columns_to_np_types,
        shuffle,
        batch_size,
        drop_remainder,
        num_workers,
    )

    return tf.data.Dataset.from_generator(data_generator, output_signature=output_signature)
