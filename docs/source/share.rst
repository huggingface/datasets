Share
======

At Hugging Face, we are on a mission to democratize NLP and we believe in the value of open source. That's why we designed 🤗 Datasets so that anyone can share a dataset with the greater NLP community. There are currently over 900 datasets in over 100 languages, and the Hugging Face team always welcomes new submissions!

This guide will show you how to add a dataset that can be easily accessed by anyone. The guide includes instructions for how to:

* Add dataset metadata.
* Download data files.
* Generate samples.
* Test if your dataset was generated correctly.
* Create a Dataset card.
* Upload a dataset to the Hugging Face Hub or Github.

Open the `SQuAD dataset loading script <https://github.com/huggingface/datasets/blob/master/datasets/squad/squad.py>`_ template to follow along on how to share a dataset.

.. tip::

   To help you get started, try beginning with the dataset loading script `template <https://github.com/huggingface/datasets/blob/master/templates/new_dataset_script.py>`_!

Add dataset attributes
----------------------

The first step is to add some information, or attributes, about your dataset in :func:`datasets.DatasetBuilder._info`. The most important attributes you should specify are:

1. :obj:`datasets.DatasetInfo.description` provides a concise description of your dataset. The description informs the user what's in the dataset, how it was collected, and how it can be used for a NLP task.

2. :obj:`datasets.DatasetInfo.features` defines the name and type of each column in your dataset. This will also provide the structure for each example, so it is possible to create nested subfields in a column if you want. Take a look at :class:`datasets.Features` for a full list of feature types you can use.

.. code-block::

   datasets.Features(
       {
           "id": datasets.Value("string"),
           "title": datasets.Value("string"),
           "context": datasets.Value("string"),
           "question": datasets.Value("string"),
           "answers": datasets.Sequence(
               {
                   "text": datasets.Value("string"),
                   "answer_start": datasets.Value("int32"),
               }
           ),
       }
   )

3. :obj:`datasets.DatasetInfo.homepage` contains a URL to the datasets homepage so users can find more details about the dataset.

4. :obj:`datasets.DatasetInfo.citation` contains a BibTex citation for the dataset.

After you've filled out all these fields in the template, it should look like the following example from the SQuAD loading script:

.. code-block::

   def _info(self):
       return datasets.DatasetInfo(
           description=_DESCRIPTION,
           features=datasets.Features(
               {
                   "id": datasets.Value("string"),
                   "title": datasets.Value("string"),
                   "context": datasets.Value("string"),
                   "question": datasets.Value("string"),
                   "answers": datasets.features.Sequence(
                       {"text": datasets.Value("string"), "answer_start": datasets.Value("int32"),}
                   ),
               }
           ),
           # No default supervised_keys (as we have to pass both question
           # and context as input).
           supervised_keys=None,
           homepage="https://rajpurkar.github.io/SQuAD-explorer/",
           citation=_CITATION,
       )

Multiple configurations
^^^^^^^^^^^^^^^^^^^^^^^

In some cases, your dataset may have multiple configurations. For example, the `SuperGLUE <https://huggingface.co/datasets/super_glue>`_ dataset is a collection of 5 datasets designed to evaluate language understanding tasks. 🤗 Datasets provides :class:`datasets.BuilderConfig` which allows you to create different configurations for the user to select from.

Let's study the `SuperGLUE loading script <https://github.com/huggingface/datasets/blob/master/datasets/super_glue/super_glue.py>`_ to see how you can define several configurations.

1. Create a :class:`datasets.BuilderConfig` class with attributes about your dataset. These attributes can be the features of your dataset, label classes, and a URL to the data files.

.. code-block::

   class SuperGlueConfig(datasets.BuilderConfig):
       """BuilderConfig for SuperGLUE."""

   def __init__(self, features, data_url, citation, url, label_classes=("False", "True"), **kwargs):
       """BuilderConfig for SuperGLUE.

       Args:
       features: `list[string]`, list of the features that will appear in the
           feature dict. Should not include "label".
       data_url: `string`, url to download the zip file from.
       citation: `string`, citation for the data set.
       url: `string`, url for information about the data set.
       label_classes: `list[string]`, the list of classes for the label if the
           label is present as a string. Non-string labels will be cast to either
           'False' or 'True'.
       **kwargs: keyword arguments forwarded to super.
       """
       # Version history:
       # 1.0.2: Fixed non-nondeterminism in ReCoRD.
       # 1.0.1: Change from the pre-release trial version of SuperGLUE (v1.9) to
       #        the full release (v2.0).
       # 1.0.0: S3 (new shuffling, sharding and slicing mechanism).
       # 0.0.2: Initial version.
       super(SuperGlueConfig, self).__init__(version=datasets.Version("1.0.2"), **kwargs)
       self.features = features
       self.label_classes = label_classes
       self.data_url = data_url
       self.citation = citation
       self.url = url

2. Sub-class the base :class:`datasets.BuilderConfig` to add additional attributes of a configuration. This gives you more flexibility to specify the name and description of each configuration. These sub-classes should be listed under :obj:`datasets.DatasetBuilder.BUILDER_CONFIGS`:

.. code-block::

   class SuperGlue(datasets.GeneratorBasedBuilder):
       """The SuperGLUE benchmark."""

       BUILDER_CONFIGS = [
           SuperGlueConfig(
               name="boolq",
               description=_BOOLQ_DESCRIPTION,
               features=["question", "passage"],
               data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/BoolQ.zip",
               citation=_BOOLQ_CITATION,
               url="https://github.com/google-research-datasets/boolean-questions",
           ),
           ...
           ...
           SuperGlueConfig(
               name="axg",
               description=_AXG_DESCRIPTION,
               features=["premise", "hypothesis"],
               label_classes=["entailment", "not_entailment"],
               data_url="https://dl.fbaipublicfiles.com/glue/superglue/data/v2/AX-g.zip",
               citation=_AXG_CITATION,
               url="https://github.com/rudinger/winogender-schemas",
           ),
       

3. Now, users can load a specific configuration of the dataset with the configuration ``name``:

.. code-block::

   >>> from datasets import load_dataset
   >>> dataset = load_dataset('super_glue', 'boolq')

Default configurations
^^^^^^^^^^^^^^^^^^^^^^

Users must specify a configuration name when they load a dataset with multiple configurations. Otherwise, 🤗 Datasets will raise a ``ValueError``, and prompt the user to select a configuration name. You can avoid this by setting a default dataset configuration with the :attr:`datasets.DatasetBuilder.DEFAULT_CONFIG_NAME` attribute:

.. code-block::

   class NewDataset(datasets.GeneratorBasedBuilder):

   VERSION = datasets.Version("1.1.0")

   BUILDER_CONFIGS = [
       datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
       datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
   ]

   DEFAULT_CONFIG_NAME = "first_domain"

.. important::

   Only use a default configuration when it makes sense. Don't set one because it may be more convenient for the user to not specify a configuration when they load your dataset. For example, multi-lingual datasets often have a separate configuration for each language. An appropriate default may be an aggregated configuration that loads all the languages of the dataset if the user doesn't request a particular one.

Download data files and organize splits
---------------------------------------

After you've defined the attributes of your dataset, the next step is to download the data files and organize them according to their splits. 

1. Create a dictionary of URLs in the loading script that point to the original SQuAD data files:

.. code-block::

   _URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/"
       _URLS = {
           "train": _URL + "train-v1.1.json",
           "dev": _URL + "dev-v1.1.json",
       }

2. :obj:`datasets.DownloadManager.download_and_extract` takes this dictionary and downloads the data files. Once the files are downloaded, :func:`datasets.SplitGenerator` organizes each split in the dataset. This is a simple class that contains:

* The :obj:`name` of each split. You should use the standard split names: :obj:`datasets.Split.TRAIN`, :obj:`datasets.Split.TEST`, and :obj:`datasets.Split.VALIDATION`.

* :obj:`gen_kwargs` provides the file paths to the data files to load for each split.

Your :obj:`datasets.DatasetBuilder._split_generator()` should look like this now:

.. code-block::

   def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
       urls_to_download = self._URLS
       downloaded_files = dl_manager.download_and_extract(urls_to_download)

       return [
           datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
           datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
       ]

Generate samples
----------------

At this point, you have:

* Added the dataset attributes.
* Provided instructions for how to download the data files.
* Organized the splits.

The next step is to actually generate the samples in each split. 

1. :obj:`datasets.DatasetBuilder._generate_examples` takes the file path provided by :obj:`gen_kwargs` to read and parse the data files. You need to write a function that loads the data files and extracts the columns.

2. Your function should yield a tuple of an ``id_``, and an example from the dataset.

.. code-block::

   def _generate_examples(self, filepath):
   """This function returns the examples in the raw (text) form."""
   logger.info("generating examples from = %s", filepath)
   with open(filepath) as f:
       squad = json.load(f)
       for article in squad["data"]:
           title = article.get("title", "").strip()
           for paragraph in article["paragraphs"]:
               context = paragraph["context"].strip()
               for qa in paragraph["qas"]:
                   question = qa["question"].strip()
                   id_ = qa["id"]

                   answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                   answers = [answer["text"].strip() for answer in qa["answers"]]

                   # Features currently used are "context", "question", and "answers".
                   # Others are extracted here for the ease of future expansions.
                   yield id_, {
                       "title": title,
                       "context": context,
                       "question": question,
                       "id": id_,
                       "answers": {"answer_start": answer_starts, "text": answers,},
                }

Testing data and checksum metadata
----------------------------------

We strongly recommend adding testing data and checksum metadata to your dataset to verify and test its behavior. This ensures the generated dataset matches your expectations.

.. important::

   Make sure you run all of the following commands **from the root** of your local ``datasets`` repository.

Dataset metadata
^^^^^^^^^^^^^^^^

1. Run the following command to create the metadata file, ``dataset_infos.json``. This will also test your new dataset loading script and make sure it works correctly.

.. code::

   datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs

2. If your dataset loading script passed the test, you should now have a ``dataset_infos.json`` file in your dataset folder. This file contains information about the dataset, like its ``features`` and ``download_size``.

Dummy data
^^^^^^^^^^

Next, you need to create some dummy data for automated testing. There are two methods for generating dummy data: automatically and manually. 

Automatic
"""""""""

If your data file is one of the following formats, then you can automatically generate the dummy data:

* txt
* csv
* tsv
* jsonl
* json
* xml

Run the command below to generate the dummy data:

.. code::

   datasets-cli dummy_data datasets/<your-dataset-folder> --auto_generate

Manual
""""""

If your data files are not among the supported formats, you will need to generate your dummy data manually. Run the command below to output detailed instructions on how to create the dummy data:

.. code-block::

   datasets-cli dummy_data datasets/<your-dataset-folder>

   ==============================DUMMY DATA INSTRUCTIONS==============================
   - In order to create the dummy data for my-dataset, please go into the folder './datasets/my-dataset/dummy/1.1.0' with `cd ./datasets/my-dataset/dummy/1.1.0` .

   - Please create the following dummy data files 'dummy_data/TREC_10.label, dummy_data/train_5500.label' from the folder './datasets/my-dataset/dummy/1.1.0'

   - For each of the splits 'train, test', make sure that one or more of the dummy data files provide at least one example

   - If the method `_generate_examples(...)` includes multiple `open()` statements, you might have to create other files in addition to 'dummy_data/TREC_10.label, dummy_data/train_5500.label'. In this case please refer to the `_generate_examples(...)` method

   - After all dummy data files are created, they should be zipped recursively to 'dummy_data.zip' with the command `zip -r dummy_data.zip dummy_data/`

   - You can now delete the folder 'dummy_data' with the command `rm -r dummy_data`

   - To get the folder 'dummy_data' back for further changes to the dummy data, simply unzip dummy_data.zip with the command `unzip dummy_data.zip`

   - Make sure you have created the file 'dummy_data.zip' in './datasets/my-dataset/dummy/1.1.0'
   ===================================================================================

.. tip::

   Manually creating dummy data can be tricky. Make sure you follow the instructions from the command ``datasets-cli dummy_data datasets/<your-dataset-folder>``. If you are still unable to succesfully generate dummy data, open a `Pull Request <https://github.com/huggingface/datasets/pulls>`_ and we will be happy to help you out!

There should be two new files in your dataset folder:

* ``dataset_infos.json`` stores the dataset metadata including the data file checksums, and the number of examples required to confirm the dataset was generated properly.

* ``dummy_data`` is a file used to test the behavior of the loading script without having to download the full dataset.

Test
^^^^

The last step is to actually test dataset generation with the real and dummy data. Run the following command to test the real data:

.. code::

   RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your_dataset_name>

Test the dummy data:

.. code::

   RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your_dataset_name>

If both tests pass, your dataset was generated correctly!

Dataset card
------------

Each dataset should be accompanied with a Dataset card to promote responsible usage, and alert the user to any potential biases within the dataset. This idea is inspired by the Model Cards proposed by `Mitchell, 2018 <https://arxiv.org/abs/1810.03993>`_. Dataset cards help users understand the contents of the dataset, context for how the dataset should be used, how it was created, and considerations for using the dataset. This guide shows you how to create your own Dataset card.

1. Create a new Dataset card by opening the `online card creator <https://huggingface.co/datasets/card-creator/>`_, or manually copying the template to your dataset folder:

.. code::

   cp ./templates/README.md ./datasets/<your_dataset_name>/README.md

2. Next, you need to generate structured tags. The tags help users discover your dataset on the Hub. Create the tags with the `online tagging app <https://huggingface.co/datasets/tagging/>`_, or clone and install the `Datasets tagging app <https://github.com/huggingface/datasets-tagging>`_ locally.

3. Select the appropriate tags for your dataset from the dropdown menus, and save the file once you are done.

4. Expand the **Show YAML output aggregating the tags** section on the right, copy the YAML tags, and paste it under the matching section on the online form. Paste the tags into your ``README.md`` file if you manually created your Dataset card.

5. Expand the **Show Markdown Data Fields** section, paste it into the **Data Fields** section under **Data Structure** on the online form (or your local ``README.md``). Modify the descriptions as needed, and briefly describe each of the fields.

6. Fill out the Dataset card to the best of your ability. Refer to the `Dataset Card Creation Guide <https://github.com/huggingface/datasets/blob/master/templates/README_guide.md>`_ for more detailed information about each section of the card. For fields you are unable to complete, you can write **[More Information Needed]**.

7. Once you are done filling out the card with the online form, click the **Export** button to download the Dataset card. Place it in the same folder as your dataset.

Upload
------

The final step is to upload your dataset. Based on your sharing workflow, there are two types of datasets: community and canonical datasets. The main differences between the two are highlighted in the table below:

.. list-table::
    :header-rows: 1

    * - Community datasets
      - Canonical datasets
    * - Faster to share, no review process.
      - Slower to add, needs to be reviewed.
    * - Data files can be stored on the Hub.
      - Data files are typically retrieved from the original URLs.
    * - Identified by a user or organization namespace like **thomwolf/my_dataset** or **huggingface/our_dataset**.
      - Identified by a root namepsace. Need to select a short name that is available.
    * - Flagged as **unsafe** because the dataset contains executable code.
      - Flagged as **safe** because the dataset has been reviewed.

.. important::

    The distinction between a canonical and community dataset is based solely on the selected sharing workflow. It does not involve any ranking, decisioning, or opinion regarding the contents of the dataset itself.

.. _upload_dataset_repo:

Community dataset
^^^^^^^^^^^^^^^^^

Sharing a community dataset will require you to create an account on `hf.co <https://huggingface.co/join>`_ if you don't already have one. You can directly create a `new dataset repository <https://huggingface.co/new-dataset>`_ from your account on the Hugging Face Hub, but this guide will show you how to upload a dataset from the terminal.

1. Make sure you are in the virtual environment where you installed 🤗 Datasets, and run the following command:

.. code::

   huggingface-cli login

2. Login using your Hugging Face Hub credentials, and create a new dataset repository:

.. code::

   huggingface-cli repo create your_dataset_name --type dataset

Add the ``-organization`` flag to create a repository under a specific organization:

.. code::

   huggingface-cli repo create your_dataset_name --type dataset --organization your-org-name

3. Install `Git LFS <https://git-lfs.github.com/>`_ and clone your repository:

.. code-block::

   # Make sure you have git-lfs installed
   # (https://git-lfs.github.com/)
   git lfs install

   git clone https://huggingface.co/datasets/username/your_dataset_name

4. Now is a good time to check your directory to ensure the only files you're uploading are:

* ``README.md`` is a Dataset card that describes the datasets contents, creation, and usage.

* ``your_dataset_name.py`` is your dataset loading script.

* ``dataset_infos.json`` contains metadata about the dataset.

* ``dummy_data`` holds a small subset of data from the dataset for tests and preview.

* Raw files of the dataset.

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

Canonical dataset
^^^^^^^^^^^^^^^^^

To share a canonical dataset:

1. Fork the 🤗 `Datasets repository <https://github.com/huggingface/datasets>`_ by clicking on the **Fork** button.

2. Clone your fork to your local disk, and add the base repository as a remote:

.. code-block::

   git clone https://github.com/<your_Github_handle>/datasets
   cd datasets
   git remote add upstream https://github.com/huggingface/datasets.git

3. Create a new branch to hold your changes. You can name the new branch using the short name of your dataset:

.. code::

   git checkout -b my-new-dataset

4. Set up a development environment by running the following command in a virtual environment:

.. code::

   pip install -e ".[dev]"

5. Create a new folder with the dataset name inside ``huggingface/datasets``, and add the dataset loading script you just created.

6. Run `Black <https://black.readthedocs.io/en/stable/index.html>`_ and `isort <https://pycqa.github.io/isort/>`_ to tidy up your code and files:

.. code-block::

   make style
   make quality

7. Add your changes, and make a commit to record your changes locally. Then you can push the changes to your account:

.. code-block::

   git add datasets/<my-new-dataset>
   git commit
   git push -u origin my-new-dataset

8. Go back to your fork on Github, and click on **Pull request** to open a pull request on the main 🤗 `Datasets repository <https://github.com/huggingface/datasets>`_ for review.