import os

import numpy as np
import tensorflow as tf


# Importing a user's collator can initialize TensorFlow before the worker target runs.
IMPORT_TIME_TENSOR = tf.constant(1, dtype=tf.int64)
GPUS_HIDDEN_AT_IMPORT = os.environ.get("CUDA_VISIBLE_DEVICES") == "" and not tf.config.get_visible_devices("GPU")


def collate_with_initialized_tensorflow(examples):
    return {
        "x": tf.convert_to_tensor([example["x"] for example in examples], dtype=tf.int64) * IMPORT_TIME_TENSOR,
        "gpus_hidden_at_import": np.full(len(examples), GPUS_HIDDEN_AT_IMPORT),
    }
