# coding=utf-8

import importlib.util
from dataclasses import dataclass
from typing import Optional

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

import datasets
from datasets.utils import logging


_has_elasticsearch = importlib.util.find_spec("elasticsearch") is not None

logger = logging.get_logger(__name__)


@dataclass
class ElasticsearchConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    host: Optional[str] = (None,)
    port: Optional[int] = (None,)
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

        # init the elasticsearch client and test connection
        self.es_client = Elasticsearch([{"host": self.config.host, "port": str(self.config.port)}])

        try:
            logger.info(f"Testing connection to elasticsearch at {self.config.host}:{self.config.port}")
            if not self.es_client.indices.exists(index=self.config.es_index_name):
                raise ResourceWarning(f"Index {self.config.es_index_name} is not available.")
            logger.info("Connection successful")
        except ConnectionError:
            msg = f"Connection error: is the elasticsearch instance really at {self.config.host}:{self.config.port}?"
            logger.critical(msg)
            raise Exception(msg)

        # TODO load index mapping to set self.config.feature
        # self.es_client.indices.get_mapping(index=self.config.es_index_name)

    def _info(self):
        # TODO use data from mapping to have more detailed dataset info
        es_dataset_info = datasets.DatasetInfo()

        return es_dataset_info

    def _split_generators(self, dl_manager):
        query = "*" if self.config.query is None else self.config.query

        # open point in time to "freeze" index state
        point_in_time = self.es_client.open_point_in_time(index=self.config.es_index_name, keep_alive="5m")

        # probe the search results to get the total number of results
        response = self.es_client.search(
            index=self.config.es_index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": 0},
            # params=point_in_time,
        )
        total_number_of_results = response["hits"]["total"]["value"]

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "query": query,
                    "point_in_time": point_in_time,
                    "max_k": total_number_of_results,
                },
            ),
        ]

    def _generate_examples(self, query, point_in_time, max_k):
        # TODO load results page by page eventually loading page in background while yielding
        body = {
            "size": 100,
            "query": {
                "match": {
                    "text": "query"
                }
            }
            ,
            "pit": {
                "id": point_in_time,
                "keep_alive": "1m"
            }
        }

        # async_response = self.es_client.async_search.submit(
        #     index=self.config.es_index_name,
        #     body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": max_k},
        # )
        #
        # print(async_response)
        #
        # response = self.es_client.async_search.get(id=async_response['id'])
        # hits = response["response"]["hits"]


        response = self.es_client.search(
            index=self.config.es_index_name,
            body={"query": {"multi_match": {"query": query, "fields": ["text"], "type": "cross_fields"}}, "size": max_k},
        )
        hits = response["hits"]["hits"]

        print(f'Found {len(hits)} results')

        for hit in hits:
            yield hit['_id'], hit['_source']['text']

        # TODO close point in time
        self.es_client.close_point_in_time(point_in_time)
