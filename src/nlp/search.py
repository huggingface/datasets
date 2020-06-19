import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
from tqdm.auto import tqdm


try:
    import elasticsearch as es
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


class MissingSearchEngine(Exception):
    pass


class BaseIndex:
    def search(self, query, k: int = 10) -> Tuple[List[float], List[int]]:
        raise NotImplementedError

    def search_batch(self, queries, k: int = 10) -> Tuple[List[List[float]], List[List[int]]]:
        total_scores, total_indices = [], []
        for query in queries:
            scores, indices = self.search(query, k)
            total_scores.append(scores)
            total_indices.append(indices)
        return total_scores, total_indices


class SparseIndex(BaseIndex):
    def __init__(self, es_client, index_name: str):
        # Elasticsearch needs to be launched in another window, and a python client is declared with
        # > es_client = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
        self.es_client = es_client
        self.index_name = index_name
        assert (
            _has_elasticsearch
        ), "You must install ElasticSearch to use SparseIndex. To do so you can run `pip install elasticsearch`"

    def add_texts(self, texts, column: Optional[str] = None):
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
        number_of_docs = len(texts)
        progress = tqdm(unit="docs", total=number_of_docs)
        successes = 0

        def passage_generator():
            if column is not None:
                for i, example in enumerate(texts):
                    yield {"text": example[column], "_id": i}
            else:
                for i, example in enumerate(texts):
                    yield {"text": example, "_id": i}

        # create the ES index
        for ok, action in es.helpers.streaming_bulk(
            client=self.es_client, index=index_name, actions=passage_generator(),
        ):
            progress.update(1)
            successes += ok
        logger.info("SearchEngineed %d documents" % (successes,))

    def search(self, query, k=10):
        response = self.es_client.search(
            index=self.index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": k},
        )
        hits = response["hits"]["hits"]
        return [hit["_score"] for hit in hits], [hit["_id"] for hit in hits]


class FaissGpuOptions:
    def __init__(self, resource_vec, device_vec, cloner_options):
        self.resource_vec = resource_vec
        self.device_vec = device_vec
        self.cloner_options = cloner_options


class DenseIndex(BaseIndex):
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
        ), "You must install Faiss to use DenseIndex. To do so you can run `pip install faiss-cpu` or `pip install faiss-gpu`"

    def add_vectors(self, vectors: np.array, column: Optional[str] = None, batch_size=1000):
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

    def search(self, query: np.array, k=10):
        assert len(query.shape) < 3
        queries = query.reshape(1, -1)
        scores, indices = self.faiss_index.search(queries, k)
        return scores[0], indices[0].astype(int)

    def search_batch(self, queries: np.array, k=10):
        assert len(queries.shape) == 2
        assert queries.shape[1] == self.size
        scores, indices = self.faiss_index.search(queries, k)
        return scores, indices.astype(int)


class IndexableMixin:
    """Add indexing features to classes"""

    def __init__(self):
        self._indexes: Dict[str, BaseIndex] = {}

    def __getitem__(self, key):
        raise NotImplementedError

    def is_index_initialized(self, name: str) -> bool:
        return name in self._indexes

    def _check_index_is_initialized(self, name: str):
        if not self.is_index_initialized(name):
            raise MissingSearchEngine(
                f"SearchEngine with name '{name}' not initialized yet. Please make sure that you call `add_vector_index` or `add_text_index` first."
            )

    def list_indexes(self) -> List[str]:
        return list(self._indexes)

    def add_vector_index(
        self,
        name: str,
        vectors,
        device: Optional[int] = None,
        string_factory: Optional[str] = None,
        faiss_gpu_options: Optional[FaissGpuOptions] = None,
        column: Optional[str] = None,
    ):
        self._indexes[name] = DenseIndex(device, string_factory, faiss_gpu_options)
        self._indexes[name].add_vectors(vectors, column=column)

    def add_text_index(self, name: str, texts, es_client, index_name, column: Optional[str] = None):
        self._indexes[name] = SparseIndex(es_client, index_name)
        self._indexes[name].add_texts(texts, column=column)

    def drop_index(self, name: str):
        del self._indexes[name]

    def search(self, name: str, query, k: int = 10) -> Tuple[List[float], List[int]]:
        self._check_index_is_initialized(name)
        return self._indexes[name].search(query, k)

    def search_batch(self, name: str, queries, k: int = 10) -> Tuple[List[List[float]], List[List[int]]]:
        self._check_index_is_initialized(name)
        return self._indexes[name].search_batch(queries, k)

    def get_nearest(self, name: str, query, k: int = 10) -> Tuple[List[float], List[dict]]:
        self._check_index_is_initialized(name)
        scores, indices = self.search(name, query, k)
        return scores, [self[int(i)] for i in indices]

    def get_nearest_batch(self, name: str, queries, k: int = 10) -> Tuple[List[List[float]], List[List[dict]]]:
        self._check_index_is_initialized(name)
        total_scores, total_indices = self.search_batch(name, queries, k)
        return total_scores, [[self[int(i)] for i in indices] for indices in total_indices]
