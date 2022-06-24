# How to add one (or several) new datasets to 🤗 Datasets

ADD DATASETS DIRECTLY ON THE 🤗 HUGGING FACE HUB !

You can share your dataset on https://huggingface.co/datasets directly using your account, see the documentation:

* [Create a dataset and upload files](https://huggingface.co/docs/datasets/upload_dataset)
* [Advanced guide using dataset scripts](https://huggingface.co/docs/datasets/share)

## What about the datasets scripts in this GitHub repository then ?

Datasets used to be hosted in this GitHub repository, but all datasets have now been migrated to the Hugging Face Hub.
The legacy GitHub datasets were added originally on the GitHub repository and therefore don't have a namespace: "squad", "glue", etc. unlike the other datasets that are named "username/dataset_name" or "org/dataset_name".
Those datasets are still maintained on GitHub, and if you'd like to edit them, please open a Pull Request on the huggingface/datasets repository.

Sharing your dataset to the Hub is the recommended way of adding a dataset.

In some rare cases it makes more sense to open a PR on GitHub. For example when you are not the author of the dataset and there is no clear organization / namespace that you can put the dataset under.

The following presents how to open a Pull Request on GitHub to add a new dataset to this repository.

## Add a new dataset to this repository (legacy)

### Start by preparing your environment

1. Fork the [repository](https://github.com/huggingface/datasets) by clicking on the 'Fork' button on the repository's page.
This creates a copy of the code under your GitHub user account.

2. Clone your fork to your local disk, and add the base repository as a remote:

	```bash
	git clone https://github.com/<your Github handle>/datasets
	cd datasets
	git remote add upstream https://github.com/huggingface/datasets.git
	```

3. (**For Windows**) You will need to install [the right version](https://pytorch.org/get-started/locally/) of PyTorch before continuing because `pip install torch` may not work well for PyTorch on Windows.

4. Set up a development environment, for instance by running the following command:

	```bash
	conda create -n env python=3.7 --y
	conda activate env
	pip install -e ".[dev]"
	```

5. Open the [online Datasets Tagging application](https://huggingface.co/spaces/huggingface/datasets-tagging).

6. You should also open the online form that will allow you to [create dataset cards](https://huggingface.co/datasets/card-creator/) in a browser window (courtesy of [Evrard t'Serstevens](https://huggingface.co/evrardts).)

Now you are ready, each time you want to add a new dataset, follow the steps in the following section:

### Adding a new dataset

#### Understand the structure of the dataset

1. Find a short-name for the dataset:

	- Select a `short name` for the dataset which is unique but not too long and is easy to guess for users, e.g. `squad`, `natural_questions`
	- Sometimes the short-list name is already given/proposed (e.g. in the spreadsheet of the data sprint to reach v2.0 if you are participating in the effort)

You are now ready to start the process of adding the dataset. We will create the following files:

- a **dataset script** which contains the code to download and pre-process the dataset: e.g. `squad.py`,
- a **dataset card** with tags and information on the dataset in a `README.md`.
- a **metadata file** (automatically created) which contains checksums and information about the dataset to guarantee that the loading went fine: `dataset_infos.json`
- a **dummy-data file** (automatically created) which contains small examples from the original files to test and guarantee that the script is working well in the future: `dummy_data.zip`

2. Let's start by creating a new branch to hold your development changes with the name of your dataset:

	```bash
	git fetch upstream
	git rebase upstream/master
	git checkout -b a-descriptive-name-for-my-changes
	```

	**Do not** work on the `master` branch.

3. Create your dataset folder under `datasets/<your_dataset_name>`:

	```bash
	mkdir ./datasets/<your_dataset_name>
	```

4. Open a new online [dataset card form](https://huggingface.co/datasets/card-creator/) to fill out: you will be able to download it to your dataset folder with the `Export` button when you are done. Alternatively, you can also manually create and edit a dataset card in the folder by copying the template:

	```bash
	cp ./templates/README.md ./datasets/<your_dataset_name>/README.md
	```

5. Now explore the dataset you have selected while completing some fields of the **dataset card** while you are doing it:

	- Find the research paper or description presenting the dataset you want to add
	- Read the relevant part of the paper/description presenting the dataset
	- Find the location of the data for your dataset
	- Download/open the data to see how it looks like
	- While you explore and read about the dataset, you can complete some sections of the dataset card (the online form or the one you have just created at `./datasets/<your_dataset_name>/README.md`). You can just copy the information you meet in your readings in the relevant sections of the dataset card (typically in `Dataset Description`, `Dataset Structure` and `Dataset Creation`).

		If you need more information on a section of the dataset card, a detailed guide is in the `README_guide.md` here: https://github.com/huggingface/datasets/blob/master/templates/README_guide.md.

		There is a also a (very detailed) example here: https://github.com/huggingface/datasets/tree/master/datasets/eli5.

		Don't spend too much time completing the dataset card, just copy what you find when exploring the dataset documentation. If you can't find all the information it's ok. You can always spend more time completing the dataset card while we are reviewing your PR (see below) and the dataset card will be open for everybody to complete them afterwards. If you don't know what to write in a section, just leave the `[More Information Needed]` text.


#### Write the loading/processing code

Now let's get coding :-)

The dataset script is the main entry point to load and process the data. It is a python script under `datasets/<your_dataset_name>/<your_dataset_name>.py`.

There is a detailed explanation on how the library and scripts are organized [here](https://huggingface.co/docs/datasets/master/about_dataset_load.html).

Note on naming: the dataset class should be camel case, while the dataset short_name is its snake case equivalent (ex: `class BookCorpus` for the dataset `book_corpus`).

To add a new dataset, you can start from the empty template which is [in the `templates` folder](https://github.com/huggingface/datasets/blob/master/templates/new_dataset_script.py):

```bash
cp ./templates/new_dataset_script.py ./datasets/<your_dataset_name>/<your_dataset_name>.py
```

And then go progressively through all the `TODO` in the template 🙂. If it's your first dataset addition and you are a bit lost among the information to fill in, you can take some time to read the [detailed explanation here](https://huggingface.co/docs/datasets/master/dataset_script.html).

You can also start (or copy any part) from one of the datasets of reference listed below. The main criteria for choosing among these reference dataset is the format of the data files (JSON/JSONL/CSV/TSV/text) and whether you need or don't need several configurations (see above explanations on configurations). Feel free to reuse any parts of the following examples and adapt them to your case:

- question-answering: [squad](https://github.com/huggingface/datasets/blob/master/datasets/squad/squad.py) (original data are in json)
- natural language inference: [snli](https://github.com/huggingface/datasets/blob/master/datasets/snli/snli.py) (original data are in text files with tab separated columns)
- POS/NER: [conll2003](https://github.com/huggingface/datasets/blob/master/datasets/conll2003/conll2003.py) (original data are in text files with one token per line)
- sentiment analysis: [allocine](https://github.com/huggingface/datasets/blob/master/datasets/allocine/allocine.py) (original data are in jsonl files)
- text classification: [ag_news](https://github.com/huggingface/datasets/blob/master/datasets/ag_news/ag_news.py) (original data are in csv files)
- translation: [flores](https://github.com/huggingface/datasets/blob/master/datasets/flores/flores.py) (original data come from text files - one per language)
- summarization: [billsum](https://github.com/huggingface/datasets/blob/master/datasets/billsum/billsum.py) (original data are in json files)
- benchmark: [glue](https://github.com/huggingface/datasets/blob/master/datasets/glue/glue.py) (original data are various formats)
- multilingual: [xquad](https://github.com/huggingface/datasets/blob/master/datasets/xquad/xquad.py) (original data are in json)
- multitask: [matinf](https://github.com/huggingface/datasets/blob/master/datasets/matinf/matinf.py) (original data need to be downloaded by the user because it requires authentication)
- speech recognition: [librispeech_asr](https://github.com/huggingface/datasets/blob/master/datasets/librispeech_asr/librispeech_asr.py) (original data is in .flac format)

While you are developing the dataset script you can list test it by opening a python interpreter and running the script (the script is dynamically updated each time you modify it):

```python
from datasets import load_dataset

data = load_dataset('./datasets/<your_dataset_name>')
```

This let you for instance use `print()` statements inside the script as well as seeing directly errors and the final dataset format.

**What are configurations and splits**

Sometimes you need to use several *configurations* and/or *splits* (usually at least splits will be defined).

* Using several **configurations** allow to have like sub-datasets inside a dataset and are needed in two main cases:

	- The dataset covers or group several sub-datasets or domains that the users may want to access independently and/or
	- The dataset comprise several sub-part with different features/organizations of the data (e.g. two types of CSV files with different types of columns). Inside a configuration of a dataset, all the data should have the same format (columns) but the columns can change across configurations.

* **Splits** are a more fine grained division than configurations. They allow you, inside a configuration of the dataset, to split the data in typically train/validation/test splits. All the splits inside a configuration should have the same columns/features and splits are thus defined for each specific configurations of there are several.


**Some rules to follow when adding the dataset**:

- try to give access to all the data, columns, features and information in the dataset. If the dataset contains various sub-parts with differing formats, create several configurations to give access to all of them.
- datasets in the `datasets` library are typed. Take some time to carefully think about the `features` (see an introduction [here](https://huggingface.co/docs/datasets/about_dataset_features.html) and the full list of possible features [here](https://huggingface.co/docs/datasets/package_reference/main_classes.html#features)
- if some of you dataset features are in a fixed set of classes (e.g. labels), you should use a `ClassLabel` feature.


**Last step:** To check that your dataset works correctly and to create its `dataset_infos.json` file run the command:

```bash
datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs
```

**Note:** If your dataset requires manually downloading the data and having the user provide the path to the dataset you can run the following command:
```bash
datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs --data_dir your/manual/dir
```
To have the configs use the path from `--data_dir` when generating them.

#### Automatically add code metadata

Now that your dataset script runs and create a dataset with the format you expected, you can add the JSON metadata and test data.

**Make sure you run all of the following commands from the root of your `datasets` git clone.**

1. To create the dummy data for continuous testing, there is a tool that automatically generates dummy data for you. At the moment it supports data files in the following format: txt, csv, tsv, jsonl, json, xml.

   If the extensions of the raw data files of your dataset are in this list, then you can automatically generate your dummy data with:

	```bash
	datasets-cli dummy_data datasets/<your-dataset-folder> --auto_generate
	```

	Example:

	```bash
	datasets-cli dummy_data ./datasets/snli --auto_generate
	```

    If your data files are not in the supported format, you can run the same command without the `--auto_generate` flag. It should give you instructions on the files to manually create (basically, the same ones as for the real dataset but with only five items).
	
	```bash
	datasets-cli dummy_data datasets/<your-dataset-folder>
	```

   If this doesn't work more information on how to add dummy data can be found in the documentation [here](https://huggingface.co/docs/datasets/dataset_script.html#dummy-data).

   If you've been fighting with dummy data creation without success for some time and can't seems to make it work: Go to the next step (open a Pull Request) and we'll help you cross the finish line 🙂.

2. Now test that both the real data and the dummy data work correctly using the following commands:

	*For the real data*:
	```bash
	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>
	```
	and

	*For the dummy data*:
	```bash
	RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>
	```

	On **Windows**, you may need to run:
	```
	$Env:RUN_SLOW = "1"
	pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>
	pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>
	```
	to enable the slow tests, instead of `RUN_SLOW=1`.

3. If all tests pass, your dataset works correctly. You can finally create the metadata JSON by running the command:

	```bash
	datasets-cli test datasets/<your-dataset-folder> --save_infos --all_configs
	```

	This first command should create a `dataset_infos.json` file in your dataset folder.


You have now finished the coding part, congratulation! 🎉 You are Awesome! 😎

Note: You can use the CLI tool from the root of the repository with the following command:
```bash
python src/datasets/commands/datasets_cli.py <command>
```

#### Open a Pull Request on the main HuggingFace repo and share your work!!

Here are the step to open the Pull-Request on the main repo.

1. Format your code. Run black, isort and flake8 so that your newly added files look nice with the following commands:

	```bash
	make style
	flake8 datasets
	```

	If you are on windows and `make style` doesn't work you can do the following steps instead:

	```bash
	pip install black
	pip install isort
	pip install flake8

	black --line-length 119 --target-version py36 datasets/your_dataset/your_dataset.py
	
	isort datasets/your_dataset/your_dataset.py

	flake8 datasets/your_dataset
	```

2. Make sure that you have a dataset card (more information in the [next section](#tag-the-dataset-and-write-the-dataset-card)) with:

    1. **Required:**
       - The YAML tags obtained with the [online Datasets Tagging app](https://huggingface.co/spaces/huggingface/datasets-tagging).
       - A description of the various fields in your dataset.
    2. Any relevant information you would like to share with users of your dataset in the appropriate paragraphs.
       - You can use the online [dataset card creator](https://huggingface.co/datasets/card-creator/)

3. Once you're happy with your dataset script file, add your changes and make a commit to record your changes locally:

	```bash
	git add datasets/<your_dataset_name>
	git commit
	```

	It is a good idea to sync your copy of the code with the original
	repository regularly. This way you can quickly account for changes:
	
	- If you haven't pushed your branch yet, you can rebase on upstream/master:

	  ```bash
	  git fetch upstream
	  git rebase upstream/master
	  ```
	  
	- If you have already pushed your branch, do not rebase but merge instead:
	
	  ```bash
	  git fetch upstream
	  git merge upstream/master
	  ```

   Push the changes to your account using:

   ```bash
   git push -u origin a-descriptive-name-for-my-changes
   ```

3. Once you are satisfied, go the webpage of your fork on GitHub. Click on "Pull request" to send your to the project maintainers for review.

Congratulation you have open a PR to add a new dataset 🙏

**Important note:** In order to merge your Pull Request the maintainers will require you to tag and add a dataset card. Here is now how to do this last step:

#### Tag the dataset and write the dataset card

Each dataset is provided with a dataset card.

The dataset card and in particular the tags which are on it are **really important** to make sure the dataset can be found on the hub and will be used by the users. Users need to have the best possible idea of what's inside the dataset and how it was created so that they can use it safely and have a good idea of the content.

Creating the dataset card goes in two steps:

1. **Tagging the dataset using the Datasets Tagging app**

   - Use the [online Datasets Tagging application](https://huggingface.co/spaces/huggingface/datasets-tagging).

   Enter the full path to your dataset folder on the left, and tag the different configs :-) (And don't forget to save to file after you're done with a config!)

2. **Copy the tags in the dataset card and complete the dataset card**

   - You can use the online [dataset card creator](https://huggingface.co/datasets/card-creator/)

   - **Essential:** Once you have saved the tags for all configs, you can expand the **Show YAML output aggregating the tags** section on the right, which will show you a YAML formatted block to put in the relevant section of the [online form](https://huggingface.co/datasets/card-creator/) (or manually  paste into your README.md).

   - **Very important as well:** On the right side of the tagging app, you will also find an expandable section called **Show Markdown Data Fields**. This gives you a starting point for the description of the fields in your dataset: you should paste it into the **Data Fields** section of the [online form](https://huggingface.co/datasets/card-creator/) (or your local README.md), then modify the description as needed. Briefly describe each of the fields and indicate if they have a default value (e.g. when there is no label). If the data has span indices, describe their attributes (character level or word level, contiguous or not, etc). If the datasets contains example IDs, state whether they have an inherent meaning, such as a mapping to other datasets or pointing to relationships between data points.

        Example from the [ELI5 card](https://github.com/huggingface/datasets/tree/master/datasets/eli5#data-fields):

            Data Fields:
                - q_id: a string question identifier for each example, corresponding to its ID in the Pushshift.io Reddit submission dumps.
                - subreddit: One of explainlikeimfive, askscience, or AskHistorians, indicating which subreddit the question came from
                - title: title of the question, with URLs extracted and replaced by URL_n tokens
                - title_urls: list of the extracted URLs, the nth element of the list was replaced by URL_n


   - **Very nice to have but optional for now:** Complete all you can find in the dataset card using the detailed instructions for completed it which are in the `README_guide.md` here: https://github.com/huggingface/datasets/blob/master/templates/README_guide.md.

		Here is a completed example: https://github.com/huggingface/datasets/tree/master/datasets/eli5 for inspiration

		If you don't know what to write in a field and can find it, write: `[More Information Needed]`

If you are using the online form, you can then click the `Export` button at the top to download a `README.md` file to your data folder. Once your `README.md` is ok you have finished all the steps to add your dataset, congratulation your Pull Request can be merged.

**You have made another dataset super easy to access for everyone in the community! 🤯**
