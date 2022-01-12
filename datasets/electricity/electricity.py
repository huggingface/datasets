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
# TODO: Address all TODOs and remove all explanatory comments
"""TODO: Add a description here."""


import csv
import json
import os
from pathlib import Path

import pandas as pd
import numpy as np

import datasets

from .utils import to_dict, save_to_file


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
_HOMEPAGE = "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014"

# TODO: Add the licence for the dataset here if you can find it
_LICENSE = ""

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "uci": "https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip",
    "lstnet": "https://raw.githubusercontent.com/laiguokun/multivariate-time-series-data/master/electricity/electricity.txt.gz",
}


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class NewDataset(datasets.GeneratorBasedBuilder):
    """TODO: Short description of my dataset."""

    VERSION = datasets.Version("1.0.0")

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
            name="uci",
            version=VERSION,
            description="This part of my dataset covers a first domain",
        ),
        datasets.BuilderConfig(
            name="lstnet",
            version=VERSION,
            description="This part of my dataset covers a second domain",
        ),
    ]

    DEFAULT_CONFIG_NAME = "lstnet"

    def _info(self):
        features = datasets.Features(
            {
                "start": datasets.Value("string"),
                "target": datasets.Sequence(datasets.Value("float32")),
                "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                # "feat_dynamic_real": ndarray type
                # "feat_dynamic_cat"
                # "feat_static_real"
                "item_id": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)

        # define the prediction problem # TODO save these in metadata
        freq = "1H"
        prediction_length = 24
        rolling_evaluations = 7
        univariate = True

        if self.config.name == "uci":
            df = pd.read_csv(
                Path(data_dir) / "LD2011_2014.txt",
                sep=";",
                index_col=0,
                parse_dates=True,
                decimal=",",
            )
            df.sort_index(inplace=True)
            df = df.resample(freq).sum()

            val_end_date = df.index.max() - pd.Timedelta(
                prediction_length * rolling_evaluations, "H"
            )
            train_end_date = val_end_date - pd.Timedelta(prediction_length, "H")

            train_ts = []
            val_ts = []
            for cat, (ts_id, ts) in enumerate(df.iteritems()):
                start_date = ts.ne(0).idxmax()

                sliced_ts = ts[start_date:train_end_date]
                train_ts.append(
                    to_dict(
                        target_values=sliced_ts.values,
                        start=start_date,
                        cat=[cat],
                        item_id=ts_id,
                    )
                )

                sliced_ts = ts[start_date:val_end_date]
                val_ts.append(
                    to_dict(
                        target_values=sliced_ts.values,
                        start=start_date,
                        cat=[cat],
                        item_id=ts_id,
                    )
                )
            save_to_file(Path(data_dir) / "train.jsonl", train_ts)
            save_to_file(Path(data_dir) / "dev.jsonl", val_ts)

            test_ts = []
            for i in range(rolling_evaluations):
                for cat, (ts_id, ts) in enumerate(df.iteritems()):
                    start_date = ts.ne(0).idxmax()

                    test_end_date = val_end_date + pd.Timedelta(
                        prediction_length * (i + 1), "H"
                    )
                    sliced_ts = ts[start_date:test_end_date]
                    test_ts.append(
                        to_dict(
                            target_values=sliced_ts.values,
                            start=start_date,
                            cat=[cat],
                            item_id=ts_id,
                        )
                    )
            save_to_file(Path(data_dir) / "test.jsonl", test_ts)
        else:
            os.rename(data_dir, Path(data_dir).parents[0] / "electricity.txt")
            os.makedirs(data_dir, exist_ok=True)

            time_index = pd.date_range(
                start="2012-01-01",
                freq=freq,
                periods=26304,
            )
            timeseries = pd.read_csv(
                Path(data_dir).parents[0] / "electricity.txt", header=None
            )
            timeseries.set_index(time_index, inplace=True)

            # train/val ends at 8/10-th of the time series
            validation_end = time_index[int(len(time_index) * (8 / 10))]
            training_end = validation_end - pd.Timedelta(prediction_length, "H")

            train_ts = []
            val_ts = []
            for cat, (ts_id, ts) in enumerate(timeseries.iteritems()):
                sliced_ts = ts[:training_end]
                if len(sliced_ts) > 0:
                    train_ts.append(
                        to_dict(
                            target_values=sliced_ts.values,
                            start=sliced_ts.index[0],
                            cat=[cat],
                            item_id=ts_id,
                        )
                    )

                sliced_ts = ts[:validation_end]
                if len(sliced_ts) > 0:
                    val_ts.append(
                        to_dict(
                            target_values=sliced_ts.values,
                            start=sliced_ts.index[0],
                            cat=[cat],
                            item_id=ts_id,
                        )
                    )

            save_to_file(Path(data_dir) / "train.jsonl", train_ts)
            save_to_file(Path(data_dir) / "dev.jsonl", val_ts)

            test_ts = []
            for i in range(rolling_evaluations):
                for cat, (ts_id, ts) in enumerate(timeseries.iteritems()):
                    testing_end = validation_end + pd.Timedelta(
                        prediction_length * (i + 1), "H"
                    )
                    sliced_ts = ts[:testing_end]
                    if len(sliced_ts) > 0:
                        test_ts.append(
                            to_dict(
                                target_values=sliced_ts.values,
                                start=sliced_ts.index[0],
                                cat=[cat],
                                item_id=ts_id,
                            )
                        )
            save_to_file(Path(data_dir) / "test.jsonl", train_ts)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "train.jsonl"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "test.jsonl"),
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "dev.jsonl"),
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as f:
            for key, row in enumerate(f):
                data = json.loads(row)
                # Yields examples as (key, example) tuples
                yield key, {
                    "target": data["target"],
                    "start": data["start"],
                    "feat_static_cat": data["feat_static_cat"],
                    "item_id": data["item_id"],
                }
