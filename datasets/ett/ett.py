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
"""Electricity Transformer Temperature (ETT) dataset."""
3
import csv
import json
import os
from dataclasses import dataclass

import pandas as pd

import datasets


_CITATION = """\
@inproceedings{haoyietal-informer-2021,
  author    = {Haoyi Zhou and
               Shanghang Zhang and
               Jieqi Peng and
               Shuai Zhang and
               Jianxin Li and
               Hui Xiong and
               Wancai Zhang},
  title     = {Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting},
  booktitle = {The Thirty-Fifth {AAAI} Conference on Artificial Intelligence, {AAAI} 2021, Virtual Conference},
  volume    = {35},
  number    = {12},
  pages     = {11106--11115},
  publisher = {{AAAI} Press},
  year      = {2021},
}
"""

_DESCRIPTION = """\
The data of Electricity Transformers from two separated counties
in China collected for two years at hourly and 15-min frequencies. 
Each data point consists of the target value "oil temperature" and 
6 power load features. The train/val/test is 12/4/4 months.
"""

_HOMEPAGE = "https://github.com/zhouhaoyi/ETDataset"

_LICENSE = "Creative Commons Attribution-NoDerivatives 4.0 International"

# TODO: Add link to the official dataset URLs here
# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "h1": "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTh1.csv",
    "h2": "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTh2.csv",
    "m1": "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTm1.csv",
    "m2": "https://raw.githubusercontent.com/zhouhaoyi/ETDataset/main/ETT-small/ETTm2.csv",
}


@dataclass
class ETTBuilderConfig(datasets.BuilderConfig):
    """ETT builder config with some added meta data."""

    prediction_length: int = 24
    multivariate: bool = False


class ETT(datasets.GeneratorBasedBuilder):
    """Electricity Transformer Temperature (ETT) dataset"""

    VERSION = datasets.Version("1.0.0")

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('ett', 'h1')
    # data = datasets.load_dataset('ett', 'm2')
    BUILDER_CONFIGS = [
        ETTBuilderConfig(
            name="h1",
            version=VERSION,
            description="Time series from first county at hourly frequency.",
        ),
        ETTBuilderConfig(
            name="h2",
            version=VERSION,
            description="Time series from second county at hourly frequency.",
        ),
        ETTBuilderConfig(
            name="m1",
            version=VERSION,
            description="Time series from first county at 15-min frequency.",
        ),
        ETTBuilderConfig(
            name="m2",
            version=VERSION,
            description="Time series from second county at 15-min frequency.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "h1"  # It's not mandatory to have a default configuration. Just use one if it make sense.

    def _info(self):
        if self.config.multivariate:
            features = datasets.Features(
                {
                    "start": datasets.Value("timestamp[s]"),
                    "target": datasets.Sequence(
                        datasets.Sequence(datasets.Value("float32"))
                    ),
                    "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                    "item_id": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "start": datasets.Value("timestamp[s]"),
                    "target": datasets.Sequence(datasets.Value("float32")),
                    "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
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
        filepath = dl_manager.download_and_extract(urls)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepath,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepath,
                    "split": "test",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": filepath,
                    "split": "dev",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        data = pd.read_csv(filepath, parse_dates=True, index_col=0)
        start_date = data.index.min()
        train_end_date_index = 12 * 30 * 24  # 1 year

        if split == "dev":
            end_date_index = 12 * 30 * 24 + 4 * 30 * 24  # 1 year + 4 months
        else:
            end_date_index = 12 * 30 * 24 + 8 * 30 * 24  # 1 year + 8 months

        if self.config.multivariate:
            if split in ["test", "dev"]:
                for i, index in range(
                    train_end_date_index, end_date_index, self.config.prediction_length
                ):
                    yield i, {
                        "start": start_date,
                        "target": data[: index + self.config.prediction_length]
                        .values.astype("float32")
                        .T,
                        "feat_static_cat": [0],
                        "item_id": "0",
                    }
            else:
                yield 0, {
                    "start": start_date,
                    "target": data[:train_end_date_index].values.astype("float32").T,
                    "feat_static_cat": [0],
                    "item_id": "0",
                }
        else:
            for i, col in enumerate(data.columns):
                if split in ["test", "dev"]:
                    for j, index in enumerate(
                        range(
                            train_end_date_index,
                            end_date_index,
                            self.config.prediction_length,
                        )
                    ):
                        target = data[col][
                            : index + self.config.prediction_length
                        ].values.astype("float32")
                        yield j * len(data.columns) + i, {
                            "start": start_date,
                            "target": target,
                            "feat_static_cat": [i],
                            "item_id": col,
                        }
                else:
                    yield i, {
                        "start": start_date,
                        "target": data[col][:train_end_date_index].values.astype(
                            "float32"
                        ),
                        "feat_static_cat": [i],
                        "item_id": col,
                    }
