<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-light.svg">
    <img alt="Hugging Face Datasets Library" src="https://huggingface.co/datasets/huggingface/documentation-images/raw/main/datasets-logo-light.svg" width="352" height="59" style="max-width: 100%;">
  </picture>
  <br/>
  <br/>
</p>

<p align="center">
    <a href="https://github.com/huggingface/datasets/actions/workflows/ci.yml?query=branch%3Amain"><img alt="Build" src="https://github.com/huggingface/datasets/actions/workflows/ci.yml/badge.svg?branch=main"></a>
    <a href="https://github.com/huggingface/datasets/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/huggingface/datasets.svg?color=blue"></a>
    <a href="https://huggingface.co/docs/datasets/index.html"><img alt="Documentation" src="https://img.shields.io/website/http/huggingface.co/docs/datasets/index.html.svg?down_color=red&down_message=offline&up_message=online"></a>
    <a href="https://github.com/huggingface/datasets/releases"><img alt="GitHub release" src="https://img.shields.io/github/release/huggingface/datasets.svg"></a>
    <a href="https://huggingface.co/datasets/"><img alt="Number of datasets" src="https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen"></a>
    <a href="CODE_OF_CONDUCT.md"><img alt="Contributor Covenant" src="https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg"></a>
    <a href="https://zenodo.org/badge/latestdoi/250213286"><img src="https://zenodo.org/badge/250213286.svg" alt="DOI"></a>
</p>

🤗 Datasets is a lightweight library providing **two** main features:

- **one-line dataloaders for many public datasets**: one-liners to download and pre-process any of the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) major public datasets (image datasets, audio datasets, text datasets in 467 languages and dialects, etc.) provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets). With a simple command like `squad_dataset = load_dataset("rajpurkar/squad")`, get any of these datasets ready to use in a dataloader for training/evaluating a ML model (Numpy/Pandas/PyTorch/TensorFlow/JAX),
- **efficient data pre-processing**: simple, fast and reproducible data pre-processing for the public datasets as well as your own local datasets in CSV, JSON, text, PNG, JPEG, WAV, MP3, Parquet, etc. With simple commands like `processed_dataset = dataset.map(process_example)`, efficiently prepare the dataset for inspection and ML model evaluation and training.

[🎓 **Documentation**](https://huggingface.co/docs/datasets/) [🔎 **Find a dataset in the Hub**](https://huggingface.co/datasets) [🌟 **Share a dataset on the Hub**](https://huggingface.co/docs/datasets/share)

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://raw.githubusercontent.com/huggingface/datasets/main/docs/source/imgs/course_banner.png"></a>
</h3>

🤗 Datasets is designed to let the community easily add and share new datasets.

🤗 Datasets has many additional interesting features:

- Thrive on large datasets: 🤗 Datasets naturally frees the user from RAM memory limitation, all datasets are memory-mapped using an efficient zero-serialization cost backend (Apache Arrow).
- Smart caching: never wait for your data to process several times.
- Lightweight and fast with a transparent and pythonic API (multi-processing/caching/memory-mapping).
- Built-in interoperability with NumPy, PyTorch, TensorFlow 2, JAX, Pandas, Polars and more.
- Native support for audio, image and video data.
- Enable streaming mode to save disk space and start iterating over the dataset immediately.

🤗 Datasets originated from a fork of the awesome [TensorFlow Datasets](https://github.com/tensorflow/datasets) and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library.

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

For more details on installation, check the installation page in the documentation: https://huggingface.co/docs/datasets/installation

## Installation to use with Machine Learning & Data frameworks frameworks

If you plan to use 🤗 Datasets with PyTorch (2.0+), TensorFlow (2.6+) or JAX (3.14+) you should also install PyTorch, TensorFlow or JAX.
🤗 Datasets is also well integrated with data frameworks like PyArrow, Pandas, Polars and Spark, which should be installed separately.

For more details on using the library with these frameworks, check the quick start page in the documentation: https://huggingface.co/docs/datasets/quickstart

# Usage

🤗 Datasets is made to be very simple to use - the API is centered around a single function, `datasets.load_dataset(dataset_name, **kwargs)`, that instantiates a dataset.

This library can be used for text/image/audio/etc. datasets. Here is an example to load a text dataset:

Here is a quick example:

```python
from datasets import load_dataset

# Print all the available datasets
from huggingface_hub import list_datasets
print([dataset.id for dataset in list_datasets()])

# Load a dataset and print the first example in the training set
squad_dataset = load_dataset('rajpurkar/squad')
print(squad_dataset['train'][0])

# Process the dataset - add a column with the length of the context texts
dataset_with_length = squad_dataset.map(lambda x: {"length": len(x["context"])})

# Process the dataset - tokenize the context texts (using a tokenizer from the 🤗 Transformers library)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

tokenized_dataset = squad_dataset.map(lambda x: tokenizer(x['context']), batched=True)
```

If your dataset is bigger than your disk or if you don't want to wait to download the data, you can use streaming:

```python
# If you want to use the dataset immediately and efficiently stream the data as you iterate over the dataset
image_dataset = load_dataset('timm/imagenet-1k-wds', streaming=True)
for example in image_dataset["train"]:
    break
```

For more details on using the library, check the quick start page in the documentation: https://huggingface.co/docs/datasets/quickstart and the specific pages on:

- Loading a dataset: https://huggingface.co/docs/datasets/loading
- What's in a Dataset: https://huggingface.co/docs/datasets/access
- Processing data with 🤗 Datasets: https://huggingface.co/docs/datasets/process
    - Processing audio data: https://huggingface.co/docs/datasets/audio_process
    - Processing image data: https://huggingface.co/docs/datasets/image_process
    - Processing text data: https://huggingface.co/docs/datasets/nlp_process
- Streaming a dataset: https://huggingface.co/docs/datasets/stream
- etc.

# Add a new dataset to the Hub

We have a very detailed step-by-step guide to add a new dataset to the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) datasets already provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets).

You can find:
- [how to upload a dataset to the Hub using your web browser or Python](https://huggingface.co/docs/datasets/upload_dataset) and also
- [how to upload it using Git](https://huggingface.co/docs/datasets/share).

# Disclaimers

You can use 🤗 Datasets to load datasets based on Python code defined by the dataset authors to parse certain data formats or structures. For security reasons, this feature is disabled by default and requires passing `trust_remote_code=True`. In this case we also ask users that want to load such datasets to:
- check the dataset scripts they're going to run beforehand and
- pin the `revision` of the repositories they use.

If you're a dataset owner and wish to update any part of it (description, citation, license, etc.), or do not want your dataset to be included in the Hugging Face Hub, please get in touch by opening a discussion or a pull request in the Community tab of the dataset page. Thanks for your contribution to the ML community!

## BibTeX

If you want to cite our 🤗 Datasets library, you can use our [paper](https://arxiv.org/abs/2109.02846):

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

If you need to cite a specific version of our 🤗 Datasets library for reproducibility, you can use the corresponding version Zenodo DOI from this [list](https://zenodo.org/search?q=conceptrecid:%224817768%22&sort=-version&all_versions=True).
