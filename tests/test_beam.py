import os
import tempfile
from unittest import TestCase

import datasets

from .utils import require_beam


if datasets.is_beam_available():
    import apache_beam as beam


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
                    os.path.join(
                        tmp_cache_dir, "dummy_beam_dataset", "default", "0.0.0", "dummy_beam_dataset-train.arrow"
                    )
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
                os.path.exists(
                    os.path.join(tmp_cache_dir, "dummy_beam_dataset", "default", "0.0.0", "dataset_info.json")
                )
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
                    os.path.join(
                        tmp_cache_dir, "nested_beam_dataset", "default", "0.0.0", "nested_beam_dataset-train.arrow"
                    )
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
                os.path.exists(
                    os.path.join(tmp_cache_dir, "nested_beam_dataset", "default", "0.0.0", "dataset_info.json")
                )
            )
            del dset
