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
import os
import datasets

# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{vivos:2016,
Address = {Ho Chi Minh, Vietnam}
title = {VIVOS: 15 hours of recording speech prepared for Vietnamese Automatic Speech Recognition},
author={Prof. Vu Hai Quan},
year={2016}
}
"""

_DESCRIPTION = """\
VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for VietnameseAutomatic Speech Recognition task.
The corpus was prepared by AILAB, a computer science lab of VNUHCM - University of Science, with Prof. Vu Hai Quan is the head of.
We publish this corpus in hope to attract more scientists to solve Vietnamese speech recognition problems. The corpus should only be used for academic purposes.
"""

_HOMEPAGE = "https://ailab.hcmus.edu.vn/vivos"

_LICENSE = "cc-by-sa-4.0"

_DATA_URL = "https://ailab.hcmus.edu.vn/assets/vivos.tar.gz"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class VivosDataset(datasets.GeneratorBasedBuilder):
    """VIVOS is a free Vietnamese speech corpus consisting of 15 hours of recording speech prepared for Vietnamese Automatic Speech Recognition task."""

    VERSION = datasets.Version("1.1.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    # BUILDER_CONFIG_CLASS = MyBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')

    def _info(self):
        # TODO: This method specifies the datasets.DatasetInfo object which contains informations and typings for the dataset
        features = datasets.Features(
            {
                "sentence": datasets.Value("string"),
                "path": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        dl_path = dl_manager.download_and_extract(_DATA_URL.format(self.config.name))
        data_dir = os.path.join(dl_path, 'vivos')
        train_dir = os.path.join(data_dir, 'train')
        test_dir = os.path.join(data_dir, 'test')
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(train_dir, "prompts.txt"),
                    "path_to_clips": os.path.join(train_dir, "waves")
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(test_dir, "prompts.txt"),
                    "path_to_clips": os.path.join(test_dir, "waves")
                },
            )
        ]

    def _generate_examples(
        self, filepath, path_to_clips  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """ Yields examples as (key, example) tuples. """
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()
            for id_, row in enumerate(lines):
                data = row.strip().split(" ", 1)
                yield id_, {
                    "path": os.path.join(path_to_clips, data[0] + ".wav"),
                    "sentence": data[1],
                }