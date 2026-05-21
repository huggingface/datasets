import numpy as np
import pandas as pd

import datasets


class SparseCsvConfig(datasets.BuilderConfig):
    """BuilderConfig for Sparse CSV."""

    def __init__(self, sep=",", chunksize=1_000, drop_id_column=True, **kwargs):
        """
        Initialize a BuilderConfig for Sparse CSV.
        Args:
            sep (str, optional): The separator used in the CSV file. Defaults to ','.
            chunksize (int, optional): Number of rows per chunk to read from the CSV file.
            drop_id_column (bool, optional): Whether to drop the 'id' column if it exists.
            **kwargs: Additional keyword arguments forwarded to the parent class.
        """
        super(SparseCsvConfig, self).__init__(**kwargs)
        self.sep = sep
        self.chunksize = chunksize
        self.drop_id_column = drop_id_column


class SparseCsv(datasets.GeneratorBasedBuilder):
    """
    High-performance Sparse CSV Reader.
    Parses wide CSVs (e.g. 100k columns) using Pandas chunks and Numpy vectorization
    to avoid the overhead of Python loops.
    """

    BUILDER_CONFIG_CLASS = SparseCsvConfig

    def _info(self):
        """
        Returns the dataset metadata (features, description, etc.).
        Returns:
            datasets.DatasetInfo: The dataset information object.
        """
        return datasets.DatasetInfo(
            description="Sparse CSV Reader for high-dimensional data.",
            features=datasets.Features(
                {
                    "row_id": datasets.Value("string"),
                    "indices": datasets.Sequence(datasets.Value("int32")),
                    "values": datasets.Sequence(datasets.Value("float32")),
                    "shape": datasets.Sequence(datasets.Value("int32"), length=2),
                }
            ),
        )

    def _split_generators(self, dl_manager):
        """
        Returns SplitGenerators for the dataset.
        Args:
            dl_manager (datasets.DownloadManager): Download manager to handle data files.
        Returns:
            list: List containing a single SplitGenerator for the training split.
        """
        if not self.config.data_files:
            raise ValueError("You must provide a data_file for SparseCsv dataset.")

        data_files = dl_manager.download_and_extract(self.config.data_files)
        splits = []
        if isinstance(data_files, dict):
            for split_name, files in data_files.items():
                if isinstance(files, str):
                    files = [files]
                splits.append(
                    datasets.SplitGenerator(
                        name=split_name,
                        gen_kwargs={"files": files},
                    )
                )
        else:
            if isinstance(data_files, str):
                data_files = [data_files]

            splits.append(
                datasets.SplitGenerator(
                    name=datasets.Split.TRAIN,
                    gen_kwargs={"files": data_files},
                )
            )
        return splits

    def _generate_examples(self, files):
        """
        Yields examples from the sparse CSV files.
        Args:
            files (list): List of file paths to process.
        Yields:
            tuple: (int, dict) where int is the row index and dict contains row_id, indices, values, and shape.
        """
        row_global_idx = 0
        for file_path in files:
            with pd.read_csv(file_path, sep=self.config.sep, chunksize=self.config.chunksize, iterator=True) as reader:
                for chunk in reader:
                    if self.config.drop_id_column:
                        # assume first column is 'id' and drop it
                        row_ids = chunk.iloc[:, 0].astype(str).values
                        data_chunk = chunk.iloc[:, 1:]
                    else:
                        row_ids = [str(i) for i in range(row_global_idx, row_global_idx + len(chunk))]
                        data_chunk = chunk

                    n_cols = data_chunk.shape[1]
                    mat = data_chunk.values
                    # Iterate numpy rows
                    for i in range(len(mat)):
                        row_vals = mat[i]
                        non_zero_indices = np.nonzero(row_vals)[0]
                        non_zero_values = row_vals[non_zero_indices]

                        yield (
                            row_global_idx,
                            {
                                "row_id": row_ids[i],
                                "indices": non_zero_indices.tolist(),
                                "values": non_zero_values.astype(np.float32).tolist(),
                                "shape": [1, n_cols],
                            },
                        )
                        row_global_idx += 1
