# How to add one (or several) new dataset(s) to Datasets?

## Start by preparing your environment

1. Fork the [repository](https://github.com/huggingface/datasets) by clicking on the 'Fork' button on the repository's page.
This creates a copy of the code under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

	```bash
	git clone git@github.com:<your Github handle>/datasets.git
	cd datasets
	git remote add upstream https://github.com/huggingface/datasets.git
	```

3. Set up a development environment, for instance by running the following command:

	```bash
	conda create -n env python=3.7 --y
	pip install -e ".[dev]"
	```

## Start adding a new dataset

### First step: understand the structure of the dataset

1. Start by preparing the field and understanding how the dataset look like:

	- Find the research paper or description presenting the dataset you want to add (if there is an associated research paper)
	- Find the location of the data for you dataset
	- Read the relevant part of the paper or description presenting the dataset
	- Open the data to see how they look

2. Define the name of the dataset:

	- Select a `short name` for the dataset which is unique but not too long and is easy to guess for users, e.g. `squad`, `natural_questions`

	- understand if the dataset is created by a single institution (all the authors belong the same company/team, e.g. `Google`)

		- if it's the case, the dataset will then be in the related organization folder, e.g. `google/natural_questions`
		- if it's not the case, the dataset will be at the root, e.g. `squad`

3. See if there is a need for several *configurations* and/or *splits* (usually at least splits will be defined).

	* Using several **configurations** allow to have like sub-datasets inside a dataset and are needed in two main cases:

		- The dataset covers or group several sub-datasets or domains that the users may want to access independantly and/or
		- The dataset comprise several sub-part with different features/organizations of the data (e.g. two types of CSV files with different types of columns). Inside a configuration of a dataset, all the data should have the same format (columns) but the columns can change accross configurations.

	* **Splits** are a more fine grained division than configurations. They allow you, inside a configuration of the dataset, to split the data in typically train/validation/test splits. All the splits inside a configuration should have the same columns/features and splits are thus defined for each specific configurations of there are several.


You are now ready to start the process of adding the dataset. We will basically create the following files:

	- a dataset script, e.g. `squad.py` which will contain the code to download and pre-process the dataset
	- a dataset cart, `README.md` which will contain general informations and tags related to the dataset

And automatically create the following additional meta-data files (using the CLI tools):

	- a metadata file `dataset_configs.json` which will contain checksums and informations about the dataset to garantee that the loading went fine.
	- a dummy-data file `dummy_data.zip` which will contain small example original files to garantee that the loading script is working well in the future.

### Second step: start writing some code

Let's get started.

1. Create a new branch to hold your development changes with the name of your dataset:

	```bash
	git checkout -b a-descriptive-name-for-my-changes
	```

	**do not** work on the `master` branch.

2. Create your dataset folder under `datasets/<your_dataset_name>` and create your dataset script under `datasets/<your_dataset_name>/<your_dataset_name>.py`. You can check out other dataset scripts under `datasets` for some inspiration. Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: `class BookCorpus(datasets.GeneratorBasedBuilder)` for the dataset `book_corpus`).

3. **Make sure you run all of the following commands from the root of your `datasets` git clone.** To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

	```bash
	python datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs
	```

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

	```bash
	python datasets-cli dummy_data datasets/<your-dataset-folder>
	```

5. Now test that both the real data and the dummy data work correctly using the following commands:

	*For the real data*:
	```bash
	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>
	```
	and

	*For the dummy data*:
	```bash
	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>
	```

6. If all tests pass, your dataset works correctly. Awesome! You can now follow steps 6, 7 and 8 of the section [*How to contribute to 🤗Datasets?*](#how-to-contribute-to-🤗Datasets). If you experience problems with the dummy data tests, you might want to take a look at the section *Help for dummy data tests* below.

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command
	```bash
	python datasets-cli dummy_data datasets/<your-dataset-folder>
	```
	and make sure you follow the exact instructions provided by the command of step 5).

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generators(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.

6. Format your code. Run black and isort so that your newly added files look nice with the following command:

	```bash
	make style
	```

7. Once you're happy with your dataset script file, add your changes and make a commit to record your changes locally:

	```bash
	git add datasets/<your_dataset_name>
	git commit
	```

	It is a good idea to sync your copy of the code with the original
	repository regularly. This way you can quickly account for changes:

	```bash
	git fetch upstream
	git rebase upstream/master
    ```

   Push the changes to your account using:

   ```bash
   git push -u origin a-descriptive-name-for-my-changes
   ```

8. Once you are satisfied, go the webpage of your fork on GitHub. Click on "Pull request" to send your to the project maintainers for review.

## How-To-Add a dataset
1. Make sure you followed steps 1-4 of the section [*How to contribute to datasets?*](#how-to-contribute-to-datasets).

