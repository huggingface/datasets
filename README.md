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
    <a href="CODE_OF_CONDUCT.md">
        <img alt="Contributor Covenant" src="https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg">
    </a>
    <a href="https://zenodo.org/badge/latestdoi/250213286"><img src="https://zenodo.org/badge/250213286.svg" alt="DOI"></a>
</p>

🤗 Datasets is a lightweight library providing **two** main features:

- **one-line dataloaders for many public datasets**: one-liners to download and pre-process any of the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) major public datasets (in 467 languages and dialects!) provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets). With a simple command like `squad_dataset = load_dataset("squad")`, get any of these datasets ready to use in a dataloader for training/evaluating a ML model (Numpy/Pandas/PyTorch/TensorFlow/JAX),
- **efficient data pre-processing**: simple, fast and reproducible data pre-processing for the above public datasets as well as your own local datasets in CSV/JSON/text. With simple commands like `tokenized_dataset = dataset.map(tokenize_example)`, efficiently prepare the dataset for inspection and ML model evaluation and training.

[🎓 **Documentation**](https://huggingface.co/docs/datasets/) [🕹 **Colab tutorial**](https://colab.research.google.com/github/huggingface/datasets/blob/master/notebooks/Overview.ipynb)

[🔎 **Find a dataset in the Hub**](https://huggingface.co/datasets) [🌟 **Add a new dataset to the Hub**](https://github.com/huggingface/datasets/blob/master/ADD_NEW_DATASET.md)

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://raw.githubusercontent.com/huggingface/datasets/master/docs/source/imgs/course_banner.png"></a>
</h3>

🤗 Datasets also provides access to +15 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics. 

🤗 Datasets has many additional interesting features:
- Thrive on large datasets: 🤗 Datasets naturally frees the user from RAM memory limitation, all datasets are memory-mapped using an efficient zero-serialization cost backend (Apache Arrow).
- Smart caching: never wait for your data to process several times.
- Lightweight and fast with a transparent and pythonic API (multi-processing/caching/memory-mapping).
- Built-in interoperability with NumPy, pandas, PyTorch, Tensorflow 2 and JAX.

🤗 Datasets originated from a fork of the awesome [TensorFlow Datasets](https://github.com/tensorflow/datasets) and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between 🤗 Datasets and `tfds` can be found in the section [Main differences between 🤗 Datasets and `tfds`](#main-differences-between--datasets-and-tfds).

# Installation

## With pip

🤗 Datasets can be installed from PyPi and has to be installed in a virtual environment (venv or conda for instance)

```bash
pip install datasets
```

## With conda

🤗 Datasets can be installed using conda as follows:

```bash
conda install -c huggingface -c conda-forge datasets
```

Follow the installation pages of TensorFlow and PyTorch to see how to install them with conda.

For more details on installation, check the installation page in the documentation: https://huggingface.co/docs/datasets/installation.html

## Installation to use with PyTorch/TensorFlow/pandas

If you plan to use 🤗 Datasets with PyTorch (1.0+), TensorFlow (2.2+) or pandas, you should also install PyTorch, TensorFlow or pandas.

For more details on using the library with NumPy, pandas, PyTorch or TensorFlow, check the quick start page in the documentation: https://huggingface.co/docs/datasets/quickstart.html

# Usage

🤗 Datasets is made to be very simple to use. The main methods are:

- `datasets.list_datasets()` to list the available datasets
- `datasets.load_dataset(dataset_name, **kwargs)` to instantiate a dataset
- `datasets.list_metrics()` to list the available metrics
- `datasets.load_metric(metric_name, **kwargs)` to instantiate a metric

Here is a quick example:

```python
from datasets import list_datasets, load_dataset, list_metrics, load_metric

# Print all the available datasets
print(list_datasets())

# Load a dataset and print the first example in the training set
squad_dataset = load_dataset('squad')
print(squad_dataset['train'][0])

# List all the available metrics
print(list_metrics())

# Load a metric
squad_metric = load_metric('squad')

# Process the dataset - add a column with the length of the context texts
dataset_with_length = squad_dataset.map(lambda x: {"length": len(x["context"])})

# Process the dataset - tokenize the context texts (using a tokenizer from the 🤗 Transformers library)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

tokenized_dataset = squad_dataset.map(lambda x: tokenizer(x['context']), batched=True)
```

For more details on using the library, check the quick start page in the documentation: https://huggingface.co/docs/datasets/quickstart.html and the specific pages on:

- Loading a dataset https://huggingface.co/docs/datasets/loading.html
- What's in a Dataset: https://huggingface.co/docs/datasets/access.html
- Processing data with 🤗 Datasets: https://huggingface.co/docs/datasets/process.html
- Writing your own dataset loading script: https://huggingface.co/docs/datasets/dataset_script.html
- etc.

Another introduction to 🤗 Datasets is the tutorial on Google Colab here:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/huggingface/datasets/blob/master/notebooks/Overview.ipynb)

# Add a new dataset to the Hub

We have a very detailed step-by-step guide to add a new dataset to the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) datasets already provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets).

You will find [the step-by-step guide here](https://github.com/huggingface/datasets/blob/master/ADD_NEW_DATASET.md) to add a dataset to this repository.

You can also have your own repository for your dataset on the Hub under your or your organization's namespace and share it with the community. More information in [the documentation section about dataset sharing](https://huggingface.co/docs/datasets/share.html).

# Main differences between 🤗 Datasets and `tfds`

If you are familiar with the great TensorFlow Datasets, here are the main differences between 🤗 Datasets and `tfds`:
- the scripts in 🤗 Datasets are not provided within the library but are queried, downloaded/cached and dynamically loaded upon request
- 🤗 Datasets also provides evaluation metrics in a similar fashion to the datasets, i.e. as dynamically installed scripts with a unified API. This gives access to the pair of a benchmark dataset and a benchmark metric for instance for benchmarks like [SQuAD](https://rajpurkar.github.io/SQuAD-explorer/) or [GLUE](https://gluebenchmark.com/).
- the backend serialization of 🤗 Datasets is based on [Apache Arrow](https://arrow.apache.org/) instead of TF Records and leverage python dataclasses for info and features with some diverging features (we mostly don't do encoding and store the raw data as much as possible in the backend serialization cache).
- the user-facing dataset object of 🤗 Datasets is not a `tf.data.Dataset` but a built-in framework-agnostic dataset class with methods inspired by what we like in `tf.data` (like a `map()` method). It basically wraps a memory-mapped Arrow table cache.

# Disclaimers

Similar to TensorFlow Datasets, 🤗 Datasets is a utility library that downloads and prepares public datasets. We do not host or distribute these datasets, vouch for their quality or fairness, or claim that you have license to use them. It is your responsibility to determine whether you have permission to use the dataset under the dataset's license.

If you're a dataset owner and wish to update any part of it (description, citation, etc.), or do not want your dataset to be included in this library, please get in touch through a [GitHub issue](https://github.com/huggingface/datasets/issues/new). Thanks for your contribution to the ML community!

## BibTeX
If you want to cite our 🤗 Datasets [paper](https://arxiv.org/abs/2109.02846) and library, you can use these:

```bibtex
@inproceedings{lhoest-etal-2021-datasets,
    title = "Datasets: A Community Library for Natural Language Processing",
    author = "Lhoest, Quentin  and
      Villanova del Moral, Albert  and
      Jernite, Yacine  and
      Thakur, Abhishek  and
      von Platen, Patrick  and
      Patil, Suraj  and
      Chaumond, Julien  and
      Drame, Mariama  and
      Plu, Julien  and
      Tunstall, Lewis  and
      Davison, Joe  and
      {\v{S}}a{\v{s}}ko, Mario  and
      Chhablani, Gunjan  and
      Malik, Bhavitvya  and
      Brandeis, Simon  and
      Le Scao, Teven  and
      Sanh, Victor  and
      Xu, Canwen  and
      Patry, Nicolas  and
      McMillan-Major, Angelina  and
      Schmid, Philipp  and
      Gugger, Sylvain  and
      Delangue, Cl{\'e}ment  and
      Matussi{\`e}re, Th{\'e}o  and
      Debut, Lysandre  and
      Bekman, Stas  and
      Cistac, Pierric  and
      Goehringer, Thibault  and
      Mustar, Victor  and
      Lagunas, Fran{\c{c}}ois  and
      Rush, Alexander  and
      Wolf, Thomas",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing: System Demonstrations",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-demo.21",
    pages = "175--184",
    abstract = "The scale, variety, and quantity of publicly-available NLP datasets has grown rapidly as researchers propose new tasks, larger models, and novel benchmarks. Datasets is a community library for contemporary NLP designed to support this ecosystem. Datasets aims to standardize end-user interfaces, versioning, and documentation, while providing a lightweight front-end that behaves similarly for small datasets as for internet-scale corpora. The design of the library incorporates a distributed, community-driven approach to adding datasets and documenting usage. After a year of development, the library now includes more than 650 unique datasets, has more than 250 contributors, and has helped support a variety of novel cross-dataset research projects and shared tasks. The library is available at https://github.com/huggingface/datasets.",
    eprint={2109.02846},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
}
```
```bibtex
@software{quentin_lhoest_2021_5639822,
  author       = {Quentin Lhoest and
                  Albert Villanova del Moral and
                  Patrick von Platen and
                  Thomas Wolf and
                  Mario Šaško and
                  Yacine Jernite and
                  Abhishek Thakur and
                  Lewis Tunstall and
                  Suraj Patil and
                  Mariama Drame and
                  Julien Chaumond and
                  Julien Plu and
                  Joe Davison and
                  Simon Brandeis and
                  Victor Sanh and
                  Teven Le Scao and
                  Kevin Canwen Xu and
                  Nicolas Patry and
                  Steven Liu and
                  Angelina McMillan-Major and
                  Philipp Schmid and
                  Sylvain Gugger and
                  Nathan Raw and
                  Sylvain Lesage and
                  Anton Lozhkov and
                  Matthew Carrigan and
                  Théo Matussière and
                  Leandro von Werra and
                  Lysandre Debut and
                  Stas Bekman and
                  Clément Delangue},
  title        = {huggingface/datasets: 1.15.1},
  month        = nov,
  year         = 2021,
  publisher    = {Zenodo},
  version      = {1.15.1},
  doi          = {10.5281/zenodo.5639822},
  url          = {https://doi.org/10.5281/zenodo.5639822}
}
```
