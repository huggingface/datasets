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

import numpy as np
import pyarrow as pa
from multiprocess import get_context
from multiprocess.shared_memory import SharedMemory
from functools import partial

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


def np_get_batch(indices, dataset, cols_to_retain, collate_fn, collate_fn_args, columns_to_np_types):
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

    getter_fn = partial(
        np_get_batch,
        dataset=dataset,
        cols_to_retain=cols_to_retain,
        collate_fn=collate_fn,
        collate_fn_args=collate_fn_args,
        columns_to_np_types=columns_to_np_types
    )

    @tf.function(input_signature=[tf.TensorSpec(None, tf.int64)])
    def fetch_function(indices):
        output = tf.numpy_function(
            getter_fn,
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
        output_signature,
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
        self.output_signature = output_signature
        self.shuffle = shuffle
        self.batch_size = batch_size
        self.drop_remainder = drop_remainder
        self.num_workers = num_workers
        self.columns_to_ranks = {col: int(spec.shape.rank) for col, spec in output_signature.items()}

    def __iter__(self):
        # Make sure we only spawn workers if they have work to do
        num_workers = min(self.num_workers, int(ceil(len(self.dataset) / self.batch_size)))
        # Do the shuffling in iter so that it's done at the start of each epoch
        per_worker_batches, final_batch, final_batch_worker = self.distribute_batches(
            self.dataset, self.batch_size, self.drop_remainder, num_workers, self.shuffle
        )
        ctx = get_context("spawn")
        names = []
        shape_shms = []
        shape_arrays = []
        workers = []
        array_ready_events = [ctx.Event() for _ in range(num_workers)]
        array_loaded_events = [ctx.Event() for _ in range(num_workers)]

        base_args = {
            "dataset": self.dataset,
            "cols_to_retain": self.cols_to_retain,
            "collate_fn": self.collate_fn,
            "collate_fn_args": self.collate_fn_args,
            "columns_to_np_types": self.columns_to_np_types,
            "columns_to_ranks": self.columns_to_ranks,
        }
        for i in range(num_workers):
            worker_name = f"datasets_tf_worker_{i}"
            names.append(worker_name)

            worker_shape_shms = {
                col: SharedMemory(name=f"{worker_name}_{col}_shape", create=True, size=rank * 8)
                for col, rank in self.columns_to_ranks.items()
            }
            worker_shape_arrays = {
                col: np.ndarray(shape=(shape_shm.size // 8,), dtype=np.int64, buffer=shape_shm.buf)
                for col, shape_shm in worker_shape_shms.items()
            }
            shape_shms.append(worker_shape_shms)
            shape_arrays.append(worker_shape_arrays)

            worker_indices = per_worker_batches[i]
            if i == final_batch_worker and final_batch is not None:
                final_batch_arg = final_batch
            else:
                final_batch_arg = None
            worker_kwargs = {
                "worker_name": worker_name,
                "indices": worker_indices,
                "extra_batch": final_batch_arg,
                "array_ready_event": array_ready_events[i],
                "array_loaded_event": array_loaded_events[i],
                **base_args,
            }
            worker = ctx.Process(target=self.worker_loop, kwargs=worker_kwargs, daemon=True)
            worker.start()
            workers.append(worker)

        end_signal_received = False
        while not end_signal_received:
            for i in range(num_workers):
                array_ready_events[i].wait()
                array_ready_events[i].clear()
                array_shapes = shape_arrays[i]
                array_sizes = {
                    col: np.prod(shape) * np.dtype(self.columns_to_np_types[col]).itemsize
                    for col, shape in array_shapes.items()
                }
                if any(size < 0 for size in array_sizes.values()):
                    # Child processes send negative array shapes to indicate
                    # that no more data is going to be sent
                    end_signal_received = True
                    break
                array_shms = {
                    col: SharedMemory(name=f"{names[i]}_{col}", create=False, size=size)
                    for col, size in array_sizes.items()
                }
                arrays = {
                    col: np.copy(
                        np.ndarray(shape=array_shapes[col], dtype=self.columns_to_np_types[col], buffer=shm.buf)
                    )
                    for col, shm in array_shms.items()
                }
                yield arrays
                for shm in array_shms.values():
                    shm.close()
                array_loaded_events[i].set()
        # Now we just do some cleanup
        for worker, shape_shms in zip(workers, shape_shms):
            worker.join()
            for shm in shape_shms.values():
                shm.unlink()

    def __call__(self):
        return self

    @staticmethod
    def worker_loop(
        dataset,
        cols_to_retain,
        collate_fn,
        collate_fn_args,
        columns_to_np_types,
        columns_to_ranks,
        indices,
        extra_batch,
        worker_name,
        array_ready_event,
        array_loaded_event,
    ):
        if config.TF_AVAILABLE:
            import tensorflow as tf
        else:
            raise ImportError("Called a Tensorflow-specific function but Tensorflow is not installed.")

        tf.config.set_visible_devices([], "GPU")  # Make sure workers don't try to allocate GPU memory

        shape_shms = {
            col: SharedMemory(name=f"{worker_name}_{col}_shape", create=False, size=rank * 8)
            for col, rank in columns_to_ranks.items()
        }
        shape_arrays = {
            col: np.ndarray(shape=(shape_shm.size // 8,), dtype=np.int64, buffer=shape_shm.buf)
            for col, shape_shm in shape_shms.items()
        }

        def send_batch_to_parent(indices):
            batch = np_get_batch(indices=indices,
                                 dataset=dataset,
                                 cols_to_retain=cols_to_retain,
                                 collate_fn=collate_fn,
                                 collate_fn_args=collate_fn_args,
                                 columns_to_np_types=columns_to_np_types)

            # Now begins the fun part where we start shovelling shared memory at the parent process
            out_shms = dict()
            out_arrays = dict()
            for col, cast_dtype in columns_to_np_types.items():
                # Everything has to be np.array for this to work, even if the collate_fn is giving us tf.Tensor
                array = np.array(batch[col]).astype(cast_dtype)
                shape_arrays[col][:] = array.shape
                out_shms[col] = SharedMemory(name=f"{worker_name}_{col}", create=True, size=array.nbytes)
                out_arrays[col] = np.ndarray(shape=array.shape, dtype=cast_dtype, buffer=out_shms[col].buf)
                out_arrays[col][:] = array

            array_ready_event.set()
            array_loaded_event.wait()
            array_loaded_event.clear()
            for shm in out_shms.values():
                shm.close()
                shm.unlink()

        for batch in indices:
            send_batch_to_parent(batch)
        if extra_batch is not None:
            send_batch_to_parent(extra_batch)
        # Now we send a batsignal to the parent process that we're done
        for col, array in shape_arrays.items():
            array[:] = -1
        array_ready_event.set()
        # Don't unlink them because the parent still needs to read them
        for shm in shape_shms.values():
            shm.close()

    @staticmethod
    def distribute_batches(dataset, batch_size, drop_remainder, num_workers, shuffle):
        indices = np.arange(len(dataset))
        if shuffle:
            np.random.shuffle(indices)
        num_samples = len(indices)
        # We distribute the batches so that reading from the workers in round-robin order yields the exact
        # order specified in indices. This is only important when shuffle is False, but we do it regardless.
        if drop_remainder or num_samples % batch_size == 0:
            last_incomplete_batch = None
        else:
            last_incomplete_batch = [indices[num_samples // batch_size * batch_size :]]
        if num_samples % batch_size != 0:
            indices = indices[: -(num_samples % batch_size)]
        indices = indices.reshape(-1, batch_size)
        if num_samples % num_workers != 0:
            final_batches = indices[-(num_samples % num_workers) :]
            indices = indices[: -(num_samples % num_workers)]
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
        dataset=dataset,
        cols_to_retain=cols_to_retain,
        collate_fn=collate_fn,
        collate_fn_args=collate_fn_args,
        columns_to_np_types=columns_to_np_types,
        output_signature=output_signature,
        shuffle=shuffle,
        batch_size=batch_size,
        drop_remainder=drop_remainder,
        num_workers=num_workers,
    )

    tf_dataset = tf.data.Dataset.from_generator(data_generator, output_signature=output_signature)
    if drop_remainder:
        dataset_length = int(len(dataset) // batch_size)
    else:
        dataset_length = int(ceil(len(dataset) / batch_size))
    return tf_dataset.apply(tf.data.experimental.assert_cardinality(dataset_length))
