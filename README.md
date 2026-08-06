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

- **one-line dataloaders for many public datasets**: one-liners to download and pre-process any of the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) major public datasets (image datasets, audio datasets, text datasets in 467 languages and dialects, 3D medical images, video datasets, agent traces, etc.) provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets). With a simple command like `squad_dataset = load_dataset("rajpurkar/squad")`, get any of these datasets ready to use in a dataloader for training/evaluating a ML model (Numpy/Pandas/PyTorch/TensorFlow/JAX/Polars),
- **efficient data pre-processing**: simple, fast and reproducible data pre-processing for the public datasets as well as your own local datasets in CSV, JSON, JSONL, Parquet, HDF5, XML, text, PNG, JPEG, WAV, MP3, PDF, NIfTI, and more. With simple commands like `processed_dataset = dataset.map(process_example)`, efficiently prepare the dataset for inspection and ML model evaluation and training.

[🎓 **Documentation**](https://huggingface.co/docs/datasets/) [🔎 **Find a dataset in the Hub**](https://huggingface.co/datasets) [🌟 **Share a dataset on the Hub**](https://huggingface.co/docs/datasets/share)

<h3 align="center">
    <a href="https://hf.co/course"><img src="https://raw.githubusercontent.com/huggingface/datasets/main/docs/source/imgs/course_banner.png"></a>
</h3>

# 🚀 Key Features

🤗 Datasets is designed to let the community easily add and share new datasets, and provides powerful capabilities for data manipulation:

| Feature | Description |
|---------|-------------|
| 📦 **One-line dataset loading** | Load AI-ready datasets from the [Hugging Face Hub](https://huggingface.co/datasets) or local files with `load_dataset()` |
| 🔍 **Multiple formats** | Native support for CSV, JSON, JSONL, Parquet, Arrow, XML, Text, Webdataset, and more |
| 🖼️ **Multi-modal data** | Built-in support for text, audio, image, video, PDF, and NIfTI (3D medical) data |
| 🚀 **Streaming mode** | Stream datasets without downloading — iterate over data on-the-fly with `streaming=True` (now up to **100x faster** with Xet backend) |
| 💾 **HF Storage Buckets** | Read and write directly from/to [Hugging Face Storage Buckets](https://huggingface.co/docs/hub/storage-buckets) for mutable, large-scale raw data |
| 🧠 **AI Agent Traces** | Load and process AI agent traces (prompts, tool calls, responses) from the Hub |
| ⚡ **Apache Arrow backend** | Zero-copy memory-mapped storage — datasets naturally free you from RAM limitations |
| 🔄 **Smart caching** | Never wait for your data to process twice — cached results are automatically reused |
| 📊 **Multi-framework interoperability** | Native conversion to/from NumPy, Pandas, Polars, Arrow, PyTorch, TensorFlow, JAX, and Spark |
| 🏎️ **Multi-processing** | Fast parallel data processing with `map(num_proc=N)` |
| 🔎 **Search & index** | Built-in FAISS and Elasticsearch index support for similarity search |
| 📦 **JSON type** | Flexible JSON/structured data support with `Json()` feature type |

# Installation

## With pip

🤗 Datasets can be installed from PyPi and should be installed in a virtual environment (venv or conda for instance):

```bash
pip install datasets
```

For the latest development version:

```bash
pip install "datasets @ git+https://github.com/huggingface/datasets.git"
```

## With conda

```bash
conda install -c huggingface -c conda-forge datasets
```

## Optional dependencies

🤗 Datasets supports various optional features via extras:

```bash
# For audio (torchcodec)
pip install datasets[audio]

# For image/video (Pillow, torchcodec)
pip install datasets[vision]

# For PDFs/NIfTI (pdfplumber, nibabel)
pip install datasets[pdfs,nibabel]

# For PyTorch/TensorFlow/JAX integration
pip install datasets[torch,tensorflow,jax]

```

For more details on installation, check the [installation page](https://huggingface.co/docs/datasets/installation).

# Quick Start

🤗 Datasets is made to be very simple to use — the API is centered around a single function, `datasets.load_dataset(dataset_name, **kwargs)`, that instantiates a dataset.

Here is a quick example:

```python
from datasets import load_dataset

# Load a dataset and print the first example in the training set
squad_dataset = load_dataset('rajpurkar/squad')
print(squad_dataset['train'][0])

# Process the dataset - add a column with the length of the context texts
dataset_with_length = squad_dataset.map(lambda x: {"length": len(x["context"])})

# Tokenize the context texts (using a tokenizer from the 🤗 Transformers library)
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-cased')

tokenized_dataset = squad_dataset.map(lambda x: tokenizer(x['context']), batched=True)

# Tokenize chat conversations with a chat template (using a model that supports chat templates)
# This is useful for fine-tuning instruction/chat models

# Load a popular chat dataset (ultrachat_200k contains ~200k AI assistant conversations)
chat_dataset = load_dataset('HuggingFaceH4/ultrachat_200k', split='train_sft')

chat_tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-7B-Instruct')

def tokenize_chat(examples):
    # Apply the chat template and tokenize in one step
    return chat_tokenizer.apply_chat_template(examples["messages"])

tokenized_chat_dataset = chat_dataset.map(tokenize_chat, batched=True)
```

## Streaming mode

If your dataset is bigger than your disk or if you don't want to wait to download the data, you can use streaming:

```python
# Stream the dataset without downloading anything
image_dataset = load_dataset('timm/imagenet-1k-wds', streaming=True)
for example in image_dataset["train"]:
    print(example["image"])
    break
```

## Multi-modal data

🤗 Datasets supports a wide variety of data types out of the box:

```python
# Audio dataset
dataset = load_dataset("openslr/librispeech_asr", "clean")

# Image dataset
dataset = load_dataset("ILSVRC/imagenet-1k")

# Video dataset
dataset = load_dataset("Shofo/shofo-tiktok-general-small")

# PDF documents
dataset = load_dataset("pixparse/pdfa-eng-wds")

# NIfTI (3D medical imaging)
dataset = load_dataset("dartbrains/localizer", "betas")
```

## From local files

```python
# Load from local CSV
dataset = load_dataset('csv', data_files='my_data.csv')

# Load from local Parquet
dataset = load_dataset('parquet', data_files='data/*.parquet')

# Load from a local directory (auto-detect format)
dataset = load_dataset('./path/to/data')
```

## From Python objects

```python
from datasets import Dataset

# From a dictionary
dataset = Dataset.from_dict({"text": ["Hello world", "How are you?"]})

# From a list
dataset = Dataset.from_list([{"text": "Hello world"}, {"text": "How are you?"}])

# From Pandas
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
dataset = Dataset.from_pandas(df)

# From a generator
def gen():
    for i in range(10):
        yield {"value": i}
dataset = Dataset.from_generator(gen)
```

For more details on using the library, check the [quick start guide](https://huggingface.co/docs/datasets/quickstart) and the specific pages on:

- [Loading a dataset](https://huggingface.co/docs/datasets/loading)
- [What's in a Dataset](https://huggingface.co/docs/datasets/access)
- [Processing data with 🤗 Datasets](https://huggingface.co/docs/datasets/process)
  - [Processing audio data](https://huggingface.co/docs/datasets/audio_process)
  - [Processing image data](https://huggingface.co/docs/datasets/image_process)
  - [Processing text data](https://huggingface.co/docs/datasets/nlp_process)
  - [Processing PDF data](https://huggingface.co/docs/datasets/pdf_process)
  - [Processing video data](https://huggingface.co/docs/datasets/video_process)
- [Streaming a dataset](https://huggingface.co/docs/datasets/stream)

# Core Classes

The library provides two main dataset classes:

| Class | Description |
|-------|-------------|
| `Dataset` | In-memory / memory-mapped dataset backed by Apache Arrow. Supports indexing, slicing, random access and caching. |
| `IterableDataset` | Lazy, streamable dataset for large-scale / out-of-core processing. Supports streaming and infinite iteration. |

Both are wrapped in `DatasetDict` / `IterableDatasetDict` for multi-split datasets (e.g., train/test/val).

# Add a new dataset to the Hub

We have a very detailed step-by-step guide to add a new dataset to the ![number of datasets](https://img.shields.io/endpoint?url=https://huggingface.co/api/shields/datasets&color=brightgreen) datasets already provided on the [HuggingFace Datasets Hub](https://huggingface.co/datasets).

You can find:
- [how to upload a dataset to the Hub using your web browser or Python](https://huggingface.co/docs/datasets/upload_dataset) and also
- [how to upload it using Git](https://huggingface.co/docs/datasets/share).

# Disclaimers

You can use 🤗 Datasets to load datasets based on versioned git repositories maintained by the dataset authors. For reproducibility reasons, we ask users to pin the `revision` of the repositories they use.

If you're a dataset owner and wish to update any part of it (description, citation, license, etc.), or do not want your dataset to be included in the Hugging Face Hub, please get in touch by opening a discussion or a pull request in the Community tab of the dataset page. Thanks for your contribution to the ML community!

# Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- How to submit issues and pull requests
- Code style guidelines (we use [Ruff](https://docs.astral.sh/ruff/))
- Testing requirements
- Documentation standards

# BibTeX

If you want to cite our 🤗 Datasets library, you can use our [paper](https://huggingface.co/papers/2109.02846):

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
