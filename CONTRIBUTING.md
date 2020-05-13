# How to Contribute

## How to add a dataset

1. **Add in private repo: tensorflow-datasets**
  - Create a `tensorflow_datasets/text/<your_dataset_name>.py` file. Look at how other datasets were added, e.g. `tensorflow_datasets/text/wikitext.py`
  - Create an *empty* checksum file: `tensorflow_datasets/url_checksums/<your_dataset_name>.txt`
  - Add an import statement in `tensorflow_datasets/text/__init__.py`. Looking at the other import statements it is easy to see what should be done here
  - Run `python -m tensorflow_datasets.scripts.download_and_prepare --register_checksums --datasets=<your_dataset_name>`
  - Adapt your `tensorflow_datasets/text/<your_dataset_name>.py` file and rerun `python -m tensorflow_datasets.scripts.download_and_prepare --register_checksums --datasets=<your_dataset_name>` until no errors appear anymore, which means that you dataset can succesfully be loaded!
  - Add a test file: `tensorflow_datasets/text/<your_dataset_name>_test.py` and create dummy data. Look at how it's done for other examples.
  - The dummy data should consists of the *same folder structure* than the one that is created when downloading the dataset from the official website
  - Add dummy data that consists of a) A dummy *train* and/or *test* and/or *validation* data file in the format as the real one has and for each dummy data file a *.json* file having the exact same output then the one that you expect to get.
  
2. **Add to nlp repo**
  - Execute the conversion script in the nlp repo as follows: `python nlp-cli convert --tfds_directory <path/to/tensorflow_datasets/text> --tfds_rel_filename <your_dataset_name>.py --nlp_directory <path/to/nlp/datasets/nlp>`
  - Now you should have a converted file in the folder `nlp/datasets/nlp/<your_dataset_name>/<your_dataset_name>.py`.
  - Upload the folder to aws. To get access to aws, first ask Julien. Make sure you don't accidently delete anything here. Use the command `aws s3 cp <path/to/nlp/datasets/nlp/<your_dataset_name>/<your_dataset_name>.py s3://datasets.huggingface.co/nlp/<your_dataset_name>/<your_dataset_name>.py`
  - Make sure that your object has public read access on AWS. Otherwise it cannot be downloaded.
  - Awesome, your dataset can now be used with nlp. You should try out that everything works as expected by opening a python shell and loading your dataset: 
     ```python 
     import nlp
     dataset = nlp.load_dataset("your_dataset_name")
     ...
     ```
