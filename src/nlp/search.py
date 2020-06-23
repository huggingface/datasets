import logging
import os
from typing import TYPE_CHECKING, Dict, List, Optional, Union, NamedTuple
import tempfile

import numpy as np
from tqdm.auto import tqdm


if TYPE_CHECKING:
    from .arrow_dataset import Dataset  # noqa: F401


try:
    import elasticsearch as es
    from elasticsearch import Elasticsearch
    import elasticsearch.helpers

    _has_elasticsearch = True
except ImportError:
    _has_elasticsearch = False

try:
    import faiss

    _has_faiss = True
except ImportError:
    _has_faiss = False


logger = logging.getLogger(__name__)


class MissingIndex(Exception):
    pass


SearchResults = NamedTuple("SearchResults", [("scores", List[float]), ("indices", List[int])])
BatchedSearchResults = NamedTuple("SearchResults", [("total_scores", List[List[float]]), ("total_indices", List[List[int]])])

NearestExamplesResults = NamedTuple("SearchResults", [("scores", List[float]), ("examples", List[dict])])
BatchedNearestExamplesResults = NamedTuple("SearchResults", [("total_scores", List[List[float]]), ("total_examples", List[List[dict]])])


class BaseIndex:
    """Base class for indexing"""

    def search(self, query, k: int = 10) -> SearchResults:
        """
        To implement.
        This method has to return the scores and the indices of the retrieved examples given a certain query.
        """
        raise NotImplementedError

    def search_batch(self, queries, k: int = 10) -> BatchedSearchResults:
        """ Find the nearest examples indices to the query.

            Args:
                `queries` (`Union[List[str], np.ndarray]`): The queries as a list of strings if `column` is a text index or as a numpy array if `column` is a vector index.
                `k` (`int`): The number of examples to retrieve per query.

            Ouput:
                `total_scores` (`List[List[float]`): The retrieval scores of the retrieved examples per query.
                `total_indices` (`List[List[int]]`): The indices of the retrieved examples per query.
        """
        total_scores, total_indices = [], []
        for query in queries:
            scores, indices = self.search(query, k)
            total_scores.append(scores)
            total_indices.append(indices)
        return BatchedSearchResults(total_scores, total_indices)


class ElasticSearchIndex(BaseIndex):
    """
    Sparse index using Elasticsearch. It is used to index text and run queries based on BM25 similarity.
    An Elasticsearch server needs to be accessible, and a python client is declared with
    ```
    es_client = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    ```
    for example.
    """

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None, es_client: Optional[Elasticsearch] = None, index_name: Optional[str] = None):
        assert (
            _has_elasticsearch
        ), "You must install ElasticSearch to use ElasticSearchIndex. To do so you can run `pip install elasticsearch`"
        assert es_client is None or (host is None and port is None), "Please specify either `es_client` or `(host, port)`, but not both."
        host = host or "localhost"
        port = port or 9200
        self.es_client = es_client if es_client is not None else Elasticsearch([{'host': host, 'port': str(port)}])
        self.index_name = index_name if index_name is not None else "huggingface_nlp_" + os.path.basename(tempfile.NamedTemporaryFile().name)

    def add_documents(self, documents: Union[List[str], "Dataset"], column: Optional[str] = None):
        """
        Add documents to the index.
        If the documents are inside a certain column, you can specify it using the `column` argument.
        """
        # TODO: don't rebuild if it already exists
        index_name = self.index_name
        index_config = {
            "settings": {
                "number_of_shards": 1,
                "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
            },
            "mappings": {
                "properties": {
                    "article_title": {"type": "text", "analyzer": "standard", "similarity": "BM25"},
                    "section_title": {"type": "text", "analyzer": "standard", "similarity": "BM25"},
                    "passage_text": {"type": "text", "analyzer": "standard", "similarity": "BM25"},
                }
            },
        }
        self.es_client.indices.create(index=index_name, body=index_config)
        number_of_docs = len(documents)
        progress = tqdm(unit="docs", total=number_of_docs)
        successes = 0

        def passage_generator():
            if column is not None:
                for i, example in enumerate(documents):
                    yield {"text": example[column], "_id": i}
            else:
                for i, example in enumerate(documents):
                    yield {"text": example, "_id": i}

        # create the ES index
        for ok, action in es.helpers.streaming_bulk(
            client=self.es_client, index=index_name, actions=passage_generator(),
        ):
            progress.update(1)
            successes += ok
        logger.info("Indexed %d documents" % (successes,))

    def search(self, query: str, k=10) -> SearchResults:
        """ Find the nearest examples indices to the query.

            Args:
                `query` (`str`): The query as a string.
                `k` (`int`): The number of examples to retrieve.

            Ouput:
                `scores` (`List[List[float]`): The retrieval scores of the retrieved examples.
                `indices` (`List[List[int]]`): The indices of the retrieved examples.
        """
        response = self.es_client.search(
            index=self.index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": k},
        )
        hits = response["hits"]["hits"]
        return SearchResults([hit["_score"] for hit in hits], [hit["_id"] for hit in hits])


class FaissGpuOptions:
    """
    Options to specify the GPU resources for Faiss.
    You can use them for multi-GPU settings for example.
    More info at https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU
    """

    def __init__(self, resource_vec, device_vec, cloner_options):
        self.resource_vec = resource_vec
        self.device_vec = device_vec
        self.cloner_options = cloner_options


class FaissIndex(BaseIndex):
    """
    Dense index using Faiss. It is used to index vectors.
    Faiss is a library for efficient similarity search and clustering of dense vectors.
    It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM.
    """

    def __init__(
        self,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        faiss_gpu_options: Optional[FaissGpuOptions] = None,
    ):
        assert not (
            device is not None and faiss_gpu_options is not None
        ), "Please specify either `device` or `faiss_gpu_options` but not both."
        self.device: int = device if device is not None else -1
        self.string_factory: Optional[str] = string_factory
        self.faiss_gpu_options: Optional[FaissGpuOptions] = faiss_gpu_options
        self.faiss_index = None
        assert (
            _has_faiss
        ), "You must install Faiss to use FaissIndex. To do so you can run `pip install faiss-cpu` or `pip install faiss-gpu`"

    def add_vectors(self, vectors: Union[np.array, "Dataset"], column: Optional[str] = None, batch_size=1000):
        """
        Add vectors to the index.
        If the arrays are inside a certain column, you can specify it using the `column` argument.
        """
        if self.faiss_index is None:
            size = len(vectors[0]) if column is None else len(vectors[0][column])
            if self.string_factory is not None:
                index = faiss.index_factory(size, self.string_factory)
            else:
                index = faiss.IndexFlatIP(size)
            if self.device > -1:
                self.faiss_res = faiss.StandardGpuResources()
                self.faiss_index = faiss.index_cpu_to_gpu(self.faiss_res, self.device, index)
            elif self.faiss_gpu_options is not None:
                self.faiss_index = faiss.index_cpu_to_gpu_multiple(
                    self.faiss_gpu_options.resource_vec,
                    self.faiss_gpu_options.device_vec,
                    index,
                    self.faiss_gpu_options.cloner_options,
                )
            else:
                self.faiss_index = index
        for i in range(0, len(vectors), batch_size):
            vecs = vectors[i : i + batch_size] if column is None else vectors[i : i + batch_size][column]
            self.faiss_index.add(vecs)

    def search(self, query: np.array, k=10) -> SearchResults:
        """ Find the nearest examples indices to the query.

            Args:
                `query` (`np.array`): The query as a numpy array.
                `k` (`int`): The number of examples to retrieve.

            Ouput:
                `scores` (`List[List[float]`): The retrieval scores of the retrieved examples.
                `indices` (`List[List[int]]`): The indices of the retrieved examples.
        """
        assert len(query.shape) == 1 or (len(query.shape) == 2 and query.shape[0] == 1)
        queries = query.reshape(1, -1)
        if not queries.flags.c_contiguous:
            queries = np.asarray(queries, order="C")
        scores, indices = self.faiss_index.search(queries, k)
        return SearchResults(scores[0], indices[0].astype(int))

    def search_batch(self, queries: np.array, k=10) -> BatchedSearchResults:
        """ Find the nearest examples indices to the queries.

            Args:
                `queries` (`np.array`): The queries as a numpy array.
                `k` (`int`): The number of examples to retrieve.

            Ouput:
                `total_scores` (`List[List[float]`): The retrieval scores of the retrieved examples per query.
                `total_indices` (`List[List[int]]`): The indices of the retrieved examples per query.
        """
        assert len(queries.shape) == 2
        if not queries.flags.c_contiguous:
            queries = np.asarray(queries, order="C")
        scores, indices = self.faiss_index.search(queries, k)
        return BatchedSearchResults(scores, indices.astype(int))


class IndexableMixin:
    """Add indexing features to `nlp.Dataset`"""

    def __init__(self):
        self._indexes: Dict[str, BaseIndex] = {}

    def __getitem__(self, key):
        raise NotImplementedError

    def is_index_initialized(self, column: str) -> bool:
        return column in self._indexes

    def _check_index_is_initialized(self, column: str):
        if not self.is_index_initialized(column):
            raise MissingIndex(
                f"Index with column '{column}' not initialized yet. Please make sure that you call `add_faiss_index` or `add_elasticsearch_index` first."
            )

    def list_indexes(self) -> List[str]:
        """List the columns/identifiers of all the attached indexes."""
        return list(self._indexes)

    def add_faiss_index(
        self,
        column: str,
        external_arrays: Optional[np.array] = None,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        faiss_gpu_options: Optional[FaissGpuOptions] = None,
    ):
        """ Add a dense index using Faiss for fast retrieval.

            Args:
                `column` (`str`): The column/identifier of the index. This is the column that is used to call `.get_nearest` or `.search`.
                `vectors` (`Union[np.ndarray, nlp.Dataset]`): The vectors to index. It can be a `nlp.Dataset` if the `dataset` is well formated
                    using `dataset.set_format("numpy")` for example.
                `device` (Optional `int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
                `string_factory` (Optional `str`): This is passed to the index factory Faiss to create the index. Default index class is IndexFlatIP.
                `faiss_gpu_options` (Optional `FaissGpuOptions`): Options to configure the GPU resources of Faiss.
        """
        self._indexes[column] = FaissIndex(device, string_factory, faiss_gpu_options)
        if external_arrays is None:
            self._indexes[column].add_vectors(self, column=column)
        else:
            self._indexes[column].add_vectors(external_arrays, column=None)

    def add_elasticsearch_index(self, column: str, host: Optional[str] = None, port: Optional[int] = None, es_client: Optional[Elasticsearch] = None, index_name: Optional[str] = None):
        """ Add a text index using ElasticSearch for fast retrieval.

            Args:
                `column` (`str`): The column/identifier of the index. This is the column that is used to call `.get_nearest` or `.search`.
                `documents` (`Union[List[str], nlp.Dataset]`): The documents to index. It can be a `nlp.Dataset`.
                `es_client` (`elasticsearch.Elasticsearch`): The elasticsearch client used to create the index.
                `index_name` (Optional `str`): The elasticsearch index name used to create the index.
        """
        self._indexes[column] = ElasticSearchIndex(host, port, es_client, index_name)
        self._indexes[column].add_documents(self, column=column)

    def drop_index(self, column: str):
        """ Drop the index with the specified column.

            Args:
                `column` (`str`): The column/identifier of the index.
        """
        del self._indexes[column]

    def search(self, column: str, query, k: int = 10) -> SearchResults:
        """ Find the nearest examples indices in the dataset to the query.

            Args:
                `column` (`str`): The name/identifier of the index.
                `query` (`Union[str, np.ndarray]`): The query as a string if `column` is a text index or as a numpy array if `column` is a vector index.
                `k` (`int`): The number of examples to retrieve.

            Ouput:
                `scores` (`List[List[float]`): The retrieval scores of the retrieved examples.
                `indices` (`List[List[int]]`): The indices of the retrieved examples.
        """
        self._check_index_is_initialized(column)
        return self._indexes[column].search(query, k)

    def search_batch(self, column: str, queries, k: int = 10) -> BatchedSearchResults:
        """ Find the nearest examples indices in the dataset to the query.

            Args:
                `column` (`str`): The column/identifier of the index.
                `queries` (`Union[List[str], np.ndarray]`): The queries as a list of strings if `column` is a text index or as a numpy array if `column` is a vector index.
                `k` (`int`): The number of examples to retrieve per query.

            Ouput:
                `total_scores` (`List[List[float]`): The retrieval scores of the retrieved examples per query.
                `total_indices` (`List[List[int]]`): The indices of the retrieved examples per query.
        """
        self._check_index_is_initialized(column)
        return self._indexes[column].search_batch(queries, k)

    def get_nearest(self, column: str, query, k: int = 10) -> NearestExamplesResults:
        """ Find the nearest examples in the dataset to the query.

            Args:
                `column` (`str`): The column/identifier of the index.
                `query` (`Union[str, np.ndarray]`): The query as a string if `column` is a text index or as a numpy array if `column` is a vector index.
                `k` (`int`): The number of examples to retrieve.

            Ouput:
                `scores` (`List[List[float]`): The retrieval scores of the retrieved examples.
                `examples` (`List[List[dict]]`): The retrieved examples.
        """
        self._check_index_is_initialized(column)
        scores, indices = self.search(column, query, k)
        return NearestExamplesResults(scores, [self[int(i)] for i in indices])

    def get_nearest_batch(self, column: str, queries, k: int = 10) -> BatchedNearestExamplesResults:
        """ Find the nearest examples in the dataset to the query.

            Args:
                `column` (`str`): The column/identifier of the index.
                `queries` (`Union[List[str], np.ndarray]`): The queries as a list of strings if `column` is a text index or as a numpy array if `column` is a vector index.
                `k` (`int`): The number of examples to retrieve per query.

            Ouput:
                `total_scores` (`List[List[float]`): The retrieval scores of the retrieved examples per query.
                `total_examples` (`List[List[dict]]`): The retrieved examples per query.
        """
        self._check_index_is_initialized(column)
        total_scores, total_indices = self.search_batch(column, queries, k)
        return BatchedNearestExamplesResults(total_scores, [[self[int(i)] for i in indices] for indices in total_indices])
