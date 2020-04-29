# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
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

# Lint as: python3
"""Wrapper around FeatureDict to allow better control over decoding.
"""

from .feature import FeatureConnector


class TopLevelFeature(FeatureConnector):
    """Top-level `FeatureConnector` to manage decoding.

    Note that `FeatureConnector` which are declared as `TopLevelFeature` can be
    nested. However, only the top-level feature can be decoded.

    `TopLevelFeature` allows better control over the decoding, and
    eventually better support for augmentations.
    """

    def __init__(self, *args, **kwargs):
        """Constructor."""
        self.__is_top_level = False
        super(TopLevelFeature, self).__init__(*args, **kwargs)

    # # AutoGraph doesn't support mangled names (__is_top_level), so we explicitly
    # # disable it in methods that use them, to avoid the warning.
    # # TODO(mdan): Remove decorator once AutoGraph supports mangled names.
    # @tf.autograph.experimental.do_not_convert()
    def _set_top_level(self):
        """Indicates that the feature is top level.

        Internal function called by `DatasetInfo`.
        """
        self.__is_top_level = True

    # # AutoGraph doesn't support mangled names (__is_top_level), so we explicitly
    # # disable it in methods that use them, to avoid the warning.
    # # TODO(mdan): Remove decorator once AutoGraph supports mangled names.
    # @tf.autograph.experimental.do_not_convert()
    def decode_example(self, serialized_example, decoders=None):
        # pylint: disable=line-too-long
        """Decode the serialize examples.

        Args:
            serialized_example: Nested `dict` of `tf.Tensor`
            decoders: Nested dict of `Decoder` objects which allow to customize the
                decoding. The structure should match the feature structure, but only
                customized feature keys need to be present. See
                [the guide](https://github.com/tensorflow/datasets/tree/master/docs/decode.md)
                for more info.

        Returns:
            example: Nested `dict` containing the decoded nested examples.
        """
        # pylint: enable=line-too-long
        if not self.__is_top_level:
            raise AssertionError(
                "Feature {} can only be decoded when defined as top-level "
                "feature, through info.features.decode_example()".format(type(self).__name__)
            )

        # Step 1: Flatten the nested dict => []
        flat_example = self._flatten(serialized_example)
        flat_features = self._flatten(self)
        flat_serialized_info = self._flatten(self.get_type())
        flat_decoders = self._flatten(decoders)

        # Step 2: Apply the decoding
        flatten_decoded = []
        for (feature, example, serialized_info, decoder,) in zip(
            flat_features, flat_example, flat_serialized_info, flat_decoders
        ):
            flatten_decoded.append(
                _decode_feature(feature=feature, example=example, serialized_info=serialized_info, decoder=decoder,)
            )

        # Step 3: Restore nesting [] => {}
        nested_decoded = self._nest(flatten_decoded)
        return nested_decoded


def _decode_feature(feature, example, serialized_info, decoder):
    """Decode a single feature."""
    # Eventually overwrite the default decoding
    if decoder is not None:
        decoder.setup(feature=feature)
    else:
        decoder = feature

    sequence_rank = _get_sequence_rank(serialized_info)
    if sequence_rank == 0:
        return decoder.decode_example(example)
    elif sequence_rank == 1:
        # Return a batch of examples from a sequence
        return decoder.decode_batch_example(example)
    elif sequence_rank > 1:
        # Use ragged tensor if the sequance rank is greater than one
        return decoder.decode_ragged_example(example)


def _get_sequence_rank(serialized_info):
    """Return the number of sequence dimensions of the feature."""
    if isinstance(serialized_info, dict):
        all_sequence_rank = [s.sequence_rank for s in serialized_info.values()]
    else:
        all_sequence_rank = [serialized_info.sequence_rank]

    sequence_ranks = set(all_sequence_rank)
    if len(sequence_ranks) != 1:
        raise NotImplementedError(
            "Decoding do not support mixing sequence and context features within a "
            "single FeatureConnector. Received inputs of different sequence_rank: "
            "{}".format(sequence_ranks)
        )
    return next(iter(sequence_ranks))
