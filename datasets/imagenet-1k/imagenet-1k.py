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
import shutil

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

_IN1K_NUM_CLASSES = 1000
_IN1K_VAL_PREP_SCRIPT = "https://raw.githubusercontent.com/soumith/imagenetloader.torch/master/valprep.sh"
_DEFAULT_CONFIG_NAME = "default"


class Imagenet1kConfig(datasets.BuilderConfig):
    def __init__(
        self,
        name=_DEFAULT_CONFIG_NAME,
        val_prep_script=_IN1K_VAL_PREP_SCRIPT,
        num_classes=_IN1K_NUM_CLASSES,
        **kwargs,
    ):
        """Config for ImageNet dataset.

        Args:
            name (string, optional): keyword to identify the config. Defaults to _DEFAULT_CONFIG_NAME.
            val_prep_script (string, optional): URL or path to script used to prep val set. Defaults to _IN1K_VAL_PREP_SCRIPT.
            synset_mapping (string, optional): URL or path to synset mapping. Defaults to _IN1K_SYNSET_MAPPING.
        """
        kwargs.pop("version", None)
        super(Imagenet1kConfig, self).__init__(version=datasets.Version("1.0.0"), name=name, **kwargs)
        self.val_prep_script = val_prep_script
        self.num_classes = num_classes


class Imagenet1k(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIG_CLASS = Imagenet1kConfig

    BUILDER_CONFIGS = [
        Imagenet1kConfig(
            name="default",
            val_prep_script=_IN1K_VAL_PREP_SCRIPT,
            num_classes=_IN1K_NUM_CLASSES,
        ),
    ]

    IMAGE_EXTENSION = ".jpeg"

    @property
    def manual_download_instructions(self):
        return (
            "To use ImageNet2012 you have to download it manually. Please download it from ("
            "https://www.kaggle.com/competitions/imagenet-object-localization-challenge/"
            "data?select=imagenet_object_localization_patched2019.tar.gz). You will "
            "need to login and download the `imagenet_object_localization_patched2019.tar.gz file. "
            "This file is about 155GB in size."
            "Don't extract the file and point the `datasets` library to the tar file by running "
            "`datasets.load_dataset('imagenet2012', "
            "data_dir='path/to/folder/imagenet_object_localization_patched2019.tar.gz')`"
        )

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "image": datasets.Image(),
                    "label": datasets.ClassLabel(
                        num_classes=self.config.num_classes, names=list(IMAGENET2012_CLASSES.values())
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
            task_templates=[ImageClassification(image_column="image", label_column="label")],
        )

    def _prep_validation(self, data_dir, val_prep_script):
        with open(val_prep_script, "r", encoding="utf-8") as f:
            commands = f.readlines()

        for command in commands:
            command = command.strip()
            if "mkdir" in command:
                folder = command.split(" ")[-1]
                folder = os.path.join(data_dir, "val", folder)
                os.makedirs(folder, exist_ok=True)
            # mkdir will definitely happen before move in continuous incremental loop.
            elif "mv" in command:
                splits = command.split(" ")
                image_file = splits[1]
                folder = splits[2]
                dst_path = os.path.join(data_dir, "val", folder)
                if os.path.exists(os.path.join(dst_path, image_file)):
                    continue
                src_path = os.path.join(data_dir, "val", image_file)
                if not os.path.exists(src_path):
                    continue
                shutil.move(src_path, dst_path)

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        data_dir = os.path.abspath(os.path.expanduser(dl_manager.extract(dl_manager.manual_dir)))

        if not os.path.exists(data_dir):
            raise FileNotFoundError(
                f"{data_dir} does not exist. Make sure you insert a manual dir via "
                "`datasets.load_dataset('imagenet2012', data_dir=...)` that points to the "
                "tar file downloaded for ImageNet 2012. Manual download instructions: "
                f"{self.manual_download_instructions}"
            )
        val_prep_script = dl_manager.download(self.config.val_prep_script)
        images_path = os.path.join(data_dir, "ILSVRC", "Data", "CLS-LOC")

        self._prep_validation(images_path, val_prep_script)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "train"))},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "val"))},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"files": dl_manager.iter_files(os.path.join(images_path, "test")), "no_labels": True},
            ),
        ]

    def _generate_examples(self, files, no_labels=False):
        """Yields examples."""
        idx = 0
        for file in files:
            _, file_ext = os.path.splitext(file)
            if file_ext.lower() == self.IMAGE_EXTENSION:
                output = {"image": file}

                if not no_labels:
                    label = os.path.basename(os.path.dirname(file))
                    output["label"] = IMAGENET2012_CLASSES[label]
                else:
                    output["label"] = -1

                yield idx, output
                idx += 1
