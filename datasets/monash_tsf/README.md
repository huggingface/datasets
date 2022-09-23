---
annotations_creators:
- no-annotation
language_creators:
- found
language:
- unknown
license:
- cc-by-4.0
multilinguality:
- monolingual
pretty_name: Monash Time Series Forecasting Repository
size_categories:
- 1K<n<10K
source_datasets:
- original
task_categories:
- time-series-forecasting
task_ids:
- univariate-time-series-forecasting
- multivariate-time-series-forecasting
dataset_info:
- config_name: weather
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 177638713
    num_examples: 3010
  - name: train
    num_bytes: 176893738
    num_examples: 3010
  - name: validation
    num_bytes: 177266226
    num_examples: 3010
  download_size: 38820451
  dataset_size: 531798677
- config_name: tourism_yearly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 71358
    num_examples: 518
  - name: train
    num_bytes: 54264
    num_examples: 518
  - name: validation
    num_bytes: 62811
    num_examples: 518
  download_size: 36749
  dataset_size: 188433
- config_name: tourism_quarterly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 190920
    num_examples: 427
  - name: train
    num_bytes: 162738
    num_examples: 427
  - name: validation
    num_bytes: 176829
    num_examples: 427
  download_size: 93833
  dataset_size: 530487
- config_name: tourism_monthly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 463986
    num_examples: 366
  - name: train
    num_bytes: 391518
    num_examples: 366
  - name: validation
    num_bytes: 427752
    num_examples: 366
  download_size: 199791
  dataset_size: 1283256
- config_name: cif_2016
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 31859
    num_examples: 72
  - name: train
    num_bytes: 24731
    num_examples: 72
  - name: validation
    num_bytes: 28295
    num_examples: 72
  download_size: 53344
  dataset_size: 84885
- config_name: london_smart_meters
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 687138394
    num_examples: 5560
  - name: train
    num_bytes: 684386194
    num_examples: 5560
  - name: validation
    num_bytes: 685762294
    num_examples: 5560
  download_size: 219673439
  dataset_size: 2057286882
- config_name: australian_electricity_demand
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 4765637
    num_examples: 5
  - name: train
    num_bytes: 4763162
    num_examples: 5
  - name: validation
    num_bytes: 4764400
    num_examples: 5
  download_size: 5770526
  dataset_size: 14293199
- config_name: wind_farms_minutely
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 710246723
    num_examples: 339
  - name: train
    num_bytes: 710078918
    num_examples: 339
  - name: validation
    num_bytes: 710162820
    num_examples: 339
  download_size: 71383130
  dataset_size: 2130488461
- config_name: bitcoin
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 340966
    num_examples: 18
  - name: train
    num_bytes: 336511
    num_examples: 18
  - name: validation
    num_bytes: 338738
    num_examples: 18
  download_size: 220403
  dataset_size: 1016215
- config_name: pedestrian_counts
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 12923256
    num_examples: 66
  - name: train
    num_bytes: 12897120
    num_examples: 66
  - name: validation
    num_bytes: 12910188
    num_examples: 66
  download_size: 4587054
  dataset_size: 38730564
- config_name: vehicle_trips
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 186688
    num_examples: 329
  - name: train
    num_bytes: 105261
    num_examples: 329
  - name: validation
    num_bytes: 145974
    num_examples: 329
  download_size: 44914
  dataset_size: 437923
- config_name: kdd_cup_2018
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 12146966
    num_examples: 270
  - name: train
    num_bytes: 12040046
    num_examples: 270
  - name: validation
    num_bytes: 12093506
    num_examples: 270
  download_size: 2456948
  dataset_size: 36280518
- config_name: nn5_daily
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 366110
    num_examples: 111
  - name: train
    num_bytes: 314828
    num_examples: 111
  - name: validation
    num_bytes: 340469
    num_examples: 111
  download_size: 287708
  dataset_size: 1021407
- config_name: nn5_weekly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 55670
    num_examples: 111
  - name: train
    num_bytes: 48344
    num_examples: 111
  - name: validation
    num_bytes: 52007
    num_examples: 111
  download_size: 62043
  dataset_size: 156021
- config_name: kaggle_web_traffic
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 486103806
    num_examples: 145063
  - name: train
    num_bytes: 415494391
    num_examples: 145063
  - name: validation
    num_bytes: 450799098
    num_examples: 145063
  download_size: 145485324
  dataset_size: 1352397295
- config_name: kaggle_web_traffic_weekly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 73816627
    num_examples: 145063
  - name: train
    num_bytes: 64242469
    num_examples: 145063
  - name: validation
    num_bytes: 69029548
    num_examples: 145063
  download_size: 28930900
  dataset_size: 207088644
- config_name: solar_10_minutes
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 29707848
    num_examples: 137
  - name: train
    num_bytes: 29640033
    num_examples: 137
  - name: validation
    num_bytes: 29673941
    num_examples: 137
  download_size: 4559353
  dataset_size: 89021822
- config_name: solar_weekly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 34265
    num_examples: 137
  - name: train
    num_bytes: 28614
    num_examples: 137
  - name: validation
    num_bytes: 31439
    num_examples: 137
  download_size: 24375
  dataset_size: 94318
- config_name: car_parts
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 661379
    num_examples: 2674
  - name: train
    num_bytes: 396653
    num_examples: 2674
  - name: validation
    num_bytes: 529016
    num_examples: 2674
  download_size: 39656
  dataset_size: 1587048
- config_name: fred_md
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 325107
    num_examples: 107
  - name: train
    num_bytes: 314514
    num_examples: 107
  - name: validation
    num_bytes: 319811
    num_examples: 107
  download_size: 169107
  dataset_size: 959432
- config_name: traffic_hourly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 62413326
    num_examples: 862
  - name: train
    num_bytes: 62071974
    num_examples: 862
  - name: validation
    num_bytes: 62242650
    num_examples: 862
  download_size: 22868806
  dataset_size: 186727950
- config_name: traffic_weekly
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 401046
    num_examples: 862
  - name: train
    num_bytes: 344154
    num_examples: 862
  - name: validation
    num_bytes: 372600
    num_examples: 862
  download_size: 245126
  dataset_size: 1117800
- config_name: hospital
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 293558
    num_examples: 767
  - name: train
    num_bytes: 217625
    num_examples: 767
  - name: validation
    num_bytes: 255591
    num_examples: 767
  download_size: 78110
  dataset_size: 766774
- config_name: covid_deaths
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 242187
    num_examples: 266
  - name: train
    num_bytes: 176352
    num_examples: 266
  - name: validation
    num_bytes: 209270
    num_examples: 266
  download_size: 27335
  dataset_size: 627809
- config_name: sunspot
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 304974
    num_examples: 1
  - name: train
    num_bytes: 304726
    num_examples: 1
  - name: validation
    num_bytes: 304850
    num_examples: 1
  download_size: 68865
  dataset_size: 914550
- config_name: saugeenday
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 97969
    num_examples: 1
  - name: train
    num_bytes: 97722
    num_examples: 1
  - name: validation
    num_bytes: 97845
    num_examples: 1
  download_size: 28721
  dataset_size: 293536
- config_name: us_births
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 30171
    num_examples: 1
  - name: train
    num_bytes: 29923
    num_examples: 1
  - name: validation
    num_bytes: 30047
    num_examples: 1
  download_size: 16332
  dataset_size: 90141
- config_name: solar_4_seconds
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 30513578
    num_examples: 1
  - name: train
    num_bytes: 30513083
    num_examples: 1
  - name: validation
    num_bytes: 30513331
    num_examples: 1
  download_size: 794502
  dataset_size: 91539992
- config_name: wind_4_seconds
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 30513269
    num_examples: 1
  - name: train
    num_bytes: 30512774
    num_examples: 1
  - name: validation
    num_bytes: 30513021
    num_examples: 1
  download_size: 2226184
  dataset_size: 91539064
- config_name: rideshare
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence:
      sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 5161435
    num_examples: 156
  - name: train
    num_bytes: 4249051
    num_examples: 156
  - name: validation
    num_bytes: 4705243
    num_examples: 156
  download_size: 1031826
  dataset_size: 14115729
- config_name: oikolab_weather
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 3302310
    num_examples: 8
  - name: train
    num_bytes: 3299142
    num_examples: 8
  - name: validation
    num_bytes: 3300726
    num_examples: 8
  download_size: 1326101
  dataset_size: 9902178
- config_name: temperature_rain
  features:
  - name: start
    dtype: timestamp[s]
  - name: target
    sequence:
      sequence: float32
  - name: feat_static_cat
    sequence: uint64
  - name: feat_dynamic_real
    sequence:
      sequence: float32
  - name: item_id
    dtype: string
  splits:
  - name: test
    num_bytes: 96059286
    num_examples: 422
  - name: train
    num_bytes: 88121466
    num_examples: 422
  - name: validation
    num_bytes: 92090376
    num_examples: 422
  download_size: 25747139
  dataset_size: 276271128
---

# Dataset Card for Monash Time Series Forecasting Repository

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contributions](#contributions)

## Dataset Description

- **Homepage:** [Monash Time Series Forecasting Repository](https://forecastingdata.org/)
- **Repository:** [Monash Time Series Forecasting Repository code repository](https://github.com/rakshitha123/TSForecasting)
- **Paper:** [Monash Time Series Forecasting Archive](https://openreview.net/pdf?id=wEc1mgAjU-)
- **Leaderboard:** [Baseline Results](https://forecastingdata.org/#results)
- **Point of Contact:** [Rakshitha Godahewa](mailto:rakshitha.godahewa@monash.edu)

### Dataset Summary

The first comprehensive time series forecasting repository containing datasets of related time series to facilitate the evaluation of global forecasting models. All datasets are intended to use only for research purpose. Our repository contains 30 datasets including both publicly available time series datasets (in different formats) and datasets curated by us. Many datasets have different versions based on the frequency and the inclusion of missing values, making the total number of dataset variations to 58. Furthermore, it includes both real-world and competition time series datasets covering varied domains.

The following table shows a list of datasets available:

| Name                          | Domain    | No. of series | Freq.  | Pred. Len. | Source                                                                                                                              |
|-------------------------------|-----------|---------------|--------|------------|-------------------------------------------------------------------------------------------------------------------------------------|
| weather                       | Nature    | 3010          | 1D     | 30         | [Sparks et al., 2020](https://cran.r-project.org/web/packages/bomrang)                                                              |
| tourism_yearly                | Tourism   | 1311          | 1Y     | 4          | [Athanasopoulos et al., 2011](https://doi.org/10.1016/j.ijforecast.2010.04.009)                                                     |
| tourism_quarterly             | Tourism   | 1311          | 1Q-JAN | 8          | [Athanasopoulos et al., 2011](https://doi.org/10.1016/j.ijforecast.2010.04.009)                                                     |
| tourism_monthly               | Tourism   | 1311          | 1M     | 24         | [Athanasopoulos et al., 2011](https://doi.org/10.1016/j.ijforecast.2010.04.009)                                                     |
| cif_2016                      | Banking   | 72            | 1M     | 12         | [Stepnicka and Burda, 2017](https://doi.org/10.1109/FUZZ-IEEE.2017.8015455)                                                         |
| london_smart_meters           | Energy    | 5560          | 30T    | 60         | [Jean-Michel, 2019](https://www.kaggle.com/jeanmidev/smart-meters-in-london)                                                        |
| australian_electricity_demand | Energy    | 5             | 30T    | 60         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU-)                                                                    |
| wind_farms_minutely           | Energy    | 339           | 1T     | 60         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )                                                                   |
| bitcoin                       | Economic  | 18            | 1D     | 30         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )                                                                   |
| pedestrian_counts             | Transport | 66            | 1H     | 48         | [City of Melbourne, 2020](https://data.melbourne.vic.gov.au/Transport/Pedestrian-Counting-System-Monthly-counts-per-hour/b2ak-trbp) |
| vehicle_trips                 | Transport | 329           | 1D     | 30         | [fivethirtyeight, 2015](https://github.com/fivethirtyeight/uber-tlc-foil-response)                                                  |
| kdd_cup_2018                  | Nature    | 270           | 1H     | 48         | [KDD Cup, 2018](https://www.kdd.org/kdd2018/kdd-cup)                                                                                |
| nn5_daily                     | Banking   | 111           | 1D     | 56         | [Ben Taieb et al., 2012](https://doi.org/10.1016/j.eswa.2012.01.039)                                                                |
| nn5_weekly                    | Banking   | 111           | 1W-MON | 8          | [Ben Taieb et al., 2012](https://doi.org/10.1016/j.eswa.2012.01.039)                                                                |
| kaggle_web_traffic            | Web       | 145063        | 1D     | 59         | [Google, 2017](https://www.kaggle.com/c/web-traffic-time-series-forecasting)                                                        |
| kaggle_web_traffic_weekly     | Web       | 145063        | 1W-WED | 8          | [Google, 2017](https://www.kaggle.com/c/web-traffic-time-series-forecasting)                                                        |
| solar_10_minutes              | Energy    | 137           | 10T    | 60         | [Solar, 2020](https://www.nrel.gov/grid/solar-power-data.html)                                                                      |
| solar_weekly                  | Energy    | 137           | 1W-SUN | 5          | [Solar, 2020](https://www.nrel.gov/grid/solar-power-data.html)                                                                      |
| car_parts                     | Sales     | 2674          | 1M     | 12         | [Hyndman, 2015](https://cran.r-project.org/web/packages/expsmooth/)                                                                 |
| fred_md                       | Economic  | 107           | 1M     | 12         | [McCracken and Ng, 2016](https://doi.org/10.1080/07350015.2015.1086655)                                                             |
| traffic_hourly                | Transport | 862           | 1H     | 48         | [Caltrans, 2020](http://pems.dot.ca.gov/)                                                                                           |
| traffic_weekly                | Transport | 862           | 1W-WED | 8          | [Caltrans, 2020](http://pems.dot.ca.gov/)                                                                                           |
| hospital                      | Health    | 767           | 1M     | 12         | [Hyndman, 2015](https://cran.r-project.org/web/packages/expsmooth/)                                                                 |
| covid_deaths                  | Health    | 266           | 1D     | 30         | [Johns Hopkins University, 2020](https://github.com/CSSEGISandData/COVID-19)                                                        |
| sunspot                       | Nature    | 1             | 1D     | 30         | [Sunspot, 2015](http://www.sidc.be/silso/newdataset)                                                                                |
| saugeenday                    | Nature    | 1             | 1D     | 30         | [McLeod and Gweon, 2013](http://www.jenvstat.org/v04/i11)                                                                           |
| us_births                     | Health    | 1             | 1D     | 30         | [Pruim et al., 2020](https://cran.r-project.org/web/packages/mosaicData)                                                            |
| solar_4_seconds               | Energy    | 1             | 4S     | 60         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )                                                                   |
| wind_4_seconds                | Energy    | 1             | 4S     | 60         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )                                                                   |
| rideshare                     | Transport | 2304          | 1H     | 48         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )                                                                   |
| oikolab_weather               | Nature    | 8             | 1H     | 48         | [Oikolab](https://oikolab.com/)                                                                                                     |
| temperature_rain              | Nature    | 32072         | 1D     | 30         | [Godahewa et al. 2021](https://openreview.net/pdf?id=wEc1mgAjU- )      


### Dataset Usage

To load a particular dataset just specify its name from the table above e.g.:

```python
load_dataset("monash_tsf", "nn5_daily")
```
> Notes:
> - Data might contain missing values as in the original datasets.
> - The prediction length is either specified in the dataset or a default value depending on the frequency is used as in the original repository benchmark.


### Supported Tasks and Leaderboards

#### `time-series-forecasting`

##### `univariate-time-series-forecasting`

The univariate time series forecasting tasks involves learning the future one dimensional `target` values of a time series in a dataset for some `prediction_length` time steps. The performance of the forecast models can then be validated via the ground truth in the `validation` split and tested via the `test` split.

##### `multivariate-time-series-forecasting`

The multivariate time series forecasting task involves learning the future vector of `target` values of a time series in a dataset for some `prediction_length` time steps. Similar to the univariate setting the performance of a multivariate model can be validated via the ground truth in the `validation` split and tested via the `test` split.

### Languages

## Dataset Structure

### Data Instances

A sample from the training set is provided below:

```python
{
  'start': datetime.datetime(2012, 1, 1, 0, 0),
  'target': [14.0, 18.0, 21.0, 20.0, 22.0, 20.0, ...],
  'feat_static_cat': [0], 
  'feat_dynamic_real': [[0.3, 0.4], [0.1, 0.6], ...],
  'item_id': '0'
}
```

### Data Fields

For the univariate regular time series each series has the following keys:

* `start`: a datetime of the first entry of each time series in the dataset
* `target`: an array[float32] of the actual target values
* `feat_static_cat`: an array[uint64] which contains a categorical identifier of each time series in the dataset
* `feat_dynamic_real`: optional array of covariate features
* `item_id`: a string identifier of each time series in a dataset for reference

For the multivariate time series the `target` is a vector of the multivariate dimension for each time point.

### Data Splits

The datasets are split in time depending on the prediction length specified in the datasets. In particular for each time series in a dataset there is a prediction length window of the future in the validation split and another prediction length more in the test split.


## Dataset Creation

### Curation Rationale

To facilitate the evaluation of global forecasting models. All datasets in our repository are intended for research purposes and to evaluate the performance of new forecasting algorithms.

### Source Data

#### Initial Data Collection and Normalization

Out of the 30 datasets, 23 were already publicly available in different platforms with different data formats. The original sources of all datasets are mentioned in the datasets table above.

After extracting and curating these datasets, we analysed them individually to identify the datasets containing series with different frequencies and missing observations. Nine datasets contain time series belonging to different frequencies and the archive contains a separate dataset per each frequency.

#### Who are the source language producers?

The data comes from the datasets listed in the table above.

### Annotations

#### Annotation process

The annotations come from the datasets listed in the table above.

#### Who are the annotators?

[More Information Needed]

### Personal and Sensitive Information

[More Information Needed]

## Considerations for Using the Data

### Social Impact of Dataset

[More Information Needed]

### Discussion of Biases

[More Information Needed]

### Other Known Limitations

[More Information Needed]

## Additional Information

### Dataset Curators

* [Rakshitha Godahewa](mailto:rakshitha.godahewa@monash.edu)
* [Christoph Bergmeir](mailto:christoph.bergmeir@monash.edu)
* [Geoff Webb](mailto:geoff.webb@monash.edu)
* [Rob Hyndman](mailto:rob.hyndman@monash.edu)
* [Pablo Montero-Manso](mailto:pablo.monteromanso@sydney.edu.au)

### Licensing Information

[Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/legalcode)

### Citation Information

```tex
@InProceedings{godahewa2021monash,
    author = "Godahewa, Rakshitha and Bergmeir, Christoph and Webb, Geoffrey I. and Hyndman, Rob J. and Montero-Manso, Pablo",
    title = "Monash Time Series Forecasting Archive",
    booktitle = "Neural Information Processing Systems Track on Datasets and Benchmarks",
    year = "2021",
    note = "forthcoming"
}
```

### Contributions

Thanks to [@kashif](https://github.com/kashif) for adding this dataset.