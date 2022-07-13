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

	**do not** work on the `main` branch.

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
	git rebase upstream/main
    ```

   Push the changes to your account using:

   ```bash
   git push -u origin a-descriptive-name-for-my-changes
   ```

8. Once you are satisfied, go the webpage of your fork on GitHub. Click on "Pull request" to send your to the project maintainers for review.

## How to add a dataset

You can share your dataset on https://huggingface.co/datasets directly using your account, see the documentation:

* [Create a dataset and upload files](https://huggingface.co/docs/datasets/upload_dataset)
* [Advanced guide using dataset scripts](https://huggingface.co/docs/datasets/share)

## How to contribute to the dataset cards

Improving the documentation of datasets is an ever increasing effort and we invite users to contribute by sharing their insights with the community in the `README.md` dataset cards provided for each dataset.

If you see that a dataset card is missing information that you are in a position to provide (as an author of the dataset or as an experienced user), the best thing you can do is to open a Pull Request on the Hugging Face Hub. To to do, go to the "Files and versions" tab of the dataset page and edit the `README.md` file. We provide:

* a [template](https://github.com/huggingface/datasets/blob/main/templates/README.md)
* a [guide](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md) describing what information should go into each of the paragraphs
* and if you need inspiration, we recommend looking through a [completed example](https://github.com/huggingface/datasets/blob/main/datasets/eli5/README.md)

Note that datasets that are outside of a namespace (`squad`, `imagenet-1k`, etc.) are maintained on GitHub. In this case you have to open a Pull request on GitHub to edit the file at `datasets/<dataset-name>/README.md`.

If you are a **dataset author**... you know what to do, it is your dataset after all ;) ! We would especially appreciate if you could help us fill in information about the process of creating the dataset, and take a moment to reflect on its social impact and possible limitations if you haven't already done so in the dataset paper or in another data statement.

If you are a **user of a dataset**, the main source of information should be the dataset paper if it is available: we recommend pulling information from there into the relevant paragraphs of the template. We also eagerly welcome discussions on the [Considerations for Using the Data](https://github.com/huggingface/datasets/blob/main/templates/README_guide.md#considerations-for-using-the-data) based on existing scholarship or personal experience that would benefit the whole community.

Finally, if you want more information on the how and why of dataset cards, we strongly recommend reading the foundational works [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) and [Data Statements for NLP](https://www.aclweb.org/anthology/Q18-1041/).

Thank you for your contribution!

## Code of conduct

This project adheres to the HuggingFace [code of conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
