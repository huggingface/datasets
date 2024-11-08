# Fast Datasets

fast-datasets is a minimally divergent fork of [HuggingFace Datasets](https://github.com/huggingface/datasets), adding some optimisations for array feature types and iterable datasets.
fast-datasets is a dependency of [bio-datasets](https://github.com/bioml-tools/bio-datasets).

If the modifications are approved as PRs to the main Datasets library, this fork will no longer be updated.

The following is the Datasets README.

[🎓 **Documentation**](https://huggingface.co/docs/datasets/) [🔎 **Find a dataset in the Hub**](https://huggingface.co/datasets) [🌟 **Share a dataset on the Hub**](https://huggingface.co/docs/datasets/share)

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://raw.githubusercontent.com/huggingface/datasets/main/docs/source/imgs/course_banner.png"></a>
</h3>

🤗 Datasets is designed to let the community easily add and share new datasets.

🤗 Datasets has many additional interesting features:

- Thrive on large datasets: 🤗 Datasets naturally frees the user from RAM memory limitation, all datasets are memory-mapped using an efficient zero-serialization cost backend (Apache Arrow).
- Smart caching: never wait for your data to process several times.
- Lightweight and fast with a transparent and pythonic API (multi-processing/caching/memory-mapping).
- Built-in interoperability with NumPy, pandas, PyTorch, TensorFlow 2 and JAX.
- Native support for audio and image data.
- Enable streaming mode to save disk space and start iterating over the dataset immediately.

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

For more details on installation, check the installation page in the documentation: https://huggingface.co/docs/datasets/installation

## Installation to use with PyTorch/TensorFlow/pandas

If you plan to use 🤗 Datasets with PyTorch (1.0+), TensorFlow (2.2+) or pandas, you should also install PyTorch, TensorFlow or pandas.

For more details on using the library with NumPy, pandas, PyTorch or TensorFlow, check the quick start page in the documentation: https://huggingface.co/docs/datasets/quickstart

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
squad_dataset = load_dataset('squad')
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
image_dataset = load_dataset('cifar100', streaming=True)
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
- Writing your own dataset loading script: https://huggingface.co/docs/datasets/dataset_script
- etc.

# Add a new dataset to the Hub

We have a very detailed step-by-step guide to add a new dataset to the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) datasets already provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets).

You can find:
- [how to upload a dataset to the Hub using your web browser or Python](https://huggingface.co/docs/datasets/upload_dataset) and also
- [how to upload it using Git](https://huggingface.co/docs/datasets/share).

# Main differences between 🤗 Datasets and `tfds`

If you are familiar with the great TensorFlow Datasets, here are the main differences between 🤗 Datasets and `tfds`:

- the scripts in 🤗 Datasets are not provided within the library but are queried, downloaded/cached and dynamically loaded upon request
- the backend serialization of 🤗 Datasets is based on [Apache Arrow](https://arrow.apache.org/) instead of TF Records and leverage python dataclasses for info and features with some diverging features (we mostly don't do encoding and store the raw data as much as possible in the backend serialization cache).
- the user-facing dataset object of 🤗 Datasets is not a `tf.data.Dataset` but a built-in framework-agnostic dataset class with methods inspired by what we like in `tf.data` (like a `map()` method). It basically wraps a memory-mapped Arrow table cache.

# Disclaimers

🤗 Datasets may run Python code defined by the dataset authors to parse certain data formats or structures. For security reasons, we ask users to:
- check the dataset scripts they're going to run beforehand and
- pin the `revision` of the repositories they use.

If you're a dataset owner and wish to update any part of it (description, citation, license, etc.), or do not want your dataset to be included in the Hugging Face Hub, please get in touch by opening a discussion or a pull request in the Community tab of the dataset page. Thanks for your contribution to the ML community!

## BibTeX

If you want to cite the 🤗 Datasets library, you can use our [paper](https://arxiv.org/abs/2109.02846):

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
