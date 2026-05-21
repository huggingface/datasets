import importlib.util
import os
import tempfile
import unittest

import numpy as np
import pandas as pd
import pytest

from datasets import load_dataset
from datasets.utils.sparse import sparse_collate_fn


class TestSparseCsv(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "test_data.csv")
        # 5 rows, 10 columns. Mostly zeros.
        # Row 0: ID="row0", [0, 1.0, 0, ..., 0]
        # Row 1: ID="row1", [0, 0, 2.5, ..., 0]
        data = np.zeros((5, 10))
        data[0, 1] = 1.0
        data[1, 2] = 2.5
        data[2, 0] = 3.0
        data[2, 9] = 4.0
        # Rows 3 and 4 remain all zeros
        self.original_data = data
        df = pd.DataFrame(data, columns=[f"col_{i}" for i in range(10)])
        df.insert(0, "id", [f"row{i}" for i in range(5)])

        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_sparse_csv(self):
        """Test if the dataset loads and matches the schema"""
        ds = load_dataset(
            "sparse_csv",
            data_files=self.csv_path,
            split="train",
            drop_id_column=True,
        )
        self.assertEqual(len(ds), 5)
        self.assertEqual(ds[0]["row_id"], "row0")

        # Check first row correctness (should be index 1, val 1.0)
        self.assertEqual(ds[0]["indices"], [1])
        self.assertEqual(ds[0]["values"], [1.0])
        self.assertEqual(ds[0]["shape"], [1, 10])
        self.assertEqual(ds[1]["values"], [2.5])

        # Check row with multiple values
        self.assertEqual(ds[2]["indices"], [0, 9])
        self.assertEqual(ds[2]["values"], [3.0, 4.0])

    @pytest.mark.skipif(
        importlib.util.find_spec("torch") is None,
        reason="PyTorch is not installed, skipping Torch collate test.",
    )
    def test_collate_torch(self):
        """Test if sparse_collate_fn produces correct Torch tensors."""
        ds = load_dataset(
            "sparse_csv",
            data_files=self.csv_path,
            split="train",
        )
        batch = [ds[i] for i in range(len(ds))]
        tensor = sparse_collate_fn(batch, target_library="torch")

        self.assertTrue(tensor.is_sparse)
        self.assertEqual(tensor.shape, (5, 10))

        dense_tensor = tensor.to_dense().numpy()
        np.testing.assert_allclose(dense_tensor, self.original_data, atol=1e-5)

    @pytest.mark.skipif(
        importlib.util.find_spec("scipy") is None,
        reason="Scipy is not installed, skipping scipy collate test.",
    )
    def test_collate_scipy(self):
        ds = load_dataset(
            "sparse_csv",
            data_files=self.csv_path,
            split="train",
        )
        batch = [ds[i] for i in range(len(ds))]
        matrix = sparse_collate_fn(batch, target_library="scipy")

        # Check integrity
        self.assertEqual(matrix.shape, (5, 10))
        # Convert to dense array and compare
        dense_matrix = matrix.toarray()
        np.testing.assert_allclose(dense_matrix, self.original_data, atol=1e-5)
