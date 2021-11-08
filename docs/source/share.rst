Share
======

At Hugging Face, we are on a mission to democratize NLP and we believe in the value of open source. That's why we designed 🤗 Datasets so that anyone can share a dataset with the greater NLP community. There are currently over 900 datasets in over 100 languages in the Hugging Face Hub, and the Hugging Face team always welcomes new contributions!

This guide will show you how to share a dataset that can be easily accessed by anyone.

There are two options to share a new dataset:

- Directly upload it on the Hub as a community provided dataset.
- Add it as a canonical dataset by opening a pull-request on the `GitHub repository for 🤗 Datasets <https://github.com/huggingface/datasets>`__.

Community vs. canonical
-----------------------

Both options offer the same features such as:

- Dataset versioning
- Commit history and diffs
- Metadata for discoverability
- Dataset cards for documentation, licensing, limitations, etc.

The main differences between the two are highlighted in the table below:

.. list-table::
    :header-rows: 1

    * - Community datasets
      - Canonical datasets
    * - Faster to share, no review process.
      - Slower to add, needs to be reviewed.
    * - Data files can be stored on the Hub.
      - Data files are typically retrieved from the original host URLs.
    * - Identified by a user or organization namespace like **thomwolf/my_dataset** or **huggingface/our_dataset**.
      - Identified by a root namespace. Need to select a short name that is available.
    * - Requires data files and/or a dataset loading script.
      - Always requires a dataset loading script.
    * - Flagged as **unsafe** because the dataset contains executable code.
      - Flagged as **safe** because the dataset has been reviewed.

For community datasets, if your dataset is in a supported format, you can skip directly below to learn how to upload your files and add a :doc:`dataset card <dataset_card>`. There is no need to write your own dataset loading script (unless you want more control over how to load your dataset). However, if the dataset isn't in one of the supported formats, you will need to write a :doc:`dataset loading script <dataset_script>`. The dataset loading script is a Python script that defines the dataset splits, feature types, and how to download and process the data.

On the other hand, a dataset script is always required for canonical datasets.

.. important::

    The distinction between a canonical and community dataset is based solely on the selected sharing workflow. It does not involve any ranking, decisioning, or opinion regarding the contents of the dataset itself.

.. _upload_dataset_repo:

Add a community dataset
-----------------------

You can share your dataset with the community with a dataset repository on the Hugging Face Hub.
In a dataset repository, you can either host all your data files and/or use a dataset script.

The dataset script is optional if your dataset is in one of the following formats: CSV, JSON, JSON lines, text or Parquet.
The script also supports many kinds of compressed file types such as: GZ, BZ2, LZ4, LZMA or ZSTD.
For example, your dataset can be made of ``.json.gz`` files.

On the other hand, if your dataset is not in a supported format or if you want more control over how your dataset is loaded, you can write your own dataset script.

When loading a dataset from the Hub:

- If there's no dataset script, all the files in the supported formats are loaded.
- If there's a dataset script, it is downloaded and executed to download and prepare the dataset.

For more information on how to load a dataset from the Hub, see how to load from the :ref:`load-from-the-hub`.

Create the repository
^^^^^^^^^^^^^^^^^^^^^

Sharing a community dataset will require you to create an account on `hf.co <https://huggingface.co/join>`_ if you don't have one yet.
You can directly create a `new dataset repository <https://huggingface.co/login?next=%2Fnew-dataset>`_ from your account on the Hugging Face Hub, but this guide will show you how to upload a dataset from the terminal.

1. Make sure you are in the virtual environment where you installed Datasets, and run the following command:

.. code::

   huggingface-cli login

2. Login using your Hugging Face Hub credentials, and create a new dataset repository:

.. code::

   huggingface-cli repo create your_dataset_name --type dataset

Add the ``-organization`` flag to create a repository under a specific organization:

.. code::

   huggingface-cli repo create your_dataset_name --type dataset --organization your-org-name

Clone the repository
^^^^^^^^^^^^^^^^^^^^

3. Install `Git LFS <https://git-lfs.github.com/>`_ and clone your repository:

.. code-block::

   # Make sure you have git-lfs installed
   # (https://git-lfs.github.com/)
   git lfs install

   git clone https://huggingface.co/datasets/namespace/your_dataset_name

Here the ``namespace`` is either your username or your organization name.

Prepare your files
^^^^^^^^^^^^^^^^^^

4. Now is a good time to check your directory to ensure the only files you're uploading are:

* ``README.md`` is a Dataset card that describes the datasets contents, creation, and usage. To write a Dataset card, see the :doc:`dataset card <dataset_card>` page.

* The raw data files of the dataset (optional, if they are hosted elsewhere you can specify the URLs in the dataset script).

* ``your_dataset_name.py`` is your dataset loading script (optional if your data files are already in the supported formats csv/jsonl/json/parquet/txt). To create a dataset script, see the :doc:`dataset script <dataset_script>` page.

* ``dataset_infos.json`` contains metadata about the dataset (required only if you have a dataset script).

Upload your files
^^^^^^^^^^^^^^^^^

You can directly upload your files from your repository on the Hugging Face Hub, but this guide will show you how to upload the files from the terminal.

5. It is important to add the large data files first with ``git lfs track`` or else you will encounter an error later when you push your files:

.. code-block::

   cp /somewhere/data/*.json .
   git lfs track *.json
   git add .gitattributes
   git add *.json
   git commit -m "add json files"

6. Add the dataset loading script and metadata file:

.. code-block::

   cp /somewhere/data/dataset_infos.json .
   cp /somewhere/data/load_script.py .
   git add --all

7. Verify the files have been correctly staged. Then you can commit and push your files:

.. code-block::

   git status
   git commit -m "First version of the your_dataset_name dataset."
   git push


Congratulations, your dataset has now been uploaded to the Hugging Face Hub where anyone can load it in a single line of code! 🥳

.. code::

   dataset = load_dataset("namespace/your_dataset_name")

Add a canonical dataset
-----------------------

Canonical datasets are dataset scripts hosted in the GitHub repository of the 🤗 Dataset library.
The code of these datasets are reviewed by the Hugging Face team, and they require test data in order to be regularly tested.

Clone the repository
^^^^^^^^^^^^^^^^^^^^

To share a canonical dataset:

1. Fork the 🤗 `Datasets repository <https://github.com/huggingface/datasets>`_ by clicking on the **Fork** button.

2. Clone your fork to your local disk, and add the base repository as a remote:

.. code-block::

   git clone https://github.com/<your_GitHub_handle>/datasets
   cd datasets
   git remote add upstream https://github.com/huggingface/datasets.git

Prepare your files
^^^^^^^^^^^^^^^^^^

3. Create a new branch to hold your changes. You can name the new branch using the short name of your dataset:

.. code::

   git checkout -b my-new-dataset

4. Set up a development environment by running the following command in a virtual environment:

.. code::

   pip install -e ".[dev]"

5. Create a new folder with the dataset name inside ``huggingface/datasets``, and add the dataset loading script. To create a dataset script, see the :doc:`dataset script <dataset_script>` page.

6. Check your directory to ensure the only files you're uploading are:

* ``README.md`` is a Dataset card that describes the datasets contents, creation, and usage. To write a Dataset card, see the :doc:`dataset card <dataset_card>` page.

* ``your_dataset_name.py`` is your dataset loading script.

* ``dataset_infos.json`` contains metadata about the dataset.

* ``dummy`` folder with ``dummy_data.zip`` files that hold a small subset of data from the dataset for tests and preview.

7. Run `Black <https://black.readthedocs.io/en/stable/index.html>`_ and `isort <https://pycqa.github.io/isort/>`_ to tidy up your code and files:

.. code-block::

   make style
   make quality

8. Add your changes, and make a commit to record your changes locally. Then you can push the changes to your account:

.. code-block::

   git add datasets/<my-new-dataset>
   git commit
   git push -u origin my-new-dataset

9. Go back to your fork on GitHub, and click on **Pull request** to open a pull request on the main 🤗 `Datasets repository <https://github.com/huggingface/datasets>`_ for review.
