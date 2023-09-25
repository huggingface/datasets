import os
import tempfile
from functools import partial
from unittest import TestCase
from unittest.mock import patch

import datasets
import datasets.config

from .utils import require_beam


class DummyBeamDataset(datasets.BeamBasedBuilder):
    """Dummy beam dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features({"content": datasets.Value("string")}),
            # No default supervised_keys.
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager, pipeline):
        return [datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"examples": get_test_dummy_examples()})]

    def _build_pcollection(self, pipeline, examples):
        import apache_beam as beam

        return pipeline | "Load Examples" >> beam.Create(examples)


class NestedBeamDataset(datasets.BeamBasedBuilder):
    """Dummy beam dataset."""

    def _info(self):
        return datasets.DatasetInfo(
            features=datasets.Features({"a": datasets.Sequence({"b": datasets.Value("string")})}),
            # No default supervised_keys.
            supervised_keys=None,
        )

    def _split_generators(self, dl_manager, pipeline):
        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"examples": get_test_nested_examples()})
        ]

    def _build_pcollection(self, pipeline, examples):
        import apache_beam as beam

        return pipeline | "Load Examples" >> beam.Create(examples)


def get_test_dummy_examples():
    return [(i, {"content": content}) for i, content in enumerate(["foo", "bar", "foobar"])]


def get_test_nested_examples():
    return [(i, {"a": {"b": [content]}}) for i, content in enumerate(["foo", "bar", "foobar"])]


class BeamBuilderTest(TestCase):
    @require_beam
    def test_download_and_prepare(self):
        expected_num_examples = len(get_test_dummy_examples())
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = DummyBeamDataset(cache_dir=tmp_cache_dir, beam_runner="DirectRunner")
            builder.download_and_prepare()
            self.assertTrue(
                os.path.exists(
                    os.path.join(tmp_cache_dir, builder.name, "default", "0.0.0", f"{builder.name}-train.arrow")
                )
            )
            self.assertDictEqual(builder.info.features, datasets.Features({"content": datasets.Value("string")}))
            dset = builder.as_dataset()
            self.assertEqual(dset["train"].num_rows, expected_num_examples)
            self.assertEqual(dset["train"].info.splits["train"].num_examples, expected_num_examples)
            self.assertDictEqual(dset["train"][0], get_test_dummy_examples()[0][1])
            self.assertDictEqual(
                dset["train"][expected_num_examples - 1], get_test_dummy_examples()[expected_num_examples - 1][1]
            )
            self.assertTrue(
                os.path.exists(os.path.join(tmp_cache_dir, builder.name, "default", "0.0.0", "dataset_info.json"))
            )
            del dset

    @require_beam
    def test_download_and_prepare_sharded(self):
        import apache_beam as beam

        original_write_parquet = beam.io.parquetio.WriteToParquet

        expected_num_examples = len(get_test_dummy_examples())
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = DummyBeamDataset(cache_dir=tmp_cache_dir, beam_runner="DirectRunner")
            with patch("apache_beam.io.parquetio.WriteToParquet") as write_parquet_mock:
                write_parquet_mock.side_effect = partial(original_write_parquet, num_shards=2)
                builder.download_and_prepare()
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_cache_dir, builder.name, "default", "0.0.0", f"{builder.name}-train-00000-of-00002.arrow"
                    )
                )
            )
            self.assertTrue(
                os.path.exists(
                    os.path.join(
                        tmp_cache_dir, builder.name, "default", "0.0.0", f"{builder.name}-train-00000-of-00002.arrow"
                    )
                )
            )
            self.assertDictEqual(builder.info.features, datasets.Features({"content": datasets.Value("string")}))
            dset = builder.as_dataset()
            self.assertEqual(dset["train"].num_rows, expected_num_examples)
            self.assertEqual(dset["train"].info.splits["train"].num_examples, expected_num_examples)
            # Order is not preserved when sharding, so we just check that all the elements are there
            self.assertListEqual(sorted(dset["train"]["content"]), sorted(["foo", "bar", "foobar"]))
            self.assertTrue(
                os.path.exists(os.path.join(tmp_cache_dir, builder.name, "default", "0.0.0", "dataset_info.json"))
            )
            del dset

    @require_beam
    def test_no_beam_options(self):
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = DummyBeamDataset(cache_dir=tmp_cache_dir)
            self.assertRaises(datasets.builder.MissingBeamOptions, builder.download_and_prepare)

    @require_beam
    def test_nested_features(self):
        expected_num_examples = len(get_test_nested_examples())
        with tempfile.TemporaryDirectory() as tmp_cache_dir:
            builder = NestedBeamDataset(cache_dir=tmp_cache_dir, beam_runner="DirectRunner")
            builder.download_and_prepare()
            self.assertTrue(
                os.path.exists(
                    os.path.join(tmp_cache_dir, builder.name, "default", "0.0.0", f"{builder.name}-train.arrow")
                )
            )
            self.assertDictEqual(
                builder.info.features, datasets.Features({"a": datasets.Sequence({"b": datasets.Value("string")})})
            )
            dset = builder.as_dataset()
            self.assertEqual(dset["train"].num_rows, expected_num_examples)
            self.assertEqual(dset["train"].info.splits["train"].num_examples, expected_num_examples)
            self.assertDictEqual(dset["train"][0], get_test_nested_examples()[0][1])
            self.assertDictEqual(
                dset["train"][expected_num_examples - 1], get_test_nested_examples()[expected_num_examples - 1][1]
            )
            self.assertTrue(
                os.path.exists(os.path.join(tmp_cache_dir, builder.name, "default", "0.0.0", "dataset_info.json"))
            )
            del dset
