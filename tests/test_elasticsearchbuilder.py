from datasets.packaged_modules.elasticsearch.elasticsearch import ElasticsearchBuilder
from datasets import load_dataset
from datasets import Dataset
import simplejson as json

es_index_config = {
    "settings": {
        "number_of_shards": 1,
        "analysis": {
            "analyzer": {
                "stop_standard": {"type": "standard", " stopwords": "_galician_"}
            }
        },
    },
    "mappings": {
        "properties": {
            "text": {"type": "text", "analyzer": "standard", "similarity": "BM25"}
        }
    },
}

ca_file = '/Users/gdupont/src/github.com/bigscience-workshop/data-tooling/index_search/ca.cert'
with open('/Users/gdupont/src/github.com/bigscience-workshop/data-tooling/index_search/credentials.json') as f:
    credentials = json.load(f)

    the_host = credentials['connection']['https']['hosts'][0]['hostname']
    the_port = credentials['connection']['https']['hosts'][0]['port']

    username = credentials['connection']['https']['authentication']['username']
    psw = credentials['connection']['https']['authentication']['password']

index_name = "oscar_unshuffled_deduplicated"
oscar_lang_code = "nn"

elasticsearch_builder = ElasticsearchBuilder(
    host=the_host, port=the_port,
    es_username=username, es_psw=psw, ca_file=ca_file,
    es_index_name=index_name, es_index_config=es_index_config,
    query="mykje arbeid og slit"
)
assert elasticsearch_builder.config.host == the_host

# elasticsearch_builder = ElasticsearchBuilder(
#     host="localhost",
#     port="9200",
#     es_index_name="oscar_unshuffled_deduplicated",
#     es_index_config=es_index_config,
#     query="mykje arbeid og slit"
# )
# assert elasticsearch_builder.config.host == "localhost"

elasticsearch_builder.download_and_prepare()

oscar_dataset = elasticsearch_builder.as_dataset()
