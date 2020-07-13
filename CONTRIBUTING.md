# How to contribute to nlp?

1. Fork the [repository](https://github.com/huggingface/nlp) by clicking on the 'Fork' button on the repository's page. This creates a copy of the code under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

	```bash
	git clone git@github.com:<your Github handle>/nlp.git
	cd nlp
	git remote add upstream https://github.com/huggingface/nlp.git
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

   (If transformers was already installed in the virtual environment, remove
   it with `pip uninstall transformers` before reinstalling it in editable
   mode with the `-e` flag.)

   Right now, we need an unreleased version of `isort` to avoid a
   [bug](https://github.com/timothycrosley/isort/pull/1000):

   ```bash
   $ pip install -U git+git://github.com/timothycrosley/isort.git@e63ae06ec7d70b06df9e528357650281a3d3ec22#egg=isort
   ```

5. Develop the features on your branch. If you want to add a dataset see more in-detail intsructions in the section *How to add a dataset*.

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

1. Make sure you followed steps 1-4 of the section *How to contribute to nlp?*.

2. Create your dataset folder under `datasets/<your_dataset_name>` and create your dataset script under `datasets/<your_dataset_name>/<your_dataset_name>.py`. You can check out other dataset scripts under `datasets` for some inspiration. Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: `class BookCorpus(nlp.GeneratorBasedBuilder)` for the dataset `book_corpus`).

3. **Make sure you run all of the following commands from the root of your `nlp` git clone.**. To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

	```bash
	python nlp-cli test datasets/<your-dataset-folder> --save_infos --all_configs
	```

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

	```bash
	python nlp-cli dummy_data datasets/<your-dataset-folder>
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

6. If all tests pass, your dataset works correctly. Awesome! You can now follow steps 6, 7 and 8 of the section *How to contribute to nlp?*. If you experience problems with the dummy data tests, you might want to take a look at the section *Help for dummy data tests* below.


### Help for dummy data tests

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command
	```bash
	python nlp-cli dummy_data datasets/<your-dataset-folder>
	```
	and make sure you follow the exact instructions provided by the command of step 5).

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generators(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.
