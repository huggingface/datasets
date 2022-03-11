from unittest.mock import patch

import datasets
from datasets import Dataset


def test_enable_disable_progress_bar():
    dset = Dataset.from_dict({"col_1": [3, 2, 0, 1]})

    with patch("tqdm.auto.tqdm") as mock_tqdm:
        datasets.disable_progress_bar()
        dset.map(lambda x: {"col_2": x["col_1"] + 1})
        mock_tqdm.assert_not_called()

        mock_tqdm.reset_mock()

        datasets.enable_progress_bar()
        dset.map(lambda x: {"col_2": x["col_1"] + 1})
        mock_tqdm.assert_called()
