# coding=utf-8

import importlib.util
from dataclasses import dataclass
from typing import Optional

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import ssl
import json

import datasets
from datasets.utils import logging


_has_elasticsearch = importlib.util.find_spec("elasticsearch") is not None

logger = logging.get_logger(__name__)


@dataclass
class ElasticsearchConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    host: Optional[str] = (None,)
    port: Optional[int] = (None,)
    es_username: Optional[int] = (None,)
    es_psw: Optional[int] = (None,)
    ca_file: Optional[int] = (None,)
    es_index_name: Optional[str] = (None,)
    es_index_config: Optional[dict] = (None,)
    query: Optional[str] = (None,)


class ElasticsearchBuilder(datasets.GeneratorBasedBuilder):
    """Elasticsearch based Builder to load datasets based on an Elasticsearch index and a filter query."""

    BUILDER_CONFIG_CLASS = ElasticsearchConfig

    es_client: Optional["Elasticsearch"] = (None,)

    def __init__(self, *args, **kwargs):
        super(ElasticsearchBuilder, self).__init__(*args, **kwargs)

        assert (
            _has_elasticsearch
        ), "You must install ElasticSearch to use ElasticSearchIndex: e.g. run `pip install elasticsearch==7.13.3`"
        assert (
            self.config.host is not None and self.config.port is not None
        ), "Please specify `(host, port)` in config."

    def _info(self):
        self._init_connexion()
        return self.info

    def _init_connexion(self):
        # init the elasticsearch client and test connection
        server_url = ('https' if self.config.ca_file is not None else 'http') + '://' + self.config.host + ':' + str(
            self.config.port)
        ssl_context = None if self.config.ca_file is None else ssl.create_default_context(cafile=self.config.ca_file)
        if self.config.es_username is None or self.config.es_psw is None:
            self.es_client = Elasticsearch([server_url], ssl_context=ssl_context)
        else:
            # authenticate user
            self.es_client = Elasticsearch([server_url], http_auth=(self.config.es_username, self.config.es_psw),
                                           ssl_context=ssl_context)
        try:
            logger.info(f"Testing connection to elasticsearch at {self.config.host}:{self.config.port}")
            if not self.es_client.indices.exists(index=self.config.es_index_name):
                raise ResourceWarning(f"Index {self.config.es_index_name} is not available.")
            logger.info("Connection successful")
        except ConnectionError:
            msg = f"Connection error: is the elasticsearch instance really at {self.config.host}:{self.config.port}?"
            logger.critical(msg)
            raise Exception(msg)
        # load dataset info from elasticsearch index
        # load dataset information from elasticsearch index metadata
        mapping_response = self.es_client.indices.get_mapping(index=self.config.es_index_name)
        self.mapping = mapping_response[self.config.es_index_name]["mappings"]
        _DESCRIPTION = self.mapping["_meta"]["description"]
        _HOMEPAGE = self.mapping["_meta"]["homepage"]
        _CITATION = self.mapping["_meta"]["citation"]
        _LICENSE = self.mapping["_meta"]["license"]

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
            homepage=None, #_HOMEPAGE,
            citation=None, #_CITATION,
            license=None, #_LICENSE,
        )

    def _split_generators(self, dl_manager):
        query = "*" if self.config.query is None else self.config.query

        # probe the search results to get the total number of results
        response = self.es_client.search(
            index=self.config.es_index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": 0},
        )
        total_number_of_results = response["hits"]["total"]["value"]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
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
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": max_k},
        )
        hits = response["hits"]["hits"]

        print(f'Found {len(hits)} results')

        for hit in hits:
            print(hit['_id'], hit['_source']['text'])
            yield hit['_id'], hit['_source']['text']

