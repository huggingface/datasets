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
"""Electricity time series dataset."""


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

# You can copy an official description
_DESCRIPTION = """\
This new dataset contains hourly kW electricity consumption time series of 370 Portuguese clients from 2011 to 2014.
"""

_HOMEPAGE = "https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014"

_LICENSE = ""

# The HuggingFace Datasets library doesn't host the datasets but only points to the original files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URLS = {
    "uci": "https://archive.ics.uci.edu/ml/machine-learning-databases/00321/LD2011_2014.txt.zip",
    "lstnet": "https://raw.githubusercontent.com/laiguokun/multivariate-time-series-data/master/electricity/electricity.txt.gz",
}


class Electricty(datasets.GeneratorBasedBuilder):
    """Hourly electricity consumption of 370 points/clients."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="uci",
            version=VERSION,
            description="Original UCI time series.",
        ),
        datasets.BuilderConfig(
            name="lstnet",
            version=VERSION,
            description="Electricity time series preporcessed as in LSTNet paper.",
        ),
    ]

    DEFAULT_CONFIG_NAME = "lstnet"

    def _info(self):
        features = datasets.Features(
            {
                "start": datasets.Value("string"),
                "target": datasets.Sequence(datasets.Value("float32")),
                "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                # "feat_static_real":  datasets.Sequence(datasets.Value("float32")),
                # "feat_dynamic_real":  datasets.Sequence(datasets.Sequence(datasets.Value("uint64"))),
                # "feat_dynamic_cat": datasets.Sequence(datasets.Sequence(datasets.Value("uint64"))),
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

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = _URLS[self.config.name]
        data_dir = dl_manager.download_and_extract(urls)

        # define the prediction problem # TODO save these in metadata
        freq = "1H"
        prediction_length = 24
        rolling_evaluations = 7

        train_ts = []
        val_ts = []
        test_ts = []

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

            val_end_date = df.index.max() - pd.Timedelta(prediction_length * rolling_evaluations, "H")
            train_end_date = val_end_date - pd.Timedelta(prediction_length, "H")

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

            for i in range(rolling_evaluations):
                for cat, (ts_id, ts) in enumerate(df.iteritems()):
                    start_date = ts.ne(0).idxmax()

                    test_end_date = val_end_date + pd.Timedelta(prediction_length * (i + 1), "H")
                    sliced_ts = ts[start_date:test_end_date]
                    test_ts.append(
                        to_dict(
                            target_values=sliced_ts.values,
                            start=start_date,
                            cat=[cat],
                            item_id=ts_id,
                        )
                    )
        else:
            time_index = pd.date_range(
                start="2012-01-01",
                freq=freq,
                periods=26304,
            )
            timeseries = pd.read_csv(data_dir, header=None, compression=None)
            timeseries.set_index(time_index[: len(timeseries)], inplace=True)

            # validation ends at 8/10-th of the time series
            validation_end = time_index[int(len(time_index) * (8 / 10)) - 1]
            # training ends at 6/10-th of the time series
            training_end = time_index[int(len(time_index) * (6 / 10)) - 1]

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

            for i in range(rolling_evaluations):
                for cat, (ts_id, ts) in enumerate(timeseries.iteritems()):
                    testing_end = validation_end + pd.Timedelta(prediction_length * (i + 1), "H")
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

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "split": train_ts,
                    "filepath": None,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "split": test_ts,
                    "filepath": None,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "split": val_ts,
                    "filepath": None,
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        for key, row in enumerate(split):
            # Yields examples as (key, example) tuples
            yield key, row
