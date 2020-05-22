## Description

This file explains how to add a dataset.

Cicle-ci should always be green so that we can be sure that newly added datasets are functional. 

## How-To-Add a dataset

**Before adding a dataset make sure that your branch is up to date**:
1. `git checkout add_datasets`
2. `git pull`

**Add a dataset** 

Make sure you run all of the following commands from the root of your `nlp` git clone.

1) Create your dataset folder under `datasets/<your_dataset_name>`
2) Create your dataset script under `datasets/<your_dataset_name>/<your_dataset_name>.py`. You can check out other dataset scripts under `datasets` for some inspiration.
3) Make sure that your dataset works correctly and create its `dataset_infos.json` file using the command:

```bash
python nlp-cli test datasets/<your-dataset-folder> --save_checksums --all_configs
```

4) Run black and isort on your newly added datascript files so that they look nice:

```bash
make style
```

5) If the command was succesful, you should now create some dummy data. Use the following command to get in-detail instructions on how to create the dummy data:

```bash
python nlp-cli dummy_data datasets/<your-dataset-folder> 
```

6) Now test that both the real data and the dummy data work correctly using the following commands:

*For the real data*:
```bash
RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_real_dataset_<your-dataset-name>
```
and 

*For the dummy data*:
```bash
RUN_SLOW=1 pytest tests/test_dataset_common.py::LocalDatasetTest::test_load_dataset_all_configs_<your-dataset-name>
```

7) push to this PR and rerun the circle ci workflow to check whether circle ci stays green.

### Help for dummy data tests

Follow these steps in case the dummy data test keeps failing:

- Verify that all filenames are spelled correctly. Rerun the command 
	```bash
	python nlp-cli dummy_data datasets/<your-dataset-folder> 
	```
	and make sure you follow the exact instructions provided by the command of step 5). 

- Your datascript might require a difficult dummy data structure. In this case make sure you fully understand the data folder logit created by the function `_split_generations(...)` and expected by the function `_generate_examples(...)` of your dataset script. Also take a look at `tests/README.md` which lists different possible cases of how the dummy data should be created.

- If the dummy data tests still fail, open a PR in the repo anyways and make a remark in the description that you need help creating the dummy data.
