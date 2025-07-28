import os
import tempfile
from functools import partial
from unittest import TestCase
from unittest.mock import patch

import numpy as np
import pytest

from datasets.arrow_dataset import Dataset
from datasets.search import ElasticSearchIndex, FaissIndex, MissingIndex

from .utils import require_elasticsearch, require_faiss


pytestmark = pytest.mark.integration


@require_faiss
class IndexableDatasetTest(TestCase):
    def _create_dummy_dataset(self):
        dset = Dataset.from_dict({"filename": ["my_name-train" + "_" + str(x) for x in np.arange(30).tolist()]})
        return dset

    def test_add_faiss_index(self):
        import faiss

        dset: Dataset = self._create_dummy_dataset()
        dset = dset.map(
            lambda ex, i: {"vecs": i * np.ones(5, dtype=np.float32)}, with_indices=True, keep_in_memory=True
        )
        dset = dset.add_faiss_index("vecs", batch_size=100, metric_type=faiss.METRIC_INNER_PRODUCT)
        scores, examples = dset.get_nearest_examples("vecs", np.ones(5, dtype=np.float32))
        self.assertEqual(examples["filename"][0], "my_name-train_29")
        dset.drop_index("vecs")

    def test_add_faiss_index_errors(self):
        import faiss

        dset: Dataset = self._create_dummy_dataset()
        with pytest.raises(ValueError, match="Wrong feature type for column 'filename'"):
            _ = dset.add_faiss_index("filename", batch_size=100, metric_type=faiss.METRIC_INNER_PRODUCT)

    def test_add_faiss_index_from_external_arrays(self):
        import faiss

        dset: Dataset = self._create_dummy_dataset()
        dset.add_faiss_index_from_external_arrays(
            external_arrays=np.ones((30, 5)) * np.arange(30).reshape(-1, 1),
            index_name="vecs",
            batch_size=100,
            metric_type=faiss.METRIC_INNER_PRODUCT,
        )
        scores, examples = dset.get_nearest_examples("vecs", np.ones(5, dtype=np.float32))
        self.assertEqual(examples["filename"][0], "my_name-train_29")

    def test_serialization(self):
        import faiss

        dset: Dataset = self._create_dummy_dataset()
        dset.add_faiss_index_from_external_arrays(
            external_arrays=np.ones((30, 5)) * np.arange(30).reshape(-1, 1),
            index_name="vecs",
            metric_type=faiss.METRIC_INNER_PRODUCT,
        )

        # Setting delete=False and unlinking manually is not pretty... but it is required on Windows to
        # ensure somewhat stable behaviour. If we don't, we get PermissionErrors. This is an age-old issue.
        # see https://bugs.python.org/issue14243 and
        # https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file/23212515
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            dset.save_faiss_index("vecs", tmp_file.name)
            dset.load_faiss_index("vecs2", tmp_file.name)
        os.unlink(tmp_file.name)

        scores, examples = dset.get_nearest_examples("vecs2", np.ones(5, dtype=np.float32))
        self.assertEqual(examples["filename"][0], "my_name-train_29")

    def test_drop_index(self):
        dset: Dataset = self._create_dummy_dataset()
        dset.add_faiss_index_from_external_arrays(
            external_arrays=np.ones((30, 5)) * np.arange(30).reshape(-1, 1), index_name="vecs"
        )
        dset.drop_index("vecs")
        self.assertRaises(MissingIndex, partial(dset.get_nearest_examples, "vecs2", np.ones(5, dtype=np.float32)))

    def test_add_elasticsearch_index(self):
        from elasticsearch import Elasticsearch

        dset: Dataset = self._create_dummy_dataset()
        with (
            patch("elasticsearch.Elasticsearch.search") as mocked_search,
            patch("elasticsearch.client.IndicesClient.create") as mocked_index_create,
            patch("elasticsearch.helpers.streaming_bulk") as mocked_bulk,
        ):
            mocked_index_create.return_value = {"acknowledged": True}
            mocked_bulk.return_value([(True, None)] * 30)
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 29}]}}
            es_client = Elasticsearch()

            dset.add_elasticsearch_index("filename", es_client=es_client)
            scores, examples = dset.get_nearest_examples("filename", "my_name-train_29")
            self.assertEqual(examples["filename"][0], "my_name-train_29")


@require_faiss
class FaissIndexTest(TestCase):
    def test_flat_ip(self):
        import faiss

        index = FaissIndex(metric_type=faiss.METRIC_INNER_PRODUCT)

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
        self.assertRaises(ValueError, index.search, query.reshape(-1, 1))
        self.assertGreater(scores[0], 0)
        self.assertEqual(indices[0], 1)

        # batched queries
        queries = np.eye(5, dtype=np.float32)[::-1]
        total_scores, total_indices = index.search_batch(queries)
        self.assertRaises(ValueError, index.search_batch, queries[0])
        best_scores = [scores[0] for scores in total_scores]
        best_indices = [indices[0] for indices in total_indices]
        self.assertGreater(np.min(best_scores), 0)
        self.assertListEqual([4, 3, 2, 1, 0], best_indices)

    def test_factory(self):
        import faiss

        index = FaissIndex(string_factory="Flat")
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsInstance(index.faiss_index, faiss.IndexFlat)
        index = FaissIndex(string_factory="LSH")
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsInstance(index.faiss_index, faiss.IndexLSH)
        with self.assertRaises(ValueError):
            _ = FaissIndex(string_factory="Flat", custom_index=faiss.IndexFlat(5))

    def test_custom(self):
        import faiss

        custom_index = faiss.IndexFlat(5)
        index = FaissIndex(custom_index=custom_index)
        index.add_vectors(np.eye(5, dtype=np.float32))
        self.assertIsInstance(index.faiss_index, faiss.IndexFlat)

    def test_serialization(self):
        import faiss

        index = FaissIndex(metric_type=faiss.METRIC_INNER_PRODUCT)
        index.add_vectors(np.eye(5, dtype=np.float32))

        # Setting delete=False and unlinking manually is not pretty... but it is required on Windows to
        # ensure somewhat stable behaviour. If we don't, we get PermissionErrors. This is an age-old issue.
        # see https://bugs.python.org/issue14243 and
        # https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file/23212515
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            index.save(tmp_file.name)
            index = FaissIndex.load(tmp_file.name)
        os.unlink(tmp_file.name)

        query = np.zeros(5, dtype=np.float32)
        query[1] = 1
        scores, indices = index.search(query)
        self.assertGreater(scores[0], 0)
        self.assertEqual(indices[0], 1)


@require_faiss
def test_serialization_fs(mockfs):
    import faiss

    index = FaissIndex(metric_type=faiss.METRIC_INNER_PRODUCT)
    index.add_vectors(np.eye(5, dtype=np.float32))

    index_name = "index.faiss"
    path = f"mock://{index_name}"
    index.save(path, storage_options=mockfs.storage_options)
    index = FaissIndex.load(path, storage_options=mockfs.storage_options)

    query = np.zeros(5, dtype=np.float32)
    query[1] = 1
    scores, indices = index.search(query)
    assert scores[0] > 0
    assert indices[0] == 1


@require_elasticsearch
class ElasticSearchIndexTest(TestCase):
    def test_elasticsearch(self):
        from elasticsearch import Elasticsearch

        with (
            patch("elasticsearch.Elasticsearch.search") as mocked_search,
            patch("elasticsearch.client.IndicesClient.create") as mocked_index_create,
            patch("elasticsearch.helpers.streaming_bulk") as mocked_bulk,
        ):
            es_client = Elasticsearch()
            mocked_index_create.return_value = {"acknowledged": True}
            index = ElasticSearchIndex(es_client=es_client)
            mocked_bulk.return_value([(True, None)] * 3)
            index.add_documents(["foo", "bar", "foobar"])

            # single query
            query = "foo"
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 0}]}}
            scores, indices = index.search(query)
            self.assertEqual(scores[0], 1)
            self.assertEqual(indices[0], 0)

            # single query with timeout
            query = "foo"
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 0}]}}
            scores, indices = index.search(query, request_timeout=30)
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

            # batched queries with timeout
            queries = ["foo", "bar", "foobar"]
            mocked_search.return_value = {"hits": {"hits": [{"_score": 1, "_id": 1}]}}
            total_scores, total_indices = index.search_batch(queries, request_timeout=30)
            best_scores = [scores[0] for scores in total_scores]
            best_indices = [indices[0] for indices in total_indices]
            self.assertGreater(np.min(best_scores), 0)
            self.assertListEqual([1, 1, 1], best_indices)
