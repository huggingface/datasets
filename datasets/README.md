## Description

This file explains how to add a dataset.

Cicle-ci should always be green so that we can be sure that newly added datasets are functional. 

## How-To-Add a dataset

**Before adding a dataset make sure that your branch is up to date**:
1. `git checkout add_datasets`
2. `git pull`

**Add a dataset via the `convert_dataset.sh` bash script:**  

Running `bash convert_dataset.sh <file/to/tfds/datascript.py>` (*e.g.* `bash convert_dataset.sh ../tensorflow-datasets/tensorflow_datasets/text/movie_rationales.py`) will automatically run all the steps mentioned in **Add a dataset manually** below. 

Make sure that you run `convert_dataset.sh` from the root folder of `nlp`.

The conversion script should work almost always for step 1): "convert dataset script from tfds to nlp format" and 2) "create checksum file" and step 3) "make style".

It can also sometimes automatically run step 4) "create the correct dummy data from tfds", but this will only work if a) there is either no config name or only one config name and b) the `tfds testing/test_data/fake_example` is in the correct form.

Nevertheless, the script should always be run in the beginning until an error occurs to be more efficient. 

If the conversion script does not work or fails at some step, then you can run the steps manually as follows:

**Add a dataset manually** 

Make sure you run all of the following commands from the root of your `nlp` git clone.
Also make sure that you changed to this branch:
```
git checkout add_datasets
```

1) the tfds datascript file should be converted to `nlp` style:

```
python nlp-cli convert --tfds_path <path/to/tensorflow_datasets/text/your_dataset_name>.py --nlp_directory datasets
```

This will convert the tdfs script and create a folder with the correct name.

2) the checksum file should be added. Use the command:
```
python nlp-cli test datasets/<your-dataset-folder> --save_checksums --all_configs
```

A checksums.txt file should be created in your folder and the structure should look as follows:

squad/
├── squad.py/
└── urls_checksums/
...........└── checksums.txt

Delete the created `*.lock` file afterward - it should not be uploaded to AWS.

3) run black and isort on your newly added datascript files so that they look nice:

```
make style
```

4) the dummy data should be added. For this it might be useful to take a look into the structure of other examples as shown in the PR here and at `<path/to/tensorflow_datasets/testing/test_data/test_data/fake_examples>` whether the same  data can be used.

5) check whether all works as expected using: 

**Important**
You have to delete the local cache with `rm -r ~/.cache/huggingface/datasets/*` to not run into "file exists" errors. TODO (PATRICK) should fix this in code... 

```
RUN_SLOW=1 pytest tests/test_dataset_common.py::DatasetTest::test_load_real_dataset_local_<your-dataset-name>
```
and 
```
RUN_SLOW=1 pytest tests/test_dataset_common.py::DatasetTest::test_load_dataset_all_configs_local_<your-dataset-name>
```

6) push to this PR and rerun the circle ci workflow to check whether circle ci stays green.

7) Edit this commend and tick off your newly added dataset :-) 

## TODO-list

- [ ] boolq - *weird download link*
- [ ] c4 - *beam dataset*
