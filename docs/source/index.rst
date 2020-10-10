HuggingFace Datasets
=======================================

Datasets and evaluation metrics for natural language processing

Compatible with NumPy, Pandas, PyTorch and TensorFlow

🤗datasets is a lightweight and extensible library to easily share and access datasets and evaluation metrics for Natural Language Processing (NLP).

🤗Datasets has many interesting features (beside easy sharing and accessing datasets/metrics):

Built-in interoperability with Numpy, Pandas, PyTorch and Tensorflow 2
Lightweight and fast with a transparent and pythonic API
Strive on large datasets: 🤗Datasets naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive by default.
Smart caching: never wait for your data to process several times
🤗Datasets currently provides access to ~100 NLP datasets and ~10 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics. You can browse the full set of datasets with the live 🤗Datasets viewer.

🤗Datasets originated from a fork of the awesome TensorFlow Datasets and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between 🤗Datasets and tfds can be found in the section Main differences between 🤗Datasets and tfds.

Contents
---------------------------------

The documentation is organized in five parts:

- **GET STARTED** contains a quick tour and the installation instructions.
- **USING DATASETS** contains general tutorials on how to use and contribute to the datasets in the library.
- **USING METRICS** contains general tutorials on how to use and contribute to the metrics in the library.
- **ADVANCED GUIDES** contains more advanced guides that are more specific to a part of the library.
- **PACKAGE REFERENCE** contains the documentation of each public class and function.

.. toctree::
    :maxdepth: 2
    :caption: Get started

    quicktour
    installation

.. toctree::
    :maxdepth: 2
    :caption: Using datasets

    loading_datasets
    exploring
    processing
    torch_tensorflow
    faiss_and_ea

.. toctree::
    :maxdepth: 2
    :caption: Using metrics

    loading_metrics
    using_metrics

.. toctree::
    :maxdepth: 2
    :caption: Adding new datasets/metrics

    add_dataset
    share_dataset
    add_metric

.. toctree::
    :maxdepth: 2
    :caption: Advanced guides

    features
    splits
    beam_dataset

.. toctree::
    :maxdepth: 2
    :caption: Package reference

    package_reference/loading_methods
    package_reference/main_classes
    package_reference/builder_classes
    package_reference/logging_methods
