<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/huggingface/nlp/master/docs/source/imgs/nlp_logo_name.png" width="400"/>
    <br>
<p>
<p align="center">
    <a href="https://circleci.com/gh/huggingface/nlp">
        <img alt="Build" src="https://img.shields.io/circleci/build/github/huggingface/nlp/master">
    </a>
    <a href="https://github.com/huggingface/nlp/blob/master/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/huggingface/nlp.svg?color=blue">
    </a>
    <!-- <a href="https://huggingface.co/nlp/index.html">
        <img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/nlp/index.html.svg?down_color=red&down_message=offline&up_message=online">
    </a> -->
    <a href="https://github.com/huggingface/nlp/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/nlp.svg">
    </a>
</p>

<h3 align="center">
<p> Datasets and evaluation metrics for natural language processing
<p> in NumPy, Pandas, PyTorch and TensorFlow
</h3>

🤗 `nlp` is a lightweight and extensible library to easily share and access datasets and evaluation metrics for Natural Language Processing (NLP).

`nlp` has many interesting features (beside easy sharing and accessing datasets/metrics):

- Build-in interoperability with Numpy, Pandas, PyTorch and Tensorflow 2
- Lightweight and fast with a transparent and pythonic API
- Strive on large datasets: `nlp` naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive by default.
- Smart caching: never wait for your data to process several times

`nlp` currently provides access to ~100 NLP datasets and ~10 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics.

`nlp` originated from a fork of the awesome [`TensorFlow Datasets`](https://github.com/tensorflow/datasets) and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between `nlp` and `tfds` can be found in the section [Main differences between `nlp` and `tfds`](#main-differences-between-nlp-and-tfds).

# Contributors

[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/0)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/0)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/1)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/1)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/2)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/2)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/3)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/3)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/4)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/4)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/5)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/5)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/6)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/6)[![](https://sourcerer.io/fame/clmnt/huggingface/nlp/images/7)](https://sourcerer.io/fame/clmnt/huggingface/nlp/links/7)

# Installation

## From PyPI

`nlp` can be installed from PyPi and has to be installed in a virtual environment (venv or conda for instance)

```bash
pip install nlp
```

## From source

You can also install `nlp` from source:
```bash
git clone https://github.com/huggingface/nlp
cd nlp
pip install .
```

When you update the repository, you should upgrade the nlp installation and its dependencies as follows:

```bash
git pull
pip install --upgrade .
```

## Using with PyTorch/TensorFlow/pandas

If you plan to use `nlp` with PyTorch (1.0+), TensorFlow (2.2+) or pandas, you should also install PyTorch, Tensorflow or pandas.

# Usage

Using `nlp` is made to be very simple to use, the main methods are:

- `nlp.list_datasets()` to list the available datasets
- `nlp.load_dataset(dataset_name, **kwargs)` to instantiate a dataset
- `nlp.list_metrics()` to list the available metrics
- `nlp.load_metric(metric_name, **kwargs)` to instantiate a metric

Here is a quick example:

```python
import nlp

# Print all the available datasets
print([dataset.id for dataset in nlp.list_datasets()])

# Load a dataset and print the first examples in the training set
squad_dataset = nlp.load_dataset('squad')
print(squad_dataset['train'][0])

# List all the available metrics
print([metric.id for metric in nlp.list_metrics()])

# Load a metric
squad_metric = nlp.load_metric('squad')
```

Now the best introduction to `nlp` is to follow the tutorial in Google Colab which is here:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/huggingface/nlp/blob/master/notebooks/Overview.ipynb)

# Main differences between `nlp` and `tfds`

If you are familiar with the great `Tensorflow Datasets`, here are the main differences between `nlp` and `tfds`:
- the scripts in `nlp` are not provided within the library but are queried, downloaded/cached and dynamically loaded upon request
- `nlp` also provides evaluation metrics in a similar fashion to the datasets, i.e. as dynamically installed scripts with a unified API. This gives access to the pair of a benchmark dataset and a benchmark metric for instance for benchmarks like SQuAD or GLUE.
- the backend serialization of `nlp` is based on Apache Arrow/Parquet instead of TF Records and leverage python dataclasses for info and features with some diverging features (we mostly don't do encoding and store the raw data as much as possible in the backend serialization cache)
- the user-facing dataset object of `nlp` is not a `tf.data.Dataset` but a built-in framework-agnostic dataset class with methods inspired by what we like in tf.data (like a map() method). It basically wraps a memory-mapped Arrow table cache.

# Disclaimers

Similarly to Tensorflow Dataset, `nlp` is a utility library that downloads and prepares public datasets. We do not host or distribute these datasets, vouch for their quality or fairness, or claim that you have license to use the dataset. It is your responsibility to determine whether you have permission to use the dataset under the dataset's license.

If you're a dataset owner and wish to update any part of it (description, citation, etc.), or do not want your dataset to be included in this library, please get in touch through a GitHub issue. Thanks for your contribution to the ML community!

If you're interested in learning more about responsible AI practices, including fairness, please see Google AI's Responsible AI Practices.

