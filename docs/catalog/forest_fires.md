<div itemscope itemtype="http://schema.org/Dataset">
  <div itemscope itemprop="includedInDataCatalog" itemtype="http://schema.org/DataCatalog">
    <meta itemprop="name" content="TensorFlow Datasets" />
  </div>
  <meta itemprop="name" content="forest_fires" />
  <meta itemprop="description" content="&#10;&#10;This is a regression task, where the aim is to predict the burned area of&#10;forest fires, in the northeast region of Portugal,&#10;by using meteorological and other data.&#10;&#10;&#10;Data Set Information:&#10;&#10;In [Cortez and Morais, 2007], the output &#x27;area&#x27; was first transformed&#10;with a ln(x+1) function.&#10;Then, several Data Mining methods were applied. After fitting the models,&#10;the outputs were&#10;post-processed with the inverse of the ln(x+1) transform. Four different&#10;input setups were&#10;used. The experiments were conducted using a 10-fold (cross-validation)&#10;x 30 runs. Two&#10;regression metrics were measured: MAD and RMSE. A Gaussian support vector&#10;machine (SVM) fed&#10;with only 4 direct weather conditions (temp, RH, wind and rain) obtained&#10;the best MAD value:&#10;12.71 +- 0.01 (mean and confidence interval within 95% using a t-student&#10;distribution). The&#10;best RMSE was attained by the naive mean predictor. An analysis to the&#10;regression error curve&#10;(REC) shows that the SVM model predicts more examples within a lower&#10;admitted error. In effect,&#10;the SVM model predicts better small fires, which are the majority.&#10;&#10;Attribute Information:&#10;&#10;For more information, read [Cortez and Morais, 2007].&#10;&#10;1. X - x-axis spatial coordinate within the Montesinho park map: 1 to 9&#10;2. Y - y-axis spatial coordinate within the Montesinho park map: 2 to 9&#10;3. month - month of the year: &#x27;jan&#x27; to &#x27;dec&#x27;&#10;4. day - day of the week: &#x27;mon&#x27; to &#x27;sun&#x27;&#10;5. FFMC - FFMC index from the FWI system: 18.7 to 96.20&#10;6. DMC - DMC index from the FWI system: 1.1 to 291.3&#10;7. DC - DC index from the FWI system: 7.9 to 860.6&#10;8. ISI - ISI index from the FWI system: 0.0 to 56.10&#10;9. temp - temperature in Celsius degrees: 2.2 to 33.30&#10;10. RH - relative humidity in %: 15.0 to 100&#10;11. wind - wind speed in km/h: 0.40 to 9.40&#10;12. rain - outside rain in mm/m2 : 0.0 to 6.4&#10;13. area - the burned area of the forest (in ha): 0.00 to 1090.84&#10;(this output variable is very skewed towards 0.0, thus it may make&#10;sense to model with the logarithm transform).&#10;&#10;&#10;&#10;To use this dataset:&#10;&#10;```python&#10;import tensorflow_datasets as tfds&#10;&#10;ds = tfds.load(&#x27;forest_fires&#x27;, split=&#x27;train&#x27;)&#10;for ex in ds.take(4):&#10;  print(ex)&#10;```&#10;&#10;See [the guide](https://www.tensorflow.org/datasets/overview) for more&#10;informations on [tensorflow_datasets](https://www.tensorflow.org/datasets).&#10;&#10;" />
  <meta itemprop="url" content="https://www.tensorflow.org/datasets/catalog/forest_fires" />
  <meta itemprop="sameAs" content="https://archive.ics.uci.edu/ml/datasets/Forest+Fires" />
  <meta itemprop="citation" content="&#10;@misc{Dua:2019 ,&#10;author = &quot;Dua, Dheeru and Graff, Casey&quot;,&#10;year = &quot;2017&quot;,&#10;title = &quot;{UCI} Machine Learning Repository&quot;,&#10;url = &quot;http://archive.ics.uci.edu/ml&quot;,&#10;institution = &quot;University of California, Irvine, School of Information and Computer Sciences&quot; }&#10;&#10;@article{cortez2007data,&#10;  title={A data mining approach to predict forest fires using meteorological data},&#10;  author={Cortez, Paulo and Morais, Anibal de Jesus Raimundo},&#10;  year={2007},&#10;  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}&#10;}&#10;" />
</div>
# `forest_fires`

*   **Description**:

This is a regression task, where the aim is to predict the burned area of forest
fires, in the northeast region of Portugal, by using meteorological and other
data.

Data Set Information:

In [Cortez and Morais, 2007], the output 'area' was first transformed with a
ln(x+1) function. Then, several Data Mining methods were applied. After fitting
the models, the outputs were post-processed with the inverse of the ln(x+1)
transform. Four different input setups were used. The experiments were conducted
using a 10-fold (cross-validation) x 30 runs. Two regression metrics were
measured: MAD and RMSE. A Gaussian support vector machine (SVM) fed with only 4
direct weather conditions (temp, RH, wind and rain) obtained the best MAD value:
12.71 +- 0.01 (mean and confidence interval within 95% using a t-student
distribution). The best RMSE was attained by the naive mean predictor. An
analysis to the regression error curve (REC) shows that the SVM model predicts
more examples within a lower admitted error. In effect, the SVM model predicts
better small fires, which are the majority.

Attribute Information:

For more information, read [Cortez and Morais, 2007].

1.  X - x-axis spatial coordinate within the Montesinho park map: 1 to 9
2.  Y - y-axis spatial coordinate within the Montesinho park map: 2 to 9
3.  month - month of the year: 'jan' to 'dec'
4.  day - day of the week: 'mon' to 'sun'
5.  FFMC - FFMC index from the FWI system: 18.7 to 96.20
6.  DMC - DMC index from the FWI system: 1.1 to 291.3
7.  DC - DC index from the FWI system: 7.9 to 860.6
8.  ISI - ISI index from the FWI system: 0.0 to 56.10
9.  temp - temperature in Celsius degrees: 2.2 to 33.30
10. RH - relative humidity in %: 15.0 to 100
11. wind - wind speed in km/h: 0.40 to 9.40
12. rain - outside rain in mm/m2 : 0.0 to 6.4
13. area - the burned area of the forest (in ha): 0.00 to 1090.84 (this output
    variable is very skewed towards 0.0, thus it may make sense to model with
    the logarithm transform).

*   **Homepage**:
    [https://archive.ics.uci.edu/ml/datasets/Forest+Fires](https://archive.ics.uci.edu/ml/datasets/Forest+Fires)
*   **Source code**:
    [`tfds.structured.forest_fires.ForestFires`](https://github.com/tensorflow/datasets/tree/master/tensorflow_datasets/structured/forest_fires.py)
*   **Versions**:
    *   **`0.0.1`** (default): No release notes.
*   **Download size**: `24.88 KiB`
*   **Dataset size**: `162.07 KiB`
*   **Auto-cached**
    ([documentation](https://www.tensorflow.org/datasets/performances#auto-caching)):
    Yes
*   **Splits**:

Split   | Examples
:------ | -------:
'train' | 517

*   **Features**:

```python
FeaturesDict({
    'area': tf.float32,
    'features': FeaturesDict({
        'DC': tf.float32,
        'DMC': tf.float32,
        'FFMC': tf.float32,
        'ISI': tf.float32,
        'RH': tf.float32,
        'X': tf.uint8,
        'Y': tf.uint8,
        'day': ClassLabel(shape=(), dtype=tf.int64, num_classes=7),
        'month': ClassLabel(shape=(), dtype=tf.int64, num_classes=12),
        'rain': tf.float32,
        'temp': tf.float32,
        'wind': tf.float32,
    }),
})
```
*   **Supervised keys** (See
    [`as_supervised` doc](https://www.tensorflow.org/datasets/api_docs/python/tfds/load#args)):
    `('area', 'features')`
*   **Citation**:

```
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences" }

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, Anibal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
```
