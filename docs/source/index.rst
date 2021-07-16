<<<<<<< HEAD
.. image:: /imgs/datasets.png
   :align: center

Datasets is a library for easily accessing and sharing datasets, and evaluation metrics for Natural Language Processing (NLP). 

Datasets provides the simplest and fastest way for users to download a dataset, and get it ready for training in a deep learning model. With built-in support for NumPy, Pandas, PyTorch and TensorFlow, Datasets ensures you can use it with a framework of your choice. We designed Datasets for speed and efficiency by using the Apache Arrow format, memory-mapping, multiprocessing, and smart caching. Datasets also supports sharing new datasets with the wider NLP community, making more resources available for training on different NLP tasks. There are currently over 900 datasets available, and in more than 100 languages.

Get started today and find your dataset on the `Datasets Hub <https://huggingface.co/datasets>`_, or take an in-depth look inside a dataset with the live `Datasets Viewer <https://huggingface.co/datasets/viewer/>`_.

.. panels::
    :card: shadow

    .. link-button:: tutorial
        :type: ref
        :text: Tutorials
        :classes: btn-primary btn-block
    Learn the basics by becoming familiar with loading, accessing and using a dataset. Start here if you are using Datasets for the first time!

    ---
    .. link-button:: how-to
        :type: ref
        :text: How-to guides
        :classes: btn-primary btn-block
    Practical guides to help you get the most out of Datasets for your use-case. Take a look at these guides for a demonstration on how to complete a specific task.

    ---
    .. link-button:: cache
        :type: ref
        :text: Conceptual guides
        :classes: btn-primary btn-block
    High-level discussions about Datasets. Read these to build a better understanding about key topics in Datasets.
    
    ---
    .. link-button:: cache
        :type: ref
        :text: Reference
        :classes: btn-primary btn-block
    Technical descriptions of Datasets APIs. Only read if you need help falling asleep.
=======
HuggingFace Datasets
=======================================

Datasets and evaluation metrics for natural language processing

Compatible with NumPy, Pandas, PyTorch and TensorFlow

🤗 Datasets is a lightweight and extensible library to easily share and access datasets and evaluation metrics for Natural Language Processing (NLP).

🤗 Datasets has many interesting features (beside easy sharing and accessing datasets/metrics):

Built-in interoperability with Numpy, Pandas, PyTorch and Tensorflow 2
Lightweight and fast with a transparent and pythonic API
Strive on large datasets: 🤗 Datasets naturally frees the user from RAM memory limitation, all datasets are memory-mapped on drive by default.
Smart caching: never wait for your data to process several times
🤗 Datasets currently provides access to ~100 NLP datasets and ~10 evaluation metrics and is designed to let the community easily add and share new datasets and evaluation metrics. You can browse the full set of datasets with the live 🤗 Datasets viewer.

🤗 Datasets originated from a fork of the awesome TensorFlow Datasets and the HuggingFace team want to deeply thank the TensorFlow Datasets team for building this amazing library. More details on the differences between 🤗 Datasets and `tfds` can be found in the section Main differences between 🤗 Datasets and `tfds`.

Contents
---------------------------------

The documentation is organized in five parts:

- **GET STARTED** contains a quick tour and the installation instructions.
- **USING DATASETS** contains general tutorials on how to use and contribute to the datasets in the library.
- **USING METRICS** contains general tutorials on how to use and contribute to the metrics in the library.
- **ADVANCED GUIDES** contains more advanced guides that are more specific to a part of the library.
- **PACKAGE REFERENCE** contains the documentation of each public class and function.
>>>>>>> master

.. toctree::
    :hidden:

    quickstart

.. toctree::
    :hidden:
    :caption: Tutorials

    tutorial
    installation
    load_hub
    access
    use_dataset
    
.. toctree::
    :hidden:
    :caption: How-to guides

    how-to
    loading
    process
    share
    cache

.. toctree::
    :hidden:
    :caption: Reference

    package_reference/loading_methods
    package_reference/main_classes
    package_reference/builder_classes
    package_reference/table_classes
    package_reference/logging_methods
    package_reference/task_templates