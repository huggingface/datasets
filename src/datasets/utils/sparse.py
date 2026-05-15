from typing import Dict, Sequence

import numpy as np


def sparse_collate_fn(batch: Sequence[Dict[str, str | float | int]], target_library: str = "torch"):
    """
    Collate a batch of sparse row dictionaries into a sparse tensor for the specified library.
    Args:
        batch (Sequence[Dict]): List of examples, each with 'indices', 'values', and 'shape' fields.
        target_library (str, optional): Target library for the sparse tensor. Supported: 'torch', 'scipy'. Defaults to 'torch'.
    Returns:
        torch.sparse_coo_tensor or scipy.sparse.csr_matrix: The collated sparse tensor in the requested format.
        Returns None if the batch is empty.
    Raises:
        ValueError: If an unsupported target_library is specified.
    """
    # 1. Extract metadata
    batch_size = len(batch)
    if batch_size == 0:
        return None

    # We assume all rows have the same number of columns (the 'shape' feature)
    # The SparseCsv builder stores shape as [1, n_cols], so we take shape[1]
    n_cols = batch[0]["shape"][1]

    all_values = []
    all_col_indices = []
    batch_row_indices = []

    csr_indptr = [0]
    cumulative_nnz = 0
    for i, example in enumerate(batch):
        vals = example["values"]
        idxs = example["indices"]
        all_values.extend(vals)
        all_col_indices.extend(idxs)
        count = len(vals)
        batch_row_indices.extend([i] * count)
        cumulative_nnz += count
        csr_indptr.append(cumulative_nnz)

    np_values = np.array(all_values, dtype=np.float32)
    np_col_indices = np.array(all_col_indices, dtype=np.int64)
    np_row_indices = np.array(batch_row_indices, dtype=np.int64)

    if target_library == "torch":
        import torch

        indices = torch.stack([torch.from_numpy(np_row_indices), torch.from_numpy(np_col_indices)])
        values = torch.from_numpy(np_values)

        return torch.sparse_coo_tensor(indices=indices, values=values, size=(batch_size, n_cols))
    elif target_library == "scipy":
        from scipy.sparse import csr_matrix

        return csr_matrix((np_values, np_col_indices, csr_indptr), shape=(batch_size, n_cols))
    else:
        raise ValueError(f"Unsupported target_library: {target_library}. Choose from: torch, scipy.")
