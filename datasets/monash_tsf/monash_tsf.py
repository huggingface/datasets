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
"""Monash Time Series Forecasting Repository Dataset."""


from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import numpy as np
from pandas.tseries.frequencies import to_offset

import datasets

from .utils import convert_tsf_to_dataframe, frequency_converter


# Find for instance the citation on arxiv or on the dataset repo/website
_CITATION = """\
@InProceedings{godahewa2021monash,
    author = "Godahewa, Rakshitha and Bergmeir, Christoph and Webb, Geoffrey I. and Hyndman, Rob J. and Montero-Manso, Pablo",
    title = "Monash Time Series Forecasting Archive",
    booktitle = "Neural Information Processing Systems Track on Datasets and Benchmarks",
    year = "2021",
    note = "forthcoming"
}
"""

# You can copy an official description
_DESCRIPTION = """\
The first repository containing datasets of related time series for global forecasting.
"""

_HOMEPAGE = "https://forecastingdata.org/"

_LICENSE = "The Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/by/4.0/"


@dataclass
class MonashTSFBuilderConfig(datasets.BuilderConfig):
    """MonashTSF builder config with some added meta data."""

    file_name: Optional[str] = None
    record: Optional[str] = None
    freq: Optional[str] = None
    prediction_length: Optional[int] = None
    item_id_column: Optional[str] = None
    data_column: Optional[str] = None
    target_fields: Optional[List[str]] = None
    feat_dynamic_real_fields: Optional[List[str]] = None
    multivariate: bool = False
    rolling_evaluations: int = 1
    ROOT: str = "https://zenodo.org/record"


# TODO: Name of the dataset usually match the script name with CamelCase instead of snake_case
class MonashTSF(datasets.GeneratorBasedBuilder):
    """Builder of Monash Time Series Forecasting repository of datasets."""

    VERSION = datasets.Version("1.0.0")

    # This is an example of a dataset with multiple configurations.
    # If you don't want/need to define several sub-sets in your dataset,
    # just remove the BUILDER_CONFIG_CLASS and the BUILDER_CONFIGS attributes.

    # If you need to make complex sub-parts in the datasets with configurable options
    # You can create your own builder configuration class to store attribute, inheriting from datasets.BuilderConfig
    BUILDER_CONFIG_CLASS = MonashTSFBuilderConfig

    # You will be able to load one or the other configurations in the following list with
    # data = datasets.load_dataset('my_dataset', 'first_domain')
    # data = datasets.load_dataset('my_dataset', 'second_domain')
    BUILDER_CONFIGS = [
        MonashTSFBuilderConfig(
            name="weather",
            version=VERSION,
            description="3010 daily time series representing the variations of four weather variables: rain, mintemp, maxtemp and solar radiation, measured at the weather stations in Australia.",
            freq="1D",
            record="4654822",
            file_name="weather_dataset.zip",
            data_column="series_type",
        ),
        MonashTSFBuilderConfig(
            name="tourism_yearly",
            version=VERSION,
            description="This dataset contains 518 yearly time series used in the Kaggle Tourism forecasting competition.",
            freq="1Y",
            record="4656103",
            file_name="tourism_yearly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="tourism_quarterly",
            version=VERSION,
            description="This dataset contains 427 quarterly time series used in the Kaggle Tourism forecasting competition.",
            freq="1Q-JAN",
            record="4656093",
            file_name="tourism_quarterly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="tourism_monthly",
            version=VERSION,
            description="This dataset contains 366 monthly time series used in the Kaggle Tourism forecasting competition.",
            freq="1M",
            record="4656096",
            file_name="tourism_monthly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="cif_2016",
            version=VERSION,
            description="72 monthly time series originated from the banking domain used in the CIF 2016 forecasting competition.",
            freq="1M",
            record="4656042",
            file_name="cif_2016_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="london_smart_meters",
            version=VERSION,
            description="5560 half hourly time series that represent the energy consumption readings of London households in kilowatt hour (kWh) from November 2011 to February 2014.",
            freq="30T",
            record="4656072",
            file_name="london_smart_meters_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="australian_electricity_demand",
            version=VERSION,
            description="5 time series representing the half hourly electricity demand of 5 states in Australia: Victoria, New South Wales, Queensland, Tasmania and South Australia.",
            freq="30T",
            record="4659727",
            file_name="australian_electricity_demand_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="wind_farms_minutely",
            version=VERSION,
            description="Minutely time series representing the wind power production of 339 wind farms in Australia.",
            freq="1T",
            record="4654909",
            file_name="wind_farms_minutely_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="bitcoin",
            version=VERSION,
            description="18 daily time series including hash rate, block size, mining difficulty etc. as well as public opinion in the form of tweets and google searches mentioning the keyword bitcoin as potential influencer of the bitcoin price.",
            freq="1D",
            record="5121965",
            file_name="bitcoin_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="pedestrian_counts",
            version=VERSION,
            description="Hourly pedestrian counts captured from 66 sensors in Melbourne city starting from May 2009.",
            freq="1H",
            record="4656626",
            file_name="pedestrian_counts_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="vehicle_trips",
            version=VERSION,
            description="329 daily time series representing the number of trips and vehicles belonging to a set of for-hire vehicle (FHV) companies.",
            freq="1D",
            record="5122535",
            file_name="vehicle_trips_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="oikolab_weather",
            version=VERSION,
            description="Eight time series representing the hourly climate data nearby Monash University, Clayton, Victoria, Australia from 2010-01-01 to 2021-05-31",
            freq="1H",
            record="5184708",
            file_name="oikolab_weather_dataset.zip",
            data_column="type",
        ),
        MonashTSFBuilderConfig(
            name="temperature_rain",
            version=VERSION,
            description="32072 daily time series showing the temperature observations and rain forecasts, gathered by the Australian Bureau of Meteorology for 422 weather stations across Australia, between 02/05/2015 and 26/04/2017",
            freq="1D",
            record="5129073",
            file_name="temperature_rain_dataset_with_missing_values.zip",
            item_id_column="station_id",
            data_column="obs_or_fcst",
            target_fields=[
                "fcst_0_DailyPoP",
                "fcst_0_DailyPoP1",
                "fcst_0_DailyPoP10",
                "fcst_0_DailyPoP15",
                "fcst_0_DailyPoP25",
                "fcst_0_DailyPoP5",
                "fcst_0_DailyPoP50",
                "fcst_0_DailyPrecip",
                "fcst_0_DailyPrecip10Pct",
                "fcst_0_DailyPrecip25Pct",
                "fcst_0_DailyPrecip50Pct",
                "fcst_0_DailyPrecip75Pct",
                "fcst_1_DailyPoP",
                "fcst_1_DailyPoP1",
                "fcst_1_DailyPoP10",
                "fcst_1_DailyPoP15",
                "fcst_1_DailyPoP25",
                "fcst_1_DailyPoP5",
                "fcst_1_DailyPoP50",
                "fcst_1_DailyPrecip",
                "fcst_1_DailyPrecip10Pct",
                "fcst_1_DailyPrecip25Pct",
                "fcst_1_DailyPrecip50Pct",
                "fcst_1_DailyPrecip75Pct",
                "fcst_2_DailyPoP",
                "fcst_2_DailyPoP1",
                "fcst_2_DailyPoP10",
                "fcst_2_DailyPoP15",
                "fcst_2_DailyPoP25",
                "fcst_2_DailyPoP5",
                "fcst_2_DailyPoP50",
                "fcst_2_DailyPrecip",
                "fcst_2_DailyPrecip10Pct",
                "fcst_2_DailyPrecip25Pct",
                "fcst_2_DailyPrecip50Pct",
                "fcst_2_DailyPrecip75Pct",
                "fcst_3_DailyPoP",
                "fcst_3_DailyPoP1",
                "fcst_3_DailyPoP10",
                "fcst_3_DailyPoP15",
                "fcst_3_DailyPoP25",
                "fcst_3_DailyPoP5",
                "fcst_3_DailyPoP50",
                "fcst_3_DailyPrecip",
                "fcst_3_DailyPrecip10Pct",
                "fcst_3_DailyPrecip25Pct",
                "fcst_3_DailyPrecip50Pct",
                "fcst_3_DailyPrecip75Pct",
                "fcst_4_DailyPoP",
                "fcst_4_DailyPoP1",
                "fcst_4_DailyPoP10",
                "fcst_4_DailyPoP15",
                "fcst_4_DailyPoP25",
                "fcst_4_DailyPoP5",
                "fcst_4_DailyPoP50",
                "fcst_4_DailyPrecip",
                "fcst_4_DailyPrecip10Pct",
                "fcst_4_DailyPrecip25Pct",
                "fcst_4_DailyPrecip50Pct",
                "fcst_4_DailyPrecip75Pct",
                "fcst_5_DailyPoP",
                "fcst_5_DailyPoP1",
                "fcst_5_DailyPoP10",
                "fcst_5_DailyPoP15",
                "fcst_5_DailyPoP25",
                "fcst_5_DailyPoP5",
                "fcst_5_DailyPoP50",
                "fcst_5_DailyPrecip",
                "fcst_5_DailyPrecip10Pct",
                "fcst_5_DailyPrecip25Pct",
                "fcst_5_DailyPrecip50Pct",
                "fcst_5_DailyPrecip75Pct",
            ],
            feat_dynamic_real_fields=["T_MEAN", "PRCP_SUM", "T_MAX", "T_MIN"],
            multivariate=True,
        ),
    ]

    # DEFAULT_CONFIG_NAME = (
    #     "first_domain"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    # )

    def _info(self):
        if self.config.multivariate:
            features = datasets.Features(
                {
                    "start": datasets.Value("timestamp[s]"),
                    "target": datasets.Sequence(datasets.Sequence(datasets.Value("float32"))),
                    "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                    # "feat_static_real":  datasets.Sequence(datasets.Value("float32")),
                    "feat_dynamic_real": datasets.Sequence(datasets.Sequence(datasets.Value("float32"))),
                    # "feat_dynamic_cat": datasets.Sequence(datasets.Sequence(datasets.Value("uint64"))),
                    "item_id": datasets.Value("string"),
                }
            )
        else:
            features = datasets.Features(
                {
                    "start": datasets.Value("timestamp[s]"),
                    "target": datasets.Sequence(datasets.Value("float32")),
                    "feat_static_cat": datasets.Sequence(datasets.Value("uint64")),
                    # "feat_static_real":  datasets.Sequence(datasets.Value("float32")),
                    "feat_dynamic_real": datasets.Sequence(datasets.Sequence(datasets.Value("float32"))),
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
        # TODO: This method is tasked with downloading/extracting the data and defining the splits depending on the configuration
        # If several configurations are possible (listed in BUILDER_CONFIGS), the configuration selected by the user is in self.config.name

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = f"{self.config.ROOT}/{self.config.record}/files/{self.config.file_name}"
        data_dir = dl_manager.download_and_extract(urls)
        file_path = Path(data_dir) / (self.config.file_name.split(".")[0] + ".tsf")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": file_path,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={"filepath": file_path, "split": "test"},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": file_path,
                    "split": "val",
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.

        (
            loaded_data,
            frequency,
            forecast_horizon,
            contain_missing_values,
            contain_equal_length,
        ) = convert_tsf_to_dataframe(filepath, value_column_name="target")

        if forecast_horizon is None:
            prediction_length_map = {
                "T": 60,
                "H": 48,
                "D": 30,
                "W": 8,
                "M": 12,
                "Y": 4,
            }
            freq = frequency_converter(frequency)
            freq = to_offset(freq).name
            forecast_horizon = prediction_length_map[freq]

        if self.config.prediction_length is not None:
            forecast_horizon = self.config.prediction_length

        if self.config.item_id_column is not None:
            loaded_data.set_index(self.config.item_id_column, inplace=True)
            loaded_data.sort_index(inplace=True)

            for cat, item_id in enumerate(loaded_data.index.unique()):
                ts = loaded_data.loc[item_id]
                start = ts.start_timestamp[0]

                if self.config.target_fields is not None:
                    target_fields = ts[ts[self.config.data_column].isin(self.config.target_fields)]
                else:
                    target_fields = self.config.data_column.unique()

                if self.config.feat_dynamic_real_fields is not None:
                    feat_dynamic_real_fields = ts[ts[self.config.data_column].isin(self.config.feat_dynamic_real_fields)]
                    feat_dynamic_real = np.vstack(feat_dynamic_real_fields.target)
                else:
                    feat_dynamic_real = None
                
                target = np.vstack(target_fields.target)

                feat_static_cat = [cat]

                if split in ["train", "val"]:
                    offset = forecast_horizon * self.config.rolling_evaluations + forecast_horizon * (split == "train")
                    target = target[..., :-offset]
                    if self.config.feat_dynamic_real_fields is not None:
                        feat_dynamic_real = feat_dynamic_real[..., :-offset]

                yield cat, {
                    "start": start,
                    "target": target,
                    "feat_dynamic_real": feat_dynamic_real,
                    "feat_static_cat": feat_static_cat,
                    "item_id": item_id,
                }
        else:
            if self.config.target_fields is not None:
                target_fields = loaded_data[loaded_data[self.config.data_column].isin(self.config.target_fields)]
            else: 
                target_fields = loaded_data
            if self.config.feat_dynamic_real_fields is not None:
                feat_dynamic_real_fields = loaded_data[loaded_data[self.config.data_column].isin(self.config.feat_dynamic_real_fields)]
            else:
                feat_dynamic_real_fields = None

            for cat, ts in target_fields.iterrows():
                start = ts.get("start_timestamp", datetime.strptime('1900-01-01 00-00-00', '%Y-%m-%d %H-%M-%S'))
                target = ts.target
                if feat_dynamic_real_fields is not None:
                    feat_dynamic_real = np.vstack(feat_dynamic_real_fields.target)
                else:
                    feat_dynamic_real = None

                feat_static_cat = [cat]
                if self.config.data_column is not None:
                    item_id = f"{ts.series_name}-{ts[self.config.data_column]}"
                else:
                    item_id = ts.series_name

                if split in ["train", "val"]:
                    offset = forecast_horizon * self.config.rolling_evaluations + forecast_horizon * (split == "train")
                    target = target[..., :-offset]
                    if feat_dynamic_real is not None:
                        feat_dynamic_real = feat_dynamic_real[..., :-offset]

                yield cat, {
                    "start": start,
                    "target": target,
                    "feat_dynamic_real": feat_dynamic_real,
                    "feat_static_cat": feat_static_cat,
                    "item_id": item_id,
                }
