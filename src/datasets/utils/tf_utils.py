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
