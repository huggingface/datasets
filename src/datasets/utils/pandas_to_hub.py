from datasets import Dataset, load_dataset

def register_pandas():
    """
    Enables `pandas.DataFrame` objects to directly push to the hub or loaded from the hub.
    
    Example::

        >>> df = pd.DataFrame.from_dict({"test": [1,2,3]})
        >>> df.push_to_hub("my_dataset")

        >>> loaded_df = df.load_from_hub("my_user/my_dataset")
    """
    from pandas.core.frame import DataFrame
    
    def push_to_hub(dataframe: DataFrame, repo_id: str, **push_to_hub_kwargs):
        """Pushes the dataset to the hub.
        The dataset is pushed using HTTP requests and does not need to have neither git or git-lfs installed.

        Args:
            repo_id (:obj:`str`):
                The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
                `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
                of the logged-in user.
        """
        ds = Dataset.from_pandas(dataframe)
        ds.push_to_hub(repo_id, **push_to_hub_kwargs)
        
    def load_from_hub(repo_id, split="train", **loading_kwargs):
        """Loads a dataset from the hub into a DataFrame.
        Args:
            repo_id (:obj:`str`):
                The ID of the repository to push to in the following format: `<user>/<dataset_name>` or
                `<org>/<dataset_name>`. Also accepts `<dataset_name>`, which will default to the namespace
                of the logged-in user.
            split (:obj:`str`): Which split of the data to load.
        """
        ds = load_dataset(repo_id, split=split, **loading_kwargs)
        ds.set_format("pandas")
        return ds[:]
    
    DataFrame.push_to_hub = push_to_hub
    DataFrame.load_from_hub = load_from_hub