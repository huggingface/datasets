Datasets
========

.. image:: /imgs/datasets_logo.png
   :align: center

🤗 Datasets is a library for easily accessing and sharing datasets, and evaluation metrics for Natural Language Processing (NLP), computer vision, and audio tasks.

Load a dataset in a single line of code, and use our powerful data processing methods to quickly get your dataset ready for training in a deep learning model. Backed by the Apache Arrow format, process large datasets with zero-copy reads without any memory constraints for optimal speed and efficiency. We also feature a deep integration with the `Hugging Face Hub <https://huggingface.co/datasets>`_, allowing you to easily load and share a dataset with the wider NLP community. There are currently over 2658 datasets, and more than 34 metrics available. 

Find your dataset today on the `Hugging Face Hub <https://huggingface.co/datasets>`_, or take an in-depth look inside a dataset with the live `Datasets Viewer <https://huggingface.co/datasets/viewer/>`_.

.. panels::
    :card: shadow

    .. link-button:: tutorial
        :type: ref
        :text: Tutorials
        :classes: btn-primary btn-block
    
    ^^^
    Learn the basics and become familiar with loading, accessing, and processing a dataset. Start here if you are using 🤗 Datasets for the first time!

    ---
    .. link-button:: how_to
        :type: ref
        :text: How-to guides
        :classes: btn-primary btn-block

    ^^^
    Practical guides to help you achieve a specific goal. Take a look at these guides to learn how to use 🤗 Datasets to solve real-world problems.

    ---
    .. link-button:: about_arrow
        :type: ref
        :text: Conceptual guides
        :classes: btn-primary btn-block

    ^^^
    High-level explanations for building a better understanding about important topics such as the underlying data format, the cache, and how datasets are generated.
    ---
    .. link-button:: package_reference/main_classes
        :type: ref
        :text: Reference
        :classes: btn-primary btn-block

    ^^^
    Technical descriptions of how 🤗 Datasets classes and methods work.

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
    upload_dataset
    
.. toctree::
    :hidden:
    :caption: How-to guides

    how_to
    loading
    process
    audio_process
    stream
    share
    dataset_script
    dataset_card
    repository_structure
    cache
    filesystems
    faiss_es
    how_to_metrics
    beam

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
