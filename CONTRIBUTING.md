# How to contribute to Datasets?
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](CODE_OF_CONDUCT.md)

Datasets is an open source project, so all contributions and suggestions are welcome.

You can contribute in many different ways: giving ideas, answering questions, reporting bugs, proposing enhancements, 
improving the documentation, fixing bugs,...

Many thanks in advance to every contributor.

In order to facilitate healthy, constructive behavior in an open and inclusive community, we all respect and abide by 
our [code of conduct](CODE_OF_CONDUCT.md).

## How to work on an open Issue?
You have the list of open Issues at: https://github.com/huggingface/datasets/issues

Some of them may have the label `help wanted`: that means that any contributor is welcomed!

If you would like to work on any of the open Issues:

1. Make sure it is not already assigned to someone else. You have the assignee (if any) on the top of the right column of the Issue page.

2. You can self-assign it by commenting on the Issue page with one of the keywords: `#take` or `#self-assign`.

3. Work on your self-assigned issue and eventually create a Pull Request.

## How to create a Pull Request?
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

5. Develop the features on your branch. If you want to add a dataset see more in-detail instructions in the section [*How to add a dataset*](#how-to-add-a-dataset). 

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

## How to add a dataset

A [more complete guide](https://github.com/huggingface/datasets/blob/master/ADD_NEW_DATASET.md) to adding a dataset was written for our December 2020 `datasets` sprint, we recommend reading through it before you start the process. Here is a summary of the steps described there:

1. Make sure you followed steps 1-4 of the section [*How to contribute to datasets?*](#how-to-contribute-to-datasets).

2. Create your dataset folder under `datasets/<your_dataset_name>` and create your dataset script under `datasets/<your_dataset_name>/<your_dataset_name>.py`. You can check out other dataset scripts under `datasets` for some inspiration. Note on naming: the dataset class should be camel case, while the dataset name is its snake case equivalent (ex: `class BookCorpus(datasets.GeneratorBasedBuilder)` for the dataset `book_corpus`).

3. **Make sure you run all of the following commands from the root of your `datasets` git clone.** To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

	```bash
	datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs
	```

4. If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

	```bash
	datasets-cli dummy_data datasets/<your-dataset-folder>
	```

	There is a tool that automatically generates dummy data for you. At the moment it supports data files in the following format: txt, csv, tsv, jsonl, json, xml.
	If the extensions of the raw data files of your dataset are in this list, then you can automatically generate your dummy data with:

	```bash
	datasets-cli dummy_data datasets/<your-dataset-folder> --auto_generate
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

6. Finally, take some time to document your dataset for other users. Each dataset should be accompanied by a `README.md` dataset card in its directory which describes the data and contains tags representing languages and tasks supported to be easily discoverable. You can find information on how to fill out the card either manually or by using our [web app](https://huggingface.co/datasets/card-creator/) in the following [guide](https://github.com/huggingface/datasets/blob/master/templates/README_guide.md).

7. If all tests pass, your dataset works correctly. Awesome! You can now follow steps 6, 7 and 8 of the section [*How to contribute to 🤗 Datasets?*](#how-to-contribute-to-Datasets). If you experience problems with the dummy data tests, you might want to take a look at the section *Help for dummy data tests* below.



### Help for dummy data tests

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command
	```bash
	datasets-cli dummy_data datasets/<your-dataset-folder>
	```
	and make sure you follow the exact instructions provided by the command of step 5).

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generators(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.

If you're looking for more details about dataset scripts creation, please refer to the [documentation](https://huggingface.co/docs/datasets/master/dataset_script).

Note: You can use the CLI tool from the root of the repository with the following command:
```bash
python src/datasets/commands/datasets_cli.py <command>
```

## How to contribute to the dataset cards

Improving the documentation of datasets is an ever increasing effort and we invite users to contribute by sharing their insights with the community in the `README.md` dataset cards provided for each dataset.

If you see that a dataset card is missing information that you are in a position to provide (as an author of the dataset or as an experienced user), the best thing you can do is to open a Pull Request with the updated `README.md` file. We provide:
- a [template](https://github.com/huggingface/datasets/blob/master/templates/README.md)
- a [guide](https://github.com/huggingface/datasets/blob/master/templates/README_guide.md) describing what information should go into each of the paragraphs
- and if you need inspiration, we recommend looking through a [completed example](https://github.com/huggingface/datasets/blob/master/datasets/eli5/README.md)

If you are a **dataset author**... you know what to do, it is your dataset after all ;) ! We would especially appreciate if you could help us fill in information about the process of creating the dataset, and take a moment to reflect on its social impact and possible limitations if you haven't already done so in the dataset paper or in another data statement.

If you are a **user of a dataset**, the main source of information should be the dataset paper if it is available: we recommend pulling information from there into the relevant paragraphs of the template. We also eagerly welcome discussions on the [Considerations for Using the Data](https://github.com/huggingface/datasets/blob/master/templates/README_guide.md#considerations-for-using-the-data) based on existing scholarship or personal experience that would benefit the whole community.

Finally, if you want more information on the how and why of dataset cards, we strongly recommend reading the foundational works [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) and [Data Statements for NLP](https://www.aclweb.org/anthology/Q18-1041/).

Thank you for your contribution!

## Code of conduct

This project adheres to the HuggingFace [code of conduct](CODE_OF_CONDUCT.md). 
By participating, you are expected to uphold this code.
