import logging
from typing import List, Optional, Tuple

import numpy as np
from tqdm.auto import tqdm


try:
    import elasticsearch as es

    _has_elasticsearch = True
except ImportError:
    _has_elasticsearch = False

try:
    import faiss

    _has_faiss = True
except ImportError:
    _has_faiss = False


logger = logging.getLogger(__name__)


class MissingSearchEngine(Exception):
    pass


class BaseSearchEngine:
    def search(self, query, k: int = 10) -> Tuple[List[float], List[int]]:
        raise NotImplementedError

    def search_batch(self, queries, k: int = 10) -> Tuple[List[List[float]], List[List[int]]]:
        total_scores, total_indices = [], []
        for query in queries:
            scores, indices = self.search(query, k)
            total_scores.append(scores)
            total_indices.append(indices)
        return total_scores, total_indices


class SparseSearchEngine(BaseSearchEngine):
    def __init__(self, es_client, index_name: str):
        # Elasticsearch needs to be launched in another window, and a python client is declared with
        # > es_client = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.es_client = es_client
        self.index_name = index_name
        assert (
            _has_elasticsearch
        ), "You must install ElasticSearch to use SparseSearchEngine. To do so you can run `pip install elasticsearch`"

    def add_texts(self, texts, column: Optional[str] = None):
        # TODO: don't rebuild if it already exists
        index_name = self.index_name
        search_engine_config = {
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
        self.es_client.indices.create(search_engine=index_name, body=search_engine_config)
        number_of_docs = len(texts)
        progress = tqdm(unit="docs", total=number_of_docs)
        successes = 0

        def passage_generator():
            if column is not None:
                for example in texts:
                    yield example[column]
            else:
                for example in texts:
                    yield example

        # create the ES search_engine
        for ok, action in es.helpers.streaming_bulk(
            client=self.es_client, search_engine=index_name, actions=passage_generator(),
        ):
            progress.update(1)
            successes += ok
        logger.info("SearchEngineed %d documents" % (successes,))

    def search(self, query, k=10):
        response = self.es_client.search(
            search_engine=self.index_name,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["article_title", "section_title", "passage_text^2"],
                        "type": "cross_fields",
                    }
                },
                "size": k,
            },
        )
        hits = response["hits"]["hits"]
        return [hit["_score"] for hit in hits], [hit["_id"] for hit in hits]


class FaissGpuOptions:
    def __init__(self, resource_vec, device_vec, cloner_options):
        self.resource_vec = resource_vec
        self.device_vec = device_vec
        self.cloner_options = cloner_options


class DenseSearchEngine(BaseSearchEngine):
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
        self.faiss_search_engine = None
        assert (
            _has_faiss
        ), "You must install Faiss to use DenseSearchEngine. To do so you can run `pip install faiss-cpu` or pip install faiss-gpu`"

    def add_embeddings(self, embeddings: np.array, column: Optional[str] = None, batch_size=1000):
        size = len(embeddings[0]) if column is None else len(embeddings[0][column])
        if self.string_factory is not None:
            search_engine = faiss.index_factory(size, self.string_factory)
        else:
            search_engine = faiss.IndexFlatIP(size)
        if self.device > -1:
            self.faiss_res = faiss.StandardGpuResources()
            self.faiss_search_engine = faiss.index_cpu_to_gpu(self.faiss_res, self.device, search_engine)
        elif self.faiss_gpu_options is not None:
            self.faiss_search_engine = faiss.index_cpu_to_gpu_multiple(
                self.faiss_gpu_options.resource_vec,
                self.faiss_gpu_options.device_vec,
                search_engine,
                self.faiss_gpu_options.cloner_options,
            )
        else:
            self.faiss_search_engine = search_engine
        for i in range(0, len(embeddings), batch_size):
            vecs = embeddings[i : i + batch_size] if column is None else embeddings[i : i + batch_size][column]
            self.faiss_search_engine.add(vecs)

    def search(self, query: np.array, k=10):
        assert len(query.shape) < 3
        queries = query.reshape(1, -1)
        scores, indices = self.faiss_search_engine.search(queries, k)
        return scores[0], indices[0].astype(int)

    def search_batch(self, queries: np.array, k=10):
        assert len(queries.shape) == 2
        assert queries.shape[1] == self.size
        scores, indices = self.faiss_search_engine.search(queries, k)
        return scores, indices.astype(int)


class SearchableMixin:
    """Add search_engineing features to classes"""

    def __init__(self):
        self._search_engine: Optional[BaseSearchEngine] = None

    def __getitem__(self, key):
        raise NotImplementedError

    def is_search_engine_initialized(self):
        return self._search_engine is not None

    def _check_search_engine_is_initialized(self):
        if not self.is_search_engine_initialized():
            raise MissingSearchEngine(
                "SearchEngine not initialized yet. Please make sure that you call `init_vector_search_engine` or `init_text_search_engine` first."
            )

    def init_vector_search_engine(
        self,
        vectors,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        faiss_gpu_options: Optional[FaissGpuOptions] = None,
        column: Optional[str] = None,
    ):
        self._search_engine = DenseSearchEngine(device, string_factory, faiss_gpu_options)
        self._search_engine.add_embeddings(vectors, column=column)

    def init_text_search_engine(self, texts, es_client, index_name, column: Optional[str] = None):
        self._search_engine = SparseSearchEngine(es_client, index_name)
        self._search_engine.add_texts(texts, column=column)

    def search(self, query, k: int = 10) -> Tuple[List[float], List[int]]:
        self._check_search_engine_is_initialized()
        return self._search_engine.query(query, k)

    def search_batch(self, queries, k: int = 10) -> Tuple[List[List[float]], List[List[int]]]:
        self._check_search_engine_is_initialized()
        return self._search_engine.query_batch(queries, k)

    def get_nearest(self, query, k: int = 10) -> Tuple[List[float], List[dict]]:
        self._check_search_engine_is_initialized()
        scores, indices = self.search(query, k)
        return scores, [self[int(i)] for i in indices]

    def get_nearest_batch(self, queries, k: int = 10) -> Tuple[List[List[float]], List[List[dict]]]:
        self._check_search_engine_is_initialized()
        total_scores, total_indices = self.search_batch(queries, k)
        return total_scores, [[self[int(i)] for i in indices] for indices in total_indices]
