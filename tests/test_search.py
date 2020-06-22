from unittest import TestCase
from unittest.mock import patch

import faiss
import numpy as np
import pyarrow as pa
from elasticsearch import Elasticsearch

from nlp.arrow_dataset import Dataset
from nlp.arrow_reader import BaseReader
from nlp.info import DatasetInfo
from nlp.search import DenseIndex, SparseIndex
from nlp.splits import SplitDict, SplitInfo


class ReaderTester(BaseReader):
    """
    Build a Dataset object out of Instruction instance(s).
    This reader is made for testing. It mocks file reads.
    """

    def _get_dataset_from_filename(self, filename_skip_take):
        """Returns a Dataset instance from given (filename, skip, take)."""
        filename, skip, take = (
            filename_skip_take["filename"],
            filename_skip_take["skip"] if "skip" in filename_skip_take else None,
            filename_skip_take["take"] if "take" in filename_skip_take else None,
        )
        pa_table = pa.Table.from_pydict({"filename": [filename + "_" + str(x) for x in np.arange(30).tolist()]})
        if skip is not None and take is not None:
            pa_table = pa_table.slice(skip, take)
        return pa_table


class IndexableDatasetTest(TestCase):
    def _create_dummy_dataset(self):
        name = "my_name"
        train_info = SplitInfo(name="train", num_examples=30)
        test_info = SplitInfo(name="test", num_examples=30)
        split_infos = [train_info, test_info]
        split_dict = SplitDict()
        split_dict.add(train_info)
        split_dict.add(test_info)
        info = DatasetInfo(splits=split_dict)
        reader = ReaderTester("", info)
        dset = reader.read(name, "train", split_infos)
        return dset

    def test_dense(self):
        dset: Dataset = self._create_dummy_dataset()
        dset = dset.map(
            lambda ex, i: {"vecs": i * np.ones(5, dtype=np.float32)}, with_indices=True, keep_in_memory=True
        )
        dset = dset.add_vector_index("vecs")
        scores, examples = dset.get_nearest("vecs", np.ones(5, dtype=np.float32))
        self.assertEqual(examples[0]["filename"], "my_name-train_29")

    def test_sparse(self):
        dset: Dataset = self._create_dummy_dataset()
        with patch("elasticsearch.Elasticsearch.search") as mocked_search, patch(
            "elasticsearch.client.IndicesClient.create"
        ) as mocked_index_create, patch("elasticsearch.helpers.streaming_bulk") as mocked_bulk:
            mocked_index_create.return_value = {"acknowledged": True}
            mocked_bulk.return_value([(True, None)] * 30)
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 29}]}}
            es_client = Elasticsearch()

            dset.add_text_index("filename", es_client, "my_index_name")
            scores, examples = dset.get_nearest("filename", "my_name-train_29")
            self.assertEqual(examples[0]["filename"], "my_name-train_29")


class DenseIndexTest(TestCase):
    def test_flat_ip(self):
        index = DenseIndex()

        # add vectors
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsNotNone(index.faiss_index)
        self.assertEqual(index.faiss_index.ntotal, 5)
        index.add_vectors(np.zeros((5, 5), dtype=np.float32))
        self.assertEqual(index.faiss_index.ntotal, 10)

        # single query
        query = np.zeros(5, dtype=np.float32)
        query[1] = 1
        scores, indices = index.search(query)
        self.assertGreater(scores[0], 0)
        self.assertEqual(indices[0], 1)

        # batched queries
        queries = np.eye(5, dtype=np.float32)[::-1]
        total_scores, total_indices = index.search_batch(queries)
        best_scores = [scores[0] for scores in total_scores]
        best_indices = [indices[0] for indices in total_indices]
        self.assertGreater(np.min(best_scores), 0)
        self.assertListEqual([4, 3, 2, 1, 0], best_indices)

    def test_factory(self):
        index = DenseIndex(string_factory="Flat")
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsInstance(index.faiss_index, faiss.IndexFlat)
        index = DenseIndex(string_factory="LSH")
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsInstance(index.faiss_index, faiss.IndexLSH)


class SparseIndexTest(TestCase):
    def test_flat_ip(self):
        with patch("elasticsearch.Elasticsearch.search") as mocked_search, patch(
            "elasticsearch.client.IndicesClient.create"
        ) as mocked_index_create, patch("elasticsearch.helpers.streaming_bulk") as mocked_bulk:
            es_client = Elasticsearch()
            mocked_index_create.return_value = {"acknowledged": True}
            index = SparseIndex(es_client, "my_index_name")
            mocked_bulk.return_value([(True, None)] * 3)
            index.add_texts(["foo", "bar", "foobar"])

            # single query
            query = "foo"
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 0}]}}
            scores, indices = index.search(query)
            self.assertEqual(scores[0], 1)
            self.assertEqual(indices[0], 0)

            # batched queries
            queries = ["foo", "bar", "foobar"]
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 1}]}}
            total_scores, total_indices = index.search_batch(queries)
            best_scores = [scores[0] for scores in total_scores]
            best_indices = [indices[0] for indices in total_indices]
            self.assertGreater(np.min(best_scores), 0)
            self.assertListEqual([1, 1, 1], best_indices)
