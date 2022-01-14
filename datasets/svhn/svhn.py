# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Street View House Numbers (SVHN) dataset."""

import io
import os

import h5py
import numpy as np
import scipy.io as sio

import datasets
from datasets.tasks import ImageClassification


logger = datasets.logging.get_logger(__name__)


_CITATION = """\
@article{netzer2011reading,
  title={Reading digits in natural images with unsupervised feature learning},
  author={Netzer, Yuval and Wang, Tao and Coates, Adam and Bissacco, Alessandro and Wu, Bo and Ng, Andrew Y},
  year={2011}
}
"""

_DESCRIPTION = """\
SVHN is a real-world image dataset for developing machine learning and object recognition algorithms with minimal requirement on data preprocessing and formatting.
It can be seen as similar in flavor to MNIST (e.g., the images are of small cropped digits), but incorporates an order of magnitude more labeled data (over 600,000 digit images)
and comes from a significantly harder, unsolved, real world problem (recognizing digits and numbers in natural scene images). SVHN is obtained from house numbers in Google Street View images.
"""

_HOMEPAGE = "http://ufldl.stanford.edu/housenumbers/"

_LICENSE = "Custom (non-commercial)"

_URLs = {
    "full_numbers": [
        "http://ufldl.stanford.edu/housenumbers/train.tar.gz",
        "http://ufldl.stanford.edu/housenumbers/test.tar.gz",
        "http://ufldl.stanford.edu/housenumbers/extra.tar.gz",
    ],
    "cropped_digits": [
        "http://ufldl.stanford.edu/housenumbers/train_32x32.mat",
        "http://ufldl.stanford.edu/housenumbers/test_32x32.mat",
        "http://ufldl.stanford.edu/housenumbers/extra_32x32.mat",
    ],
}

_DIGIT_LABELS = [str(num) for num in range(10)]


class SVHN(datasets.GeneratorBasedBuilder):
    """Street View House Numbers (SVHN) dataset."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="full_numbers",
            version=VERSION,
            description="Contains the original, variable-resolution, color house-number images with character level bounding boxes.",
        ),
        datasets.BuilderConfig(
            name="cropped_digits",
            version=VERSION,
            description="Character level ground truth in an MNIST-like format. All digits have been resized to a fixed resolution of 32-by-32 pixels. The original character bounding boxes are extended in the appropriate dimension to become square windows, so that resizing them to 32-by-32 pixels does not introduce aspect ratio distortions. Nevertheless this preprocessing introduces some distracting digits to the sides of the digit of interest.",
        ),
    ]

    def _info(self):
        if self.config.name == "full_numbers":
            features = datasets.Features(
                {
                    "image": datasets.Image(),
                    "digits": datasets.Sequence(
                        {
                            "bbox": datasets.Sequence(datasets.Value("int32"), length=4),
                            "label": datasets.ClassLabel(num_classes=10),
                        }
                    ),
                }
            )
        else:
            features = datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(num_classes=10),
                }
            )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")]
            if self.config.name == "cropped_digits"
            else None,
        )

    def _split_generators(self, dl_manager):
        if self.config.name == "full_numbers":
            train_archive, test_archive, extra_archive = dl_manager.download(_URLs[self.config.name])
            for path, f in dl_manager.iter_archive(train_archive):
                if path.endswith("digitStruct.mat"):
                    train_annot_data = f.read()
                    break
            for path, f in dl_manager.iter_archive(test_archive):
                if path.endswith("digitStruct.mat"):
                    test_annot_data = f.read()
                    break
            for path, f in dl_manager.iter_archive(extra_archive):
                if path.endswith("digitStruct.mat"):
                    extra_annot_data = f.read()
                    break
            train_archive = dl_manager.iter_archive(train_archive)
            test_archive = dl_manager.iter_archive(test_archive)
            extra_archive = dl_manager.iter_archive(extra_archive)
            train_filepath, test_filepath, extra_filepath = None, None, None
        else:
            train_annot_data, test_annot_data, extra_annot_data = None, None, None
            train_archive, test_archive, extra_archive = None, None, None
            train_filepath, test_filepath, extra_filepath = dl_manager.download(_URLs[self.config.name])
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "annot_data": train_annot_data,
                    "files": train_archive,
                    "filepath": train_filepath,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "annot_data": test_annot_data,
                    "files": test_archive,
                    "filepath": test_filepath,
                },
            ),
            datasets.SplitGenerator(
                name="extra",
                gen_kwargs={
                    "annot_data": extra_annot_data,
                    "files": extra_archive,
                    "filepath": extra_filepath,
                },
            ),
        ]

    def _generate_examples(self, annot_data, files, filepath):
        if self.config.name == "full_numbers":

            def _get_digits(bboxes, h5_file):
                def key_to_values(key, bbox):
                    if bbox[key].shape[0] == 1:
                        return [int(bbox[key][0][0])]
                    else:
                        return [int(h5_file[bbox[key][i][0]][()].item()) for i in range(bbox[key].shape[0])]

                bbox = h5_file[bboxes[0]]
                assert bbox.keys() == {"height", "left", "top", "width", "label"}
                bbox_columns = [key_to_values(key, bbox) for key in ["left", "top", "width", "height", "label"]]
                return [
                    {"bbox": [left, top, width, height], "label": label % 10}
                    for left, top, width, height, label in zip(*bbox_columns)
                ]

            with h5py.File(io.BytesIO(annot_data), "r") as h5_file:
                for path, f in files:
                    root, ext = os.path.splitext(path)
                    if ext != ".png":
                        continue
                    img_idx = int(os.path.basename(root)) - 1
                    yield img_idx, {
                        "image": {"path": path, "bytes": f.read()},
                        "digits": _get_digits(h5_file["digitStruct/bbox"][img_idx], h5_file),
                    }
        else:
            data = sio.loadmat(filepath)
            for i, (image_array, label) in enumerate(zip(np.rollaxis(data["X"], -1), data["y"])):
                yield i, {
                    "image": image_array,
                    "label": label.item() % 10,
                }
