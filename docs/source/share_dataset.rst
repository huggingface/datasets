Sharing your dataset
=============================================

Once you've written a new dataset loading script as detailed on the :doc:`add_dataset` page, you may want to share it with the community for instance on the `HuggingFace Hub <https://huggingface.co/datasets>`__.

There are two options to do that:
- add it as a canonical dataset by opening a pull-request on the `GitHub repository for 🤗nlp <https://github.com/huggingface/nlp>`__,
- directly upload it on the Hub as a community provided dataset.

Here are the main differences between these two options.

- **Community provided** datasets:
	* are faster to share (no reviewing process)
	* can contain the data files themselves on the Hub
	* are identified under the namespace of a user or organization: ``thomwolf/my_dataset`` or ``huggingface/our_dataset``
	* are flagged as ``unsafe`` by default because a dataset contains executable code so the users need to inspect and opt-in to use the datasets

- **Canonical** datasets:
	* are solwer to add (need to go through the reviewing process on the githup repo)
	* are identified under the root namespace (``my_dataset``) so they need to select a shortname which is still free
	* usually don't contain the data files which are retrieved from the original URLs (but this can be changed under specific request to add the files to the Hub)
	* are flagged as ``safe`` by default since they went through the reviewing process (no need to opt-in).

.. note::

	The distinctions between "canonical" and "community provided" datasets is made purely based on the selected sharing workflow and don't involve any ranking, decision or opinion regarding the content of the dataset it-self.

.. _canonical-dataset:

Sharing a "canonical" dataset
--------------------------------

To add a "canonical" dataset to the library, you need to do the following steps:

1. Fork the `🤗nlp repository <https://github.com/huggingface/nlp>`__ by clicking on the 'Fork' button on the repository's home page. This creates a copy of the code under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

.. code::

	git clone https://github.com/<your_Github_handle>/nlp
	cd nlp
	git remote add upstream https://github.com/huggingface/nlp.git


3. Create a new branch to hold your development changes:

.. code::

	git checkout -b my-new-dataset

.. note::

	**do not** work on the ``master`` branch.

4. Set up a development environment by running the following command **in a virtual environment**:

.. code::

	pip install -e ".[dev]"

.. note::

   If 🤗nlp was already installed in the virtual environment, remove
   it with ``pip uninstall nlp`` before reinstalling it in editable
   mode with the ``-e`` flag.

   Right now, we need an unreleased version of ``isort`` to avoid a
   `bug <https://github.com/timothycrosley/isort/pull/1000>`__:

.. code-block::

   pip install -U git+git://github.com/timothycrosley/isort.git@e63ae06ec7d70b06df9e528357650281a3d3ec22#egg=isort

5. Create a new folder with your dataset name inside the `datasets folder <https://github.com/huggingface/nlp/tree/master/datasets>`__ of the repository and add the dataset script you wrote and tested while following the instruction on the :doc:`add_dataset` page. 

6. Format your code. Run black and isort so that your newly added files look nice with the following command:

.. code::

	make style
	make quality


7. Once you're happy with your dataset script file, add your changes and make a commit to record your changes locally:

.. code::

	git add datasets/<my-new-dataset>
	git commit

	It is a good idea to sync your copy of the code with the original
	repository regularly. This way you can quickly account for changes:

.. code::

	git fetch upstream
	git rebase upstream/master

   Push the changes to your account using:

.. code::

   git push -u origin my-new-dataset

8. We also recommanded to add **tests** and **metadata** to the dataset script if possible. To generate these files go read the :ref:`adding-tests` section.

9. Once you are satisfied with the dataset, go the webpage of your fork on GitHub and cick on "Pull request" to open a pull-request on the `main github repository <https://github.com/huggingface/nlp>`__ for review.

.. _community-dataset:

Sharing a "community provided" dataset
-----------------------------------------

[UNDER CONSTRUCTION]


.. _adding-tests:

Adding tests and metadata to the dataset
---------------------------------------------

It's recommended to add testing data and checksum metadata to your dataset so it's behavior can be tested and verified, and the generated dataset can be certified.

In this section we'll explain how you can add two objects to the repository for that:

- ``dummy data`` which are used for testing the behavior of the script (without having to download the full data files), and

- ``dataset_infos.json`` which are metadata used to store the matedata of the dataset including the data files checksums and the number of exampes which can used to confirm that the dataset generation procedure went well.

.. note::

	In the rest of this section, you should make sure that you run all of the commands **from the root** of your local ``nlp`` repository.

Adding metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can check that the new dataset loading script works correctly and create the ``dataset_infos.json`` file at the same time by running the command:

.. code-block::

	python nlp-cli test datasets/<your-dataset-folder> --save_infos --all_configs

If the command was succesful, you should now have a ``dataset_infos.json`` file created in the folder of your dataset loading script.

Here is a dummy example of the content for a dataset with a single configuration:

.. code-block::

	{
		"default": {
			"description": "The Text REtrieval Conference (TREC) Question Classification dataset contains 5500 ...\n",
			"citation": "@inproceedings{li-roth-2002-learning,\n    title = \"Learning Question Classifiers\",..\",\n}\n",
			"homepage": "https://cogcomp.seas.upenn.edu/Data/QA/QC/",
			"license": "",
			"features": {
				"label-coarse": {
					"num_classes": 6,
					"names": ["DESC", "ENTY", "ABBR", "HUM", "NUM", "LOC"],
					"names_file": null,
					"id": null,
					"_type": "ClassLabel"
				},
				"text": {
					"dtype": "string",
					"id": null,
					"_type": "Value"
				}
			},
			"supervised_keys": null,
			"builder_name": "trec",
			"config_name": "default",
			"version": {
				"version_str": "1.1.0", "description": null,
				"nlp_version_to_prepare": null,
				"major": 1, "minor": 1, "patch": 0
			},
			"splits": {
				"train": {
					"name": "train",
					"num_bytes": 385090,
					"num_examples": 5452,
					"dataset_name": "trec"
				},
				"test": {
					"name": "test",
					"num_bytes": 27983,
					"num_examples": 500,
					"dataset_name": "trec"
				}
			},
			"download_checksums": {
				"http://cogcomp.org/Data/QA/QC/train_5500.label": {
					"num_bytes": 335858,
					"checksum": "9e4c8bdcaffb96ed61041bd64b564183d52793a8e91d84fc3a8646885f466ec3"
				},
				"http://cogcomp.org/Data/QA/QC/TREC_10.label": {
					"num_bytes": 23354,
					"checksum": "033f22c028c2bbba9ca682f68ffe204dc1aa6e1cf35dd6207f2d4ca67f0d0e8e"
				}
			},
			"download_size": 359212,
			"dataset_size": 413073,
			"size_in_bytes": 772285
		}
	}

Adding tests dummy data
^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have the metadata prepared we can also create some dummy data for automated testing. You can use the following command to get in-detail instructions on how to create the dummy data:

.. code-block::

	python nlp-cli dummy_data datasets/<your-dataset-folder> 

This command will output instructions which are specifically tailored for your dataset and will look like:

.. code-block::

	==============================DUMMY DATA INSTRUCTIONS==============================
	- In order to create the dummy data for my-dataset, please go into the folder './datasets/my-dataset/dummy/1.1.0' with `cd ./datasets/my-dataset/dummy/1.1.0` . 

	- Please create the following dummy data files 'dummy_data/TREC_10.label, dummy_data/train_5500.label' from the folder './datasets/my-dataset/dummy/1.1.0'

	- For each of the splits 'train, test', make sure that one or more of the dummy data files provide at least one example 

	- If the method `_generate_examples(...)` includes multiple `open()` statements, you might have to create other files in addition to 'dummy_data/TREC_10.label, dummy_data/train_5500.label'. In this case please refer to the `_generate_examples(...)` method 

	-After all dummy data files are created, they should be zipped recursively to 'dummy_data.zip' with the command `zip -r dummy_data.zip dummy_data/` 

	-You can now delete the folder 'dummy_data' with the command `rm -r dummy_data` 

	- To get the folder 'dummy_data' back for further changes to the dummy data, simply unzip dummy_data.zip with the command `unzip dummy_data.zip` 

	- Make sure you have created the file 'dummy_data.zip' in './datasets/my-dataset/dummy/1.1.0' 
	===================================================================================


Now test that both the real data and the dummy data work correctly.

Go back to **the root of your nlp** folder and use the following command:

*For the real data*:

.. code-block::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>

	and 

*For the dummy data*:

.. code-block::

	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>


If all tests pass, your dataset works correctly. Awesome! You can now follow the last steps of the :ref:`canonical-dataset` or :ref:`community-dataset` sections to share the dataset with the community.

If you experienced problems with the dummy data tests, here are some additional tips:

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command 

.. code-block::

		python nlp-cli dummy_data datasets/<your-dataset-folder> 

and make sure you follow the exact instructions provided by the command. 

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function ``_split_generations(...)`` and expected by the function ``_generate_examples(...)`` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the main repository on github and make a remark in the description that you need help creating the dummy data and we will be happy to help you.
