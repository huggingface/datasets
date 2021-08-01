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
"""TODO: Add a description here."""


import csv
import glob
import json
import os

import datasets

import numpy as np

# TODO: Add BibTeX citation
# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{huggingface:dataset,
title = {A great new dataset},
author={huggingface, Inc.
},
year={2020}
}
"""

# TODO: Add description of the dataset here
# You can copy an official description
_DESCRIPTION = """\
This new dataset is designed to solve this great NLP task and is crafted with a lot of care.
"""

# TODO: Add a link to an official homepage for the dataset here
_HOMEPAGE = "http://interactionmining.org/rico"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace dataset library don't host the datasets but only point to the original files
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_DATA_URLs = {
    "screenshots_hierarchies": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/unique_uis.tar.gz",
    "ui_metadata": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/ui_details.csv",
    "layout_vectors": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/ui_layout_vectors.zip",
    "traces": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/traces.tar.gz",
    "animations": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/animations.tar.gz",
    "playstore_metadata": "https://storage.googleapis.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/app_details.csv",
    "screenshots_semantic_hierarchies": "https://storage.cloud.google.com/crowdstf-rico-uiuc-4540/rico_dataset_v0.1/semantic_annotations.zip",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class RicoDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

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
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="screenshots_hierarchies",
            version=VERSION,
            description="Contains 66k+ unique UI screens. For each UI, we present a screenshot (PNG file) and a detailed view hierarchy (JSON object).",
        ),
        datasets.BuilderConfig(name="ui_metadata", version=VERSION, description=""),
        datasets.BuilderConfig(name="layout_vectors", version=VERSION, description=""),
        datasets.BuilderConfig(name="traces", version=VERSION, description=""),
        datasets.BuilderConfig(name="animations", version=VERSION, description=""),
        datasets.BuilderConfig(
            name="playstore_metadata", version=VERSION, description=""
        ),
        datasets.BuilderConfig(
            name="screenshots_semantic_hierarchies", version=VERSION, description=""
        ),
    ]

    DEFAULT_CONFIG_NAME = "screenshots_hierarchies"

    def _info(self):
        if self.config.name == "screenshots_hierarchies":
            features = datasets.Features(
                {
                    "screenshot_path": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "hierarchy": datasets.Value("string"),
                }
            )
        elif self.config.name == "ui_metadata":
            features = datasets.Features(
                {
                    "UI Number": datasets.Value("int32"),
                    "App Package Name": datasets.Value("string"),
                    "Interaction Trace Number": datasets.Value("int32"),
                    "UI Number in Trace": datasets.Value("int32"),
                }
            )
        elif self.config.name == "layout_vectors":
            features = datasets.Features(
                {
                    "ui_name": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "ui_vector": datasets.Sequence(datasets.Value("float32")),
                }
            )
        elif self.config.name == "traces":
            features = datasets.Features(
                {
                    "screenshot_path": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "hierarchy": datasets.Value("string"),
                }
            )
        elif self.config.name == "animations":
            features = datasets.Features(
                {
                    "screenshot_path": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "hierarchy": datasets.Value("string"),
                }
            )
        elif self.config.name == "playstore_metadata":
            features = datasets.Features(
                {
                    "screenshot_path": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "hierarchy": datasets.Value("string"),
                }
            )
        elif self.config.name == "screenshots_semantic_hierarchies":
            features = datasets.Features(
                {
                    "screenshot_path": datasets.Value("string"),
                    # This is a JSON obj, but will be coded as a string
                    "hierarchy": datasets.Value("string"),
                }
            )

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            supervised_keys=None,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLs
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        my_urls = _DATA_URLs[self.config.name]
        if self.config.name == "screenshots_hierarchies":
            data_dir = dl_manager.download_and_extract(my_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "combined"),
                        "split": "train",
                    },
                )
            ]
        elif self.config.name == "ui_metadata":
            data_dir = dl_manager.download(my_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": data_dir,
                        "split": "train",
                    },
                )
            ]
        elif self.config.name == "layout_vectors":
            data_dir = dl_manager.download_and_extract(my_urls)
            return [
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, "ui_layout_vectors"),
                        "split": "train",
                    },
                )
            ]
        elif self.config.name == "traces":
            return []
        elif self.config.name == "animations":
            return []
        elif self.config.name == "playstore_metadata":
            return []
        elif self.config.name == "screenshots_semantic_hierarchies":
            return []

    def _generate_examples(
        self,
        filepath,
        split,  # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    ):
        """Yields examples as (key, example) tuples."""
        # This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is here for legacy reason (tfds) and is not important in itself.

        if self.config.name == "screenshots_hierarchies":
            screen_glob = sorted(glob.glob(os.path.join(filepath, "*.jpg")))
            hierarchy_glob = sorted(glob.glob(os.path.join(filepath, "*.json")))
            for idx, (screen_filepath, hierarchy_filepath) in enumerate(
                zip(screen_glob, hierarchy_glob)
            ):
                with open(hierarchy_filepath, "r") as f:
                    hierarchy = f.read()

                yield idx, {"screenshot_path": screen_filepath, "hierarchy": hierarchy}
        elif self.config.name == "ui_metadata":
            with open(filepath, encoding="utf-8") as csv_file:
                csv_reader = csv.reader(
                    csv_file,
                    delimiter=",",
                    quoting=csv.QUOTE_ALL,
                )
                header = next(csv_reader, None)
                for idx, row in enumerate(csv_reader):
                    yield idx, {k: v for k, v in zip(header, row)}
        elif self.config.name == "layout_vectors":
            with open(os.path.join(filepath, "ui_names.json"), "r") as f:
                ui_names = json.load(f)["ui_names"]

            ui_vectors = np.load(os.path.join(filepath, "ui_vectors.npy"))
            for idx, (name, vector) in enumerate(zip(ui_names, ui_vectors)):
                yield idx, {"ui_name": name, "ui_vector": vector}
        elif self.config.name == "traces":
            return []
        elif self.config.name == "animations":
            return []
        elif self.config.name == "playstore_metadata":
            return []
        elif self.config.name == "screenshots_semantic_hierarchies":
            return []
        #     pass

        # with open(filepath, encoding="utf-8") as f:
        #     for id_, row in enumerate(f):
        #         data = json.loads(row)
        #         if self.config.name == "first_domain":
        #             yield id_, {
        #                 "sentence": data["sentence"],
        #                 "option1": data["option1"],
        #                 "answer": "" if split == "test" else data["answer"],
        #             }
        #         else:
        #             yield id_, {
        #                 "sentence": data["sentence"],
        #                 "option2": data["option2"],
        #                 "second_domain_answer": "" if split == "test" else data["second_domain_answer"],
        #             }
