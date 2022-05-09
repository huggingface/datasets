# coding=utf-8
# Copyright 2022 the HuggingFace Datasets Authors.
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

import os

import datasets
from datasets.tasks import ImageClassification

from .classes import IMAGENET2012_CLASSES


_CITATION = """\
@article{imagenet15russakovsky,
    Author = {Olga Russakovsky and Jia Deng and Hao Su and Jonathan Krause and Sanjeev Satheesh and Sean Ma and Zhiheng Huang and Andrej Karpathy and Aditya Khosla and Michael Bernstein and Alexander C. Berg and Li Fei-Fei},
    Title = { {ImageNet Large Scale Visual Recognition Challenge} },
    Year = {2015},
    journal   = {International Journal of Computer Vision (IJCV)},
    doi = {10.1007/s11263-015-0816-y},
    volume={115},
    number={3},
    pages={211-252}
}
"""

_HOMEPAGE = "https://image-net.org/index.php"

_DESCRIPTION = """\
ILSVRC 2012, commonly known as 'ImageNet' is an image dataset organized according to the WordNet hierarchy. Each meaningful concept in WordNet, possibly described by multiple words or word phrases, is called a "synonym set" or "synset". There are more than 100,000 synsets in WordNet, majority of them are nouns (80,000+). ImageNet aims to provide on average 1000 images to illustrate each synset. Images of each concept are quality-controlled and human-annotated. In its completion, ImageNet hopes to offer tens of millions of cleanly sorted images for most of the concepts in the WordNet hierarchy. ImageNet 2012 is the most commonly used subset of ImageNet. This dataset spans 1000 object classes and contains 1,281,167 training images, 50,000 validation images and 100,000 test images
"""

_DATA_URL = (
    "https://huggingface.co/datasets/imagenet-1k/resolve/main/data/imagenet_object_localization_patched2019.tar.gz"
)
_IN1K_VAL_PREP_SCRIPT = "https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh"


class Imagenet1k(datasets.GeneratorBasedBuilder):
    IMAGE_EXTENSION = ".jpeg"

    VERSION = datasets.Version("1.0.0")

    DEFAULT_WRITER_BATCH_SIZE = 1000

    def _info(self):
        assert len(IMAGENET2012_CLASSES) == 1000
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(names=list(IMAGENET2012_CLASSES.values())),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _prep_val(self, val_prep_script):
        with open(val_prep_script, "r", encoding="utf-8") as f:
            commands = f.readlines()

        val_fixes = {}
        for command in commands:
            command = command.strip()
            if "mv" in command:
                splits = command.split(" ")
                image_file = splits[1]
                folder = splits[2]
                # image_file[:-5] to remove the .JPEG extension
                # folder[:-1] to remove the trailing slash
                val_fixes[image_file[:-5]] = folder[:-1]
        return val_fixes

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        archive = dl_manager.download(_DATA_URL)
        val_prep_script = dl_manager.download(_IN1K_VAL_PREP_SCRIPT)

        val_fixes = self._prep_val(val_prep_script)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dl_manager.iter_archive(archive), "fixes": None, "split": "train"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "files": dl_manager.iter_archive(archive),
                    "fixes": val_fixes,
                    "split": "val",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"files": dl_manager.iter_archive(archive), "fixes": None, "split": "test"},
            ),
        ]

    def _generate_examples(self, files, fixes, split):
        """Yields examples."""
        idx = 0
        for path, file in files:
            if split in path:
                file_root, file_ext = os.path.splitext(path)
                if file_ext.lower() == self.IMAGE_EXTENSION:
                    output = {"image": {"path": path, "bytes": file.read()}}

                    if split == "train":
                        label = os.path.basename(os.path.dirname(file_root))
                        output["label"] = IMAGENET2012_CLASSES[label]
                    elif split == "val":
                        label = fixes.get(os.path.basename(file_root))
                        output["label"] = label if label is not None else os.path.basename(os.path.dirname(file_root))
                        output["label"] = IMAGENET2012_CLASSES[label]
                    else:  # test
                        output["label"] = -1

                    yield idx, output
                    idx += 1
