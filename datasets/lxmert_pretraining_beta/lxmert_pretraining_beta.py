# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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

from __future__ import absolute_import, division, print_function

import nlp


_DESCRIPTION = """\
LXMERT multimodal pretraining dataset beta
"""

_CITATION = """\
@inproceedings{tan2019lxmert,
  title={LXMERT: Learning Cross-Modality Encoder Representations from Transformers},
  author={Tan, Hao and Bansal, Mohit},
  booktitle={Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing},
  year={2019}
}
"""

_URL = "https://arxiv.org/abs/1908.07490"

_ARROW_URL_PATH_TRAIN = None
_ARROW_URL_PATH_VAL = None

_LXMERT_FEATURES = nlp.Features(
    {
        "image": nlp.features.Array2D(dtype="float32"),
        "img_id": nlp.Value("string"),
        "boxes": nlp.features.Array2D(dtype="int32"),
        "img_h": nlp.Value("int32"),
        "img_w": nlp.Value("int32"),
        "labels": nlp.features.Array2D(dtype="string"),
        "labels_confidence": nlp.features.Array2D(dtype="float32"),
        "num_boxes": nlp.Value("int32"),
        "attrs_id": nlp.features.Sequence(nlp.ClassLabel(num_classes=400)),
        "objs_id": nlp.features.Sequence(nlp.ClassLabel(num_classes=1600)),
        "attrs_confidence": nlp.features.Sequence(nlp.Value("float32")),
        "objs_confidence": nlp.features.Sequence(nlp.Value("float32")),
        "captions": nlp.features.Sequence(nlp.Value("string")),
        "questions": nlp.features.Sequence(nlp.Value("string")),
    }
)

_SUPERVISED_KEYS = tuple(_LXMERT_FEATURES.keys())


class LxmertPretrainingBeta(nlp.GeneratorBasedBuilder):
    """CNN/DailyMail non-anonymized summarization dataset."""

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=_LXMERT_FEATURES,
            homepage=_URL,
            citation=_CITATION,
            supervised_keys=_SUPERVISED_KEYS,
        )

    def _split_generators(self, dl_manager):

        arrow_train = dl_manager.download_and_extract(_ARROW_URL_PATH_TRAIN)
        arrow_val = dl_manager.download_and_extract(_ARROW_URL_PATH_VAL)

        return [
            nlp.SplitGenerator(name=nlp.Split.TRAIN, gen_kwargs={"filepath": arrow_train}),
            nlp.SplitGenerator(name=nlp.Split.VAL, gen_kwargs={"filepath": arrow_val}),
            # nlp.SplitGenerator(, gen_kwargs={"files" _subset_file()"),
        ]

    def _generate_examples(self, filepath):
        dataset = nlp.Dataset.from_file(filepath)
        for i in range(dataset.num_rows):
            yield {key: dataset[key] for key in _SUPERVISED_KEYS}
