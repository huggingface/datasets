from unittest import TestCase
from datasets import Dataset, DatasetDict, load_dataset
import time


REPO_NAME = "repo-{}".format(int(time.time() * 10e3))


class TestPushToHub(TestCase):
    def test_push_dataset_dict_to_hub(self):
        ds = Dataset.from_dict({
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        })

        local_ds = DatasetDict({
            "random": ds
        })

        ds_name = f"Jikiwa/test-{int(time.time() * 10e3)}"
        local_ds.push_to_hub(ds_name)
        hub_ds = load_dataset(ds_name, download_mode="force_redownload")

        self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
        self.assertListEqual(list(local_ds["random"].features.keys()), list(hub_ds["random"].features.keys()))
        self.assertDictEqual(local_ds["random"].features, hub_ds["random"].features)

    def test_push_dataset_to_hub(self):
        local_ds = Dataset.from_dict({
            "x": [1, 2, 3],
            "y": [4, 5, 6]
        })

        ds_name = f"Jikiwa/test-{int(time.time() * 10e3)}"
        local_ds.push_to_hub(ds_name, split_name="random")
        local_ds_dict = {"random": local_ds}
        hub_ds_dict = load_dataset(ds_name, download_mode="force_redownload")

        self.assertListEqual(list(local_ds_dict.keys()), list(hub_ds_dict.keys()))

        for ds_split_name in local_ds_dict.keys():
            local_ds = local_ds_dict[ds_split_name]
            hub_ds = hub_ds_dict[ds_split_name]
            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["random"].features.keys()), list(hub_ds["random"].features.keys()))
            self.assertDictEqual(local_ds["random"].features, hub_ds["random"].features)

