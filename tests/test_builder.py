import os
import tempfile
from unittest import TestCase

from nlp.arrow_dataset import Dataset
from nlp.arrow_writer import ArrowWriter
from nlp.builder import DatasetBuilder
from nlp.dataset_dict import DatasetDict
from nlp.features import Features, Value
from nlp.info import DatasetInfo
from nlp.splits import SplitDict, SplitInfo


class DummyBuilder(DatasetBuilder):
    def _info(self):
        return DatasetInfo()


class BuilderTest(TestCase):
    def test_as_dataset(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            dummy_builder = DummyBuilder(cache_dir=tmp_dir, name="dummy")
            os.makedirs(dummy_builder.cache_dir)

            dummy_builder.info.splits = SplitDict()
            dummy_builder.info.splits.add(SplitInfo("train"))
            dummy_builder.info.splits.add(SplitInfo("test"))

            for split in dummy_builder.info.splits:
                writer = ArrowWriter(
                    path=os.path.join(dummy_builder.cache_dir, f"dummy_builder-{split}.arrow"),
                    features=Features({"text": Value("string")}),
                )
                writer.write_batch({"text": ["foo"] * 10})
                writer.finalize()

            dsets = dummy_builder.as_dataset()
            self.assertIsInstance(dsets, DatasetDict)

            dset = dummy_builder.as_dataset("train")
            self.assertIsInstance(dset, Dataset)

            dset = dummy_builder.as_dataset("train+test[:30%]")
            self.assertIsInstance(dset, Dataset)
