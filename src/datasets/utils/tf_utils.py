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

from .. import config


if config.TF_AVAILABLE:
    import tensorflow as tf

    def minimal_tf_collate_fn(features):
        first = features[0]
        batch = {}
        for k, v in first.items():
            if isinstance(v, np.ndarray):
                batch[k] = np.stack([f[k] for f in features])
            elif isinstance(v, tf.Tensor):
                batch[k] = np.stack([f[k].numpy() for f in features])
            else:
                batch[k] = np.array([f[k] for f in features])
        return batch

else:
    minimal_tf_collate_fn = None
