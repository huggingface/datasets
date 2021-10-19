# coding=utf-8

import importlib.util
from dataclasses import dataclass
from typing import Optional

import datasets
from datasets.utils import logging


_has_elasticsearch = importlib.util.find_spec("elasticsearch") is not None

logger = logging.get_logger(__name__)


@dataclass
class ElasticsearchConfig(datasets.BuilderConfig):
    """BuilderConfig for ElasticsearchBuilder."""

    host: Optional[str] = None
    port: Optional[int] = None
    es_username: Optional[int] = None
    es_psw: Optional[int] = None
    ca_file: Optional[int] = None
    es_index_name: Optional[str] = None
    es_index_config: Optional[dict] = None
    query: Optional[str] = None


class ElasticsearchBuilder(datasets.GeneratorBasedBuilder):
    """Elasticsearch based Builder to load datasets based on an Elasticsearch index and a filter query."""

    BUILDER_CONFIG_CLASS = ElasticsearchConfig

    es_client: Optional["Elasticsearch"] = None

    def __init__(self, *args, **kwargs):
        super(ElasticsearchBuilder, self).__init__(*args, **kwargs)

        assert (
            _has_elasticsearch
        ), "You must install ElasticSearch to use ElasticSearchIndex: e.g. run `pip install elasticsearch==7.10.1`"
        assert (
            self.config.host is not None and self.config.port is not None
        ), "Please specify `(host, port)` in config."

    def _info(self):
        self._init_connexion()
        return self.info

    def _init_connexion(self):
        from datasets.search import ElasticSearchIndex

        logger.info(f"Testing connection to elasticsearch at {self.config.host}:{self.config.port}")

        self.es_client = ElasticSearchIndex.get_es_client(
            self.config.host,
            self.config.port,
            es_username=self.config.es_username,
            es_psw=self.config.es_psw,
            ca_file=self.config.ca_file
        )

        self.config.es_index_name = ElasticSearchIndex.check_index_name_or_default(self.config.es_index_name)

        _DESCRIPTION = None
        _HOMEPAGE = None
        _CITATION = None
        _LICENSE = None

        if not self.es_client.indices.exists(index=self.config.es_index_name):
            logger.warning(f"Index [{self.config.es_index_name}] is not available in {self.config.host} server.")
        else:
            # load dataset information from elasticsearch index metadata
            mapping_response = self.es_client.indices.get_mapping(index=self.config.es_index_name)
            self.mapping = mapping_response[self.config.es_index_name]["mappings"]

            if "_meta" in self.mapping.keys():
                _DESCRIPTION = self.mapping["_meta"]["description"]
                _HOMEPAGE = self.mapping["_meta"]["homepage"]
                _CITATION = self.mapping["_meta"]["citation"]
                _LICENSE = self.mapping["_meta"]["license"]
            else:
                logger.warning(
                    f"No meta on this ES index {self.config.es_index_name}. The dataset will not have metadata."
                )

        self.info = datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                # TODO load index mapping to set self.config.feature
                {
                    "id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    # "length": datasets.Value("long"),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
            license=_LICENSE,
        )

        print(self.info)

    def _split_generators(self, dl_manager):
        query = "*" if self.config.query is None else self.config.query

        # probe the search results to get the total number of results
        response = self.es_client.search(
            index=self.config.es_index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": 0},
        )
        total_number_of_results = response["hits"]["total"]["value"]

        import sys

        return [
            datasets.SplitGenerator(
                name=f"{self.config.es_index_name}_{sys.maxsize + hash(query)}",
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "query": query,
                    "max_k": total_number_of_results,
                },
            ),
        ]

    def _generate_examples(self, query, max_k):
        # TODO load results page by page eventually loading page in background while yielding
        response = self.es_client.search(
            index=self.config.es_index_name,
            body={
                "query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}},
                "size": max_k,
            },
            request_timeout=1800,
        )
        hits = response["hits"]["hits"]

        for hit in hits:
            yield hit["_id"], {"id": hit["_id"], "text": hit["_source"]["text"]}
