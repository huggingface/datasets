<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/huggingface/datasets/master/docs/source/imgs/datasets_logo_name.jpg" width="400"/>
    <br>
<p>
<p align="center">
    <a href="https://circleci.com/gh/huggingface/datasets">
        <img alt="Build" src="https://img.shields.io/circleci/build/github/huggingface/datasets/master">
    </a>
    <a href="https://github.com/huggingface/datasets/blob/master/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/huggingface/datasets.svg?color=blue">
    </a>
    <a href="https://huggingface.co/docs/datasets/index.html">
        <img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/datasets/index.html.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/huggingface/datasets/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/datasets.svg">
    </a>
    <a href="https://huggingface.co/datasets/">
        <img alt="Number of datasets" src="https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen">
    </a>
</p>

`🤗Datasets` is a lightweight library providing two main features:

- **ready-to-use dataloaders** for ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) major public datasets in 467 languages and dialects. With one line (`squad_dataset = load_datasets("squad")`) download and pre-process any of these public or private datasets to have it ready to use for training/evaluating a ML model (Numpy/Pandas/PyTorch/TensorFlow/JAX), and
- **an efficient dataset class** for simple, fast and reproducible data pre-processing optimized for ML model evaluation and training (see more below).

[🎓 **Documentation**](https://huggingface.co/docs/datasets/) [🕹 **Colab demo**](https://colab.research.google.com/github/huggingface/datasets/blob/master/notebooks/Overview.ipynb) [🔎 **Online dataset explorer**](https://huggingface.co/datasets/viewer)

`🤗Datasets` has many interesting features (beside easy sharing and accessing datasets/metrics):

- Built-in interoperability with NumPy, pandas, PyTorch, Tensorflow 2 and JAX.
- Lightweight and fast with a transparent and pythonic API (multi-processing/caching/memory-mapping).
- Thrive on large datasets: `🤗Datasets` naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive using an efficient zero-serialization cost backend (Apache Arrow).
- Smart caching: never wait for your data to process several times.

`🤗Datasets` also provides access to +15 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics. You can browse the full set of datasets with the [live datasets viewer](https://huggingface.co/datasets/viewer).

`🤗Datasets` originated from a fork of the awesome [`TensorFlow Datasets`](https://github.com/tensorflow/datasets) and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between `🤗Datasets` and `tfds` can be found in the section [Main differences between `🤗Datasets` and `tfds`](#main-differences-between-datasets-and-tfds).

# Installation

`🤗Datasets` can be installed from PyPi and has to be installed in a virtual environment (venv or conda for instance)

```bash
pip install datasets
```

For more details on installation, check the installation page in the documentation: https://huggingface.co/docs/datasets/installation.html

## Using with PyTorch/TensorFlow/pandas

If you plan to use `🤗Datasets` with PyTorch (1.0+), TensorFlow (2.2+) or pandas, you should also install PyTorch, TensorFlow or pandas.

For more details on using the library with NumPy, pandas, PyTorch or TensorFlow, check the quick tour page in the documentation: https://huggingface.co/docs/datasets/quicktour.html

# Usage

`🤗Datasets` is made to be very simple to use. The main methods are:

- `datasets.list_datasets()` to list the available datasets
- `datasets.load_dataset(dataset_name, **kwargs)` to instantiate a dataset
- `datasets.list_metrics()` to list the available metrics
- `datasets.load_metric(metric_name, **kwargs)` to instantiate a metric

Here is a quick example:

```python
from datasets import list_datasets, load_dataset, list_metrics, load_metric

# Print all the available datasets
print(list_datasets())

# Load a dataset and print the first examples in the training set
squad_dataset = load_dataset('squad')
print(squad_dataset['train'][0])

# List all the available metrics
print(list_metrics())

# Load a metric
squad_metric = load_metric('squad')
```

For more details on using the library, check the quick tour page in the documentation: https://huggingface.co/docs/datasets/quicktour.html and the specific pages on

- Loading a dataset https://huggingface.co/docs/datasets/loading_datasets.html
- What's in a Dataset: https://huggingface.co/docs/datasets/exploring.html
- Processing data with `🤗Datasets`: https://huggingface.co/docs/datasets/processing.html
- Writing your own dataset loading script: https://huggingface.co/docs/datasets/add_dataset.html
- etc

Another introduction to `🤗Datasets` is the tutorial on Google Colab here:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/huggingface/datasets/blob/master/notebooks/Overview.ipynb)

# Main differences between `🤗Datasets` and `tfds`

If you are familiar with the great `Tensorflow Datasets`, here are the main differences between `🤗Datasets` and `tfds`:
- the scripts in `🤗Datasets` are not provided within the library but are queried, downloaded/cached and dynamically loaded upon request
- `🤗Datasets` also provides evaluation metrics in a similar fashion to the datasets, i.e. as dynamically installed scripts with a unified API. This gives access to the pair of a benchmark dataset and a benchmark metric for instance for benchmarks like [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) or [GLUE](https://gluebenchmark.com/).
- the backend serialization of `🤗Datasets` is based on [Apache Arrow](https://arrow.apache.org/) instead of TF Records and leverage python dataclasses for info and features with some diverging features (we mostly don't do encoding and store the raw data as much as possible in the backend serialization cache).
- the user-facing dataset object of `🤗Datasets` is not a `tf.data.Dataset` but a built-in framework-agnostic dataset class with methods inspired by what we like in `tf.data` (like a `map()` method). It basically wraps a memory-mapped Arrow table cache.

# Disclaimers

Similar to `TensorFlow Datasets`, `🤗Datasets` is a utility library that downloads and prepares public datasets. We do not host or distribute these datasets, vouch for their quality or fairness, or claim that you have license to use them. It is your responsibility to determine whether you have permission to use the dataset under the dataset's license.

If you're a dataset owner and wish to update any part of it (description, citation, etc.), or do not want your dataset to be included in this library, please get in touch through a [GitHub issue](https://github.com/huggingface/datasets/issues/new). Thanks for your contribution to the ML community!
