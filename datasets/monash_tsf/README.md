---
annotations_creators:
- no-annotation
language_creators:
- found
languages:
- unknown
licenses:
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
