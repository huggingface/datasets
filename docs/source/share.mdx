# Share

At Hugging Face, we are on a mission to democratize good Machine Learning and we believe in the value of open source. That's why we designed 🤗 Datasets so that anyone can share a dataset with the greater ML community. There are currently thousands of datasets in over 100 languages in the Hugging Face Hub, and the Hugging Face team always welcomes new contributions!

Dataset repositories offer features such as:

- Free dataset hosting
- Dataset versioning
- Commit history and diffs
- Metadata for discoverability
- Dataset cards for documentation, licensing, limitations, etc.

This guide will show you how to share a dataset that can be easily accessed by anyone.

<a id='upload_dataset_repo'></a>

## Add a dataset

You can share your dataset with the community with a dataset repository on the Hugging Face Hub.
It can also be a private dataset if you want to control who has access to it.

In a dataset repository, you can either host all your data files and/or use a dataset script.

The dataset script is optional if your dataset is in one of the following formats: CSV, JSON, JSON lines, text or Parquet.
The script also supports many kinds of compressed file types such as: GZ, BZ2, LZ4, LZMA or ZSTD.
For example, your dataset can be made of `.json.gz` files.

On the other hand, if your dataset is not in a supported format or if you want more control over how your dataset is loaded, you can write your own dataset script.

When loading a dataset from the Hub:

- If there's no dataset script, all the files in the supported formats are loaded.
- If there's a dataset script, it is downloaded and executed to download and prepare the dataset.

For more information on how to load a dataset from the Hub, take a look at the [load a dataset from the Hub](./load_hub) tutorial.

### Create the repository

Sharing a community dataset will require you to create an account on [hf.co](https://huggingface.co/join) if you don't have one yet.
You can directly create a [new dataset repository](https://huggingface.co/login?next=%2Fnew-dataset) from your account on the Hugging Face Hub, but this guide will show you how to upload a dataset from the terminal.

1. Make sure you are in the virtual environment where you installed Datasets, and run the following command:

```
huggingface-cli login
```

2. Login using your Hugging Face Hub credentials, and create a new dataset repository:

```
huggingface-cli repo create your_dataset_name --type dataset
```

Add the `-organization` flag to create a repository under a specific organization:

```
huggingface-cli repo create your_dataset_name --type dataset --organization your-org-name
```

### Clone the repository

3. Install [Git LFS](https://git-lfs.github.com/) and clone your repository:

```
# Make sure you have git-lfs installed
# (https://git-lfs.github.com/)
git lfs install

git clone https://huggingface.co/datasets/namespace/your_dataset_name
```

Here the `namespace` is either your username or your organization name.

### Prepare your files

4. Now is a good time to check your directory to ensure the only files you're uploading are:

- The raw data files of the dataset (optional, if they are hosted elsewhere you can specify the URLs in the dataset script). If you don't need a dataset script, you can take a look at [how to structure your dataset repository for your data files](repository_structure).

- `your_dataset_name.py` is your dataset loading script (optional if your data files are already in the supported formats csv/jsonl/json/parquet/txt). To create a dataset script, see the [dataset script](dataset_script) page.

### Upload your files

You can directly upload your files to your repository on the Hugging Face Hub, but this guide will show you how to upload the files from the terminal.

5. It is important to add the large data files first with `git lfs track` or else you will encounter an error later when you push your files:

```
cp /somewhere/data/*.json .
git lfs track *.json
git add .gitattributes
git add *.json
git commit -m "add json files"
```

6. Add the dataset loading script:

```
cp /somewhere/data/load_script.py .
git add --all
```

7. Verify the files have been correctly staged. Then you can commit and push your files:

```
git status
git commit -m "First version of the your_dataset_name dataset."
git push
```

Congratulations, your dataset has now been uploaded to the Hugging Face Hub where anyone can load it in a single line of code! 🥳

```
dataset = load_dataset("namespace/your_dataset_name")
```

Finally, don't forget to create a dataset card to document your dataset and make it discoverable! Check out the [Create a dataset card](dataset_card) guide to learn more.

### Ask for a help and reviews

If you need help with a dataset script, feel free to check the [datasets forum](https://discuss.huggingface.co/c/datasets/10): it's possible that someone had similar issues and shared how they managed to fix them.

Then if your script is ready and if you wish your dataset script to be reviewed by the Hugging Face team, you can open a discussion in the Community tab of your dataset with this message:

```
# Dataset rewiew request for <Dataset name>

## Description

<brief description of the dataset>

## Files to review

- file1
- file2
- ...

cc @lhoestq @polinaeterna @mariosasko @albertvillanova
```

Members of the Hugging Face team will be happy to review your dataset script and give you advice.

## Datasets on GitHub (legacy)

Datasets used to be hosted on our GitHub repository, but all datasets have now been migrated to the Hugging Face Hub.

The legacy GitHub datasets were added originally on our GitHub repository and therefore don't have a namespace on the Hub: "squad", "glue", etc. unlike the other datasets that are named "username/dataset_name" or "org/dataset_name".

<Tip>

The distinction between a Hub dataset within or without a namespace only comes from the legacy sharing workflow. It does not involve any ranking, decisioning, or opinion regarding the contents of the dataset itself.

</Tip>

Those datasets are now maintained on the Hub: if you think a fix is needed, please use their "Community" tab to open a discussion or create a Pull Request.
The code of these datasets is reviewed by the Hugging Face team.
