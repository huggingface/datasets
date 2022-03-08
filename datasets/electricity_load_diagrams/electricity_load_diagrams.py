# coding=utf-8
# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""Electricity Load Diagrams 2011-2014 time series dataset."""
from pathlib import Path

import pandas as pd

import datasets

from .utils import to_dict


_CITATION = """\
@inproceedings{10.1145/3209978.3210006,
    author = {Lai, Guokun and Chang, Wei-Cheng and Yang, Yiming and Liu, Hanxiao},
    title = {Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks},
    year = {2018},
    isbn = {9781450356572},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3209978.3210006},
    doi = {10.1145/3209978.3210006},
    booktitle = {The 41st International ACM SIGIR Conference on Research & Development in Information Retrieval},
    pages = {95--104},
    numpages = {10},
    location = {Ann Arbor, MI, USA},
    series = {SIGIR '18}
}
"""

_DESCRIPTION = """\
This new dataset contains hourly kW electricity consumption time series of 370 Portuguese clients from 2011 to 2014.
"""

_HOMEPAGE = "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014"

_LICENSE = ""

_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip"


class ElectricityLoadDiagramsConfig(datasets.BuilderConfig):
    """A builder config with some added meta data."""

    freq: str = "1H"
    prediction_length: int = 24
    rolling_evaluations: int = 7


class ElectricityLoadDiagrams(datasets.GeneratorBasedBuilder):
    """Hourly electricity consumption of 370 points/clients."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        ElectricityLoadDiagramsConfig(
            name="uci",
            version=VERSION,
            description="Original UCI time series.",
        ),
        ElectricityLoadDiagramsConfig(
            name="lstnet",
            version=VERSION,
            description="Electricity time series preprocessed as in LSTNet paper.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "lstnet"

    def _info(self):
        features = datasets.Features(
            {
                "start": datasets.Value("timestamp[s]"),
                "target": datasets.Sequence(datasets.Value("float32")),
                "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                # "feat_static_real":  datasets.Sequence(datasets.Value("float32")),
                # "feat_dynamic_real":  datasets.Sequence(datasets.Sequence(datasets.Value("uint64"))),
                # "feat_dynamic_cat": datasets.Sequence(datasets.Sequence(datasets.Value("uint64"))),
                "item_id": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        data_dir = dl_manager.download_and_extract(_URL)

        train_ts = []
        val_ts = []
        test_ts = []

        df = pd.read_csv(
            Path(data_dir) / "LD2011_2014.txt",
            sep=";",
            index_col=0,
            parse_dates=True,
            decimal=",",
        )
        df.sort_index(inplace=True)
        df = df.resample(self.config.freq).sum()
        unit = pd.tseries.frequencies.to_offset(self.config.freq).name

        if self.config.name == "uci":
            val_end_date = df.index.max() - pd.Timedelta(
                self.config.prediction_length * self.config.rolling_evaluations, unit
            )
            train_end_date = val_end_date - pd.Timedelta(self.config.prediction_length, unit)
        else:
            # concate the time series to be from 2012 till 2014
            df = df[(df.index.year >= 2012) & (df.index.year <= 2014)]

            # drop time series which are zero at the start
            df = df.T[df.iloc[0] > 0].T

            # tran/val/test split from LSTNet paper
            # validation ends at 8/10-th of the time series
            val_end_date = df.index[int(len(df) * (8 / 10)) - 1]
            # training ends at 6/10-th of the time series
            train_end_date = df.index[int(len(df) * (6 / 10)) - 1]

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

        for i in range(self.config.rolling_evaluations):
            for cat, (ts_id, ts) in enumerate(df.iteritems()):
                start_date = ts.ne(0).idxmax()

                test_end_date = val_end_date + pd.Timedelta(self.config.prediction_length * (i + 1), unit)
                sliced_ts = ts[start_date:test_end_date]
                test_ts.append(
                    to_dict(
                        target_values=sliced_ts.values,
                        start=start_date,
                        cat=[cat],
                        item_id=ts_id,
                    )
                )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "split": train_ts,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "split": test_ts,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "split": val_ts,
                },
            ),
        ]

    def _generate_examples(self, split):
        for key, row in enumerate(split):
            yield key, row
