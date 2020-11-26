# How to contribute to Datasets?

1. Fork the [repository](https://github.com/huggingface/datasets) by clicking on the 'Fork' button on the repository's page. This creates a copy of the code under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

	```bash
	git clone git@github.com:<your Github handle>/datasets.git
	cd datasets
	git remote add upstream https://github.com/huggingface/datasets.git
	```

3. Create a new branch to hold your development changes:

	```bash
	git checkout -b a-descriptive-name-for-my-changes
	```

	**do not** work on the `master` branch.

4. Set up a development environment by running the following command in a virtual environment:

	```bash
	pip install -e ".[dev]"
	```

   (If datasets was already installed in the virtual environment, remove
   it with `pip uninstall datasets` before reinstalling it in editable
   mode with the `-e` flag.)

5. Develop the features on your branch. If you want to add a dataset see more in-detail intsructions in the section [*How to add a dataset*](#how-to-add-a-dataset). Alternatively, you can follow the steps to [add a dataset](https://huggingface.co/docs/datasets/add_dataset.html) and [share a dataset](https://huggingface.co/docs/datasets/share_dataset.html) in the documentation.

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

2. Create your dataset folder under `datasets/<your_dataset_name>` and create your dataset script under `datasets/<your_dataset_name>/<your_dataset_name>.py`. You can check out other dataset scripts under `datasets` for some inspiration. Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: `class BookCorpus(datasets.GeneratorBasedBuilder)` for the dataset `book_corpus`).

3. **Make sure you run all of the following commands from the root of your `datasets` git clone.** To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

	```bash
	python datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs
	```

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

	```bash
	python datasets-cli dummy_data datasets/<your-dataset-folder>
	```
	
	There is a tool that automatically generates dummy data for you. At the moment it supports data files in the following format: txt, csv, tsv, jsonl, json, xml.
	If the extensions of the raw data files of your dataset are in this list, then you can automatically generate your dummy data with:

	```bash
	python datasets-cli dummy_data datasets/<your-dataset-folder> --auto_generate
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


### Help for dummy data tests

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command
	```bash
	python datasets-cli dummy_data datasets/<your-dataset-folder>
	```
	and make sure you follow the exact instructions provided by the command of step 5).

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generators(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.

If you're looking for more details about dataset scripts creation, please refer to the [documentation](https://huggingface.co/docs/datasets/add_dataset.html).
