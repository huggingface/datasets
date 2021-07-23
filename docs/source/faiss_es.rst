Document retrieval
==================

Searching for specific examples in a dataset is now possible due to `FAISS <https://github.com/facebookresearch/faiss>`_ and `ElasticSearch <https://www.elastic.co/elasticsearch/>`_ support. This can be useful when you want to retrieve specific examples from a dataset that are relevant to a specific question you want to answer. For example, if you are working on a Open Domain Question Answering task, you may want to retrieve examples that are relevant to answering the question.

This guide will show you how to build an index for your dataset that will allow you to search it.

FAISS
-----

FAISS retrieves documents based on the similiarity of their vector representations. In this example, you will generate vector representations with the `DPR <https://huggingface.co/transformers/model_doc/dpr.html>`_ model.

1. Download the DPR model from Transformers:

    >>> from transformers import DPRContextEncoder, DPRContextEncoderTokenizer
    >>> import torch
    >>> torch.set_grad_enabled(False)
    >>> ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
    >>> ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

2. Load your dataset and compute the representations:

    >>> from datasets import load_dataset
    >>> ds = load_dataset('crime_and_punish', split='train[:100]')
    >>> ds_with_embeddings = ds.map(lambda example: {'embeddings': ctx_encoder(**ctx_tokenizer(example["line"], return_tensors="pt"))[0][0].numpy()})

3. Create the index with :func:`datasets.Dataset.add_faiss_index`:

    >>> ds_with_embeddings.add_faiss_index(column='embeddings')

4. Now you can query your dataset with the index ``embeddings``. Load the DPR Question Encoder and then search for a question with :func:`datasets.Dataset.get_nearest_examples`:

    >>> from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer
    >>> q_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
    >>> q_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
    >>>
    >>> question = "Is it serious ?"
    >>> question_embedding = q_encoder(**q_tokenizer(question, return_tensors="pt"))[0][0].numpy()
    >>> scores, retrieved_examples = ds_with_embeddings.get_nearest_examples('embeddings', question_embedding, k=10)
    >>> retrieved_examples["line"][0]
    '_that_ serious? It is not serious at all. It’s simply a fantasy to amuse\r\n'

5. When you are done querying, you can save the index on disk:

    >>> ds_with_embeddings.save_faiss_index('embeddings', 'my_index.faiss')

6. Reload it later when you want to use it again with :func:`datasets.Dataset.load_faiss_index`:

    >>> ds = load_dataset('crime_and_punish', split='train[:100]')
    >>> ds.load_faiss_index('embeddings', 'my_index.faiss')

ElasticSearch
-------------

Unlike FAISS, ElasticSearch retrieves documents based on exact matches.

1. Start ElasticSearch on your machine:

    >>> from datasets import load_dataset
    >>> squad = load_dataset('squad', split='validation')

2. Build the index with :func:`datasets.Dataset.add_elasticsearch_index`:

    >>> squad.add_elasticsearch_index("context", host="localhost", port="9200")

3. Then you can query the index of the ``context`` column with :func:`datasets.Dataset.get_nearest_examples`:

    >>> query = "machine"
    >>> scores, retrieved_examples = squad.get_nearest_examples("context", query, k=10)
    >>> retrieved_examples["title"][0]
    'Computational_complexity_theory'

4. If you want to reuse the index, specify the ElasticSearch index name when you build the index:

    >>> from datasets import load_dataset
    >>> squad = load_dataset('squad', split='validation')
    >>> squad.add_elasticsearch_index("context", host="localhost", port="9200", es_index_name="hf_squad_val_context")
    >>> squad.get_index("context").es_index_name
    hf_squad_val_context

5. Reload it later when you are ready to use it again by specifiying the index name when you call :func:`datasets.Dataset.load_elasticsearch_index`:

    >>> from datasets import load_dataset
    >>> squad = load_dataset('squad', split='validation')
    >>> squad.load_elasticsearch_index("context", host="localhost", port="9200", es_index_name="hf_squad_val_context")
    >>> query = "machine"
    >>> scores, retrieved_examples = squad.get_nearest_examples("context", query, k=10)

For more advanced usage of ElasticSearch, you can specify your own configuration with custom settings:

    >>> import elasticsearch as es
    >>> import elasticsearch.helpers
    >>> from elasticsearch import Elasticsearch
    >>> es_client = Elasticsearch([{"host": "localhost", "port": "9200"}])  # default client
    >>> es_config = {
            "settings": {
                "number_of_shards": 1,
                "analysis": {"analyzer": {"stop_standard": {"type": "standard", " stopwords": "_english_"}}},
            },
            "mappings": {"properties": {"text": {"type": "text", "analyzer": "standard", "similarity": "BM25"}}},
        }  # default config
    >>> es_index_name = "hf_squad_context"  # name of the index in ElasticSearch
    >>> squad.add_elasticsearch_index("context", es_client=es_client, es_config=es_config, es_index_name=es_index_name)