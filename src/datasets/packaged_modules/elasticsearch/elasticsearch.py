# coding=utf-8

import importlib.util

from elasticsearch import Elasticsearch
from dataclasses import dataclass
from typing import Optional

import datasets
from datasets.utils import logging

_has_elasticsearch = importlib.util.find_spec("elasticsearch") is not None

logger = logging.get_logger(__name__)


@dataclass
class ElasticsearchConfig(datasets.BuilderConfig):
    """BuilderConfig for JSON."""

    host: Optional[str] = None,
    port: Optional[int] = None,
    es_index_name: Optional[str] = None,
    es_index_config: Optional[dict] = None,


class ElasticsearchBuilder(datasets.ArrowBasedBuilder):
    """Elasticsearch based Builder to load datasets based on an Elasticsearch index and a filter query."""

    BUILDER_CONFIG_CLASS = ElasticsearchConfig

    es_client: Optional["Elasticsearch"] = None,

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

        logger.info(f"Testing connection to elasticsearch at {self.config.host}:{self.config.port}")
        print(self.es_client.indices.exists(index=self.config.es_index_name))
        logger.info("Connection successful")

        # TODO load index mapping to set self.config.feature

    def _info(self):
        return datasets.DatasetInfo()

    def _split_generators(self, dl_manager):
        pass

    def _generate_tables(self, **kwargs):
        pass
