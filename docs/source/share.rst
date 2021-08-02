Share
======

At Hugging Face, we are on a mission to democratize NLP and we believe in the significance of open source. That's why we designed Datasets so that anyone can share a dataset with the greater NLP community. There are currently over 900 datasets in over 100 languages, and the Hugging Face team always welcomes new submissions! 🤗

This guide will show you how to add a dataset or metric that can be easily accessed by anyone in the community. The guide includes instructions for:

* how to add dataset and metric metadata
* how to download data files
* how to generate samples
* how to compute a metric
* how to upload a dataset to the Hub

Open the `SQuAD dataset loading script <https://github.com/huggingface/datasets/blob/master/datasets/squad/squad.py>`_ template to follow along on how to share a dataset.

.. tip::

    To help you get started, try beginning with the `dataset loading script template <https://github.com/huggingface/datasets/blob/master/templates/new_dataset_script.py>`_.

Add dataset attributes
----------------------

The first step is to add some information, or attributes, about your dataset with the :func:`datasets.DatasetBuilder._info` method. The most important attributes you should specify are:

1. :obj:`datasets.DatasetInfo.description` provides a concise description of your dataset that informs the user what's in the dataset, how it was collected, and how it can be used for a NLP task.

2. :obj:`datasets.DatasetInfo.features` defines the name and type of each column in your dataset. This will also provide the structure for each example, so you can create nested subfields in each column if you want. Take a look at the `reference <https://huggingface.co/docs/datasets/package_reference/main_classes.html#datasets.DatasetInfo>`_ for a full list of feature types you can use.

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

3. :obj:`datasets.DatasetInfo.homepage` contains a URL to the datasets homepage so users can find more about detailed information about it.

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

In some cases, your dataset may have multiple configurations. For example, the `SuperGLUE <https://huggingface.co/datasets/super_glue>`_ dataset is a collection of 5 datasets designed to evaluate more difficult language understanding tasks. Datasets provides the :class:`datasets.BuilderConfig` that allows you to provide different configurations for the user to select from.

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

2. Add additional attributes to a configuration by sub-classing the base :class:`datasets.BuilderConfig`. This provides more flexibility for specifying the name and description of each configuration. These sub-classes should be listed under :obj:`datasets.DatasetBuilder.BUILDER_CONFIGS`:

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
            ]

3. Now, users can load a specific configuration of the dataset with the configuration ``name``:

   .. code-block::

        from datasets import load_dataset
        dataset = load_dataset('super_glue', 'boolq')


Default configurations
^^^^^^^^^^^^^^^^^^^^^^

Users must specify a configuration name when they load a dataset with multiple configurations. Otherwise, a ``ValueError`` is raised and Datasets will prompt the user to select a configuration name. You can avoid this by setting a default dataset configuration with the :attr:`datasets.DatasetBuilder.DEFAULT_CONFIG_NAME` attribute:

.. code-block::

    class NewDataset(datasets.GeneratorBasedBuilder):

    VERSION = datasets.Version("1.1.0")

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="first_domain", version=VERSION, description="This part of my dataset covers a first domain"),
        datasets.BuilderConfig(name="second_domain", version=VERSION, description="This part of my dataset covers a second domain"),
    ]

    DEFAULT_CONFIG_NAME = "first_domain"

.. tip::

    Only use a default configuration when it makes sense. Don't use it because it may be more convenient for the user to not specify a configuration when they load your dataset. For example, multi-lingual datasets often have a separate configuration for each language. An appropriate default may be an aggregated configuration that loads all the languages of the dataset if the user doesn't request a particular language.

Download data files and organize splits
---------------------------------------

After you've defined the metadata of your dataset, the next step is to download the data files and organize them according to their splits. 

1. Create a dictionary of URLs in the loading script that point to the original SQuAD data files:

   .. code-block::

        _URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/"
            _URLS = {
                "train": _URL + "train-v1.1.json",
                "dev": _URL + "dev-v1.1.json",
            }

2. The :obj:`datasets.DownloadManager.download_and_extract` method takes this dictionary and downloads the data files. Once the files are downloaded, :func:`datasets.SplitGenerator` organizes each split in the dataset. This is a simple class that contains:

    * The :obj:`name` of each split. You should use the standard split names: :obj:`datasets.Split.TRAIN`, :obj:`datasets.Split.TEST`, and :obj:`datasets.Split.VALIDATION`.

    * :obj:`gen_kwargs` provides the filepaths to the data files to load for each split.

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

So far you have added the dataset metadata, provided instructions for how to download the data files, and organized the splits. The next step is to actually generate the samples in each split. 

1. The :obj:`datasets.DatasetBuilder._generate_examples` method takes the filepath provided by :obj:`gen_kwargs` to read and parse the data files. You need to write a function that loads the data files and extracts the columns.

2. This should yield a tuple of an ``id_`` and an example from the dataset.

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

We strongly recommend adding testing data and checksum metadata to your dataset to verify and test its behavior. This ensures the generated dataset matches your expectations. This section will show you how to generate two files:

* ``dataset_infos.json`` stores the dataset metadata inclduing the data file checksums, and the number of examples required to confirm the dataset was properly generated.

* ``dummy_data`` is a file used to test the behavior of the loading script without having to download the full dataset.

.. important::

    Make sure you run all of the following commands **from the root** of your local ``datasets`` repository.

Dataset metadata
^^^^^^^^^^^^^^^^

1. Run the following command to create the metadata file, ``dataset_infos.json``. This will also make sure your new dataset loading script works correctly.

   .. code-block::

        datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs

2. If your dataset loading script behaved normally, you should now have a ``dataset_infos.json`` file in your dataset folder. This file will contain information about the dataset like its ``features`` and ``download_size``.

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

.. code-block::

    datasets-cli dummy_data datasets/<your-dataset-folder> --auto_generate

Manual
""""""

If your data files are not among the supported formats, you will need to generate your dummy data manually. Run the command below which will output detailed instructions on how to create the dummy data:

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

    Sometimes you may struggle with manually creating dummy data. Make sure you follow the instructions from the command ``datasets-cli dummy_data datasets/<your-dataset-folder>``. If you are still unable to succesfully generate your dummy data, open a `Pull Request <https://github.com/huggingface/datasets/pulls>`_ and we will be happy to help you out!

Test
^^^^

The last step is to actually test dataset generation with the real and dummy data. Test the real data by:

.. code-block::

    RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your_dataset_name>

And to test the dummy data:

.. code-block::

    RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your_dataset_name>

If both tests pass, your dataset was correctly generated! 🤗

Dataset card
------------

Each dataset should be accompanied with a Dataset card to promote responsible usage, and alert the user to any potential biases within the dataset. This idea is inspired by the Model Cards proposed by `Mitchell, 2018 <https://arxiv.org/abs/1810.03993>`_. Dataset cards help users understand the contents of the dataset, context for how the dataset should be used, how it was created, and considerations for using the dataset. This guide shows you how to create your own Dataset card.

1. Create a new Dataset card by opening the `online card creator <https://huggingface.co/datasets/card-creator/>`_, or manually copying the template:

   .. code-block::

        cp ./templates/README.md ./datasets/<your_dataset_name>/README.md

2. Next, you need to generate the structured tags. These help users discover your dataset on the Hub. Create the tags with the `online tagging app <https://huggingface.co/datasets/tagging/>`_, or you can clone and install the `Dataset tagging app <https://github.com/huggingface/datasets-tagging>`_ locally.

3. Select the appropriate tags for your dataset from the dropdown menus, and save the file once you are done.

4. Expand the **Show YAML output aggregating the tags** section on the right, copy the YAML tags, and paste it under the matching section on the online form. Paste the tags into your ``README.md`` file if you manually created your Dataset card.

5. Expand the **Show Markdown Data Fields** section, paste it into the **Data Fields** section under **Data Structure** on the online form (or your local ``README.md``). Modify the descriptions as needed, and briefly describe each of the fields.

6. Fill out the Dataset card to the best of your ability. Refer to the `Dataset Card Creation Guide <https://github.com/huggingface/datasets/blob/master/templates/README_guide.md>`_ for more detailed information about each section of the card. For fields you are unable to complete, you can write **[More Information Needed]**.

7. Once you are done filling out the card with the online form, click the **Export** button to download the Dataset card. Place it in the same folder as your dataset.

Upload
------

The final step is to upload your dataset! There are two types of datasets based on your sharing workflow: community and canonical datasets. The main differences between the two are highlighted in the table below:

.. list-table::
    :header-rows: 1

    * - Canonical datasets
      - Community datasets
    * - Faster to share, no review process.
      - Slower to add, needs to be reviewed.
    * - Data files can be stored on the Hub.
      - Data files are typically retrieved from the original URLs.
    * - Identified by a user or organization namespace like `thomwolf/my_dataset` or `huggingface/our_dataset`.
      - Identified by a root namepsace, need to select a short name that is available.
    * - Flagged as `unsafe` because the dataset contains executable code.
      - Flagged as `safe` because the dataset has been reviewed.

.. important::

    The distinction between a canonical and community dataset is based solely on the selected sharing workflow. It does not involve any ranking, decisioning, or opinion regarding the contents of the dataset itself.

.. _upload_dataset_repo:

Community dataset
^^^^^^^^^^^^^^^^^

Sharing a community dataset will require you to create an account on `hf.co <https://huggingface.co/join>`_ if you don't already have one. You can directly create a `new dataset repository <https://huggingface.co/new-dataset>`_ from your account on the Datasets Hub, but this guide will show you how to upload a dataset from the terminal.

1. Make sure you are in the virtual environment where you installed Datasets, and run the following command:

   .. code-block::

        huggingface-cli login

2. Login using your Datasets Hub credentials, and create a new dataset repository:

   .. code-block::

        huggingface-cli repo create your_dataset_name --type dataset

    If you want to create a repository under a specific organization, add the ``-organization`` flag:

   .. code-block::

        huggingface-cli repo create your_dataset_name --type dataset --organization your-org-name

3. Install `Git LFS <https://git-lfs.github.com/>`_ and clone your repository:

   .. code-block::

        # Make sure you have git-lfs installed
        # (https://git-lfs.github.com/)
        git lfs install

        git clone https://huggingface.co/datasets/username/your_dataset_name

4. Now is a good time to check your directory to ensure the only files you are uploading to the Hub are:

   * ``README.md`` is a Dataset card that describes the datasets contents, creation, and usage.

   * ``your_dataset_name.py`` is your dataset loading script.

   * ``dataset_infos.json`` contains the metadata about the dataset.

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

7. Verify the files have been correctly staged, then you can commit and push your files:

   .. code-block::

        git status
        git commit -m "First version of the your_dataset_name dataset."
        git push


Congratulations, your dataset has now been uploaded to the Datasets Hub where anyone can load it with a single line of code! 🤗

.. code-block::

    dataset = load_dataset("namespace/your_dataset_name")

Canonical dataset
^^^^^^^^^^^^^^^^^

To share a canonical dataset:

1. Fork the `Datasets repository <https://github.com/huggingface/datasets>`_ by clicking on the **Fork** button.

2. Clone your fork to your local disk, and add the base repository as a remote:

   .. code-block::

        git clone https://github.com/<your_Github_handle>/datasets
        cd datasets
        git remote add upstream https://github.com/huggingface/datasets.git

3. Create a new branch to hold your changes. You can name the new branch using the short name of your dataset:

   .. code-block::

        git checkout -b my-new-dataset

4. Set up a development environment by running the following command in a virtual environment:

   .. code-block::

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

8. Go back to your fork on Github, and click on **Pull request** to open a pull request on the main repository for review.

Metric
------

Just like datasets, you can share your own custom metric or a new metric with the community. To help you get started, open the `SQuAD metric loading script <https://github.com/huggingface/datasets/blob/master/metrics/squad/squad.py>`_ and follow along.

.. tip::

    To help you get started, try beginning with the `metric loading script template <https://github.com/huggingface/datasets/blob/master/templates/new_metric_script.py>`_.

Add metric attributes
^^^^^^^^^^^^^^^^^^^^^

Start by adding some information about your metric with :func:`datasets.Metric._info`. The most important attributes you should specify are:

1. :attr:`datasets.MetricInfo.description` provides a brief description about your metric.

2. :attr:`datasets.MetricInfo.citation` contains a BibTex citation for the metric.

3. :attr:`datasets.MetricInfo.inputs_description` describes the expected inputs and outputs. It may also provide some example usage of the metric.

4. :attr:`datasets.MetricInfo.features` defines the name and type of the predictions and references.

After you've filled out all these fields in the template, it should look like the following example from the SQuAD metric script:

.. code-block::

    class Squad(datasets.Metric):
    def _info(self):
        return datasets.MetricInfo(
            description=_DESCRIPTION,
            citation=_CITATION,
            inputs_description=_KWARGS_DESCRIPTION,
            features=datasets.Features(
                {
                    "predictions": {"id": datasets.Value("string"), "prediction_text": datasets.Value("string")},
                    "references": {
                        "id": datasets.Value("string"),
                        "answers": datasets.features.Sequence(
                            {
                                "text": datasets.Value("string"),
                                "answer_start": datasets.Value("int32"),
                            }
                        ),
                    },
                }
            ),
            codebase_urls=["https://rajpurkar.github.io/SQuAD-explorer/"],
            reference_urls=["https://rajpurkar.github.io/SQuAD-explorer/"],
        )

Download metric files
^^^^^^^^^^^^^^^^^^^^^

If your metric needs to download, or retrieve local files, you will need to use the :func:`datasets.Metric._download_and_prepare` method. For this example, let's examine the `BLEURT metric loading script <https://github.com/huggingface/datasets/blob/master/metrics/bleurt/bleurt.py>`_. 

1. You should provide a dictionary of URLs that point to the metric files:

   .. code-block::

        CHECKPOINT_URLS = {
        "bleurt-tiny-128": "https://storage.googleapis.com/bleurt-oss/bleurt-tiny-128.zip",
        "bleurt-tiny-512": "https://storage.googleapis.com/bleurt-oss/bleurt-tiny-512.zip",
        "bleurt-base-128": "https://storage.googleapis.com/bleurt-oss/bleurt-base-128.zip",
        "bleurt-base-512": "https://storage.googleapis.com/bleurt-oss/bleurt-base-512.zip",
        "bleurt-large-128": "https://storage.googleapis.com/bleurt-oss/bleurt-large-128.zip",
        "bleurt-large-512": "https://storage.googleapis.com/bleurt-oss/bleurt-large-512.zip",
        }
        
.. hint::

    If the files are stored locally, provide a dictionary of path(s) instead of URLs.

2. The :func:`datasets.Metric._download_and_prepare` method will take the URLs and download the metric file specified:

   .. code-block::

        def _download_and_prepare(self, dl_manager):

            # check that config name specifies a valid BLEURT model
            if self.config_name == "default":
                logger.warning(
                    "Using default BLEURT-Base checkpoint for sequence maximum length 128. "
                    "You can use a bigger model for better results with e.g.: datasets.load_metric('bleurt', 'bleurt-large-512')."
                )
                self.config_name = "bleurt-base-128"
            if self.config_name not in CHECKPOINT_URLS.keys():
                raise KeyError(
                    f"{self.config_name} model not found. You should supply the name of a model checkpoint for bleurt in {CHECKPOINT_URLS.keys()}"
                )

            # download the model checkpoint specified by self.config_name and set up the scorer
            model_path = dl_manager.download_and_extract(CHECKPOINT_URLS[self.config_name])
            self.scorer = score.BleurtScorer(os.path.join(model_path, self.config_name))


Compute score
^^^^^^^^^^^^^

The :func:`datasets.DatasetBuilder._compute` method defines how to compute a metric given the predictions and references. Now let's return to the SQuAD metric loading script.

1. Provide a method(s) for :func:`datasets.DatasetBuilder._compute` to calculate your metric:

   .. code-block::

        def simple_accuracy(preds, labels):
        return (preds == labels).mean().item()
        ...
        ...
        def acc_and_f1(preds, labels):
            acc = simple_accuracy(preds, labels)
            f1 = f1_score(y_true=labels, y_pred=preds).item()
            return {
                "accuracy": acc,
                "f1": f1,
            }
        ...
        ...
        def pearson_and_spearman(preds, labels):
            pearson_corr = pearsonr(preds, labels)[0].item()
            spearman_corr = spearmanr(preds, labels)[0].item()
            return {
                "pearson": pearson_corr,
                "spearmanr": spearman_corr,
            }

2. Create :func:`datasets.DatasetBuilder._compute` with instructions for what metric to calculate for each configuration:

   .. code-block::

        def _compute(self, predictions, references):
            if self.config_name == "cola":
                return {"matthews_correlation": matthews_corrcoef(references, predictions)}
            elif self.config_name == "stsb":
                return pearson_and_spearman(predictions, references)
            elif self.config_name in ["mrpc", "qqp"]:
                return acc_and_f1(predictions, references)
            elif self.config_name in ["sst2", "mnli", "mnli_mismatched", "mnli_matched", "qnli", "rte", "wnli", "hans"]:
                return {"accuracy": simple_accuracy(predictions, references)}
            else:
                raise KeyError(
                    "You should supply a configuration name selected in "
                    '["sst2", "mnli", "mnli_mismatched", "mnli_matched", '
                    '"cola", "stsb", "mrpc", "qqp", "qnli", "rte", "wnli", "hans"]'
                )

Test
^^^^

Once you're finished with your metric loading script, try to load it locally:

    >>> from datasets import load_metric
    >>> metric = load_metric('PATH/TO/MY/SCRIPT.py')