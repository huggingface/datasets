import importlib.util
import os
import tempfile
from pathlib import PurePath
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Optional, Union

import numpy as np

from . import utils
from .utils import logging


if TYPE_CHECKING:
    from .arrow_dataset import Dataset  # noqa: F401

    try:
        from elasticsearch import Elasticsearch  # noqa: F401

    except ImportError:
        pass
    try:
        import faiss  # noqa: F401

    except ImportError:
        pass

_has_elasticsearch = importlib.util.find_spec("elasticsearch") is not None
_has_faiss = importlib.util.find_spec("faiss") is not None


logger = logging.get_logger(__name__)


class MissingIndex(Exception):
    pass


class SearchResults(NamedTuple):
    scores: List[float]
    indices: List[int]


class BatchedSearchResults(NamedTuple):
    total_scores: List[List[float]]
    total_indices: List[List[int]]


class NearestExamplesResults(NamedTuple):
    scores: List[float]
    examples: dict


class BatchedNearestExamplesResults(NamedTuple):
    total_scores: List[List[float]]
    total_examples: List[dict]


class BaseIndex:
    """Base class for indexing"""

    def search(self, query, k: int = 10) -> SearchResults:
        """
        To implement.
        This method has to return the scores and the indices of the retrieved examples given a certain query.
        """
        raise NotImplementedError

    def search_batch(self, queries, k: int = 10) -> BatchedSearchResults:
        """Find the nearest examples indices to the query.

        Args:
            queries (`Union[List[str], np.ndarray]`): The queries as a list of strings if `column` is a text index or as a numpy array if `column` is a vector index.
            k (`int`): The number of examples to retrieve per query.

        Ouput:
            total_scores (`List[List[float]`): The retrieval scores of the retrieved examples per query.
            total_indices (`List[List[int]]`): The indices of the retrieved examples per query.
        """
        total_scores, total_indices = [], []
        for query in queries:
            scores, indices = self.search(query, k)
            total_scores.append(scores)
            total_indices.append(indices)
        return BatchedSearchResults(total_scores, total_indices)

    def save(self, file: Union[str, PurePath]):
        """Serialize the index on disk"""
        raise NotImplementedError

    @classmethod
    def load(cls, file: Union[str, PurePath]) -> "BaseIndex":
        """Deserialize the index from disk"""
        raise NotImplementedError


class ElasticSearchIndex(BaseIndex):
    """
    Sparse index using Elasticsearch. It is used to index text and run queries based on BM25 similarity.
    An Elasticsearch server needs to be accessible, and a python client is declared with
    ```
    es_client = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
    ```
    for example.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        es_client: Optional["Elasticsearch"] = None,
        es_index_name: Optional[str] = None,
        es_index_config: Optional[dict] = None,
    ):
        if not _has_elasticsearch:
            raise ImportError(
                "You must install ElasticSearch to use ElasticSearchIndex. To do so you can run `pip install elasticsearch==7.7.1 for example`"
            )
        if es_client is not None and (host is not None or port is not None):
            raise ValueError("Please specify either `es_client` or `(host, port)`, but not both.")
        host = host or "localhost"
        port = port or 9200

        import elasticsearch.helpers  # noqa: need this to properly load all the es features
        from elasticsearch import Elasticsearch  # noqa: F811

        self.es_client = es_client if es_client is not None else Elasticsearch([{"host": host, "port": str(port)}])
        self.es_index_name = (
            es_index_name
            if es_index_name is not None
            else "huggingface_datasets_" + os.path.basename(tempfile.NamedTemporaryFile().name)
        )
        self.es_index_config = (
            es_index_config
            if es_index_config is not None
            else {
                "settings": {
                    "number_of_shards": 1,
                    "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
                },
                "mappings": {"properties": {"text": {"type": "text", "analyzer": "standard", "similarity": "BM25"}}},
            }
        )

    def add_documents(self, documents: Union[List[str], "Dataset"], column: Optional[str] = None):
        """
        Add documents to the index.
        If the documents are inside a certain column, you can specify it using the `column` argument.
        """
        index_name = self.es_index_name
        index_config = self.es_index_config
        self.es_client.indices.create(index=index_name, body=index_config)
        number_of_docs = len(documents)
        progress = utils.tqdm(
            unit="docs", total=number_of_docs, disable=bool(logging.get_verbosity() == logging.NOTSET)
        )
        successes = 0

        def passage_generator():
            if column is not None:
                for i, example in enumerate(documents):
                    yield {"text": example[column], "_id": i}
            else:
                for i, example in enumerate(documents):
                    yield {"text": example, "_id": i}

        # create the ES index
        import elasticsearch as es

        for ok, action in es.helpers.streaming_bulk(
            client=self.es_client,
            index=index_name,
            actions=passage_generator(),
        ):
            progress.update(1)
            successes += ok
        if successes != len(documents):
            logger.warning(
                f"Some documents failed to be added to ElasticSearch. Failures: {len(documents)-successes}/{len(documents)}"
            )
        logger.info(f"Indexed {successes:d} documents")

    def search(self, query: str, k=10) -> SearchResults:
        """Find the nearest examples indices to the query.

        Args:
            query (`str`): The query as a string.
            k (`int`): The number of examples to retrieve.

        Ouput:
            scores (`List[List[float]`): The retrieval scores of the retrieved examples.
            indices (`List[List[int]]`): The indices of the retrieved examples.
        """
        response = self.es_client.search(
            index=self.es_index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": k},
        )
        hits = response["hits"]["hits"]
        return SearchResults([hit["_score"] for hit in hits], [int(hit["_id"]) for hit in hits])

    def search_batch(self, queries, k: int = 10, max_workers=10) -> BatchedSearchResults:
        import concurrent.futures

        total_scores, total_indices = [None] * len(queries), [None] * len(queries)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {executor.submit(self.search, query, k): i for i, query in enumerate(queries)}
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                results: SearchResults = future.result()
                total_scores[index] = results.scores
                total_indices[index] = results.indices
        return BatchedSearchResults(total_indices=total_indices, total_scores=total_scores)


class FaissIndex(BaseIndex):
    """
    Dense index using Faiss. It is used to index vectors.
    Faiss is a library for efficient similarity search and clustering of dense vectors.
    It contains algorithms that search in sets of vectors of any size, up to ones that possibly do not fit in RAM.
    You can find more information about Faiss here:
    - For index types and the string factory: https://github.com/facebookresearch/faiss/wiki/The-index-factory
    - For GPU settings: https://github.com/facebookresearch/faiss/wiki/Faiss-on-the-GPU
    """

    def __init__(
        self,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        metric_type: Optional[int] = None,
        custom_index: Optional["faiss.Index"] = None,
    ):
        """
        Create a Dense index using Faiss. You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
        You can find more information about Faiss here:
        - For `string factory`: https://github.com/facebookresearch/faiss/wiki/The-index-factory
        """
        if string_factory is not None and custom_index is not None:
            raise ValueError("Please specify either `string_factory` or `custom_index` but not both.")
        self.device = device
        self.string_factory = string_factory
        self.metric_type = metric_type
        self.faiss_index = custom_index
        if not _has_faiss:
            raise ImportError(
                "You must install Faiss to use FaissIndex. To do so you can run `pip install faiss-cpu` or `pip install faiss-gpu`"
            )

    def add_vectors(
        self,
        vectors: Union[np.array, "Dataset"],
        column: Optional[str] = None,
        batch_size: int = 1000,
        train_size: Optional[int] = None,
        faiss_verbose: Optional[bool] = None,
    ):
        """
        Add vectors to the index.
        If the arrays are inside a certain column, you can specify it using the `column` argument.
        """
        import faiss  # noqa: F811

        # Create index
        if self.faiss_index is None:
            size = len(vectors[0]) if column is None else len(vectors[0][column])
            if self.string_factory is not None:
                if self.metric_type is None:
                    index = faiss.index_factory(size, self.string_factory)
                else:
                    index = faiss.index_factory(size, self.string_factory, self.metric_type)
            else:
                if self.metric_type is None:
                    index = faiss.IndexFlat(size)
                else:
                    index = faiss.IndexFlat(size, self.metric_type)
            if self.device is not None and self.device > -1:
                self.faiss_res = faiss.StandardGpuResources()
                index = faiss.index_cpu_to_gpu(self.faiss_res, self.device, index)
            self.faiss_index = index
            logger.info(f"Created faiss index of type {type(self.faiss_index)}")

        # Set verbosity level
        if faiss_verbose is not None:
            self.faiss_index.verbose = faiss_verbose
            if hasattr(self.faiss_index, "index") and self.faiss_index.index is not None:
                self.faiss_index.index.verbose = faiss_verbose
            if hasattr(self.faiss_index, "quantizer") and self.faiss_index.quantizer is not None:
                self.faiss_index.quantizer.verbose = faiss_verbose
            if hasattr(self.faiss_index, "clustering_index") and self.faiss_index.clustering_index is not None:
                self.faiss_index.clustering_index.verbose = faiss_verbose

        # Train
        if train_size is not None:
            train_vecs = vectors[:train_size] if column is None else vectors[:train_size][column]
            logger.info(f"Training the index with the first {len(train_vecs)} vectors")
            self.faiss_index.train(train_vecs)
        else:
            logger.info("Ignored the training step of the faiss index as `train_size` is None.")

        # Add vectors
        logger.info(f"Adding {len(vectors)} vectors to the faiss index")
        for i in utils.tqdm(
            range(0, len(vectors), batch_size), disable=bool(logging.get_verbosity() == logging.NOTSET)
        ):
            vecs = vectors[i : i + batch_size] if column is None else vectors[i : i + batch_size][column]
            self.faiss_index.add(vecs)

    def search(self, query: np.array, k=10) -> SearchResults:
        """Find the nearest examples indices to the query.

        Args:
            query (`np.array`): The query as a numpy array.
            k (`int`): The number of examples to retrieve.

        Ouput:
            scores (`List[List[float]`): The retrieval scores of the retrieved examples.
            indices (`List[List[int]]`): The indices of the retrieved examples.
        """
        if len(query.shape) != 1 and (len(query.shape) != 2 or query.shape[0] != 1):
            raise ValueError("Shape of query is incorrect, it has to be either a 1D array or 2D (1, N)")

        queries = query.reshape(1, -1)
        if not queries.flags.c_contiguous:
            queries = np.asarray(queries, order="C")
        scores, indices = self.faiss_index.search(queries, k)
        return SearchResults(scores[0], indices[0].astype(int))

    def search_batch(self, queries: np.array, k=10) -> BatchedSearchResults:
        """Find the nearest examples indices to the queries.

        Args:
            queries (`np.array`): The queries as a numpy array.
            k (`int`): The number of examples to retrieve.

        Ouput:
            total_scores (`List[List[float]`): The retrieval scores of the retrieved examples per query.
            total_indices (`List[List[int]]`): The indices of the retrieved examples per query.
        """
        if len(queries.shape) != 2:
            raise ValueError("Shape of query must be 2D")
        if not queries.flags.c_contiguous:
            queries = np.asarray(queries, order="C")
        scores, indices = self.faiss_index.search(queries, k)
        return BatchedSearchResults(scores, indices.astype(int))

    def save(self, file: Union[str, PurePath]):
        """Serialize the FaissIndex on disk"""
        import faiss  # noqa: F811

        if self.device is not None and self.device > -1:
            index = faiss.index_gpu_to_cpu(self.faiss_index)
        else:
            index = self.faiss_index

        faiss.write_index(index, str(file))

    @classmethod
    def load(
        cls,
        file: Union[str, PurePath],
        device: Optional[int] = None,
    ) -> "FaissIndex":
        """Deserialize the FaissIndex from disk"""
        import faiss  # noqa: F811

        faiss_index = cls(device=device)
        index = faiss.read_index(str(file))
        if faiss_index.device is not None and faiss_index.device > -1:
            faiss_index.faiss_res = faiss.StandardGpuResources()
            index = faiss.index_cpu_to_gpu(faiss_index.faiss_res, faiss_index.device, index)
        faiss_index.faiss_index = index
        return faiss_index


class IndexableMixin:
    """Add indexing features to `datasets.Dataset`"""

    def __init__(self):
        self._indexes: Dict[str, BaseIndex] = {}

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def is_index_initialized(self, index_name: str) -> bool:
        return index_name in self._indexes

    def _check_index_is_initialized(self, index_name: str):
        if not self.is_index_initialized(index_name):
            raise MissingIndex(
                f"Index with index_name '{index_name}' not initialized yet. Please make sure that you call `add_faiss_index` or `add_elasticsearch_index` first."
            )

    def list_indexes(self) -> List[str]:
        """List the colindex_nameumns/identifiers of all the attached indexes."""
        return list(self._indexes)

    def get_index(self, index_name: str) -> BaseIndex:
        """List the index_name/identifiers of all the attached indexes.

        Args:
            index_name (:obj:`str`): Index name.

        Returns:
            :class:`BaseIndex`
        """
        self._check_index_is_initialized(index_name)
        return self._indexes[index_name]

    def add_faiss_index(
        self,
        column: str,
        index_name: Optional[str] = None,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        metric_type: Optional[int] = None,
        custom_index: Optional["faiss.Index"] = None,
        train_size: Optional[int] = None,
        faiss_verbose: bool = False,
    ):
        """Add a dense index using Faiss for fast retrieval.
        The index is created using the vectors of the specified column.
        You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
        You can find more information about Faiss here:
        - For `string factory`: https://github.com/facebookresearch/faiss/wiki/The-index-factory

        Args:
            column (:obj:`str`): The column of the vectors to add to the index.
            index_name (Optional :obj:`str`): The index_name/identifier of the index. This is the index_name that is used to call `.get_nearest` or `.search`.
                By defaul it corresponds to `column`.
            device (Optional :obj:`int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
            string_factory (Optional :obj:`str`): This is passed to the index factory of Faiss to create the index. Default index class is IndexFlatIP.
            metric_type (Optional :obj:`int`): Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
            custom_index (Optional :obj:`faiss.Index`): Custom Faiss index that you already have instantiated and configured for your needs.
            train_size (Optional :obj:`int`): If the index needs a training step, specifies how many vectors will be used to train the index.
            faiss_verbose (:obj:`bool`, defaults to False): Enable the verbosity of the Faiss index.
        """
        index_name = index_name if index_name is not None else column
        faiss_index = FaissIndex(
            device=device, string_factory=string_factory, metric_type=metric_type, custom_index=custom_index
        )
        faiss_index.add_vectors(self, column=column, train_size=train_size, faiss_verbose=faiss_verbose)
        self._indexes[index_name] = faiss_index

    def add_faiss_index_from_external_arrays(
        self,
        external_arrays: np.array,
        index_name: str,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        metric_type: Optional[int] = None,
        custom_index: Optional["faiss.Index"] = None,
        train_size: Optional[int] = None,
        faiss_verbose: bool = False,
    ):
        """Add a dense index using Faiss for fast retrieval.
        The index is created using the vectors of `external_arrays`.
        You can specify `device` if you want to run it on GPU (`device` must be the GPU index).
        You can find more information about Faiss here:
        - For `string factory`: https://github.com/facebookresearch/faiss/wiki/The-index-factory

        Args:
            external_arrays (:obj:`np.array`): If you want to use arrays from outside the lib for the index, you can set `external_arrays`.
                It will use `external_arrays` to create the Faiss index instead of the arrays in the given `column`.
            index_name (:obj:`str`): The index_name/identifier of the index. This is the index_name that is used to call `.get_nearest` or `.search`.
            device (Optional :obj:`int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
            string_factory (Optional :obj:`str`): This is passed to the index factory of Faiss to create the index. Default index class is IndexFlatIP.
            metric_type (Optional :obj:`int`): Type of metric. Ex: faiss.faiss.METRIC_INNER_PRODUCT or faiss.METRIC_L2.
            custom_index (Optional :obj:`faiss.Index`): Custom Faiss index that you already have instantiated and configured for your needs.
            train_size (Optional :obj:`int`): If the index needs a training step, specifies how many vectors will be used to train the index.
            faiss_verbose (:obj:`bool`, defaults to False): Enable the verbosity of the Faiss index.
        """
        faiss_index = FaissIndex(
            device=device, string_factory=string_factory, metric_type=metric_type, custom_index=custom_index
        )
        faiss_index.add_vectors(external_arrays, column=None, train_size=train_size, faiss_verbose=faiss_verbose)
        self._indexes[index_name] = faiss_index

    def save_faiss_index(self, index_name: str, file: Union[str, PurePath]):
        """Save a FaissIndex on disk.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index. This is the index_name that is used to call `.get_nearest` or `.search`.
            file (:obj:`str`): The path to the serialized faiss index on disk.
        """
        index = self.get_index(index_name)
        if not isinstance(index, FaissIndex):
            raise ValueError(f"Index '{index_name}' is not a FaissIndex but a '{type(index)}'")
        index.save(file)
        logger.info(f"Saved FaissIndex {index_name} at {file}")

    def load_faiss_index(
        self,
        index_name: str,
        file: Union[str, PurePath],
        device: Optional[int] = None,
    ):
        """Load a FaissIndex from disk.

        If you want to do additional configurations, you can have access to the faiss index object by doing
        `.get_index(index_name).faiss_index` to make it fit your needs.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index. This is the index_name that is used to
                call `.get_nearest` or `.search`.
            file (:obj:`str`): The path to the serialized faiss index on disk.
            device (Optional :obj:`int`): If not None, this is the index of the GPU to use. By default it uses the CPU.
        """
        index = FaissIndex.load(file, device=device)
        if index.faiss_index.ntotal != len(self):
            raise ValueError(
                f"Index size should match Dataset size, but Index '{index_name}' at {file} has {index.faiss_index.ntotal} elements while the dataset has {len(self)} examples."
            )
        self._indexes[index_name] = index
        logger.info(f"Loaded FaissIndex {index_name} from {file}")

    def add_elasticsearch_index(
        self,
        column: str,
        index_name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        es_client: Optional["Elasticsearch"] = None,
        es_index_name: Optional[str] = None,
        es_index_config: Optional[dict] = None,
    ):
        """Add a text index using ElasticSearch for fast retrieval.

        Args:
            column (:obj:`str`): The column of the documents to add to the index.
            index_name (Optional :obj:`str`): The index_name/identifier of the index. This is the index name that is used to call `.get_nearest` or `.search`.
                By defaul it corresponds to `column`.
            host (Optional :obj:`str`, defaults to localhost):
                host of where ElasticSearch is running
            port (Optional :obj:`str`, defaults to 9200):
                port of where ElasticSearch is running
            es_client (Optional :obj:`elasticsearch.Elasticsearch`):
                The elasticsearch client used to create the index if host and port are None.
            es_index_name (Optional :obj:`str`): The elasticsearch index name used to create the index.
            es_index_config (Optional :obj:`dict`):
                The configuration of the elasticsearch index.
                Default config is:

        Config::

            {
                "settings": {
                    "number_of_shards": 1,
                    "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
                },
                "mappings": {
                    "properties": {
                        "text": {
                            "type": "text",
                            "analyzer": "standard",
                            "similarity": "BM25"
                        },
                    }
                },
            }
        """
        index_name = index_name if index_name is not None else column
        es_index = ElasticSearchIndex(
            host=host, port=port, es_client=es_client, es_index_name=es_index_name, es_index_config=es_index_config
        )
        es_index.add_documents(self, column=column)
        self._indexes[index_name] = es_index

    def load_elasticsearch_index(
        self,
        index_name: str,
        es_index_name: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        es_client: Optional["Elasticsearch"] = None,
        es_index_config: Optional[dict] = None,
    ):
        """Load an existing text index using ElasticSearch for fast retrieval.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index. This is the index name that is used to call `.get_nearest` or `.search`.
            es_index_name (:obj:`str`): The name of elasticsearch index to load.
            host (Optional :obj:`str`, defaults to localhost):
                host of where ElasticSearch is running
            port (Optional :obj:`str`, defaults to 9200):
                port of where ElasticSearch is running
            es_client (Optional :obj:`elasticsearch.Elasticsearch`):
                The elasticsearch client used to create the index if host and port are None.
            es_index_config (Optional :obj:`dict`):
                The configuration of the elasticsearch index.
                Default config is::

                    {
                        "settings": {
                            "number_of_shards": 1,
                            "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
                        },
                        "mappings": {
                            "properties": {
                                "text": {
                                    "type": "text",
                                    "analyzer": "standard",
                                    "similarity": "BM25"
                                },
                            }
                        },
                    }
        """
        self._indexes[index_name] = ElasticSearchIndex(
            host=host, port=port, es_client=es_client, es_index_name=es_index_name, es_index_config=es_index_config
        )

    def drop_index(self, index_name: str):
        """Drop the index with the specified column.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index.
        """
        del self._indexes[index_name]

    def search(self, index_name: str, query: Union[str, np.array], k: int = 10) -> SearchResults:
        """Find the nearest examples indices in the dataset to the query.

        Args:
            index_name (:obj:`str`): The name/identifier of the index.
            query (:obj:`Union[str, np.ndarray]`): The query as a string if `index_name` is a text index or as a numpy array if `index_name` is a vector index.
            k (:obj:`int`): The number of examples to retrieve.

        Returns:
            scores (:obj:`List[List[float]`): The retrieval scores of the retrieved examples.
            indices (:obj:`List[List[int]]`): The indices of the retrieved examples.
        """
        self._check_index_is_initialized(index_name)
        return self._indexes[index_name].search(query, k)

    def search_batch(self, index_name: str, queries: Union[List[str], np.array], k: int = 10) -> BatchedSearchResults:
        """Find the nearest examples indices in the dataset to the query.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index.
            queries (:obj:`Union[List[str], np.ndarray]`): The queries as a list of strings if `index_name` is a text index or as a numpy array if `index_name` is a vector index.
            k (:obj:`int`): The number of examples to retrieve per query.

        Returns:
            total_scores (:obj:`List[List[float]`): The retrieval scores of the retrieved examples per query.
            total_indices (:obj:`List[List[int]]`): The indices of the retrieved examples per query.
        """
        self._check_index_is_initialized(index_name)
        return self._indexes[index_name].search_batch(queries, k)

    def get_nearest_examples(
        self, index_name: str, query: Union[str, np.array], k: int = 10
    ) -> NearestExamplesResults:
        """Find the nearest examples in the dataset to the query.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index.
            query (:obj:`Union[str, np.ndarray]`): The query as a string if `index_name` is a text index or as a numpy array if `index_name` is a vector index.
            k (:obj:`int`): The number of examples to retrieve.

        Returns:
            scores (:obj:`List[float]`): The retrieval scores of the retrieved examples.
            examples (:obj:`dict`): The retrieved examples.
        """
        self._check_index_is_initialized(index_name)
        scores, indices = self.search(index_name, query, k)
        return NearestExamplesResults(scores, self[[i for i in indices if i >= 0]])

    def get_nearest_examples_batch(
        self, index_name: str, queries: Union[List[str], np.array], k: int = 10
    ) -> BatchedNearestExamplesResults:
        """Find the nearest examples in the dataset to the query.

        Args:
            index_name (:obj:`str`): The index_name/identifier of the index.
            queries (:obj:`Union[List[str], np.ndarray]`): The queries as a list of strings if `index_name` is a text index or as a numpy array if `index_name` is a vector index.
            k (:obj:`int`): The number of examples to retrieve per query.

        Returns:
            total_scores (`List[List[float]`): The retrieval scores of the retrieved examples per query.
            total_examples (`List[dict]`): The retrieved examples per query.
        """
        self._check_index_is_initialized(index_name)
        total_scores, total_indices = self.search_batch(index_name, queries, k)
        return BatchedNearestExamplesResults(
            total_scores, [self[[i for i in indices if i >= 0]] for indices in total_indices]
        )
