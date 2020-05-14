<p align="center">
    <br>
    <img src="https://raw.githubusercontent.com/huggingface/transformers/master/docs/source/imgs/nlp_logo_name.png" width="400"/>
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
<p> Datasets and Metrics for Natural Language Processing in NumPy, Pandas, PyTorch and TensorFlow 2.0
</h3>

🤗 `nlp` is a lightweight and extensible library to easily share and access datasets and evaluation metrics for Natural Language Processing (NLP).

`nlp` has many interesting features (beside easy share and access to datasets/metrics):

- Build-in interoperability with Numpy, Pandas, PyTorch and Tensorflow 2
- A small and fast library with a transparent and pythonic API
- Strive on large datasets: `nlp` naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive by default.
- Smart caching with an intelligent tf.data-like cache: never wait for your data to process several times

`nlp` currently provides access to ~100 NLP datasets and ~10 metrics and let the community very easily add new datasets and metrics.

`nlp` originated from a fork of the awesome [`TensorFlow Datasets`](https://github.com/tensorflow/datasets) and the HuggingFace team want to deeply thank the TensorFlow Datasets team behind this amazing library and user API.

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

If you plan to use `nlp` with PyTorch (1.0+), TensorFlow (2.2+) or pandas, you should also install the relevant framework.

# Usage

Using `nlp` is rather simple, the main methods are:

- `nlp.list_datasets()`
- `nlp.load_dataset(dataset_name, **kwargs)`
- `nlp.list_metrics()`
- `nlp.load_metric(metric_name, **kwargs)`

Here is a quick example:

```python
import nlp

# List all the available datasets
print(dataset.id for dataset in nlp.list_datasets())

# Load a dataset and print the first examples in the training set
squad_dataset = nlp.load_dataset('squad')
print(squad_dataset['train'][0])

# List all the available metrics
print(metric.id for metric in nlp.list_metrics())

# Load a metric
squad_metric = nlp.load_metric('squad')
```

Now the best introduction to `nlp` is to follow the tutorial in Google Colab which is here:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/huggingface/nlp/blob/master/notebooks/Overview.ipynb)
