nlp
=======================================

Datasets and evaluation metrics for natural language processing

Compatible with NumPy, Pandas, PyTorch and TensorFlow

🤗nlp is a lightweight and extensible library to easily share and access datasets and evaluation metrics for Natural Language Processing (NLP).

nlp has many interesting features (beside easy sharing and accessing datasets/metrics):

Built-in interoperability with Numpy, Pandas, PyTorch and Tensorflow 2
Lightweight and fast with a transparent and pythonic API
Strive on large datasets: nlp naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive by default.
Smart caching: never wait for your data to process several times
nlp currently provides access to ~100 NLP datasets and ~10 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics. You can browse the full set of datasets with the live nlp viewer.

nlp originated from a fork of the awesome TensorFlow Datasets and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between nlp and tfds can be found in the section Main differences between nlp and tfds.

Contents
---------------------------------

The documentation is organized in five parts:

- **GET STARTED** contains a quick tour, the installation instructions and some useful information about our philosophy
  and a glossary.
- **RESEARCH** focuses on tutorials that have less to do with how to use the library but more about general resarch in
  transformers model
- **PACKAGE REFERENCE** contains the documentation of each public class and function.

.. toctree::
    :maxdepth: 2
    :caption: Get started

    quicktour
    installation

.. toctree::
    :maxdepth: 2
    :caption: Using 🤗nlp

    loading_methods
    main_classes
    splits
    beam_dataset

.. toctree::
    :maxdepth: 2
    :caption: Adding new datasets and metrics

    add_dataset

