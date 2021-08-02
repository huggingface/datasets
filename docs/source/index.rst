Datasets
========

.. image:: /imgs/datasets_logo.png
   :align: center

🤗 Datasets is a library for easily accessing and sharing datasets, and evaluation metrics for Natural Language Processing (NLP). 

🤗 Datasets provides the simplest and fastest way for users to download a dataset, and get it ready for training in a deep learning model. With built-in support for NumPy, Pandas, PyTorch and TensorFlow, 🤗 Datasets ensures you can use it with a framework of your choice. We designed 🤗 Datasets for speed and efficiency by using the Apache Arrow format, memory-mapping, multiprocessing, and smart caching. 🤗 Datasets also supports sharing new datasets with the wider NLP community, making more resources available for training on different NLP tasks. There are currently over 900 datasets available, and in more than 100 languages.

Get started today and find your dataset on the `Hugging Face Hub <https://huggingface.co/datasets>`_, or take an in-depth look inside a dataset with the live `Datasets Viewer <https://huggingface.co/datasets/viewer/>`_.

.. panels::
    :card: shadow

    .. link-button:: tutorial
        :type: ref
        :text: Tutorials
        :classes: btn-primary btn-block
    
    ^^^
    Learn the basics by becoming familiar with loading, accessing and using a dataset. Start here if you are using 🤗 Datasets for the first time!

    ---
    .. link-button:: how-to
        :type: ref
        :text: How-to guides
        :classes: btn-primary btn-block

    ^^^
    Practical guides to help you get the most out of 🤗 Datasets for your use-case. Take a look at these guides for a demonstration on how to complete a specific task.

    ---
    .. link-button:: about_arrow
        :type: ref
        :text: Conceptual guides
        :classes: btn-primary btn-block

    ^^^
    High-level discussions about 🤗 Datasets. Read these to build a better understanding about key topics.
    
    ---
    .. link-button:: package_reference/main_classes
        :type: ref
        :text: Reference
        :classes: btn-primary btn-block

    ^^^
    Technical descriptions of 🤗 Datasets APIs.

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
    metrics
    
.. toctree::
    :hidden:
    :caption: How-to guides

    how-to
    loading
    process
    stream
    beam
    how_to_metrics
    share
    cache
    filesystems
    faiss_es

.. toctree::
    :hidden:
    :caption: Conceptual guides

    about_arrow
    about_cache
    about_dataset_features
    about_dataset_load
    about_map_batch
    about_metrics

.. toctree::
    :hidden:
    :caption: Reference

    package_reference/main_classes
    package_reference/builder_classes
    package_reference/loading_methods
    package_reference/table_classes
    package_reference/logging_methods
    package_reference/task_templates