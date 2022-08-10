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


from dataclasses import dataclass
from datetime import datetime
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

_DESCRIPTION = """\
Monash Time Series Forecasting Repository which contains 30+ datasets of related time series for global forecasting research. This repository includes both real-world and competition time series datasets covering varied domains.
"""

_HOMEPAGE = "https://forecastingdata.org/"

_LICENSE = "The Creative Commons Attribution 4.0 International License. https://creativecommons.org/licenses/by/4.0/"

_ROOT_URL = "https://zenodo.org/record"


@dataclass
class MonashTSFBuilderConfig(datasets.BuilderConfig):
    """MonashTSF builder config with some added meta data."""

    file_name: Optional[str] = None
    record: Optional[str] = None
    prediction_length: Optional[int] = None
    item_id_column: Optional[str] = None
    data_column: Optional[str] = None
    target_fields: Optional[List[str]] = None
    feat_dynamic_real_fields: Optional[List[str]] = None
    multivariate: bool = False
    rolling_evaluations: int = 1


class MonashTSF(datasets.GeneratorBasedBuilder):
    """Builder of Monash Time Series Forecasting repository of datasets."""

    VERSION = datasets.Version("1.0.0")

    BUILDER_CONFIG_CLASS = MonashTSFBuilderConfig

    BUILDER_CONFIGS = [
        MonashTSFBuilderConfig(
            name="weather",
            version=VERSION,
            description="3010 daily time series representing the variations of four weather variables: rain, mintemp, maxtemp and solar radiation, measured at the weather stations in Australia.",
            record="4654822",
            file_name="weather_dataset.zip",
            data_column="series_type",
        ),
        MonashTSFBuilderConfig(
            name="tourism_yearly",
            version=VERSION,
            description="This dataset contains 518 yearly time series used in the Kaggle Tourism forecasting competition.",
            record="4656103",
            file_name="tourism_yearly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="tourism_quarterly",
            version=VERSION,
            description="This dataset contains 427 quarterly time series used in the Kaggle Tourism forecasting competition.",
            record="4656093",
            file_name="tourism_quarterly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="tourism_monthly",
            version=VERSION,
            description="This dataset contains 366 monthly time series used in the Kaggle Tourism forecasting competition.",
            record="4656096",
            file_name="tourism_monthly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="cif_2016",
            version=VERSION,
            description="72 monthly time series originated from the banking domain used in the CIF 2016 forecasting competition.",
            record="4656042",
            file_name="cif_2016_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="london_smart_meters",
            version=VERSION,
            description="5560 half hourly time series that represent the energy consumption readings of London households in kilowatt hour (kWh) from November 2011 to February 2014.",
            record="4656072",
            file_name="london_smart_meters_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="australian_electricity_demand",
            version=VERSION,
            description="5 time series representing the half hourly electricity demand of 5 states in Australia: Victoria, New South Wales, Queensland, Tasmania and South Australia.",
            record="4659727",
            file_name="australian_electricity_demand_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="wind_farms_minutely",
            version=VERSION,
            description="Minutely time series representing the wind power production of 339 wind farms in Australia.",
            record="4654909",
            file_name="wind_farms_minutely_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="bitcoin",
            version=VERSION,
            description="18 daily time series including hash rate, block size, mining difficulty etc. as well as public opinion in the form of tweets and google searches mentioning the keyword bitcoin as potential influencer of the bitcoin price.",
            record="5121965",
            file_name="bitcoin_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="pedestrian_counts",
            version=VERSION,
            description="Hourly pedestrian counts captured from 66 sensors in Melbourne city starting from May 2009.",
            record="4656626",
            file_name="pedestrian_counts_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="vehicle_trips",
            version=VERSION,
            description="329 daily time series representing the number of trips and vehicles belonging to a set of for-hire vehicle (FHV) companies.",
            record="5122535",
            file_name="vehicle_trips_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="kdd_cup_2018",
            version=VERSION,
            description="Hourly time series representing the air quality levels in 59 stations in 2 cities from 01/01/2017 to 31/03/2018.",
            record="4656719",
            file_name="kdd_cup_2018_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="nn5_daily",
            version=VERSION,
            description="111 time series to predicting the daily cash withdrawals from ATMs in UK.",
            record="4656110",
            file_name="nn5_daily_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="nn5_weekly",
            version=VERSION,
            description="111 time series to predicting the weekly cash withdrawals from ATMs in UK.",
            record="4656125",
            file_name="nn5_weekly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="kaggle_web_traffic",
            version=VERSION,
            description="145063 daily time series representing the number of hits or web traffic for a set of Wikipedia pages from 2015-07-01 to 2017-09-10.",
            record="4656080",
            file_name="kaggle_web_traffic_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="kaggle_web_traffic_weekly",
            version=VERSION,
            description="145063 daily time series representing the number of hits or web traffic for a set of Wikipedia pages from 2015-07-01 to 2017-09-10.",
            record="4656664",
            file_name="kaggle_web_traffic_weekly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="solar_10_minutes",
            version=VERSION,
            description="137 time series representing the solar power production recorded per every 10 minutes in Alabama state in 2006.",
            record="4656144",
            file_name="solar_10_minutes_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="solar_weekly",
            version=VERSION,
            description="137 time series representing the weekly solar power production in Alabama state in 2006.",
            record="4656151",
            file_name="solar_weekly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="car_parts",
            version=VERSION,
            description="2674 intermittent monthly time series that represent car parts sales from January 1998 to March 2002.",
            record="4656022",
            file_name="car_parts_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="fred_md",
            version=VERSION,
            description="107 monthly time series showing a set of macro-economic indicators from the Federal Reserve Bank.",
            record="4654833",
            file_name="fred_md_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="traffic_hourly",
            version=VERSION,
            description="862 hourly time series showing the road occupancy rates on the San Francisco Bay area freeways from 2015 to 2016.",
            record="4656132",
            file_name="traffic_hourly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="traffic_weekly",
            version=VERSION,
            description="862 weekly time series showing the road occupancy rates on the San Francisco Bay area freeways from 2015 to 2016.",
            record="4656135",
            file_name="traffic_weekly_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="hospital",
            version=VERSION,
            description="767 monthly time series that represent the patient counts related to medical products from January 2000 to December 2006.",
            record="4656014",
            file_name="hospital_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="covid_deaths",
            version=VERSION,
            description="266 daily time series that represent the COVID-19 deaths in a set of countries and states from 22/01/2020 to 20/08/2020.",
            record="4656009",
            file_name="covid_deaths_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="sunspot",
            version=VERSION,
            description="A single very long daily time series of sunspot numbers from 1818-01-08 to 2020-05-31.",
            record="4654773",
            file_name="sunspot_dataset_with_missing_values.zip",
        ),
        MonashTSFBuilderConfig(
            name="saugeenday",
            version=VERSION,
            description="A single very long time series representing the daily mean flow of the Saugeen River at Walkerton in cubic meters per second from 01/01/1915 to 31/12/1979.",
            record="4656058",
            file_name="saugeenday_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="us_births",
            version=VERSION,
            description="A single very long daily time series representing the number of births in US from 01/01/1969 to 31/12/1988.",
            record="4656049",
            file_name="us_births_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="solar_4_seconds",
            version=VERSION,
            description="A single very long daily time series representing the solar power production in MW recorded per every 4 seconds starting from 01/08/2019.",
            record="4656027",
            file_name="solar_4_seconds_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="wind_4_seconds",
            version=VERSION,
            description="A single very long daily time series representing the wind power production in MW recorded per every 4 seconds starting from 01/08/2019.",
            record="4656032",
            file_name="wind_4_seconds_dataset.zip",
        ),
        MonashTSFBuilderConfig(
            name="rideshare",
            version=VERSION,
            description="156 hourly time series representations of attributes related to Uber and Lyft rideshare services for various locations in New York between 26/11/2018 and 18/12/2018.",
            record="5122114",
            file_name="rideshare_dataset_with_missing_values.zip",
            item_id_column=["source_location", "provider_name", "provider_service"],
            data_column="type",
            target_fields=[
                "price_min",
                "price_mean",
                "price_max",
                "distance_min",
                "distance_mean",
                "distance_max",
                "surge_min",
                "surge_mean",
                "surge_max",
                "api_calls",
            ],
            feat_dynamic_real_fields=["temp", "rain", "humidity", "clouds", "wind"],
            multivariate=True,
        ),
        MonashTSFBuilderConfig(
            name="oikolab_weather",
            version=VERSION,
            description="Eight time series representing the hourly climate data nearby Monash University, Clayton, Victoria, Australia from 2010-01-01 to 2021-05-31",
            record="5184708",
            file_name="oikolab_weather_dataset.zip",
            data_column="type",
        ),
        MonashTSFBuilderConfig(
            name="temperature_rain",
            version=VERSION,
            description="32072 daily time series showing the temperature observations and rain forecasts, gathered by the Australian Bureau of Meteorology for 422 weather stations across Australia, between 02/05/2015 and 26/04/2017",
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
        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS
        # It can accept any type or nested list/dict and will give back the same structure with the url replaced with path to local files.
        # By default the archives will be extracted and a path to a cached folder where they are extracted is returned instead of the archive
        urls = f"{_ROOT_URL}/{self.config.record}/files/{self.config.file_name}"
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
        (
            loaded_data,
            frequency,
            forecast_horizon,
            _,
            _,
        ) = convert_tsf_to_dataframe(filepath, value_column_name="target")

        if forecast_horizon is None:
            prediction_length_map = {
                "S": 60,
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
                    feat_dynamic_real_fields = ts[
                        ts[self.config.data_column].isin(self.config.feat_dynamic_real_fields)
                    ]
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
                feat_dynamic_real_fields = loaded_data[
                    loaded_data[self.config.data_column].isin(self.config.feat_dynamic_real_fields)
                ]
            else:
                feat_dynamic_real_fields = None

            for cat, ts in target_fields.iterrows():
                start = ts.get("start_timestamp", datetime.strptime("1900-01-01 00-00-00", "%Y-%m-%d %H-%M-%S"))
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
